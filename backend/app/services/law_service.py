"""법령 검색 서비스"""
from typing import List, Dict, Any
import logging
import xml.etree.ElementTree as ET

import httpx

from app.mock.law_data import (
    get_all_laws,
    get_law_by_id,
    search_laws_by_keyword,
    get_article_by_id,
)
from app.core.cache import get_cache, set_cache, get_cache_key
from app.core.config import settings


logger = logging.getLogger(__name__)


class LawService:
    """법령 검색 및 조회 서비스

    기본적으로 목업 데이터를 사용하지만, .env에 LAW_API_KEY 가 설정되어 있으면
    국가법령정보센터(법제처) Open API를 통해 실제 법령/조문을 조회합니다.
    """

    # 검색용
    LAW_API_BASE_URL = "https://www.law.go.kr/DRF/lawSearch.do"
    # 상세(조문 포함) 조회용
    LAW_DETAIL_BASE_URL = "https://www.law.go.kr/DRF/lawService.do"

    @staticmethod
    def _use_external_api() -> bool:
        """외부 법령 API 사용 여부"""
        return bool(getattr(settings, "law_api_key", "").strip())

    @classmethod
    def _search_laws_external(cls, keyword: str) -> List[Dict[str, Any]]:
        """법제처 Open API를 이용한 실제 법령 검색

        응답은 XML 이므로 최소한의 필드만 파싱해서 프론트에서 쓰는 형태로 변환합니다.
        (id, name, type, enactment_date, amendment_date, category, articles)
        """
        params = {
            "OC": settings.law_api_key,  # 발급받은 인증키
            "target": "law",
            "type": "XML",
            "query": keyword,
        }

        try:
            resp = httpx.get(cls.LAW_API_BASE_URL, params=params, timeout=10.0)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"법제처 API 호출 실패: {e}. 목업 데이터로 대체합니다.")
            # 외부 API 실패 시 목업 검색으로 graceful fallback
            return search_laws_by_keyword(keyword)

        try:
            root = ET.fromstring(resp.text)
        except ET.ParseError as e:
            logger.error(f"법제처 API XML 파싱 오류: {e}. 목업 데이터로 대체합니다.")
            return search_laws_by_keyword(keyword)

        laws: List[Dict[str, Any]] = []

        # DRF 응답에서 <law> 요소들을 찾아서 변환
        for law_el in root.findall("law"):
            # 태그 이름은 공식 스펙에 따라 달라질 수 있어, 여러 후보를 순서대로 시도
            law_id = (
                law_el.findtext("법령ID")
                or law_el.findtext("lawId")
                or law_el.findtext("법령일련번호")
                or ""
            )
            name = (
                law_el.findtext("법령명한글")
                or law_el.findtext("법령명_한글")
                or law_el.findtext("법령명")
                or ""
            )
            law_type = (
                law_el.findtext("법령종류")
                or law_el.findtext("법종류")
                or law_el.findtext("법령종류코드")
                or ""
            )
            # 날짜 정보는 API 스펙에 맞춰 보정 필요
            enactment_date = (
                law_el.findtext("시행일자")
                or law_el.findtext("공포일자")
                or ""
            )
            amendment_date = (
                law_el.findtext("최종시행일자")
                or law_el.findtext("개정일자")
                or ""
            )

            laws.append(
                {
                    "id": law_id or name or keyword,
                    "name": name or keyword,
                    "type": law_type,
                    "enactment_date": enactment_date,
                    "amendment_date": amendment_date,
                    "category": [],  # 외부 API에는 별도 카테고리 개념이 없으므로 비워둠
                    "articles": [],  # 상세 조문은 별도 API를 통해 확장 가능
                    "source": "law.go.kr",
                }
            )

        return laws

    @classmethod
    def _get_law_external(cls, law_id: str) -> Dict[str, Any] | None:
        """법제처 lawService.do 를 이용해 단일 법령 + 조문 목록 조회

        NOTE: law.go.kr DRF 스펙에 따라 태그명이 조금씩 다를 수 있어서,
        여러 후보 태그를 순서대로 시도하도록 구현합니다.
        """
        params = {
            "OC": settings.law_api_key,
            "target": "law",
            "type": "XML",
            "ID": law_id,
        }

        try:
            resp = httpx.get(cls.LAW_DETAIL_BASE_URL, params=params, timeout=10.0)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"법제처 lawService.do 호출 실패: {e}")
            return None

        try:
            root = ET.fromstring(resp.text)
        except ET.ParseError as e:
            logger.error(f"법제처 lawService.do XML 파싱 오류: {e}")
            return None

        # 최상위 law 요소 찾기
        law_el = root.find("law")
        if law_el is None:
            # 일부 응답은 <Law> 대문자일 수도 있음
            law_el = root.find("Law")
        if law_el is None:
            logger.warning("lawService.do 응답에서 <law> 요소를 찾지 못했습니다.")
            return None

        # 법령 기본 정보
        name = (
            law_el.findtext("법령명한글")
            or law_el.findtext("법령명_한글")
            or law_el.findtext("법령명")
            or ""
        )
        law_type = (
            law_el.findtext("법령종류")
            or law_el.findtext("법종류")
            or law_el.findtext("법령종류코드")
            or ""
        )
        enactment_date = (
            law_el.findtext("시행일자")
            or law_el.findtext("공포일자")
            or ""
        )
        amendment_date = (
            law_el.findtext("최종시행일자")
            or law_el.findtext("개정일자")
            or ""
        )

        # 조문 목록 파싱
        articles: List[Dict[str, Any]] = []

        # 일반적으로 lawService.do 응답에는 <조문> 리스트가 포함됨
        for article_el in root.findall(".//조문"):
            art_number = (
                article_el.findtext("조문번호")
                or article_el.findtext("조문번호_한글")
                or ""
            )
            art_title = (
                article_el.findtext("조문제목")
                or article_el.findtext("조문명")
                or ""
            )
            art_content = (
                article_el.findtext("조문내용")
                or article_el.findtext("조문내용_한글")
                or ""
            )

            # 우리 앱의 타입에 맞게 변환
            articles.append(
                {
                    "id": f"{law_id}-{art_number}" if art_number else f"{law_id}-article-{len(articles)+1}",
                    "law_id": law_id,
                    "number": art_number,
                    "title": art_title,
                    "content": art_content,
                    "subparagraphs": [],
                    "related_articles": [],
                }
            )

        return {
            "id": law_id,
            "name": name or law_id,
            "type": law_type,
            "enactment_date": enactment_date,
            "amendment_date": amendment_date,
            "category": [],
            "articles": articles,
            "source": "law.go.kr",
        }

    @classmethod
    def search_laws(cls, keyword: str) -> List[Dict[str, Any]]:
        """
        키워드로 법령 검색 (캐싱 적용)

        - LAW_API_KEY 가 설정되어 있으면: 법제처 Open API 사용
        - 아니면: 기존 목업 데이터 기반 검색
        """
        # 캐시 키 생성 (데이터 소스까지 포함해서 분리)
        source = "external" if cls._use_external_api() else "mock"
        cache_key = get_cache_key(f"law_search_{source}", keyword)

        # 캐시에서 가져오기
        cached_result = get_cache(cache_key, ttl=1800)  # 30분 캐시
        if cached_result is not None:
            return cached_result

        # 검색 실행
        if cls._use_external_api():
            results = cls._search_laws_external(keyword)
        else:
            results = search_laws_by_keyword(keyword)

        # 결과 캐싱
        set_cache(cache_key, results, ttl=1800)

        return results
    
    @staticmethod
    def get_law(law_id: str) -> Dict[str, Any] | None:
        """
        법령 ID로 법령 조회 (캐싱 적용)

        - LAW_API_KEY 가 설정되어 있으면: 법제처 lawService.do 로 상세 + 조문까지 조회
        - 아니면: 기존 목업 데이터에서 조회
        
        Args:
            law_id: 법령 ID
        
        Returns:
            법령 데이터 또는 None
        """
        # 캐시 키 생성
        cache_key = get_cache_key("law_detail", law_id)
        
        # 캐시에서 가져오기
        cached_result = get_cache(cache_key, ttl=3600)  # 1시간 캐시
        if cached_result is not None:
            return cached_result
        
        # 조회 실행
        if LawService._use_external_api():
            law = LawService._get_law_external(law_id)
        else:
            law = get_law_by_id(law_id)

        # 결과 캐싱 (None이 아닌 경우만)
        if law is not None:
            set_cache(cache_key, law, ttl=3600)

        return law
    
    @staticmethod
    def get_all_laws() -> List[Dict[str, Any]]:
        """
        모든 법령 조회
        
        Returns:
            모든 법령 리스트
        """
        return get_all_laws()
    
    @staticmethod
    def get_article(article_id: str) -> Dict[str, Any] | None:
        """
        조문 ID로 조문 조회
        
        Args:
            article_id: 조문 ID
        
        Returns:
            조문 데이터 또는 None
        """
        # 외부 API를 쓰는 경우, 조문 단독 조회보다는 get_law(law_id) 결과의 articles 중에서
        # 필터링해서 사용하는 것을 권장하지만,
        # 여기서는 기존 목업용 조문 조회만 그대로 유지합니다.
        return get_article_by_id(article_id)
    
    @staticmethod
    def rank_search_results(
        results: List[Dict[str, Any]],
        keyword: str
    ) -> List[Dict[str, Any]]:
        """
        검색 결과를 관련도 순으로 정렬
        
        Args:
            results: 검색 결과 리스트
            keyword: 검색 키워드
        
        Returns:
            정렬된 검색 결과 리스트
        """
        keyword_lower = keyword.lower()
        
        def calculate_score(law: Dict[str, Any]) -> int:
            """법령의 관련도 점수 계산"""
            score = 0
            
            # 법령명에 키워드가 포함되면 높은 점수
            if keyword_lower in law["name"].lower():
                score += 10
            
            # 카테고리에 키워드가 포함되면 점수 추가
            for cat in law.get("category", []):
                if keyword_lower in cat.lower():
                    score += 5
                    break
            
            # 조문 내용에 키워드가 포함되면 점수 추가
            for article in law.get("articles", []):
                if keyword_lower in article.get("content", "").lower():
                    score += 2
                    break
            
            return score
        
        # 점수 순으로 정렬
        sorted_results = sorted(
            results,
            key=calculate_score,
            reverse=True
        )
        
        return sorted_results

