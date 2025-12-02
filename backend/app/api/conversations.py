"""대화 세션 관리 API"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.chat import ConversationCreate, ConversationResponse, MessageResponse
from app.core.exceptions import ConversationNotFoundError, InvalidRequestError
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):
    """새 대화 세션 생성"""
    conversation_repo = ConversationRepository(db)
    new_conversation = conversation_repo.create(conversation)
    
    return ConversationResponse(
        id=new_conversation.id,
        title=new_conversation.title,
        created_at=new_conversation.created_at,
        updated_at=new_conversation.updated_at
    )


@router.get("/", response_model=List[ConversationResponse])
async def get_conversations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """모든 대화 세션 목록 조회"""
    conversation_repo = ConversationRepository(db)
    conversations = conversation_repo.get_all(skip=skip, limit=limit)
    
    return [
        ConversationResponse(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at
        )
        for conv in conversations
    ]


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """대화 세션 상세 조회"""
    if not conversation_id or not conversation_id.strip():
        raise InvalidRequestError("대화 세션 ID를 입력해주세요.")
    
    conversation_repo = ConversationRepository(db)
    conversation = conversation_repo.get_by_id(conversation_id)
    
    if not conversation:
        raise ConversationNotFoundError(conversation_id)
    
    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """대화 세션의 모든 메시지 조회"""
    message_repo = MessageRepository(db)
    messages = message_repo.get_by_conversation_id(conversation_id)
    
    result = []
    for msg in messages:
        # law_references 파싱
        law_references = None
        if msg.law_references:
            try:
                law_refs_data = json.loads(msg.law_references)
                from app.schemas.chat import LawReference
                law_references = [
                    LawReference(
                        law_id=ref.get("law_id", ""),
                        title=ref.get("title"),
                        article=ref.get("article")
                    )
                    for ref in law_refs_data
                ]
            except:
                pass
        
        result.append(MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            conversation_id=msg.conversation_id,
            created_at=msg.created_at,
            law_references=law_references
        ))
    
    return result


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """대화 세션 삭제"""
    if not conversation_id or not conversation_id.strip():
        raise InvalidRequestError("대화 세션 ID를 입력해주세요.")
    
    conversation_repo = ConversationRepository(db)
    success = conversation_repo.delete(conversation_id)
    
    if not success:
        raise ConversationNotFoundError(conversation_id)
    
    return {"success": True, "message": "Conversation deleted"}

