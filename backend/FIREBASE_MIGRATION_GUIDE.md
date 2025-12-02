# Firebase 전환 가이드

## 현재 구조 (SQLite)

```
backend/
├── app/
│   ├── db/
│   │   ├── database.py      # SQLAlchemy 연결
│   │   └── models.py        # ORM 모델
│   └── services/            # 비즈니스 로직
```

## Firebase 전환 시 변경 사항

### 1. 데이터베이스 타입 선택
환경 변수로 데이터베이스 타입을 선택:
```env
DB_TYPE=firestore  # 또는 sqlite
```

### 2. Firestore 구조
- Collections: `conversations`, `messages`
- Document ID: 자동 생성 또는 커스텀
- Timestamps: Firestore Timestamp 타입 사용

### 3. 필요한 변경
- `app/db/database.py` → Firestore 클라이언트로 교체
- `app/db/models.py` → Pydantic 모델로 변환
- Repository 패턴으로 데이터 접근 추상화

### 4. Firebase 설정
```env
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_PATH=path/to/service-account.json
```


