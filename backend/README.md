# WebScraping Automation Builder - Backend

## 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── api/
│   │   ├── __init__.py      # API router aggregation
│   │   └── v1/
│   │       ├── auth.py      # Authentication endpoints
│   │       ├── scraping.py  # Scraping endpoints
│   │       └── insights.py  # LLM insights endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Settings management
│   ├── services/
│   │   ├── firecrawl_service.py  # Firecrawl API wrapper
│   │   └── llm_service.py        # OpenRouter LLM service
│   └── models/              # SQLAlchemy models (Phase 2)
├── requirements.txt
└── README.md
```

## 로컬 개발 환경 설정

### 1. 가상환경 생성

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일 편집하여 API 키 설정
```

### 4. 서버 실행

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. API 문서 확인

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### 스크래핑 API (`/api/v1/scraping`)

- `POST /scrape` - 단일 URL 스크래핑
- `POST /extract` - 구조화된 데이터 추출
- `POST /quick` - 빠른 스크래핑 + 자동 추출 + 인사이트

### 인사이트 API (`/api/v1/insights`)

- `POST /analyze` - 데이터 분석 및 인사이트 생성
- `POST /compare` - 데이터 비교 분석
- `POST /report` - 리포트 생성
- `GET /templates` - 인사이트 템플릿 목록

### 인증 API (`/api/v1/auth`)

- `POST /register` - 회원가입
- `POST /login` - 로그인
- `GET /me` - 현재 사용자 정보

## 개발 상태

- [x] API 구조 설계
- [x] Firecrawl 서비스 연동
- [x] LLM 서비스 (OpenRouter)
- [ ] 데이터베이스 모델
- [ ] 인증 구현
- [ ] Celery 작업 큐
