"use client";

import { Database, FileJson } from "lucide-react";

interface ResultsPanelProps {
  data: Record<string, unknown> | null;
  rawContent?: string | null;
}

export function ResultsPanel({ data, rawContent }: ResultsPanelProps) {
  if (!data) return null;

  return (
    <div className="bg-card border rounded-xl shadow-sm overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b bg-muted/30">
        <Database className="w-4 h-4 text-primary" />
        <h3 className="font-semibold">추출된 데이터</h3>
        <span className="ml-auto text-xs text-muted-foreground">
          {getItemCount(data)} items
        </span>
      </div>

      {/* Content */}
      <div className="p-4 max-h-[500px] overflow-auto">
        {/* Detected Type */}
        {data.detected_type && (
          <div className="mb-4 flex items-center gap-2">
            <span className="text-sm text-muted-foreground">감지된 타입:</span>
            <span className="px-2 py-0.5 bg-primary/10 text-primary text-sm rounded-full">
              {String(data.detected_type)}
            </span>
          </div>
        )}

        {/* Items */}
        {Array.isArray(data.items) && data.items.length > 0 ? (
          <div className="space-y-3">
            {data.items.slice(0, 10).map((item: unknown, index: number) => (
              <div
                key={index}
                className="p-3 bg-muted/30 rounded-lg border border-border/50"
              >
                <DataItem data={item} />
              </div>
            ))}
            {data.items.length > 10 && (
              <p className="text-sm text-muted-foreground text-center py-2">
                + {data.items.length - 10}개 더 있음
              </p>
            )}
          </div>
        ) : (
          <div className="p-4 bg-muted/30 rounded-lg">
            <pre className="text-sm whitespace-pre-wrap break-all">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>
        )}

        {/* Raw Content Preview */}
        {rawContent && (
          <details className="mt-4">
            <summary className="cursor-pointer text-sm text-muted-foreground hover:text-foreground">
              <FileJson className="w-4 h-4 inline mr-1" />
              원본 콘텐츠 미리보기
            </summary>
            <pre className="mt-2 p-3 bg-muted/30 rounded-lg text-xs whitespace-pre-wrap break-all max-h-40 overflow-auto">
              {rawContent}
            </pre>
          </details>
        )}
      </div>
    </div>
  );
}

function DataItem({ data }: { data: unknown }) {
  if (typeof data !== "object" || data === null) {
    return <span className="text-sm">{String(data)}</span>;
  }

  const obj = data as Record<string, unknown>;
  const entries = Object.entries(obj).slice(0, 6);

  return (
    <dl className="grid grid-cols-2 gap-x-4 gap-y-1 text-sm">
      {entries.map(([key, value]) => (
        <div key={key} className="contents">
          <dt className="text-muted-foreground truncate">{key}:</dt>
          <dd className="font-medium truncate" title={String(value)}>
            {formatValue(value)}
          </dd>
        </div>
      ))}
    </dl>
  );
}

function getItemCount(data: Record<string, unknown>): number {
  if (Array.isArray(data.items)) {
    return data.items.length;
  }
  return Object.keys(data).length;
}

function formatValue(value: unknown): string {
  if (value === null || value === undefined) return "-";
  if (typeof value === "boolean") return value ? "✓" : "✗";
  if (typeof value === "number") return value.toLocaleString("ko-KR");
  if (typeof value === "string") return value;
  if (Array.isArray(value)) return `[${value.length} items]`;
  if (typeof value === "object") return `{...}`;
  return String(value);
}
