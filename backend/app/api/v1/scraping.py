"""
Web Scraping endpoints using Firecrawl
Core MVP functionality: URL → Scrape → Extract
"""
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl

from app.services.firecrawl_service import FirecrawlService
from app.services.llm_service import LLMService

router = APIRouter()

firecrawl = FirecrawlService()
llm = LLMService()


class ScrapeRequest(BaseModel):
    """Single URL scrape request."""
    url: HttpUrl
    formats: List[str] = ["markdown"]
    only_main_content: bool = True
    wait_for: Optional[int] = None  # milliseconds


class ScrapeResponse(BaseModel):
    """Scrape result."""
    success: bool
    url: str
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ExtractRequest(BaseModel):
    """Structured data extraction request."""
    url: HttpUrl
    prompt: str
    schema: Optional[Dict[str, Any]] = None


class ExtractResponse(BaseModel):
    """Extraction result with structured data."""
    success: bool
    url: str
    data: Optional[Dict[str, Any]] = None
    raw_content: Optional[str] = None
    error: Optional[str] = None


class QuickScrapeRequest(BaseModel):
    """MVP: Quick scrape with auto extraction."""
    url: HttpUrl
    data_type: str = "auto"  # auto, products, articles, contacts, etc.


class QuickScrapeResponse(BaseModel):
    """MVP: Complete scrape result with extraction."""
    success: bool
    url: str
    extracted_data: Optional[Dict[str, Any]] = None
    insights: Optional[Dict[str, Any]] = None
    raw_content: Optional[str] = None
    error: Optional[str] = None


@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_url(request: ScrapeRequest):
    """
    URL 스크래핑
    
    Firecrawl을 사용하여 단일 URL의 콘텐츠를 추출합니다.
    
    - **url**: 스크래핑할 URL
    - **formats**: 출력 형식 (markdown, html, rawHtml)
    - **only_main_content**: 메인 콘텐츠만 추출
    """
    try:
        result = await firecrawl.scrape(
            url=str(request.url),
            formats=request.formats,
            only_main_content=request.only_main_content,
            wait_for=request.wait_for
        )
        return ScrapeResponse(
            success=True,
            url=str(request.url),
            content=result.get("markdown") or result.get("html"),
            metadata=result.get("metadata")
        )
    except Exception as e:
        return ScrapeResponse(
            success=False,
            url=str(request.url),
            error=str(e)
        )


@router.post("/extract", response_model=ExtractResponse)
async def extract_data(request: ExtractRequest):
    """
    구조화된 데이터 추출
    
    LLM을 사용하여 웹페이지에서 구조화된 데이터를 추출합니다.
    
    - **url**: 데이터를 추출할 URL
    - **prompt**: 추출할 데이터에 대한 설명
    - **schema**: 추출할 데이터의 JSON 스키마 (선택사항)
    """
    try:
        # First scrape the page
        scraped = await firecrawl.scrape(
            url=str(request.url),
            formats=["markdown"],
            only_main_content=True
        )
        
        raw_content = scraped.get("markdown", "")
        
        # Then extract structured data using LLM
        extracted = await llm.extract_structured_data(
            content=raw_content,
            prompt=request.prompt,
            schema=request.schema
        )
        
        return ExtractResponse(
            success=True,
            url=str(request.url),
            data=extracted,
            raw_content=raw_content[:1000] if raw_content else None  # Truncate
        )
    except Exception as e:
        return ExtractResponse(
            success=False,
            url=str(request.url),
            error=str(e)
        )


@router.post("/quick", response_model=QuickScrapeResponse)
async def quick_scrape(request: QuickScrapeRequest):
    """
    MVP 핵심 기능: 빠른 스크래핑 + 자동 추출 + 인사이트
    
    URL 하나로 스크래핑 → 데이터 추출 → 인사이트 생성을 한번에 수행합니다.
    
    - **url**: 분석할 URL
    - **data_type**: 데이터 타입 (auto, products, articles, contacts)
    """
    try:
        # Step 1: Scrape the page
        scraped = await firecrawl.scrape(
            url=str(request.url),
            formats=["markdown"],
            only_main_content=True
        )
        raw_content = scraped.get("markdown", "")
        
        # Step 2: Auto-detect and extract data
        extracted = await llm.auto_extract(
            content=raw_content,
            data_type=request.data_type
        )
        
        # Step 3: Generate insights
        insights = await llm.generate_insights(
            data=extracted,
            data_type=request.data_type
        )
        
        return QuickScrapeResponse(
            success=True,
            url=str(request.url),
            extracted_data=extracted,
            insights=insights,
            raw_content=raw_content[:500] if raw_content else None
        )
    except Exception as e:
        return QuickScrapeResponse(
            success=False,
            url=str(request.url),
            error=str(e)
        )


@router.get("/test")
async def test_connection():
    """
    Firecrawl 연결 테스트
    """
    try:
        # Test with a simple URL
        result = await firecrawl.scrape(
            url="https://example.com",
            formats=["markdown"],
            only_main_content=True
        )
        return {
            "status": "connected",
            "firecrawl": "ok",
            "sample_length": len(result.get("markdown", ""))
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Firecrawl 연결 실패: {str(e)}"
        )
