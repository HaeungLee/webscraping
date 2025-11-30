"""
Firecrawl Service - Web Scraping Engine
Connects to self-hosted Firecrawl instance
"""
import httpx
from typing import Optional, Dict, Any, List

from app.core.config import settings


class FirecrawlService:
    """
    Firecrawl API wrapper for web scraping.
    
    Supports both cloud and self-hosted Firecrawl instances.
    MVP uses self-hosted version via Docker.
    """
    
    def __init__(self):
        self.base_url = settings.FIRECRAWL_API_URL.rstrip("/")
        self.api_key = settings.FIRECRAWL_API_KEY
        self.timeout = 60.0  # seconds
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key if configured."""
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    async def scrape(
        self,
        url: str,
        formats: List[str] = ["markdown"],
        only_main_content: bool = True,
        wait_for: Optional[int] = None,
        include_tags: Optional[List[str]] = None,
        exclude_tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Scrape a single URL.
        
        Args:
            url: URL to scrape
            formats: Output formats (markdown, html, rawHtml, links)
            only_main_content: Extract only main content
            wait_for: Wait time in milliseconds
            include_tags: HTML tags to include
            exclude_tags: HTML tags to exclude
            
        Returns:
            Scraped content with metadata
        """
        payload = {
            "url": url,
            "formats": formats,
            "onlyMainContent": only_main_content,
        }
        
        if wait_for:
            payload["waitFor"] = wait_for
        if include_tags:
            payload["includeTags"] = include_tags
        if exclude_tags:
            payload["excludeTags"] = exclude_tags
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/v1/scrape",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            data = response.json()
            
            # Firecrawl returns data nested in "data" key
            if "data" in data:
                return data["data"]
            return data
    
    async def batch_scrape(
        self,
        urls: List[str],
        formats: List[str] = ["markdown"],
        only_main_content: bool = True,
    ) -> Dict[str, Any]:
        """
        Batch scrape multiple URLs.
        
        Args:
            urls: List of URLs to scrape
            formats: Output formats
            only_main_content: Extract only main content
            
        Returns:
            Batch operation ID and status
        """
        payload = {
            "urls": urls,
            "formats": formats,
            "onlyMainContent": only_main_content,
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/v1/batch/scrape",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
    
    async def map_site(
        self,
        url: str,
        limit: int = 100,
        include_subdomains: bool = False,
    ) -> Dict[str, Any]:
        """
        Map a website to discover all URLs.
        
        Args:
            url: Starting URL
            limit: Maximum number of URLs to return
            include_subdomains: Include subdomain URLs
            
        Returns:
            List of discovered URLs
        """
        payload = {
            "url": url,
            "limit": limit,
            "includeSubdomains": include_subdomains,
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/v1/map",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
    
    async def extract(
        self,
        urls: List[str],
        prompt: str,
        schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Extract structured data using Firecrawl's LLM extraction.
        
        Note: MVP uses our own LLM extraction via OpenRouter for cost control.
        This method is available for future use with Firecrawl cloud.
        
        Args:
            urls: URLs to extract from
            prompt: Extraction prompt
            schema: JSON schema for structured output
            
        Returns:
            Extracted structured data
        """
        payload = {
            "urls": urls,
            "prompt": prompt,
        }
        
        if schema:
            payload["schema"] = schema
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/v1/extract",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
    
    async def health_check(self) -> bool:
        """Check if Firecrawl service is available."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except Exception:
            return False
