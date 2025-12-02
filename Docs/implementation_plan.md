# 법령 Q&A 웹앱 구현 계획

## 1. 프로젝트 구조 설계

### 프론트엔드 (React + TypeScript + Vite)
```
frontend/
├── public/
│   ├── favicon.ico
│   └── assets/
├── src/
│   ├── components/
│   │   ├── Chat/
│   │   │   ├── ChatContainer.tsx       # 전체 채팅 컨테이너
│   │   │   ├── ChatMessage.tsx         # 개별 메시지 컴포넌트
│   │   │   ├── ChatInput.tsx           # 메시지 입력 컴포넌트
│   │   │   └── ChatHistory.tsx         # 대화 히스토리 관리
│   │   ├── UI/
│   │   │   ├── Header.tsx              # 헤더 컴포넌트
│   │   │   ├── Footer.tsx              # 푸터 컴포넌트
│   │   │   ├── Button.tsx              # 재사용 버튼 컴포넌트
│   │   │   └── Loading.tsx             # 로딩 인디케이터
│   │   └── LawReference/
│   │       ├── LawCitation.tsx         # 법령 인용 컴포넌트
│   │       └── LawLink.tsx             # 법령 링크 컴포넌트
│   ├── hooks/
│   │   ├── useChat.ts                  # 채팅 관련 커스텀 훅
│   │   └── useLocalStorage.ts          # 로컬 스토리지 관리
│   ├── services/
│   │   ├── api.ts                      # API 호출 함수
│   │   └── lawService.ts               # 법령 관련 서비스
│   ├── types/
│   │   ├── chat.ts                     # 채팅 관련 타입
│   │   └── law.ts                      # 법령 관련 타입
│   ├── utils/
│   │   ├── formatters.ts               # 포맷팅 유틸리티
│   │   └── validators.ts               # 유효성 검사
│   ├── App.tsx                         # 메인 앱 컴포넌트
│   ├── main.tsx                        # 앱 진입점
│   └── styles/
│       ├── global.css                  # 전역 스타일
│       └── variables.css               # CSS 변수
├── package.json
├── tsconfig.json
└── vite.config.ts
```

### 백엔드 (FastAPI + SQLite / Firebase Firestore)
```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py                     # 채팅 관련 API
│   │   └── law.py                      # 법령 관련 API
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                   # 환경 설정 (DB_TYPE 선택 가능)
│   │   └── security.py                 # API 키 관리
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py                 # DB 연결 관리 (SQLite)
│   │   └── models.py                   # SQLite ORM 모델
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py                     # Repository 인터페이스
│   │   ├── conversation_repository.py  # 대화 데이터 접근 (추상화)
│   │   └── message_repository.py       # 메시지 데이터 접근 (추상화)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat.py                     # Pydantic 스키마 (Firestore 호환)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py             # 채팅 처리 서비스
│   │   ├── law_service.py              # 법령 검색 서비스
│   │   └── openai_service.py           # OpenAI API 연동
│   ├── utils/
│   │   ├── __init__.py
│   │   └── date_utils.py               # 날짜/시간 처리 (UTC/KST)
│   ├── mock/
│   │   ├── __init__.py
│   │   └── law_data.py                 # 목업 법령 데이터
│   └── main.py                         # FastAPI 앱 진입점
├── requirements.txt
├── README.md                           # 프로젝트 문서
├── FIREBASE_MIGRATION_GUIDE.md         # Firebase 전환 가이드
└── .env.example                        # 환경변수 예시
```

**데이터베이스 전략:**
- **로컬 개발**: SQLite 사용 (기본값)
- **Firebase 전환**: `DB_TYPE=firestore` 환경 변수로 전환 가능
- **Repository 패턴**: 데이터 접근 로직 추상화로 DB 변경 시 영향 최소화
- **Pydantic 스키마**: Firestore와 호환되는 데이터 검증 구조

### 환경 및 시간대 관리 원칙
- **시간대 단일화**: 모든 날짜/시간은 서버 내부에서 UTC로 저장하고, 사용자 출력 시에만 KST 등 현지 시간으로 변환한다. 서버와 프론트엔드 모두 `date_utils.py`(또는 동등한 헬퍼)만 사용하도록 강제한다.
- **규칙 문서 동기화**: `time_rules.md`와 실제 코드의 규칙이 달라지지 않도록, 변경 시 두 곳을 동시에 업데이트한다.
- **환경 변수 문서화**: `.env.example`에 필수 키(OpenAI API 키, 법령 API 키, TIMEZONE, APP_ENV 등)를 모두 포함하고 README에서 설명한다. FastAPI 기동 시 누락된 변수는 즉시 에러를 발생시켜 조기에 감지한다.
- **데이터베이스 선택**: `DB_TYPE` 환경 변수로 `sqlite`(로컬) 또는 `firestore`(Firebase)를 선택할 수 있다. 기본값은 `sqlite`이며, Firebase 전환 시 최소한의 코드 변경으로 전환 가능하도록 Repository 패턴으로 추상화되어 있다.
- **Docker 미사용 전제**: Docker 없이도 동일한 환경을 재현하기 위해 `python-dotenv`와 간단한 PowerShell/Unix 스크립트를 제공하고, OS 별 경로/인코딩 차이를 고려한다.
- **로컬/배포 분기**: 로컬에서는 SQLite를 사용하고, 나중에 Firebase Firestore로 전환할 수 있도록 설계한다. Firebase 전환 시 `FIREBASE_PROJECT_ID`와 `FIREBASE_CREDENTIALS_PATH` 환경 변수만 설정하면 된다.

## 2. 개발 단계별 구현 계획

### Phase 1: 기본 구조 개발 (1주)

#### Day 1-2: 프로젝트 초기 설정
1. **프론트엔드 설정**
   - Vite로 React + TypeScript 프로젝트 생성
   - 필요한 패키지 설치 (React Router, Axios, TailwindCSS)
   - 기본 폴더 구조 생성

2. **백엔드 설정**
   - FastAPI 프로젝트 생성
   - SQLite 데이터베이스 설정 (로컬 개발용)
   - Repository 패턴으로 데이터 접근 추상화 (Firebase 전환 대비)
   - Pydantic 스키마 정의 (Firestore 호환)
   - 기본 API 엔드포인트 구성
   - `.env` 로더, 필수 변수 검증 로직, 단일 타임존 헬퍼 초안 작성
   - `DB_TYPE` 환경 변수로 데이터베이스 타입 선택 가능하도록 설정

#### Day 3-4: 챗봇 UI 컴포넌트 구현
1. **기본 UI 컴포넌트 개발**
   - 헤더/푸터 컴포넌트
   - 채팅 컨테이너 및 메시지 컴포넌트
   - 메시지 입력 폼

2. **반응형 디자인 적용**
   - 모바일 최적화 레이아웃
   - TailwindCSS 스타일링

#### Day 5-7: 목업 데이터 준비
1. **법령 샘플 데이터 구조 설계**
   - 법령 데이터 모델 정의 (법령명, 조문, 내용 등)
   - 국가법령정보센터 API 응답 구조 분석 및 모방

2. **핵심 법령 샘플 데이터 생성**
   - 건축법, 도시계획법, 전기사업법 등 주요 법령 샘플
   - 인허가 관련 조문 중심으로 데이터 구성

### Phase 2: 핵심 기능 개발 (1-2주)

#### Week 1: 검색 및 ChatGPT 연동
1. **법령 검색 기능 구현**
   - 키워드 기반 검색 엔진 개발
   - 검색 결과 정렬 및 필터링 기능

2. **ChatGPT API 연동**
   - OpenAI API 클라이언트 구현
   - 프롬프트 엔지니어링 및 최적화
   - 법령 컨텍스트 주입 로직 개발

#### Week 2: 질의응답 시스템 및 대화 관리
1. **질의응답 시스템 구현**
   - 사용자 질문 분석 및 키워드 추출
   - 관련 법령 검색 및 컨텍스트 구성
   - GPT 응답 생성 및 법령 출처 추가

2. **대화 관리 기능 개발**
   - 대화 세션 저장 및 불러오기
   - 대화 히스토리 관리
   - 답변 복사 및 공유 기능

### Phase 3: 배포 및 최적화 (1주)

#### Day 1-2: 도메인 설정 및 배포
1. **프론트엔드 배포**
   - Vercel 배포 설정
   - 개인 도메인 연결

2. **백엔드 배포**
   - Railway 또는 Render에 백엔드 배포
   - 환경변수 및 API 키 설정

#### Day 3-5: 실제 API 연동 준비
1. **API 연동 코드 개발**
   - 국가법령정보센터 API 클라이언트 구현
   - 목업 데이터에서 실제 API로 전환 준비
   - API 응답 처리 및 에러 핸들링

#### Day 6-7: 성능 최적화 및 안정화
1. **성능 최적화**
   - API 응답 캐싱
   - 검색 성능 개선
   - 로딩 상태 관리 최적화

2. **안정화 및 테스트**
   - 에러 처리 및 예외 상황 대응
   - 다양한 질문 유형에 대한 테스트
   - 사용자 피드백 수집 준비

## 3. 즉시 구현 기능 상세 계획

### 모바일 최적화
- 반응형 그리드 레이아웃 적용
- 터치 친화적 UI 요소 설계
- 모바일에서 가독성 높은 폰트 크기 및 여백

### 즐겨찾기 기능
- 중요 대화 즐겨찾기 표시
- 로컬 스토리지를 활용한 즐겨찾기 저장
- 즐겨찾기 목록 관리 UI

### 복사하기 버튼
- 각 메시지별 복사 버튼 제공
- 클립보드 API를 활용한 복사 기능
- 복사 성공 피드백 제공

## 4. 목업 데이터 구조 설계

### 법령 데이터 모델
```typescript
// 법령 데이터 타입 정의
interface Law {
  id: string;           // 법령 ID
  name: string;         // 법령명
  type: string;         // 법령 종류 (법률, 시행령, 시행규칙 등)
  enactmentDate: string; // 제정일
  amendmentDate: string; // 개정일
  category: string[];   // 분류 (건설/건축, 에너지, 환경 등)
  articles: Article[];  // 조문 목록
}

interface Article {
  id: string;           // 조문 ID
  lawId: string;        // 소속 법령 ID
  number: string;       // 조번호 (예: "제1조")
  title: string;        // 조제목
  content: string;      // 조문 내용
  subparagraphs: Subparagraph[]; // 항/호/목 목록
  relatedArticles: string[]; // 관련 조문 ID 목록
}

interface Subparagraph {
  id: string;           // 항/호/목 ID
  articleId: string;    // 소속 조문 ID
  type: string;         // 유형 (항, 호, 목)
  number: string;       // 번호 (예: "1", "가")
  content: string;      // 내용
}
```

### 샘플 데이터 예시 (건축법 일부)
```javascript
const mockLaws = [
  {
    id: "law-001",
    name: "건축법",
    type: "법률",
    enactmentDate: "1962-01-20",
    amendmentDate: "2023-06-11",
    category: ["건설", "건축"],
    articles: [
      {
        id: "art-001-001",
        lawId: "law-001",
        number: "제1조",
        title: "목적",
        content: "이 법은 건축물의 대지·구조·설비 기준 및 용도 등을 정하여 건축물의 안전·기능·환경 및 미관을 향상시킴으로써 공공복리의 증진에 이바지하는 것을 목적으로 한다.",
        subparagraphs: [],
        relatedArticles: []
      },
      {
        id: "art-001-002",
        lawId: "law-001",
        number: "제2조",
        title: "정의",
        content: "이 법에서 사용하는 용어의 뜻은 다음과 같다.",
        subparagraphs: [
          {
            id: "subp-001-002-001",
            articleId: "art-001-002",
            type: "항",
            number: "1",
            content: "\"건축물\"이란 토지에 정착하는 공작물 중 지붕과 기둥 또는 벽이 있는 것과 이에 딸린 시설물을 말한다."
          },
          {
            id: "subp-001-002-002",
            articleId: "art-001-002",
            type: "항",
            number: "2",
            content: "\"건축물의 용도\"란 건축물의 종류를 유사한 구조, 이용 목적 및 형태별로 묶어 분류한 것을 말한다."
          }
        ],
        relatedArticles: ["art-001-003"]
      }
    ]
  },
  // 추가 법령 데이터...
]
```

## 5. API 설계

### 프론트엔드-백엔드 API
```
1. 채팅 API
   - POST /api/chat
     - 요청: { message: string, conversationId?: string }
     - 응답: { id: string, content: string, lawReferences: LawReference[] }

2. 법령 검색 API
   - GET /api/laws/search?query={query}&category={category}
     - 응답: Law[]

3. 대화 관리 API
   - GET /api/conversations
     - 응답: Conversation[]
   - GET /api/conversations/{id}
     - 응답: { id: string, messages: Message[] }
   - POST /api/conversations
     - 요청: { title: string }
     - 응답: { id: string, title: string }
   - DELETE /api/conversations/{id}
     - 응답: { success: boolean }
```

### 국가법령정보센터 API 연동 (승인 후)
```
1. 법령 검색
   - GET /api/external/law-search?query={query}
     - 내부적으로 국가법령정보센터 API 호출
     - 응답: { laws: Law[] }

2. 법령 상세 조회
   - GET /api/external/law/{id}
     - 내부적으로 국가법령정보센터 API 호출
     - 응답: Law
```

## 6. 프롬프트 엔지니어링

### 기본 프롬프트 템플릿
```
당신은 법령 전문가 AI 비서입니다. 다음 법령 정보를 바탕으로 사용자의 질문에 정확하게 답변해주세요:

[법령 컨텍스트]
{법령_데이터}

[사용자 질문]
{사용자_질문}

답변 시 다음 사항을 지켜주세요:
1. 관련 법령과 조문을 명확히 인용해주세요.
2. 법률 용어는 가능한 쉽게 설명해주세요.
3. 인허가 절차가 있다면 단계별로 구분하여 설명해주세요.
4. 담당 기관이나 부서 정보도 포함해주세요.
5. 답변 마지막에는 "이 답변은 참고용이며, 정확한 법적 판단은 전문가와 상담하세요."라는 면책 문구를 포함해주세요.
```

### 인허가 절차 질문용 프롬프트
```
당신은 공기업 인허가 담당자를 돕는 법령 전문가입니다. 다음 법령 정보를 바탕으로 인허가 절차에 대해 상세히 답변해주세요:

[법령 컨텍스트]
{법령_데이터}

[지역 정보]
{지역_데이터}

[사용자 질문]
{사용자_질문}

답변 시 다음 형식으로 제공해주세요:
1. 필요한 인허가 종류 요약
2. 단계별 인허가 절차 (순서대로)
   - 각 단계별 필요 서류
   - 담당 기관 및 부서
   - 예상 소요 기간
3. 주의사항 및 팁
4. 관련 법령 조문 인용

답변 마지막에는 "이 답변은 참고용이며, 정확한 법적 판단은 전문가와 상담하세요."라는 면책 문구를 포함해주세요.
```

## 7. 개발 일정 및 마일스톤

### Week 1: 기본 구조 개발
- **Day 1-2**: 프로젝트 초기 설정 완료
- **Day 3-4**: 기본 UI 컴포넌트 구현
- **Day 5-7**: 목업 데이터 생성 및 연동

### Week 2-3: 핵심 기능 개발
- **Day 8-10**: 법령 검색 기능 구현
- **Day 11-14**: ChatGPT API 연동
- **Day 15-17**: 질의응답 시스템 구현
- **Day 18-21**: 대화 관리 기능 개발

### Week 4: 배포 및 최적화
- **Day 22-23**: 도메인 설정 및 배포
- **Day 24-26**: 실제 API 연동 준비
- **Day 27-28**: 성능 최적화 및 안정화

## 8. 테스트 계획

### 단위 테스트
- 법령 검색 알고리즘 테스트
- 프롬프트 생성 로직 테스트
- API 응답 처리 테스트

### 통합 테스트
- 프론트엔드-백엔드 API 통합 테스트
- ChatGPT API 연동 테스트
- 대화 흐름 테스트

### 사용자 시나리오 테스트
- 인허가 절차 질문 시나리오
- 법령 해석 질문 시나리오
- 복합 법령 적용 시나리오
