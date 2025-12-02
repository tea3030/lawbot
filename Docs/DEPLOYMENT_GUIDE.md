# 배포 가이드

## 개요

이 문서는 법령 Q&A 챗봇을 프로덕션 환경에 배포하는 방법을 설명합니다.

## 배포 전 준비사항

### 1. 필수 계정 및 서비스

- **Firebase 계정**: Firestore 데이터베이스 사용
- **Vercel 계정**: 프론트엔드 배포
- **Railway/Render 계정**: 백엔드 배포 (선택사항)
- **OpenAI API 키**: ChatGPT API 사용

### 2. 환경 변수 준비

#### 백엔드 환경 변수
```env
# 필수
OPENAI_API_KEY=your_openai_api_key
DB_TYPE=firestore

# Firebase 설정
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_CREDENTIALS_PATH=/path/to/service-account.json

# 선택사항
DEBUG=false
APP_ENV=production
CORS_ORIGINS=https://your-domain.com
```

#### 프론트엔드 환경 변수
```env
VITE_BACKEND_URL=https://your-backend-url.com
```

## 배포 단계

### Step 1: Firebase 프로젝트 설정

1. **Firebase 콘솔에서 프로젝트 생성**
   - https://console.firebase.google.com 접속
   - 새 프로젝트 생성
   - 프로젝트 ID 기록

2. **Firestore 데이터베이스 활성화**
   - Firestore Database 선택
   - 프로덕션 모드로 시작
   - 리전 선택 (asia-northeast3 권장)

3. **서비스 계정 키 생성**
   - 프로젝트 설정 > 서비스 계정
   - "새 비공개 키 생성" 클릭
   - JSON 파일 다운로드
   - 파일을 안전한 위치에 저장

4. **환경 변수 설정**
   ```env
   FIREBASE_PROJECT_ID=your_project_id
   FIREBASE_CREDENTIALS_PATH=/path/to/service-account.json
   ```

### Step 2: SQLite → Firestore 마이그레이션

1. **마이그레이션 스크립트 실행**
   ```bash
   cd backend
   python scripts/migrate_to_firestore.py
   ```

2. **데이터 검증**
   - Firestore 콘솔에서 데이터 확인
   - 대화 세션 및 메시지 데이터 확인

### Step 3: 백엔드 배포

#### 옵션 A: Railway 배포

1. **Railway 프로젝트 생성**
   - https://railway.app 접속
   - 새 프로젝트 생성
   - GitHub 저장소 연결

2. **환경 변수 설정**
   - Railway 대시보드에서 환경 변수 추가
   - 모든 필수 환경 변수 입력

3. **배포 설정**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### 옵션 B: Render 배포

1. **Render 서비스 생성**
   - https://render.com 접속
   - 새 Web Service 생성
   - GitHub 저장소 연결

2. **환경 변수 설정**
   - Render 대시보드에서 환경 변수 추가

3. **배포 설정**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### 옵션 C: Firebase Cloud Functions

1. **Firebase Functions 설정**
   ```bash
   cd backend
   firebase init functions
   ```

2. **함수 코드 작성**
   - `functions/main.py`에 FastAPI 앱 배포

3. **배포**
   ```bash
   firebase deploy --only functions
   ```

### Step 4: 프론트엔드 배포 (Vercel)

1. **Vercel 프로젝트 생성**
   - https://vercel.com 접속
   - 새 프로젝트 생성
   - GitHub 저장소 연결

2. **환경 변수 설정**
   - Vercel 대시보드에서 환경 변수 추가
   - `VITE_BACKEND_URL`: 백엔드 URL 입력

3. **빌드 설정**
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **배포**
   - 자동 배포 또는 수동 배포
   - 커스텀 도메인 연결 (선택사항)

### Step 5: 도메인 설정 (선택사항)

1. **도메인 구매**
   - 원하는 도메인 구매

2. **DNS 설정**
   - Vercel에서 도메인 추가
   - DNS 레코드 설정

3. **SSL 인증서**
   - Vercel에서 자동으로 SSL 인증서 발급

## 배포 후 확인사항

### 1. 헬스 체크
```bash
curl https://your-backend-url.com/health
```

### 2. API 테스트
```bash
curl https://your-backend-url.com/api/laws/search?keyword=건축
```

### 3. 프론트엔드 접속
- 브라우저에서 프론트엔드 URL 접속
- 채팅 기능 테스트
- 법령 검색 테스트

## 모니터링 및 로깅

### 1. 에러 모니터링
- Railway/Render: 내장 로깅 사용
- Firebase: Cloud Logging 사용

### 2. 성능 모니터링
- Vercel Analytics (프론트엔드)
- 백엔드 로그 분석

## 롤백 절차

### 프론트엔드 롤백
1. Vercel 대시보드에서 이전 배포 선택
2. "Promote to Production" 클릭

### 백엔드 롤백
1. Railway/Render에서 이전 배포로 롤백
2. 또는 Git에서 이전 커밋으로 배포

## 보안 체크리스트

- [ ] 환경 변수에 API 키가 올바르게 설정되었는지 확인
- [ ] Firebase 보안 규칙 설정
- [ ] CORS 설정이 올바른지 확인
- [ ] HTTPS 사용 확인
- [ ] API 키가 클라이언트에 노출되지 않는지 확인

## 문제 해결

### 일반적인 문제

1. **환경 변수 누락**
   - 모든 필수 환경 변수가 설정되었는지 확인
   - 배포 플랫폼의 환경 변수 설정 확인

2. **Firebase 연결 실패**
   - 서비스 계정 키 경로 확인
   - Firebase 프로젝트 ID 확인
   - 권한 확인

3. **CORS 오류**
   - 백엔드 CORS 설정 확인
   - 프론트엔드 URL이 허용 목록에 있는지 확인

4. **빌드 실패**
   - 의존성 설치 확인
   - Node.js/Python 버전 확인
   - 빌드 로그 확인

## 추가 리소스

- [Firebase 문서](https://firebase.google.com/docs)
- [Vercel 문서](https://vercel.com/docs)
- [Railway 문서](https://docs.railway.app)
- [Render 문서](https://render.com/docs)

