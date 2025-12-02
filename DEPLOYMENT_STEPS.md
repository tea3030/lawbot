# 배포 단계별 가이드

이 문서는 실제 배포를 단계별로 안내합니다.

## ⚠️ 사전 준비

배포를 시작하기 전에 다음이 준비되어 있어야 합니다:

1. **Firebase 계정** 및 프로젝트 생성
2. **Vercel 계정** (프론트엔드 배포용)
3. **Railway 또는 Render 계정** (백엔드 배포용)
4. **OpenAI API 키**

## Step 1: Firebase 프로젝트 설정

### 1.1 Firebase 프로젝트 생성

1. https://console.firebase.google.com 접속
2. "프로젝트 추가" 클릭
3. 프로젝트 이름 입력 (예: `lawchat`)
4. Google Analytics 설정 (선택사항)
5. 프로젝트 생성 완료

### 1.2 Firestore 데이터베이스 활성화

1. Firebase 콘솔에서 프로젝트 선택
2. 왼쪽 메뉴에서 "Firestore Database" 클릭
3. "데이터베이스 만들기" 클릭
4. **프로덕션 모드** 선택
5. 리전 선택: **asia-northeast3 (서울)** 권장
6. "사용 설정" 클릭

### 1.3 서비스 계정 키 생성

1. Firebase 콘솔 > 프로젝트 설정 > 서비스 계정
2. "새 비공개 키 생성" 클릭
3. JSON 파일 다운로드
4. 파일을 안전한 위치에 저장 (예: `backend/firebase-key.json`)
5. **⚠️ 이 파일은 절대 Git에 커밋하지 마세요!**

### 1.4 Firestore 보안 규칙 설정

Firebase 콘솔 > Firestore Database > 규칙:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // 대화 세션: 사용자별 접근 제어 (향후 인증 추가 시)
    match /conversations/{conversationId} {
      allow read, write: if true; // 임시: 모든 사용자 접근 허용
    }
    
    // 메시지: 대화 세션에 속한 메시지만 접근
    match /messages/{messageId} {
      allow read, write: if true; // 임시: 모든 사용자 접근 허용
    }
  }
}
```

**⚠️ 프로덕션에서는 인증을 추가하여 보안을 강화하세요!**

## Step 2: 백엔드 배포

### 옵션 A: Railway 배포 (권장)

#### 2.1 Railway 프로젝트 생성

1. https://railway.app 접속
2. GitHub로 로그인
3. "New Project" 클릭
4. "Deploy from GitHub repo" 선택
5. `lawchat` 저장소 선택
6. `backend` 디렉토리 선택

#### 2.2 환경 변수 설정

Railway 대시보드 > Variables 탭에서 다음 변수 추가:

```
OPENAI_API_KEY=your_openai_api_key
DB_TYPE=firestore
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_PATH=/path/to/service-account.json
APP_ENV=production
DEBUG=false
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

**⚠️ Firebase 인증서 파일 업로드:**
- Railway > Settings > Volumes
- 새 볼륨 생성
- 인증서 파일 업로드
- `FIREBASE_CREDENTIALS_PATH`를 볼륨 경로로 설정

#### 2.3 배포

1. Railway가 자동으로 배포 시작
2. 배포 완료 후 URL 확인 (예: `https://lawchat-backend.railway.app`)

### 옵션 B: Render 배포

#### 2.1 Render 서비스 생성

1. https://render.com 접속
2. GitHub로 로그인
3. "New +" > "Web Service" 선택
4. 저장소 연결
5. 설정:
   - **Name**: `lawchat-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### 2.2 환경 변수 설정

Render 대시보드 > Environment에서 변수 추가 (Railway와 동일)

#### 2.3 배포

1. "Create Web Service" 클릭
2. 배포 완료 후 URL 확인

## Step 3: 프론트엔드 배포 (Vercel)

### 3.1 Vercel 프로젝트 생성

1. https://vercel.com 접속
2. GitHub로 로그인
3. "Add New..." > "Project" 선택
4. `lawchat` 저장소 선택
5. 설정:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 3.2 환경 변수 설정

Vercel 대시보드 > Settings > Environment Variables:

```
VITE_BACKEND_URL=https://your-backend-url.railway.app
```

### 3.3 배포

1. "Deploy" 클릭
2. 배포 완료 후 URL 확인 (예: `https://lawchat.vercel.app`)

## Step 4: 데이터 마이그레이션

### 4.1 로컬에서 마이그레이션 실행

```bash
cd backend
python scripts/migrate_to_firestore.py
```

### 4.2 데이터 검증

Firebase 콘솔 > Firestore Database에서 데이터 확인:
- `conversations` 컬렉션
- `messages` 컬렉션

## Step 5: 최종 확인

### 5.1 백엔드 헬스 체크

```bash
curl https://your-backend-url.railway.app/health
```

예상 응답:
```json
{"status": "healthy"}
```

### 5.2 프론트엔드 접속

브라우저에서 프론트엔드 URL 접속:
- https://your-frontend-url.vercel.app

### 5.3 기능 테스트

- [ ] 법령 검색 기능
- [ ] 채팅 기능
- [ ] 대화 세션 저장/불러오기
- [ ] 즐겨찾기 기능
- [ ] 피드백 기능

## Step 6: 도메인 설정 (선택사항)

### 6.1 커스텀 도메인 추가

1. Vercel 대시보드 > Settings > Domains
2. 도메인 추가
3. DNS 설정 안내에 따라 DNS 레코드 추가
4. SSL 인증서 자동 발급 (몇 분 소요)

## 문제 해결

### 백엔드 연결 실패

1. `VITE_BACKEND_URL` 환경 변수 확인
2. CORS 설정 확인 (`CORS_ORIGINS`)
3. 백엔드 로그 확인

### Firebase 연결 실패

1. `FIREBASE_PROJECT_ID` 확인
2. `FIREBASE_CREDENTIALS_PATH` 확인
3. 서비스 계정 키 파일 확인
4. Firestore 데이터베이스 활성화 확인

### 빌드 실패

1. 의존성 설치 확인
2. Node.js/Python 버전 확인
3. 빌드 로그 확인

## 다음 단계

배포가 완료되면:
1. 모니터링 설정
2. 에러 로깅 설정
3. 성능 최적화
4. 사용자 피드백 수집

