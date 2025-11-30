import { useMutation } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";

interface QuickScrapeRequest {
  url: string;
  data_type?: string;
}

interface QuickScrapeResponse {
  success: boolean;
  url: string;
  extracted_data: Record<string, unknown> | null;
  insights: {
    summary?: string;
    key_findings?: string[];
    trends?: string[];
    recommendations?: string[];
    risk_factors?: string[];
    confidence_score?: number;
  } | null;
  raw_content: string | null;
  error: string | null;
}

export function useQuickScrape() {
  return useMutation<QuickScrapeResponse, Error, QuickScrapeRequest>({
    mutationFn: async (request) => {
      const response = await apiClient.post<QuickScrapeResponse>(
        "/api/v1/scraping/quick",
        request
      );
      
      if (!response.data.success) {
        throw new Error(response.data.error || "스크래핑에 실패했습니다.");
      }
      
      return response.data;
    },
  });
}

interface ScrapeRequest {
  url: string;
  formats?: string[];
  only_main_content?: boolean;
}

interface ScrapeResponse {
  success: boolean;
  url: string;
  content: string | null;
  metadata: Record<string, unknown> | null;
  error: string | null;
}

export function useScrape() {
  return useMutation<ScrapeResponse, Error, ScrapeRequest>({
    mutationFn: async (request) => {
      const response = await apiClient.post<ScrapeResponse>(
        "/api/v1/scraping/scrape",
        request
      );
      
      if (!response.data.success) {
        throw new Error(response.data.error || "스크래핑에 실패했습니다.");
      }
      
      return response.data;
    },
  });
}

interface ExtractRequest {
  url: string;
  prompt: string;
  schema?: Record<string, unknown>;
}

interface ExtractResponse {
  success: boolean;
  url: string;
  data: Record<string, unknown> | null;
  raw_content: string | null;
  error: string | null;
}

export function useExtract() {
  return useMutation<ExtractResponse, Error, ExtractRequest>({
    mutationFn: async (request) => {
      const response = await apiClient.post<ExtractResponse>(
        "/api/v1/scraping/extract",
        request
      );
      
      if (!response.data.success) {
        throw new Error(response.data.error || "데이터 추출에 실패했습니다.");
      }
      
      return response.data;
    },
  });
}
