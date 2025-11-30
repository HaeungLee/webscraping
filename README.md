# WebScraping Automation Builder

🚀 **노코드 웹 스크래핑 자동화 빌더** - AI 데이터 인텔리전스 플랫폼

URL 하나로 웹 스크래핑부터 AI 인사이트까지. 코딩 없이 데이터를 추출하고 비즈니스 인사이트를 얻으세요.

## ✨ 핵심 기능

- **🔗 URL 기반 스크래핑**: URL 입력만으로 자동 데이터 추출
- **🤖 AI 데이터 추출**: LLM이 자동으로 구조화된 데이터 생성
- **📊 AI 인사이트**: 추출된 데이터에서 비즈니스 인사이트 도출
- **📝 리포트 생성**: 분석 결과를 보기 좋은 리포트로 제공

## 🏗️ 기술 스택

| 영역 | 기술 |
|------|------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, shadcn/ui |
| Backend | FastAPI (Python), Pydantic |
| Scraping | Firecrawl (Self-hosted) |
| LLM | OpenRouter (Free models → GPT-5) |
| Database | PostgreSQL |
| Cache/Queue | Redis, Celery (Phase 2) |

## 📁 프로젝트 구조

```
webscraping/
├── frontend/           # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/       # App Router pages
│   │   ├── components/ # React 컴포넌트
│   │   ├── hooks/     # Custom hooks
│   │   └── lib/       # 유틸리티
│   └── package.json
├── backend/           # FastAPI 백엔드
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Config, security
│   │   ├── services/  # Business logic
│   │   └── models/    # Database models
│   └── requirements.txt
├── docs/              # 문서
│   ├── 요구사항명세.md
│   ├── 아키텍처.md
│   ├── MVP설계.md
│   └── 실행계획.md
├── docker-compose.yml # Docker 개발 환경
└── .env.example       # 환경 변수 템플릿
```

## 🚀 빠른 시작

### 사전 요구사항

- **Node.js** 18+ 
- **Python** 3.11+
- **Docker** & Docker Compose
- **OpenRouter API Key** ([무료 가입](https://openrouter.ai/keys))

### 1. 저장소 클론 & 환경 설정

```powershell
# 환경 변수 설정
cp .env.example .env
# .env 파일에 OPENROUTER_API_KEY 입력
```

### 2. Docker 서비스 시작 (PostgreSQL, Redis, Firecrawl)

```powershell
docker-compose up -d
```

### 3. Backend 설정 & 실행

```powershell
cd backend

# 가상환경 생성
python -m venv venv
.\venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 복사
cp .env.example .env

# 서버 시작
uvicorn app.main:app --reload --port 8000
```

### 4. Frontend 설정 & 실행

```powershell
cd frontend

# 의존성 설치
npm install

# 환경 변수 복사
cp .env.example .env.local

# 개발 서버 시작
npm run dev
```

### 5. 접속

- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Firecrawl**: http://localhost:3002

## 📖 API 사용법

### Quick Scrape (URL → 데이터 + 인사이트)

```bash
curl -X POST http://localhost:8000/api/v1/scraping/quick \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.coupang.com/np/categories/194176", "data_type": "auto"}'
```

### Response Example

```json
{
  "success": true,
  "url": "https://www.coupang.com/np/categories/194176",
  "extracted_data": {
    "detected_type": "products",
    "items": [
      {"name": "상품명", "price": 29900, "rating": 4.8}
    ]
  },
  "insights": {
    "summary": "총 20개 상품 분석. 평균 가격 32,450원...",
    "key_findings": ["가격 범위 15,000원~89,000원", "평균 평점 4.5점"],
    "recommendations": ["고평점 상품 벤치마킹 추천"]
  }
}
```

## 🗺️ 로드맵

| Phase | 기간 | 목표 |
|-------|------|------|
| Phase 0 | 2-3일 | PoC - Firecrawl + LLM 테스트 |
| Phase 1 | 1주 | 프로젝트 셋업 + 인증 + DB |
| Phase 2 | 1주 | 스크래핑 + LLM API 구현 |
| Phase 3 | 1주 | 프론트엔드 UI 완성 |
| Phase 4 | 1주 | 테스트 + 배포 + 런칭 |

## 🤝 Contributing

이 프로젝트는 개인 프로젝트입니다. 피드백과 제안은 언제나 환영합니다!

## 📄 License

MIT License

---

Made with ❤️ for Korean Market First 🇰🇷
