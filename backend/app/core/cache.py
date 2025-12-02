"""캐시 유틸리티"""
from typing import Optional, Any
from datetime import datetime, timedelta
import hashlib
import json

# 간단한 인메모리 캐시 (프로덕션에서는 Redis 등을 사용 권장)
_cache: dict[str, dict[str, Any]] = {}


def get_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    캐시 키 생성
    
    Args:
        prefix: 캐시 키 접두사
        *args: 위치 인자
        **kwargs: 키워드 인자
    
    Returns:
        캐시 키 문자열
    """
    # 인자를 JSON으로 직렬화하여 해시 생성
    key_data = {
        "prefix": prefix,
        "args": args,
        "kwargs": kwargs
    }
    key_str = json.dumps(key_data, sort_keys=True)
    key_hash = hashlib.md5(key_str.encode()).hexdigest()
    return f"{prefix}:{key_hash}"


def get_cache(key: str, ttl: int = 3600) -> Optional[Any]:
    """
    캐시에서 값 가져오기
    
    Args:
        key: 캐시 키
        ttl: Time To Live (초 단위, 기본값 1시간)
    
    Returns:
        캐시된 값 또는 None
    """
    if key not in _cache:
        return None
    
    cached_item = _cache[key]
    expires_at = cached_item.get("expires_at")
    
    # 만료 시간 확인
    if expires_at and datetime.now() > expires_at:
        del _cache[key]
        return None
    
    return cached_item.get("value")


def set_cache(key: str, value: Any, ttl: int = 3600) -> None:
    """
    캐시에 값 저장
    
    Args:
        key: 캐시 키
        value: 저장할 값
        ttl: Time To Live (초 단위, 기본값 1시간)
    """
    expires_at = datetime.now() + timedelta(seconds=ttl)
    _cache[key] = {
        "value": value,
        "expires_at": expires_at,
        "created_at": datetime.now()
    }


def clear_cache(prefix: Optional[str] = None) -> int:
    """
    캐시 삭제
    
    Args:
        prefix: 접두사로 시작하는 키만 삭제 (None이면 전체 삭제)
    
    Returns:
        삭제된 항목 수
    """
    if prefix is None:
        count = len(_cache)
        _cache.clear()
        return count
    
    keys_to_delete = [key for key in _cache.keys() if key.startswith(prefix)]
    for key in keys_to_delete:
        del _cache[key]
    
    return len(keys_to_delete)


def cache_decorator(ttl: int = 3600, prefix: str = "cache"):
    """
    함수 결과를 캐싱하는 데코레이터
    
    Args:
        ttl: 캐시 유지 시간 (초)
        prefix: 캐시 키 접두사
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 캐시 키 생성
            cache_key = get_cache_key(prefix, func.__name__, *args, **kwargs)
            
            # 캐시에서 가져오기
            cached_value = get_cache(cache_key, ttl)
            if cached_value is not None:
                return cached_value
            
            # 함수 실행
            result = func(*args, **kwargs)
            
            # 결과 캐싱
            set_cache(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator

