"""Law API endpoints"""
from fastapi import APIRouter, Query
from app.services.law_service import LawService
from app.core.exceptions import LawNotFoundError, InvalidRequestError
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/laws", tags=["laws"])
law_service = LawService()


@router.get("/")
async def get_laws():
    """모든 법령 목록 조회"""
    laws = law_service.get_all_laws()
    return {"laws": laws, "count": len(laws)}


@router.get("/search")
async def search_laws(keyword: str = Query(..., description="검색 키워드")):
    """키워드로 법령 검색 (관련도 순 정렬)"""
    if not keyword or not keyword.strip():
        raise InvalidRequestError("검색 키워드를 입력해주세요.")
    
    if len(keyword) > 100:
        raise InvalidRequestError("검색 키워드는 100자 이하로 입력해주세요.")
    
    try:
        results = law_service.search_laws(keyword)
        # 관련도 순으로 정렬
        ranked_results = law_service.rank_search_results(results, keyword)
        return {"laws": ranked_results, "count": len(ranked_results), "keyword": keyword}
    except Exception as e:
        logger.error(f"법령 검색 중 오류: {str(e)}")
        raise


@router.get("/{law_id}")
async def get_law(law_id: str):
    """법령 ID로 법령 상세 조회"""
    law = law_service.get_law(law_id)
    if not law:
        raise LawNotFoundError(law_id)
    return {"law": law}


@router.get("/{law_id}/articles/{article_id}")
async def get_article(law_id: str, article_id: str):
    """조문 ID로 조문 상세 조회"""
    article = law_service.get_article(article_id)
    if not article:
        raise LawNotFoundError(f"조문을 찾을 수 없습니다. (ID: {article_id})")
    return {"article": article}


