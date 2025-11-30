"use client";

import { useState } from "react";
import { useQuickScrape } from "@/hooks/use-scraping";
import { UrlInput } from "@/components/url-input";
import { ResultsPanel } from "@/components/results-panel";
import { InsightsPanel } from "@/components/insights-panel";

export default function Home() {
  const [url, setUrl] = useState("");
  const { mutate: scrape, data, isPending, error } = useQuickScrape();

  const handleScrape = () => {
    if (url.trim()) {
      scrape({ url, data_type: "auto" });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted/20">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-sm">WS</span>
              </div>
              <h1 className="text-xl font-bold">WebScraping Builder</h1>
            </div>
            <nav className="flex items-center gap-4">
              <span className="text-sm text-muted-foreground">MVP v0.1</span>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">
            URL 하나로 데이터 추출부터 인사이트까지
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            웹사이트 URL을 입력하면 AI가 자동으로 데이터를 추출하고
            비즈니스 인사이트를 생성합니다.
          </p>
        </div>

        {/* URL Input Section */}
        <div className="max-w-3xl mx-auto mb-12">
          <UrlInput
            value={url}
            onChange={setUrl}
            onSubmit={handleScrape}
            isLoading={isPending}
          />
        </div>

        {/* Error Display */}
        {error && (
          <div className="max-w-3xl mx-auto mb-8 p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
            <p className="text-destructive text-sm">
              오류가 발생했습니다: {error.message}
            </p>
          </div>
        )}

        {/* Results Section */}
        {data && (
          <div className="grid lg:grid-cols-2 gap-8">
            <ResultsPanel data={data.extracted_data} rawContent={data.raw_content} />
            <InsightsPanel insights={data.insights} />
          </div>
        )}

        {/* Empty State */}
        {!data && !isPending && (
          <div className="text-center py-16">
            <div className="max-w-md mx-auto">
              <div className="text-6xl mb-4">🔍</div>
              <h3 className="text-xl font-semibold mb-2">시작하기</h3>
              <p className="text-muted-foreground">
                분석하고 싶은 웹페이지 URL을 입력하세요.
                <br />
                상품 페이지, 뉴스 기사, 블로그 등 다양한 페이지를 지원합니다.
              </p>
              <div className="mt-6 flex flex-wrap justify-center gap-2">
                <ExampleButton 
                  url="https://www.coupang.com/np/categories/194176" 
                  label="쿠팡 카테고리"
                  onClick={setUrl}
                />
                <ExampleButton 
                  url="https://news.naver.com" 
                  label="네이버 뉴스"
                  onClick={setUrl}
                />
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t mt-auto py-6">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          © 2024 WebScraping Automation Builder. AI Data Intelligence Platform.
        </div>
      </footer>
    </div>
  );
}

function ExampleButton({ 
  url, 
  label, 
  onClick 
}: { 
  url: string; 
  label: string; 
  onClick: (url: string) => void;
}) {
  return (
    <button
      onClick={() => onClick(url)}
      className="px-3 py-1.5 text-sm border rounded-full hover:bg-muted transition-colors"
    >
      {label}
    </button>
  );
}
