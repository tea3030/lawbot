"""에러 핸들러"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    LawChatException,
    OpenAIAPIError,
    LawNotFoundError,
    ConversationNotFoundError,
    InvalidRequestError
)
import logging

logger = logging.getLogger(__name__)


async def lawchat_exception_handler(request: Request, exc: LawChatException):
    """LawChat 커스텀 예외 핸들러"""
    logger.error(f"LawChatException: {exc.message} (Status: {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "type": exc.__class__.__name__
        }
    )


async def openai_error_handler(request: Request, exc: OpenAIAPIError):
    """OpenAI API 오류 핸들러"""
    logger.error(f"OpenAI API Error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "type": "OpenAIAPIError",
            "suggestion": "OpenAI API 키를 확인하거나 잠시 후 다시 시도해주세요."
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """일반 예외 핸들러"""
    logger.exception(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "서버 내부 오류가 발생했습니다.",
            "type": "InternalServerError"
        }
    )

