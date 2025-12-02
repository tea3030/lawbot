"""Chat-related Pydantic schemas"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class LawReference(BaseModel):
    """법령 출처 정보"""
    law_id: str
    title: Optional[str] = None
    article: Optional[str] = None


class MessageBase(BaseModel):
    """메시지 기본 스키마"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    law_references: Optional[List[LawReference]] = None


class MessageCreate(MessageBase):
    """메시지 생성 스키마"""
    conversation_id: Optional[str] = None


class MessageResponse(MessageBase):
    """메시지 응답 스키마"""
    id: str
    conversation_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    """대화 세션 기본 스키마"""
    title: Optional[str] = None


class ConversationCreate(ConversationBase):
    """대화 세션 생성 스키마"""
    pass


class ConversationResponse(ConversationBase):
    """대화 세션 응답 스키마"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """채팅 요청 스키마"""
    message: str = Field(..., description="User message")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID")


class ChatResponse(BaseModel):
    """채팅 응답 스키마"""
    id: str
    content: str
    law_references: Optional[List[LawReference]] = None


