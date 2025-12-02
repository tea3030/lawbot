"""Message repository - SQLite implementation"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models import Message
from app.schemas.chat import MessageCreate, MessageResponse
from app.utils.date_utils import now_utc


class MessageRepository:
    """Message repository for SQLite"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, message: MessageCreate) -> Message:
        """Create a new message"""
        import uuid
        import json
        # LawReference를 dict로 변환
        law_refs_json = None
        if message.law_references:
            law_refs_json = json.dumps([
                {
                    "law_id": ref.law_id,
                    "title": ref.title,
                    "article": ref.article
                }
                for ref in message.law_references
            ])
        
        db_message = Message(
            id=str(uuid.uuid4()),
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            law_references=law_refs_json,
            created_at=now_utc()
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
    
    def get_by_id(self, id: str) -> Optional[Message]:
        """Get message by ID"""
        return self.db.query(Message).filter(Message.id == id).first()
    
    def get_by_conversation_id(self, conversation_id: str) -> List[Message]:
        """Get all messages in a conversation"""
        return self.db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Message]:
        """Get all messages"""
        return self.db.query(Message).offset(skip).limit(limit).all()
    
    def delete(self, id: str) -> bool:
        """Delete message"""
        message = self.get_by_id(id)
        if message:
            self.db.delete(message)
            self.db.commit()
            return True
        return False


