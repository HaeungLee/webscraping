# MVP 설계 문서

> 작성일: 2025-11-30  
> 목표: LLM 인사이트 가치 검증 (4주)

---

## 1. MVP 목표

### 1.1 핵심 가설
> **"스크래핑 데이터에 LLM 인사이트를 더하면, 사용자가 돈을 낼 것이다"**

### 1.2 성공 지표
- [ ] 10명 이상의 테스트 사용자 확보
- [ ] 3명 이상 "돈 내고 쓰겠다" 피드백
- [ ] 인사이트 리포트 품질 만족도 4/5 이상

---

## 2. MVP 기능 명세

### 2.1 사용자 플로우

```
┌─────────────────────────────────────────────────────────────────┐
│                        MVP 사용자 여정                          │
└─────────────────────────────────────────────────────────────────┘

[1] 랜딩 페이지
    │
    ▼
[2] 회원가입/로그인 (이메일)
    │
    ▼
[3] 대시보드
    │
    ├──▶ [새 분석 시작]
    │         │
    │         ▼
    │    ┌─────────────────────────────────────────┐
    │    │  URL 입력                               │
    │    │  ┌─────────────────────────────────┐   │
    │    │  │ https://www.coupang.com/...     │   │
    │    │  └─────────────────────────────────┘   │
    │    │                                         │
    │    │  또는 템플릿 선택:                      │
    │    │  [쿠팡 카테고리] [네이버쇼핑] [...]    │
    │    │                                         │
    │    │  분석 요청 (자연어):                    │
    │    │  ┌─────────────────────────────────┐   │
    │    │  │ "상품별 가격과 리뷰 분석해줘"   │   │
    │    │  └─────────────────────────────────┘   │
    │    │                                         │
    │    │  [분석 시작] 버튼                       │
    │    └─────────────────────────────────────────┘
    │         │
    │         ▼
    │    ┌─────────────────────────────────────────┐
    │    │  로딩 (실시간 진행 상황)                │
    │    │  ✓ 페이지 수집 중...                   │
    │    │  ✓ 데이터 추출 중...                   │
    │    │  ○ 인사이트 생성 중...                 │
    │    └─────────────────────────────────────────┘
    │         │
    │         ▼
    │    ┌─────────────────────────────────────────┐
    │    │  결과 페이지                            │
    │    │                                         │
    │    │  📊 수집 데이터 (테이블)               │
    │    │  ┌─────────────────────────────────┐   │
    │    │  │ 상품명 │ 가격  │ 리뷰수 │ 평점 │   │
    │    │  │ ────── │ ───── │ ────── │ ──── │   │
    │    │  │ 노트북 │ 89만  │ 1,234  │ 4.5  │   │
    │    │  │ ...    │ ...   │ ...    │ ...  │   │
    │    │  └─────────────────────────────────┘   │
    │    │                                         │
    │    │  💡 AI 인사이트                        │
    │    │  ┌─────────────────────────────────┐   │
    │    │  │ ## 가격대 분석                  │   │
    │    │  │ - 50만원 미만: 35%              │   │
    │    │  │ - 50-100만원: 45%               │   │
    │    │  │ - 100만원 이상: 20%             │   │
    │    │  │                                 │   │
    │    │  │ ## 인기 상품 특징               │   │
    │    │  │ - 리뷰 1000개 이상 상품은...    │   │
    │    │  │                                 │   │
    │    │  │ ## 제안                         │   │
    │    │  │ - 70-90만원대 진입 추천         │   │
    │    │  └─────────────────────────────────┘   │
    │    │                                         │
    │    │  [CSV 다운로드] [리포트 PDF]           │
    │    └─────────────────────────────────────────┘
    │
    └──▶ [이전 분석 결과]
              │
              ▼
         결과 목록 → 상세 보기
```

---

### 2.2 페이지 구성

| 페이지 | 경로 | 설명 |
|--------|------|------|
| 랜딩 | `/` | 서비스 소개, CTA |
| 로그인 | `/login` | 이메일 로그인 |
| 회원가입 | `/register` | 이메일 회원가입 |
| 대시보드 | `/dashboard` | 분석 목록, 새 분석 시작 |
| 새 분석 | `/analyze` | URL 입력, 템플릿 선택 |
| 결과 | `/results/[id]` | 데이터 테이블 + 인사이트 |

---

### 2.3 API 설계 (최소)

```
POST /api/auth/register     # 회원가입
POST /api/auth/login        # 로그인
GET  /api/auth/me           # 현재 사용자

POST /api/analyze           # 분석 시작
GET  /api/analyze/[id]      # 분석 결과 조회
GET  /api/analyze           # 내 분석 목록

GET  /api/templates         # 템플릿 목록
```

---

### 2.4 데이터 모델 (최소)

```sql
-- 사용자
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 분석 작업
CREATE TABLE analyses (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  
  -- 입력
  url TEXT NOT NULL,
  template_id VARCHAR(50),  -- 'coupang', 'naver' 등
  prompt TEXT,              -- 사용자 자연어 요청
  
  -- 상태
  status VARCHAR(20) DEFAULT 'pending',  -- pending, processing, completed, failed
  
  -- 결과
  raw_data JSONB,           -- Firecrawl 원본
  extracted_data JSONB,     -- LLM 구조화 데이터
  insights TEXT,            -- LLM 인사이트 (마크다운)
  
  -- 메타
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP
);

-- 템플릿 (시드 데이터)
CREATE TABLE templates (
  id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  url_pattern TEXT,         -- URL 패턴 예시
  extraction_prompt TEXT,   -- LLM 추출 프롬프트
  insight_prompt TEXT,      -- LLM 인사이트 프롬프트
  is_active BOOLEAN DEFAULT true
);
```

---

## 3. MVP 아키텍처 (간소화)

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend                                 │
│                     Next.js (Vercel)                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │ 랜딩    │  │ 인증    │  │대시보드 │  │ 결과    │           │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend API                                 │
│                   FastAPI (Railway)                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Auth API   │  │ Analyze API │  │Template API │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
│   PostgreSQL    │ │  Firecrawl  │ │   OpenRouter    │
│   (Railway)     │ │  (Railway)  │ │   (LLM API)     │
└─────────────────┘ └─────────────┘ └─────────────────┘
```

### 3.1 기술 스택 (MVP)

| 영역 | 기술 | 이유 |
|------|------|------|
| Frontend | Next.js 14 + TypeScript | 빠른 개발, SSR |
| UI | shadcn/ui + Tailwind | 빠른 UI 구축 |
| Backend | FastAPI | 비동기, LLM 통합 용이 |
| DB | PostgreSQL (Railway) | 간단한 셋업 |
| 스크래핑 | Firecrawl (Self-hosted) | 검증된 솔루션 |
| LLM | OpenRouter (무료 모델) | 비용 절감 |
| 배포 | Vercel + Railway | 빠른 배포 |

### 3.2 MVP에서 제외된 것들

- ❌ Redis (세션은 JWT로)
- ❌ Celery (동기 처리로 시작)
- ❌ 복잡한 큐잉 (순차 처리)
- ❌ Chrome 확장 프로그램
- ❌ 워크플로우 빌더
- ❌ 스케줄링

---

## 4. LLM 프롬프트 설계

### 4.1 데이터 추출 프롬프트

```python
EXTRACTION_PROMPT = """
당신은 웹 스크래핑 데이터 추출 전문가입니다.

다음 웹페이지 콘텐츠에서 사용자가 원하는 데이터를 추출하세요.

## 웹페이지 콘텐츠:
{markdown_content}

## 사용자 요청:
{user_prompt}

## 추출 가이드:
{template_extraction_guide}

## 출력 형식:
JSON 배열로 출력하세요. 각 항목은 추출된 데이터 객체입니다.

```json
[
  {
    "field1": "value1",
    "field2": "value2"
  }
]
```
"""
```

### 4.2 인사이트 생성 프롬프트

```python
INSIGHT_PROMPT = """
당신은 데이터 분석 전문가입니다.

다음 데이터를 분석하고 비즈니스 인사이트를 제공하세요.

## 수집된 데이터:
{extracted_data}

## 데이터 출처:
{source_url}

## 사용자 컨텍스트:
{user_prompt}

## 분석 요청:
{template_insight_guide}

## 출력 형식:
마크다운으로 작성하세요. 다음 섹션을 포함하세요:

1. **📊 데이터 요약**: 수집된 데이터의 기본 통계
2. **💡 핵심 발견**: 눈에 띄는 패턴이나 특이점
3. **📈 트렌드 분석**: 가격/인기도 등의 경향
4. **🎯 제안사항**: 이 데이터를 어떻게 활용할 수 있는지
5. **⚠️ 주의사항**: 데이터 해석 시 고려할 점
"""
```

### 4.3 쿠팡 템플릿 예시

```python
COUPANG_TEMPLATE = {
    "id": "coupang_category",
    "name": "쿠팡 카테고리 분석",
    "description": "쿠팡 카테고리 페이지에서 상품 정보를 수집하고 분석합니다",
    "url_pattern": "https://www.coupang.com/np/categories/*",
    
    "extraction_prompt": """
다음 필드를 추출하세요:
- product_name: 상품명
- price: 가격 (숫자만)
- original_price: 원가 (할인 전, 있는 경우)
- discount_rate: 할인율 (%, 있는 경우)
- rating: 평점 (5점 만점)
- review_count: 리뷰 수
- rocket_delivery: 로켓배송 여부 (true/false)
- seller: 판매자명
""",
    
    "insight_prompt": """
다음 관점에서 분석해주세요:
1. 가격대별 상품 분포
2. 할인율과 리뷰 수의 상관관계
3. 로켓배송 상품의 특징
4. 가장 인기있는 가격대와 그 이유
5. 이 카테고리 진입 시 추천 전략
"""
}
```

---

## 5. 개발 일정 (4주)

### Week 1: 기반 구축
```
Day 1-2: 프로젝트 셋업
├── Next.js 프로젝트 생성
├── FastAPI 프로젝트 생성
├── Railway 설정 (PostgreSQL, Firecrawl)
└── 기본 배포 파이프라인

Day 3-4: 인증 구현
├── 회원가입/로그인 API
├── JWT 토큰 관리
└── 프론트엔드 인증 플로우

Day 5: DB 설계 & 마이그레이션
├── 스키마 생성
├── 시드 데이터 (템플릿)
└── ORM 설정
```

### Week 2: 핵심 기능
```
Day 1-2: Firecrawl 연동
├── Firecrawl 셀프호스팅 설정
├── 스크래핑 API 구현
└── 에러 핸들링

Day 3-4: LLM 파이프라인
├── OpenRouter 연동
├── 데이터 추출 로직
├── 인사이트 생성 로직
└── 프롬프트 튜닝

Day 5: 분석 API 완성
├── 전체 파이프라인 연결
├── 상태 관리
└── 결과 저장
```

### Week 3: 프론트엔드
```
Day 1-2: 레이아웃 & 인증 UI
├── 공통 레이아웃
├── 로그인/회원가입 페이지
└── 대시보드 껍데기

Day 3-4: 분석 UI
├── URL 입력 폼
├── 템플릿 선택
├── 로딩 상태
└── 결과 페이지 (테이블 + 인사이트)

Day 5: 결과 & 다운로드
├── 결과 목록
├── CSV 다운로드
└── 인사이트 복사/공유
```

### Week 4: 마무리 & 테스트
```
Day 1-2: 통합 테스트
├── E2E 플로우 테스트
├── 버그 수정
└── 에러 처리 강화

Day 3-4: 랜딩 페이지
├── 서비스 소개
├── 데모 영상/스크린샷
└── CTA

Day 5: 배포 & 피드백 준비
├── 프로덕션 배포
├── 모니터링 설정
└── 피드백 수집 폼
```

---

## 6. MVP 이후 로드맵

### Phase 2 (MVP 검증 후)
- [ ] 스케줄링 기능
- [ ] Google Sheets 연동
- [ ] 추가 템플릿 (네이버쇼핑, 당근마켓)
- [ ] 결제 시스템 (토스페이먼츠)

### Phase 3
- [ ] 비주얼 셀렉터 (Chrome 확장)
- [ ] 워크플로우 빌더
- [ ] 팀 기능

### Phase 4 (North Star)
- [ ] Playwright MCP 기반 화면 직접 추출
- [ ] 에이전트 오케스트레이션
- [ ] "리서치 → 분석 → 결정 → 실행" 풀 자동화

---

## 7. 디렉토리 구조

### Frontend (Next.js)
```
frontend/
├── app/
│   ├── page.tsx              # 랜딩
│   ├── login/page.tsx
│   ├── register/page.tsx
│   ├── dashboard/page.tsx
│   ├── analyze/page.tsx
│   └── results/[id]/page.tsx
├── components/
│   ├── ui/                   # shadcn/ui
│   ├── layout/
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── analyze/
│   │   ├── UrlInput.tsx
│   │   ├── TemplateSelector.tsx
│   │   └── ProgressIndicator.tsx
│   └── results/
│       ├── DataTable.tsx
│       └── InsightCard.tsx
├── lib/
│   ├── api.ts                # API 클라이언트
│   ├── auth.ts               # 인증 유틸
│   └── utils.ts
└── hooks/
    ├── useAuth.ts
    └── useAnalysis.ts
```

### Backend (FastAPI)
```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── auth.py
│   │   ├── analyze.py
│   │   └── templates.py
│   ├── models/
│   │   ├── user.py
│   │   └── analysis.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── analysis.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── scraping_service.py
│   │   └── llm_service.py
│   └── utils/
│       ├── security.py
│       └── prompts.py
├── alembic/
└── requirements.txt
```

---

## 8. 즉시 시작할 것

### 오늘
1. [ ] 프로젝트 디렉토리 생성
2. [ ] Next.js 프로젝트 초기화
3. [ ] FastAPI 프로젝트 초기화
4. [ ] Railway 계정/프로젝트 설정

### 내일
5. [ ] Firecrawl 로컬 테스트
6. [ ] OpenRouter API 테스트
7. [ ] 쿠팡 페이지 스크래핑 + LLM 분석 PoC

---

*이 문서는 MVP 개발 중 업데이트됩니다.*
