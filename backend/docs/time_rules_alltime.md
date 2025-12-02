# 날짜/시간 처리 규칙 (상세 가이드)

## 모든 시간대 처리 시나리오

### 시나리오별 처리 방법

#### 1. 사용자 입력 받기

```python
# 사용자가 "2025-11-26 15:30" 형식으로 입력한 경우
# 입력 시간대를 명시적으로 처리

from app.utils.date_utils import parse_datetime, to_utc

# 사용자 입력은 KST로 가정
user_input = "2025-11-26 15:30"
user_dt = parse_datetime(user_input, timezone=KST)

# 저장 시 UTC로 변환
utc_dt = to_utc(user_dt)
```

#### 2. 법령 날짜 처리

```python
# 법령의 제정일, 개정일은 날짜만 (시간 없음)
# 이런 경우 자정(00:00:00) UTC로 저장

from app.utils.date_utils import parse_datetime, to_utc

enactment_date_str = "2023-06-11"  # 날짜만
enactment_dt = parse_datetime(f"{enactment_date_str} 00:00:00", timezone=KST)
enactment_utc = to_utc(enactment_dt)
```

#### 3. 대화 세션 시간

```python
# 대화 시작 시간, 마지막 메시지 시간 등

from app.utils.date_utils import now_utc, format_datetime, to_kst

# 세션 시작
session_start = now_utc()

# 사용자에게 표시
display_time = format_datetime(to_kst(session_start))
```

#### 4. 검색 필터링

```python
# "최근 7일 내 메시지" 같은 필터링

from app.utils.date_utils import now_utc, to_kst
from datetime import timedelta

# 현재 시간 (UTC)
now = now_utc()

# 7일 전 (UTC)
seven_days_ago = now - timedelta(days=7)

# 데이터베이스 쿼리 (UTC 기준)
messages = db.query(Message).filter(
    Message.created_at >= seven_days_ago,
    Message.created_at <= now
).all()

# 사용자에게 표시할 때는 KST로 변환
for msg in messages:
    display_time = format_datetime(to_kst(msg.created_at))
```

#### 5. 정렬 및 그룹화

```python
# 날짜별로 메시지 그룹화

from app.utils.date_utils import format_datetime, to_kst
from collections import defaultdict

messages_by_date = defaultdict(list)

for msg in messages:
    kst_time = to_kst(msg.created_at)
    date_key = format_datetime(kst_time, format_str="YYYY-MM-DD")
    messages_by_date[date_key].append(msg)
```

## 에러 처리

### timezone 정보 없는 datetime 처리

```python
from app.utils.date_utils import to_utc

def safe_to_utc(dt: datetime) -> datetime:
    """timezone 정보가 없는 datetime을 안전하게 UTC로 변환"""
    if dt.tzinfo is None:
        # timezone 정보가 없으면 KST로 가정하고 UTC로 변환
        return to_utc(dt)
    return to_utc(dt)
```

### 잘못된 형식 처리

```python
from app.utils.date_utils import parse_datetime

def safe_parse_datetime(dt_str: str) -> Optional[datetime]:
    """안전하게 datetime 파싱"""
    try:
        return parse_datetime(dt_str, timezone=UTC)
    except Exception:
        # 로깅하고 None 반환
        logger.warning(f"Failed to parse datetime: {dt_str}")
        return None
```

## 테스트 가이드

### 단위 테스트 예시

```python
import pytest
from app.utils.date_utils import now_utc, to_kst, format_datetime

def test_timezone_conversion():
    """시간대 변환 테스트"""
    utc_time = now_utc()
    kst_time = to_kst(utc_time)
    
    # KST는 UTC보다 9시간 앞서야 함
    assert (kst_time - utc_time).total_seconds() == 9 * 3600

def test_format_datetime():
    """포맷팅 테스트"""
    utc_time = now_utc()
    formatted = format_datetime(utc_time)
    
    # 형식 확인
    assert len(formatted) == 19  # "YYYY-MM-DD HH:mm:ss"
    assert formatted.count("-") == 2
    assert formatted.count(":") == 2
```

## 마이그레이션 가이드

### 기존 코드에서 전환

#### Before (잘못된 방법)

```python
from datetime import datetime

# ❌ timezone 정보 없음
created_at = datetime.now()

# ❌ 직접 변환
kst_time = created_at + timedelta(hours=9)
```

#### After (올바른 방법)

```python
from app.utils.date_utils import now_utc, to_kst, format_datetime

# ✅ UTC로 저장
created_at = now_utc()

# ✅ 변환 함수 사용
kst_time = to_kst(created_at)
formatted = format_datetime(kst_time)
```

## FAQ

### Q: 왜 UTC로 저장하나요?

A: 
- 시간대 변환 오류 방지
- 서버가 다른 지역으로 이동해도 문제없음
- 국제 표준 관행

### Q: 사용자가 다른 시간대에 있으면?

A: 현재는 한국 사용자만 대상이므로 KST만 사용. 향후 확장 시 사용자 설정에 따라 변환 가능.

### Q: 법령 날짜는 어떻게 처리하나요?

A: 법령의 제정일/개정일은 날짜만 있으므로, 해당 날짜의 자정(00:00:00) KST를 UTC로 변환하여 저장.

### Q: 데이터베이스에서 직접 쿼리할 때는?

A: 모든 쿼리는 UTC 기준으로 수행. 표시할 때만 KST로 변환.

## 변경 이력

- 2025-11-26: 초기 문서 작성
- 규칙 변경 시 이 섹션에 기록

