# WebScraping Automation Builder - Frontend

## 프로젝트 구조

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx      # 루트 레이아웃
│   │   ├── page.tsx        # 메인 페이지
│   │   ├── providers.tsx   # React Query, Theme providers
│   │   └── globals.css     # 전역 스타일
│   ├── components/
│   │   ├── url-input.tsx   # URL 입력 컴포넌트
│   │   ├── results-panel.tsx   # 추출 결과 표시
│   │   └── insights-panel.tsx  # AI 인사이트 표시
│   ├── hooks/
│   │   └── use-scraping.ts # 스크래핑 API hooks
│   └── lib/
│       ├── api-client.ts   # Axios 클라이언트
│       └── utils.ts        # 유틸리티 함수
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

## 로컬 개발

### 1. 의존성 설치

```bash
npm install
```

### 2. 환경 변수 설정

```bash
cp .env.example .env.local
```

### 3. 개발 서버 시작

```bash
npm run dev
```

### 4. 접속

http://localhost:3000

## 사용된 라이브러리

- **Next.js 14**: React 프레임워크 (App Router)
- **TypeScript**: 타입 안전성
- **Tailwind CSS**: 유틸리티 CSS
- **React Query**: 서버 상태 관리
- **Zustand**: 클라이언트 상태 관리
- **Axios**: HTTP 클라이언트
- **Lucide React**: 아이콘
- **React Hook Form + Zod**: 폼 관리

## 주요 컴포넌트

### UrlInput
URL 입력 및 스크래핑 시작 버튼

### ResultsPanel
추출된 데이터를 카드 형태로 표시

### InsightsPanel
AI가 생성한 인사이트를 섹션별로 표시

## 개발 상태

- [x] 기본 UI 레이아웃
- [x] URL 입력 컴포넌트
- [x] 결과 표시 패널
- [x] API 연동 hooks
- [ ] 로그인/회원가입 페이지
- [ ] 스크래핑 히스토리
- [ ] 리포트 다운로드
