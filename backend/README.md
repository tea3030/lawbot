# LawChat Backend

법령 Q&A 웹앱 백엔드 서버

## 환경 설정

### 1. 가상환경 생성 및 활성화

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. 의존성 설치

```powershell
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
# 필수 변수
OPENAI_API_KEY=your_openai_api_key_here

# 데이터베이스 설정
DB_TYPE=sqlite  # sqlite (로컬) 또는 firestore (Firebase)
DATABASE_URL=sqlite:///./lawchat.db  # SQLite 사용 시

# Firebase 설정 (Firestore 사용 시)
# FIREBASE_PROJECT_ID=your-project-id
# FIREBASE_CREDENTIALS_PATH=path/to/service-account.json

# 선택 변수
LAW_API_KEY=your_law_api_key_here
APP_ENV=development
TIMEZONE=Asia/Seoul
HOST=0.0.0.0
PORT=8000
DEBUG=true
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**중요**: `OPENAI_API_KEY`는 필수입니다. 설정하지 않으면 서버가 시작되지 않습니다.

### 4. 서버 실행

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

또는

```powershell
python -m uvicorn app.main:app --reload
```

## 프로젝트 구조

```
backend/
├── app/
│   ├── api/           # API 엔드포인트
│   ├── core/          # 설정 및 보안
│   ├── db/            # 데이터베이스 모델 (SQLite)
│   ├── repositories/   # 데이터 접근 추상화 (Firebase 전환 용이)
│   ├── schemas/       # Pydantic 스키마 (Firestore 호환)
│   ├── services/      # 비즈니스 로직
│   ├── utils/         # 유틸리티 (날짜/시간 처리 등)
│   └── main.py        # FastAPI 앱 진입점
├── requirements.txt   # Python 의존성
├── README.md          # 이 파일
└── FIREBASE_MIGRATION_GUIDE.md  # Firebase 전환 가이드
```

## Firebase 전환 준비

현재 구조는 SQLite를 사용하지만, Firebase Firestore로 전환할 수 있도록 설계되었습니다:

- **Repository 패턴**: 데이터 접근 로직을 추상화하여 DB 변경 시 영향 최소화
- **Pydantic 스키마**: Firestore와 호환되는 데이터 검증
- **환경 변수**: `DB_TYPE=firestore`로 간단히 전환 가능

자세한 내용은 `FIREBASE_MIGRATION_GUIDE.md`를 참고하세요.

## 시간대 처리 규칙

- **저장**: 모든 날짜/시간은 UTC로 저장
- **출력**: 사용자에게 표시할 때만 KST(Asia/Seoul)로 변환
- **유틸리티**: `app.utils.date_utils` 모듈 사용

## API 엔드포인트

- `GET /` - 루트 엔드포인트
- `GET /health` - 헬스 체크
- `POST /api/chat` - 채팅 메시지 전송 (구현 예정)
- `GET /api/laws/search` - 법령 검색 (구현 예정)

