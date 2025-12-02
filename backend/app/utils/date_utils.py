"""
중앙화된 날짜/시간 처리 유틸리티 모듈

규칙:
- 모든 날짜/시간은 서버 내부에서 UTC로 저장
- 사용자 출력 시에만 KST(Asia/Seoul)로 변환
- Pendulum 라이브러리를 사용하여 시간대 처리
"""
import pendulum
from typing import Optional
from datetime import datetime


# 시간대 상수
UTC = "UTC"
KST = "Asia/Seoul"


def now_utc() -> datetime:
    """현재 시간을 UTC로 반환"""
    return pendulum.now(UTC)


def now_kst() -> datetime:
    """현재 시간을 KST로 반환"""
    return pendulum.now(KST)


def to_utc(dt: datetime) -> datetime:
    """주어진 datetime을 UTC로 변환"""
    if dt.tzinfo is None:
        # timezone 정보가 없으면 KST로 가정
        dt = pendulum.instance(dt).in_timezone(KST)
    return pendulum.instance(dt).in_timezone(UTC)


def to_kst(dt: datetime) -> datetime:
    """주어진 datetime을 KST로 변환"""
    if dt.tzinfo is None:
        # timezone 정보가 없으면 UTC로 가정
        dt = pendulum.instance(dt).in_timezone(UTC)
    return pendulum.instance(dt).in_timezone(KST)


def format_datetime(dt: datetime, timezone: str = KST, format_str: str = "YYYY-MM-DD HH:mm:ss") -> str:
    """
    datetime을 지정된 시간대와 형식으로 포맷팅
    
    Args:
        dt: 포맷팅할 datetime
        timezone: 출력할 시간대 (기본값: KST)
        format_str: 포맷 문자열 (기본값: "YYYY-MM-DD HH:mm:ss")
    
    Returns:
        포맷팅된 문자열
    """
    if dt.tzinfo is None:
        # timezone 정보가 없으면 UTC로 가정
        dt = pendulum.instance(dt).in_timezone(UTC)
    
    pdt = pendulum.instance(dt)
    return pdt.in_timezone(timezone).format(format_str)


def parse_datetime(dt_str: str, timezone: str = UTC) -> datetime:
    """
    문자열을 datetime으로 파싱
    
    Args:
        dt_str: 파싱할 문자열
        timezone: 시간대 (기본값: UTC)
    
    Returns:
        파싱된 datetime
    """
    return pendulum.parse(dt_str, tz=timezone)


def iso_format(dt: datetime, timezone: str = UTC) -> str:
    """datetime을 ISO 8601 형식 문자열로 변환"""
    if dt.tzinfo is None:
        dt = pendulum.instance(dt).in_timezone(timezone)
    return pendulum.instance(dt).in_timezone(timezone).to_iso8601_string()


def from_iso(iso_str: str, timezone: str = UTC) -> datetime:
    """ISO 8601 형식 문자열을 datetime으로 변환"""
    return pendulum.parse(iso_str).in_timezone(timezone)


