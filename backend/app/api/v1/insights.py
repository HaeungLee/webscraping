"""
LLM Insights endpoints
MVP 핵심 차별화 기능: 스크래핑 데이터 → AI 분석 → 인사이트 리포트
"""
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.services.llm_service import LLMService

router = APIRouter()

llm = LLMService()


class InsightRequest(BaseModel):
    """Insight generation request."""
    data: Dict[str, Any]
    data_type: str = "auto"  # products, articles, competitors, etc.
    analysis_type: str = "summary"  # summary, trends, recommendations


class InsightResponse(BaseModel):
    """Generated insight response."""
    success: bool
    analysis_type: str
    insights: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    recommendations: Optional[List[str]] = None
    error: Optional[str] = None


class CompareRequest(BaseModel):
    """Data comparison request."""
    data_sets: List[Dict[str, Any]]
    labels: List[str]
    comparison_type: str = "side_by_side"  # side_by_side, trends, competitive


class CompareResponse(BaseModel):
    """Comparison result."""
    success: bool
    comparison: Optional[Dict[str, Any]] = None
    highlights: Optional[List[str]] = None
    error: Optional[str] = None


class ReportRequest(BaseModel):
    """Full report generation request."""
    data: Dict[str, Any]
    report_type: str = "executive"  # executive, detailed, technical
    language: str = "ko"  # ko, en


class ReportResponse(BaseModel):
    """Generated report."""
    success: bool
    report: Optional[str] = None  # Markdown formatted report
    sections: Optional[Dict[str, str]] = None
    error: Optional[str] = None


@router.post("/analyze", response_model=InsightResponse)
async def analyze_data(request: InsightRequest):
    """
    데이터 분석 및 인사이트 생성
    
    스크래핑한 데이터를 LLM으로 분석하여 인사이트를 생성합니다.
    
    - **data**: 분석할 데이터 (스크래핑 결과)
    - **data_type**: 데이터 유형 (products, articles, competitors)
    - **analysis_type**: 분석 유형 (summary, trends, recommendations)
    """
    try:
        insights = await llm.generate_insights(
            data=request.data,
            data_type=request.data_type,
            analysis_type=request.analysis_type
        )
        
        return InsightResponse(
            success=True,
            analysis_type=request.analysis_type,
            insights=insights,
            summary=insights.get("summary"),
            recommendations=insights.get("recommendations")
        )
    except Exception as e:
        return InsightResponse(
            success=False,
            analysis_type=request.analysis_type,
            error=str(e)
        )


@router.post("/compare", response_model=CompareResponse)
async def compare_data(request: CompareRequest):
    """
    데이터 비교 분석
    
    여러 데이터셋을 비교하여 차이점과 인사이트를 생성합니다.
    예: 경쟁사 가격 비교, 시간에 따른 변화 분석
    
    - **data_sets**: 비교할 데이터셋 목록
    - **labels**: 각 데이터셋의 라벨 (예: 쿠팡, 네이버쇼핑)
    - **comparison_type**: 비교 유형
    """
    try:
        comparison = await llm.compare_data(
            data_sets=request.data_sets,
            labels=request.labels,
            comparison_type=request.comparison_type
        )
        
        return CompareResponse(
            success=True,
            comparison=comparison,
            highlights=comparison.get("highlights")
        )
    except Exception as e:
        return CompareResponse(
            success=False,
            error=str(e)
        )


@router.post("/report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    인사이트 리포트 생성
    
    분석 결과를 보기 좋은 리포트 형식으로 생성합니다.
    
    - **data**: 리포트에 포함할 데이터
    - **report_type**: 리포트 유형 (executive, detailed, technical)
    - **language**: 언어 (ko, en)
    """
    try:
        report = await llm.generate_report(
            data=request.data,
            report_type=request.report_type,
            language=request.language
        )
        
        return ReportResponse(
            success=True,
            report=report.get("full_report"),
            sections=report.get("sections")
        )
    except Exception as e:
        return ReportResponse(
            success=False,
            error=str(e)
        )


@router.get("/templates")
async def get_insight_templates():
    """
    사용 가능한 인사이트 템플릿 목록
    """
    return {
        "data_types": [
            {"id": "products", "name": "상품 데이터", "description": "이커머스 상품 정보 분석"},
            {"id": "articles", "name": "기사/블로그", "description": "뉴스 및 콘텐츠 분석"},
            {"id": "competitors", "name": "경쟁사", "description": "경쟁사 분석 및 비교"},
            {"id": "reviews", "name": "리뷰", "description": "고객 리뷰 감성 분석"},
            {"id": "pricing", "name": "가격", "description": "가격 동향 및 비교 분석"},
        ],
        "analysis_types": [
            {"id": "summary", "name": "요약", "description": "핵심 내용 요약"},
            {"id": "trends", "name": "트렌드", "description": "패턴 및 트렌드 분석"},
            {"id": "recommendations", "name": "추천", "description": "액션 아이템 추천"},
            {"id": "sentiment", "name": "감성 분석", "description": "긍/부정 감성 분석"},
        ],
        "report_types": [
            {"id": "executive", "name": "임원 보고서", "description": "핵심 인사이트 중심"},
            {"id": "detailed", "name": "상세 보고서", "description": "전체 분석 내용 포함"},
            {"id": "technical", "name": "기술 보고서", "description": "데이터 중심 분석"},
        ]
    }
