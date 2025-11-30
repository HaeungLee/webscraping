import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "WebScraping Automation Builder",
  description: "노코드 웹 스크래핑 자동화 빌더 - AI 데이터 인텔리전스 플랫폼",
  keywords: ["웹 스크래핑", "자동화", "AI", "데이터 분석", "노코드"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
