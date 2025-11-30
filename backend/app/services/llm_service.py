"""
LLM Service - AI-powered data extraction and insights
Uses OpenRouter for LLM access (free models for MVP)
"""
import json
import httpx
from typing import Optional, Dict, Any, List

from app.core.config import settings


# Prompt templates for Korean market
EXTRACTION_PROMPT_TEMPLATE = """당신은 웹 데이터 추출 전문가입니다.
다음 웹페이지 콘텐츠에서 {data_type} 데이터를 추출해주세요.

웹페이지 콘텐츠:
{content}

{schema_instruction}

JSON 형식으로만 응답해주세요. 다른 설명은 필요 없습니다.
"""

AUTO_EXTRACT_PROMPT = """당신은 웹 데이터 분석 전문가입니다.
다음 웹페이지 콘텐츠를 분석하여 주요 데이터를 구조화된 JSON으로 추출해주세요.

웹페이지 콘텐츠:
{content}

데이터 유형 힌트: {data_type}

다음 형식으로 응답해주세요:
{{
    "detected_type": "감지된 데이터 유형",
    "items": [추출된 항목들],
    "metadata": {{
        "source_type": "ecommerce|news|blog|etc",
        "item_count": 숫자,
        "language": "ko|en"
    }}
}}

JSON 형식으로만 응답해주세요.
"""

INSIGHT_PROMPT_TEMPLATE = """당신은 {data_type} 데이터 분석 전문가입니다.
다음 데이터를 분석하여 인사이트를 생성해주세요.

데이터:
{data}

분석 유형: {analysis_type}

다음 형식으로 응답해주세요:
{{
    "summary": "핵심 요약 (2-3문장)",
    "key_findings": ["주요 발견 1", "주요 발견 2", "주요 발견 3"],
    "trends": ["트렌드 1", "트렌드 2"],
    "recommendations": ["추천 액션 1", "추천 액션 2"],
    "risk_factors": ["리스크 요인들"],
    "confidence_score": 0.0-1.0 사이의 신뢰도
}}

JSON 형식으로만 응답해주세요.
"""

REPORT_PROMPT_TEMPLATE = """당신은 비즈니스 리포트 작성 전문가입니다.
다음 데이터와 분석 결과를 바탕으로 {report_type} 리포트를 작성해주세요.

데이터:
{data}

언어: {language}
리포트 유형: {report_type}

마크다운 형식으로 보기 좋은 리포트를 작성해주세요.
섹션은 다음을 포함해야 합니다:
1. 요약 (Executive Summary)
2. 주요 발견 (Key Findings)
3. 상세 분석 (Detailed Analysis)
4. 추천 사항 (Recommendations)
5. 결론 (Conclusion)
"""

COMPARE_PROMPT_TEMPLATE = """당신은 데이터 비교 분석 전문가입니다.
다음 데이터셋들을 비교 분석해주세요.

{data_description}

비교 유형: {comparison_type}

다음 형식으로 응답해주세요:
{{
    "comparison_summary": "비교 요약",
    "similarities": ["공통점들"],
    "differences": ["차이점들"],
    "highlights": ["주목할 포인트들"],
    "winner": "특정 기준에서의 우위 (해당시)",
    "detailed_comparison": {{}}
}}

JSON 형식으로만 응답해주세요.
"""


class LLMService:
    """
    LLM-powered data extraction and insights generation.
    Uses OpenRouter API for access to multiple LLM models.
    """
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.model = settings.LLM_MODEL
        self.timeout = 120.0  # LLM responses can be slow
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers for OpenRouter."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://webscraping.app",  # Required by OpenRouter
            "X-Title": "WebScraping Automation Builder",
        }
    
    async def _chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4000,
    ) -> str:
        """
        Send chat completion request to OpenRouter.
        
        Args:
            messages: Chat messages
            temperature: Response randomness (0-1)
            max_tokens: Maximum response tokens
            
        Returns:
            LLM response text
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            data = response.json()
            
            return data["choices"][0]["message"]["content"]
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON from LLM response, handling markdown code blocks.
        """
        # Remove markdown code blocks if present
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
        
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            # Return as-is if parsing fails
            return {"raw_response": response}
    
    async def extract_structured_data(
        self,
        content: str,
        prompt: str,
        schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Extract structured data from content using LLM.
        
        Args:
            content: Web page content
            prompt: Extraction instructions
            schema: Expected output schema
            
        Returns:
            Extracted structured data
        """
        schema_instruction = ""
        if schema:
            schema_instruction = f"추출 결과는 다음 스키마를 따라야 합니다:\n{json.dumps(schema, ensure_ascii=False, indent=2)}"
        
        full_prompt = EXTRACTION_PROMPT_TEMPLATE.format(
            data_type=prompt,
            content=content[:8000],  # Truncate for token limits
            schema_instruction=schema_instruction
        )
        
        response = await self._chat_completion([
            {"role": "system", "content": "당신은 정확한 데이터 추출 전문가입니다. JSON 형식으로만 응답합니다."},
            {"role": "user", "content": full_prompt}
        ])
        
        return self._parse_json_response(response)
    
    async def auto_extract(
        self,
        content: str,
        data_type: str = "auto",
    ) -> Dict[str, Any]:
        """
        Automatically detect and extract data from content.
        
        Args:
            content: Web page content
            data_type: Hint for data type (auto, products, articles, etc.)
            
        Returns:
            Extracted data with detected type
        """
        prompt = AUTO_EXTRACT_PROMPT.format(
            content=content[:8000],
            data_type=data_type
        )
        
        response = await self._chat_completion([
            {"role": "system", "content": "당신은 웹 데이터 분석 전문가입니다. JSON 형식으로만 응답합니다."},
            {"role": "user", "content": prompt}
        ])
        
        return self._parse_json_response(response)
    
    async def generate_insights(
        self,
        data: Dict[str, Any],
        data_type: str = "auto",
        analysis_type: str = "summary",
    ) -> Dict[str, Any]:
        """
        Generate insights from extracted data.
        
        Args:
            data: Extracted data to analyze
            data_type: Type of data (products, articles, etc.)
            analysis_type: Type of analysis (summary, trends, recommendations)
            
        Returns:
            Generated insights
        """
        prompt = INSIGHT_PROMPT_TEMPLATE.format(
            data_type=data_type,
            data=json.dumps(data, ensure_ascii=False, indent=2)[:6000],
            analysis_type=analysis_type
        )
        
        response = await self._chat_completion([
            {"role": "system", "content": "당신은 데이터 인사이트 생성 전문가입니다. JSON 형식으로만 응답합니다."},
            {"role": "user", "content": prompt}
        ])
        
        return self._parse_json_response(response)
    
    async def compare_data(
        self,
        data_sets: List[Dict[str, Any]],
        labels: List[str],
        comparison_type: str = "side_by_side",
    ) -> Dict[str, Any]:
        """
        Compare multiple data sets.
        
        Args:
            data_sets: List of data sets to compare
            labels: Labels for each data set
            comparison_type: Type of comparison
            
        Returns:
            Comparison results
        """
        data_description = ""
        for i, (data, label) in enumerate(zip(data_sets, labels)):
            data_description += f"\n--- {label} ---\n"
            data_description += json.dumps(data, ensure_ascii=False, indent=2)[:3000]
        
        prompt = COMPARE_PROMPT_TEMPLATE.format(
            data_description=data_description,
            comparison_type=comparison_type
        )
        
        response = await self._chat_completion([
            {"role": "system", "content": "당신은 데이터 비교 분석 전문가입니다. JSON 형식으로만 응답합니다."},
            {"role": "user", "content": prompt}
        ])
        
        return self._parse_json_response(response)
    
    async def generate_report(
        self,
        data: Dict[str, Any],
        report_type: str = "executive",
        language: str = "ko",
    ) -> Dict[str, Any]:
        """
        Generate a formatted report.
        
        Args:
            data: Data and analysis to include
            report_type: Type of report (executive, detailed, technical)
            language: Report language (ko, en)
            
        Returns:
            Generated report in markdown format
        """
        prompt = REPORT_PROMPT_TEMPLATE.format(
            data=json.dumps(data, ensure_ascii=False, indent=2)[:6000],
            report_type=report_type,
            language=language
        )
        
        response = await self._chat_completion([
            {"role": "system", "content": "당신은 비즈니스 리포트 작성 전문가입니다."},
            {"role": "user", "content": prompt}
        ], temperature=0.5)  # Slightly more creative for reports
        
        # Parse sections from markdown response
        sections = {}
        current_section = "intro"
        current_content = []
        
        for line in response.split("\n"):
            if line.startswith("## "):
                if current_content:
                    sections[current_section] = "\n".join(current_content)
                current_section = line[3:].strip().lower().replace(" ", "_")
                current_content = []
            else:
                current_content.append(line)
        
        if current_content:
            sections[current_section] = "\n".join(current_content)
        
        return {
            "full_report": response,
            "sections": sections
        }
    
    async def health_check(self) -> bool:
        """Check if LLM service is available."""
        try:
            response = await self._chat_completion(
                [{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return len(response) > 0
        except Exception:
            return False
