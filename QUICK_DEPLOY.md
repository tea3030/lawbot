# 빠른 배포 가이드

이 가이드는 배포를 빠르게 시작할 수 있도록 핵심 단계만 정리했습니다.

## 🚀 빠른 시작 (5분)

### 1. Firebase 설정 (2분)

```bash
# 1. Firebase 콘솔 접속
https://console.firebase.google.com

# 2. 프로젝트 생성
# - 프로젝트 이름: lawchat
# - Firestore 활성화 (프로덕션 모드)
# - 리전: asia-northeast3 (서울)

# 3. 서비스 계정 키 다운로드
# - 프로젝트 설정 > 서비스 계정
# - "새 비공개 키 생성"
# - JSON 파일 다운로드 → backend/firebase-key.json
```

### 2. Railway 백엔드 배포 (2분)

```bash
# 1. Railway 접속
https://railway.app

# 2. GitHub 저장소 연결
# - New Project > Deploy from GitHub
# - lawchat 저장소 선택
# - Root Directory: backend

# 3. 환경 변수 설정
OPENAI_API_KEY=your_key
DB_TYPE=firestore
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_CREDENTIALS_PATH=/app/firebase-key.json
APP_ENV=production
DEBUG=false

# 4. Firebase 키 파일 업로드
# - Settings > Volumes
# - 새 볼륨 생성
# - firebase-key.json 업로드
```

### 3. Vercel 프론트엔드 배포 (1분)

```bash
# 1. Vercel 접속
https://vercel.com

# 2. GitHub 저장소 연결
# - Add New Project
# - lawchat 저장소 선택
# - Root Directory: frontend
# - Framework: Vite

# 3. 환경 변수 설정
VITE_BACKEND_URL=https://your-backend.railway.app

# 4. Deploy!
```

## ✅ 배포 확인

```bash
# 백엔드 헬스 체크
curl https://your-backend.railway.app/health

# 프론트엔드 접속
# 브라우저에서 https://your-app.vercel.app 접속
```

## 📚 상세 가이드

더 자세한 내용은 다음 문서를 참고하세요:
- [배포 단계별 가이드](DEPLOYMENT_STEPS.md)
- [배포 가이드](Docs/DEPLOYMENT_GUIDE.md)
- [배포 체크리스트](DEPLOYMENT_CHECKLIST.md)

