"""커스텀 예외 클래스"""
from fastapi import HTTPException, status


class LawChatException(Exception):
    """기본 예외 클래스"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class OpenAIAPIError(LawChatException):
    """OpenAI API 호출 오류"""
    def __init__(self, message: str = "OpenAI API 호출 중 오류가 발생했습니다."):
        super().__init__(message, status_code=503)


class LawNotFoundError(LawChatException):
    """법령을 찾을 수 없음"""
    def __init__(self, law_id: str = None):
        message = f"법령을 찾을 수 없습니다." + (f" (ID: {law_id})" if law_id else "")
        super().__init__(message, status_code=404)


class ConversationNotFoundError(LawChatException):
    """대화 세션을 찾을 수 없음"""
    def __init__(self, conversation_id: str = None):
        message = f"대화 세션을 찾을 수 없습니다." + (f" (ID: {conversation_id})" if conversation_id else "")
        super().__init__(message, status_code=404)


class InvalidRequestError(LawChatException):
    """잘못된 요청"""
    def __init__(self, message: str = "잘못된 요청입니다."):
        super().__init__(message, status_code=400)

