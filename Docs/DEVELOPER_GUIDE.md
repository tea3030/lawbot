# 법령 Q&A 챗봇 개발자 가이드

## 프로젝트 구조

```
lawchat/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 엔드포인트
│   │   ├── core/           # 핵심 설정 및 유틸리티
│   │   ├── db/             # 데이터베이스 모델
│   │   ├── mock/           # 목업 데이터
│   │   ├── repositories/   # 데이터 접근 레이어
│   │   ├── schemas/        # Pydantic 스키마
│   │   ├── services/       # 비즈니스 로직
│   │   └── utils/          # 유틸리티 함수
│   ├── tests/              # 테스트 코드
│   └── requirements.txt    # Python 의존성
├── frontend/               # React 프론트엔드
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   ├── hooks/          # Custom Hooks
│   │   ├── services/       # API 서비스
│   │   ├── types/          # TypeScript 타입
│   │   └── utils/          # 유틸리티 함수
│   └── package.json        # Node.js 의존성
└── Docs/                   # 문서
```

## 개발 환경 설정

### 백엔드 설정

1. Python 3.10 이상 설치
2. 가상 환경 생성 및 활성화:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. 의존성 설치:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. 환경 변수 설정 (`.env` 파일):
   ```env
   OPENAI_API_KEY=your_openai_api_key
   DEBUG=true
   ```
5. 데이터베이스 초기화:
   ```bash
   python -m app.db.database
   ```
6. 서버 실행:
   ```bash
   uvicorn app.main:app --reload
   ```

### 프론트엔드 설정

1. Node.js 18 이상 설치
2. 의존성 설치:
   ```bash
   cd frontend
   npm install
   ```
3. 환경 변수 설정 (`.env` 파일):
   ```env
   VITE_BACKEND_URL=http://localhost:8000
   ```
4. 개발 서버 실행:
   ```bash
   npm run dev
   ```

## 주요 기술 스택

### 백엔드
- **FastAPI**: 웹 프레임워크
- **SQLAlchemy**: ORM
- **Pydantic**: 데이터 검증
- **Pendulum**: 날짜/시간 처리
- **OpenAI API**: GPT-4o 모델

### 프론트엔드
- **React 18**: UI 라이브러리
- **TypeScript**: 타입 안정성
- **Vite**: 빌드 도구
- **TailwindCSS**: 스타일링
- **Axios**: HTTP 클라이언트

## 아키텍처

### 백엔드 아키텍처

```
API Layer (FastAPI)
    ↓
Service Layer (비즈니스 로직)
    ↓
Repository Layer (데이터 접근)
    ↓
Database (SQLite / Firestore)
```

### 프론트엔드 아키텍처

```
Components
    ↓
Hooks (상태 관리)
    ↓
Services (API 호출)
    ↓
Backend API
```

## 주요 기능 구현

### 1. 법령 검색

**백엔드**: `app/services/law_service.py`
- 키워드 기반 검색
- 관련도 순 정렬
- 캐싱 적용 (30분)

**프론트엔드**: `frontend/src/services/api.ts`
- `searchLaws()` 함수

### 2. ChatGPT 연동

**백엔드**: `app/services/openai_service.py`
- GPT-4o 모델 사용
- 법령 컨텍스트 주입
- 프롬프트 엔지니어링

**API 엔드포인트**: `POST /api/chat/`

### 3. 대화 관리

**백엔드**: `app/api/conversations.py`
- 대화 세션 CRUD
- 메시지 조회

**프론트엔드**: `frontend/src/hooks/useChat.ts`
- 대화 상태 관리

### 4. 즐겨찾기

**프론트엔드**: `frontend/src/hooks/useFavorites.ts`
- 로컬 스토리지 기반
- 추가/제거/조회 기능

## 데이터베이스 스키마

### Conversation
- `id`: UUID
- `title`: 제목
- `created_at`: 생성 시간 (UTC)
- `updated_at`: 수정 시간 (UTC)

### Message
- `id`: UUID
- `conversation_id`: 대화 세션 ID
- `role`: 역할 (user/assistant)
- `content`: 메시지 내용
- `law_references`: 법령 출처 (JSON)
- `created_at`: 생성 시간 (UTC)

## API 엔드포인트

### 법령 API
- `GET /api/laws`: 모든 법령 조회
- `GET /api/laws/search?keyword={keyword}`: 법령 검색
- `GET /api/laws/{law_id}`: 법령 상세 조회

### 채팅 API
- `POST /api/chat/`: 메시지 전송

### 대화 API
- `POST /api/conversations`: 대화 세션 생성
- `GET /api/conversations`: 대화 세션 목록
- `GET /api/conversations/{id}`: 대화 세션 조회
- `GET /api/conversations/{id}/messages`: 메시지 목록
- `DELETE /api/conversations/{id}`: 대화 세션 삭제

## 환경 변수

### 백엔드
- `OPENAI_API_KEY`: OpenAI API 키 (필수)
- `DEBUG`: 디버그 모드 (기본값: false)
- `DB_TYPE`: 데이터베이스 타입 (sqlite/firestore)
- `DATABASE_URL`: 데이터베이스 URL

### 프론트엔드
- `VITE_BACKEND_URL`: 백엔드 URL (기본값: http://localhost:8000)

## 테스트

### 백엔드 테스트
```bash
cd backend
pytest tests/
```

### 프론트엔드 테스트
```bash
cd frontend
npm test
```

## 배포

### 로컬 배포
- 백엔드: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- 프론트엔드: `npm run build` 후 정적 파일 서빙

### 프로덕션 배포
- 프론트엔드: Vercel
- 백엔드: Railway/Render 또는 Firebase Cloud Functions
- 데이터베이스: Firebase Firestore

## 주의사항

### 날짜/시간 처리
- 모든 날짜는 UTC로 저장
- 표시는 KST로 변환
- `app/utils/date_utils.py` 사용

### 에러 처리
- 커스텀 예외 클래스 사용
- 전역 에러 핸들러 등록
- 사용자 친화적 에러 메시지

### 보안
- 환경 변수는 서버에서만 읽기
- API 키는 절대 클라이언트에 노출하지 않기
- 입력 검증 필수

## 기여 가이드

1. 기능 브랜치 생성
2. 변경사항 커밋
3. 테스트 작성 및 실행
4. Pull Request 생성

## 라이선스

이 프로젝트는 공기업용으로 개발되었습니다.

