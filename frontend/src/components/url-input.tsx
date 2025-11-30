"use client";

import { useState } from "react";
import { Loader2, Search, ArrowRight } from "lucide-react";

interface UrlInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading?: boolean;
}

export function UrlInput({ value, onChange, onSubmit, isLoading }: UrlInputProps) {
  const [focused, setFocused] = useState(false);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !isLoading) {
      onSubmit();
    }
  };

  return (
    <div
      className={`
        relative flex items-center gap-2 p-2 
        bg-background border-2 rounded-xl shadow-lg
        transition-all duration-200
        ${focused ? "border-primary ring-4 ring-primary/10" : "border-border"}
      `}
    >
      <div className="flex items-center justify-center w-10 h-10 text-muted-foreground">
        <Search className="w-5 h-5" />
      </div>
      
      <input
        type="url"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        onKeyDown={handleKeyDown}
        placeholder="분석할 URL을 입력하세요 (예: https://www.coupang.com/...)"
        className="flex-1 bg-transparent text-lg outline-none placeholder:text-muted-foreground/60"
        disabled={isLoading}
      />
      
      <button
        onClick={onSubmit}
        disabled={isLoading || !value.trim()}
        className={`
          flex items-center gap-2 px-6 py-3 rounded-lg font-medium
          transition-all duration-200
          ${
            isLoading || !value.trim()
              ? "bg-muted text-muted-foreground cursor-not-allowed"
              : "bg-primary text-primary-foreground hover:bg-primary/90 active:scale-95"
          }
        `}
      >
        {isLoading ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>분석 중...</span>
          </>
        ) : (
          <>
            <span>분석 시작</span>
            <ArrowRight className="w-4 h-4" />
          </>
        )}
      </button>
    </div>
  );
}
