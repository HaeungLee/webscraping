"""
API Router aggregation
"""
from fastapi import APIRouter

from app.api.v1 import scraping, insights, auth

router = APIRouter()

# V1 API routes
router.include_router(auth.router, prefix="/v1/auth", tags=["인증"])
router.include_router(scraping.router, prefix="/v1/scraping", tags=["스크래핑"])
router.include_router(insights.router, prefix="/v1/insights", tags=["인사이트"])
