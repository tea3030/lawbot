# 날짜/시간 처리 규칙

## 개요

법령 Q&A 웹앱에서 날짜/시간을 일관되게 처리하기 위한 규칙과 가이드라인입니다.

## 핵심 원칙

### 1. 저장 규칙: UTC 사용

**모든 날짜/시간은 서버 내부에서 UTC로 저장합니다.**

- 데이터베이스에 저장되는 모든 `datetime` 필드는 UTC 시간대를 사용
- 서버 로직 내부에서 날짜/시간을 처리할 때는 UTC 기준
- 이유: 시간대 변환 오류 방지, 글로벌 확장성, 일관성 유지

### 2. 출력 규칙: KST 변환

**사용자에게 표시할 때만 KST(Asia/Seoul)로 변환합니다.**

- API 응답에서 날짜/시간을 사용자에게 보여줄 때만 KST로 변환
- 프론트엔드에서 날짜/시간을 표시할 때도 KST 사용
- 이유: 한국 사용자에게 직관적인 시간 표시

### 3. 단일 유틸리티 사용

**모든 날짜/시간 처리는 `app.utils.date_utils` 모듈만 사용합니다.**

- 서버와 프론트엔드 모두 동일한 헬퍼 함수 사용
- 직접 `datetime` 객체를 생성하거나 변환하지 않음
- 이유: 일관성 보장, 버그 방지, 유지보수 용이

## 구현 상세

### 시간대 상수

```python
UTC = "UTC"
KST = "Asia/Seoul"
```

### 핵심 함수

#### 1. 현재 시간 가져오기

```python
from app.utils.date_utils import now_utc, now_kst

# 서버 내부에서 사용 (저장용)
current_time = now_utc()  # UTC 시간

# 사용자에게 표시할 때만 사용
display_time = now_kst()  # KST 시간
```

#### 2. 시간대 변환

```python
from app.utils.date_utils import to_utc, to_kst

# UTC로 변환 (저장 전)
utc_time = to_utc(some_datetime)

# KST로 변환 (표시 전)
kst_time = to_kst(utc_time)
```

#### 3. 포맷팅

```python
from app.utils.date_utils import format_datetime

# 기본 포맷 (KST)
formatted = format_datetime(dt)  # "2025-11-26 15:30:45"

# 커스텀 포맷
formatted = format_datetime(dt, format_str="YYYY년 MM월 DD일 HH시 mm분")
```

#### 4. ISO 8601 형식

```python
from app.utils.date_utils import iso_format, from_iso

# UTC로 ISO 형식 변환 (API 응답용)
iso_string = iso_format(dt, timezone=UTC)

# ISO 문자열에서 파싱
dt = from_iso(iso_string, timezone=UTC)
```

## 사용 시나리오

### 시나리오 1: 메시지 생성 시

```python
from app.utils.date_utils import now_utc

# 메시지 생성 시 UTC로 저장
message = Message(
    id=uuid.uuid4(),
    content="질문 내용",
    created_at=now_utc()  # UTC로 저장
)
```

### 시나리오 2: API 응답 시

```python
from app.utils.date_utils import format_datetime, to_kst

# 저장된 UTC 시간을 KST로 변환하여 표시
response = {
    "id": message.id,
    "content": message.content,
    "created_at": format_datetime(to_kst(message.created_at))  # KST로 변환 후 포맷
}
```

### 시나리오 3: 프론트엔드 표시

```typescript
// frontend/src/utils/date.ts
import { format } from 'date-fns';
import { utcToZonedTime } from 'date-fns-tz';

export function formatDateTime(isoString: string): string {
  const utcDate = new Date(isoString);
  const kstDate = utcToZonedTime(utcDate, 'Asia/Seoul');
  return format(kstDate, 'yyyy-MM-dd HH:mm:ss');
}
```

## 데이터베이스 모델

### SQLite 모델 예시

```python
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from app.utils.date_utils import now_utc

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # 또는
    created_at = Column(DateTime(timezone=True), default=now_utc)
```

### Firestore 모델 예시

```python
from app.utils.date_utils import now_utc, iso_format

# 저장 시
message_data = {
    "id": message_id,
    "content": content,
    "created_at": iso_format(now_utc(), timezone=UTC)  # UTC ISO 문자열
}

# 읽기 시
created_at = from_iso(message_data["created_at"], timezone=UTC)
display_time = format_datetime(to_kst(created_at))
```

## 주의사항

### 1. timezone 정보 없는 datetime 처리

```python
# ❌ 잘못된 방법
dt = datetime.now()  # timezone 정보 없음

# ✅ 올바른 방법
dt = now_utc()  # UTC 명시
```

### 2. 문자열 파싱 시

```python
# ❌ 잘못된 방법
dt = datetime.strptime("2025-11-26 15:30:45", "%Y-%m-%d %H:%M:%S")
# timezone 정보가 없어서 혼란 발생

# ✅ 올바른 방법
dt = parse_datetime("2025-11-26 15:30:45", timezone=UTC)
```

### 3. 프론트엔드와의 통신

```python
# API 응답 시 ISO 8601 형식 사용
{
    "created_at": iso_format(message.created_at, timezone=UTC)
    # 예: "2025-11-26T06:30:45+00:00"
}
```

## 검증 체크리스트

코드 리뷰 시 다음 사항을 확인:

- [ ] 모든 `datetime` 생성이 `date_utils` 함수를 사용하는가?
- [ ] 데이터베이스 저장 시 UTC를 사용하는가?
- [ ] API 응답에서 사용자에게 표시할 때 KST로 변환하는가?
- [ ] timezone 정보 없는 `datetime` 객체를 생성하지 않는가?
- [ ] 직접 `datetime.now()`를 호출하지 않는가?

## 문서 동기화

이 문서(`time_rules.md`)와 실제 구현(`app/utils/date_utils.py`)은 항상 동기화되어야 합니다.

**변경 시 동시 업데이트:**
1. `date_utils.py` 함수 수정/추가
2. `time_rules.md` 문서 업데이트
3. 이 문서의 "핵심 원칙" 섹션과 실제 구현이 일치하는지 확인

## 참고 자료

- Pendulum 라이브러리 문서: https://pendulum.eustace.io/
- ISO 8601 표준: https://en.wikipedia.org/wiki/ISO_8601
- Python datetime 모범 사례: https://docs.python.org/3/library/datetime.html

