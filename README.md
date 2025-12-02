# 법령 Q&A 챗봇 (LawChat)

인허가 절차 및 관련 법령에 대한 질문에 답변을 제공하는 AI 기반 웹 애플리케이션입니다.

## 주요 기능

- 🤖 **AI 기반 법령 질의응답**: GPT-4o를 활용한 정확한 법령 해석 및 답변
- 🔍 **법령 검색**: 키워드 기반 법령 검색 및 관련도 순 정렬
- 💬 **대화 관리**: 대화 세션 저장 및 히스토리 관리
- ⭐ **즐겨찾기**: 중요한 답변을 즐겨찾기에 저장
- 📋 **답변 복사**: 클립보드로 답변 복사
- 💭 **피드백 수집**: 사용자 피드백을 통한 서비스 개선

## 기술 스택

### 프론트엔드
- React 18 + TypeScript
- Vite
- TailwindCSS
- Axios

### 백엔드
- FastAPI
- SQLite (로컬) / Firebase Firestore (배포)
- OpenAI GPT-4o
- SQLAlchemy
- Pydantic

## 빠른 시작

### 백엔드 설정

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`.env` 파일 생성:
```env
OPENAI_API_KEY=your_openai_api_key
DB_TYPE=sqlite
```

서버 실행:
```bash
uvicorn app.main:app --reload
```

### 프론트엔드 설정

```bash
cd frontend
npm install
```

`.env` 파일 생성:
```env
VITE_BACKEND_URL=http://localhost:8000
```

개발 서버 실행:
```bash
npm run dev
```

## 프로젝트 구조

```
lawchat/
├── backend/          # FastAPI 백엔드
├── frontend/         # React 프론트엔드
├── Docs/            # 문서
└── README.md        # 이 파일
```

## 문서

- [사용자 가이드](Docs/USER_GUIDE.md)
- [개발자 가이드](Docs/DEVELOPER_GUIDE.md)
- [배포 가이드](Docs/DEPLOYMENT_GUIDE.md)
- [배포 체크리스트](DEPLOYMENT_CHECKLIST.md)
- [Firebase 마이그레이션 가이드](backend/FIREBASE_MIGRATION_GUIDE.md)

## 배포

배포 방법은 [배포 가이드](Docs/DEPLOYMENT_GUIDE.md)를 참고하세요.

## 라이선스

이 프로젝트는 공기업용으로 개발되었습니다.

## 문의

문제가 발생하거나 개선 사항이 있으면 이슈를 등록해주세요.

