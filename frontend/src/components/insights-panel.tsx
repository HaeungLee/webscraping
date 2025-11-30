"use client";

import { Sparkles, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react";

interface InsightsPanelProps {
  insights: {
    summary?: string;
    key_findings?: string[];
    trends?: string[];
    recommendations?: string[];
    risk_factors?: string[];
    confidence_score?: number;
  } | null;
}

export function InsightsPanel({ insights }: InsightsPanelProps) {
  if (!insights) return null;

  return (
    <div className="bg-card border rounded-xl shadow-sm overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b bg-gradient-to-r from-primary/5 to-primary/10">
        <Sparkles className="w-4 h-4 text-primary" />
        <h3 className="font-semibold">AI 인사이트</h3>
        {insights.confidence_score !== undefined && (
          <span className="ml-auto text-xs px-2 py-0.5 bg-primary/20 text-primary rounded-full">
            신뢰도: {Math.round(insights.confidence_score * 100)}%
          </span>
        )}
      </div>

      {/* Content */}
      <div className="p-4 space-y-5">
        {/* Summary */}
        {insights.summary && (
          <div>
            <h4 className="font-medium text-sm text-muted-foreground mb-2">요약</h4>
            <p className="text-foreground leading-relaxed">{insights.summary}</p>
          </div>
        )}

        {/* Key Findings */}
        {insights.key_findings && insights.key_findings.length > 0 && (
          <div>
            <h4 className="font-medium text-sm text-muted-foreground mb-2 flex items-center gap-1">
              <CheckCircle className="w-4 h-4 text-green-500" />
              주요 발견
            </h4>
            <ul className="space-y-2">
              {insights.key_findings.map((finding, index) => (
                <li
                  key={index}
                  className="flex items-start gap-2 text-sm"
                >
                  <span className="w-5 h-5 rounded-full bg-green-100 text-green-700 text-xs flex items-center justify-center flex-shrink-0 mt-0.5">
                    {index + 1}
                  </span>
                  <span>{finding}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Trends */}
        {insights.trends && insights.trends.length > 0 && (
          <div>
            <h4 className="font-medium text-sm text-muted-foreground mb-2 flex items-center gap-1">
              <TrendingUp className="w-4 h-4 text-blue-500" />
              트렌드
            </h4>
            <div className="flex flex-wrap gap-2">
              {insights.trends.map((trend, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-blue-50 text-blue-700 text-sm rounded-full"
                >
                  {trend}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations */}
        {insights.recommendations && insights.recommendations.length > 0 && (
          <div>
            <h4 className="font-medium text-sm text-muted-foreground mb-2 flex items-center gap-1">
              <Sparkles className="w-4 h-4 text-primary" />
              추천 액션
            </h4>
            <ul className="space-y-2">
              {insights.recommendations.map((rec, index) => (
                <li
                  key={index}
                  className="flex items-start gap-2 text-sm p-2 bg-primary/5 rounded-lg"
                >
                  <span className="text-primary">→</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Risk Factors */}
        {insights.risk_factors && insights.risk_factors.length > 0 && (
          <div>
            <h4 className="font-medium text-sm text-muted-foreground mb-2 flex items-center gap-1">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              리스크 요인
            </h4>
            <ul className="space-y-1">
              {insights.risk_factors.map((risk, index) => (
                <li
                  key={index}
                  className="flex items-start gap-2 text-sm text-amber-700"
                >
                  <span>⚠</span>
                  <span>{risk}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
