# 로컬 개발 환경 설정 가이드

로컬에서 프로젝트를 실행하기 위한 단계별 가이드입니다.

## 사전 준비

1. **Python 3.10 이상** 설치
2. **Node.js 18 이상** 설치
3. **OpenAI API 키** 준비

## Step 1: 백엔드 설정

### 1.1 가상 환경 생성 및 활성화

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 1.2 의존성 설치

```powershell
pip install -r requirements.txt
```

### 1.3 환경 변수 설정

`.env.example` 파일을 `.env`로 복사하고 OpenAI API 키를 입력하세요:

```powershell
Copy-Item .env.example .env
```

`.env` 파일을 열어서 다음을 수정:
```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

### 1.4 데이터베이스 초기화

서버를 처음 실행하면 자동으로 데이터베이스가 생성됩니다.

### 1.5 서버 실행

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

서버가 정상적으로 실행되면:
- http://localhost:8000 에서 접속 가능
- http://localhost:8000/docs 에서 API 문서 확인 가능

## Step 2: 프론트엔드 설정

### 2.1 의존성 설치

새 터미널 창에서:

```powershell
cd frontend
npm install
```

### 2.2 환경 변수 설정

`.env.example` 파일을 `.env`로 복사:

```powershell
Copy-Item .env.example .env
```

`.env` 파일은 이미 올바른 값으로 설정되어 있습니다:
```env
VITE_BACKEND_URL=http://localhost:8000
```

### 2.3 개발 서버 실행

```powershell
npm run dev
```

프론트엔드가 정상적으로 실행되면:
- http://localhost:5173 에서 접속 가능

## Step 3: 실행 확인

### 3.1 백엔드 확인

브라우저에서 다음 URL 접속:
- http://localhost:8000/health
- 예상 응답: `{"status": "healthy"}`

### 3.2 프론트엔드 확인

브라우저에서 http://localhost:5173 접속

### 3.3 기능 테스트

1. **법령 검색 테스트**
   - 헤더의 "법령 검색" 클릭
   - 키워드 입력 (예: "건축")

2. **채팅 테스트**
   - 질문 입력 (예: "건축법에 대해 알려주세요")
   - 답변 확인

3. **즐겨찾기 테스트**
   - 답변에 마우스 오버
   - 하트 아이콘 클릭
   - 헤더의 "즐겨찾기" 클릭하여 확인

## 문제 해결

### 백엔드가 시작되지 않는 경우

1. **OpenAI API 키 확인**
   ```
   OPENAI_API_KEY가 올바르게 설정되었는지 확인
   ```

2. **포트 충돌 확인**
   ```
   다른 프로세스가 8000 포트를 사용 중인지 확인
   netstat -ano | findstr :8000
   ```

3. **의존성 확인**
   ```
   pip install -r requirements.txt --upgrade
   ```

### 프론트엔드가 시작되지 않는 경우

1. **포트 충돌 확인**
   ```
   다른 프로세스가 5173 포트를 사용 중인지 확인
   ```

2. **의존성 확인**
   ```
   npm install
   ```

3. **캐시 삭제**
   ```
   rm -rf node_modules
   npm install
   ```

### 백엔드 연결 실패

1. **백엔드 서버 실행 확인**
   - http://localhost:8000/health 접속하여 확인

2. **CORS 설정 확인**
   - 백엔드 `.env`의 `CORS_ORIGINS`에 `http://localhost:5173` 포함 확인

3. **환경 변수 확인**
   - 프론트엔드 `.env`의 `VITE_BACKEND_URL` 확인

## 개발 팁

### 백엔드 자동 재시작
`--reload` 옵션으로 코드 변경 시 자동 재시작됩니다.

### 프론트엔드 핫 리로드
Vite가 자동으로 변경사항을 감지하고 브라우저를 새로고침합니다.

### API 테스트
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 다음 단계

로컬에서 정상적으로 실행되면:
1. 기능 테스트
2. 코드 수정 및 개발
3. 배포 준비

