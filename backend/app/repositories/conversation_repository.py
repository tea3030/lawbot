"""Conversation repository - SQLite implementation"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models import Conversation
from app.schemas.chat import ConversationCreate, ConversationResponse
from app.utils.date_utils import now_utc


class ConversationRepository:
    """Conversation repository for SQLite"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, conversation: ConversationCreate) -> Conversation:
        """Create a new conversation"""
        import uuid
        db_conversation = Conversation(
            id=str(uuid.uuid4()),
            title=conversation.title,
            created_at=now_utc(),
            updated_at=now_utc()
        )
        self.db.add(db_conversation)
        self.db.commit()
        self.db.refresh(db_conversation)
        return db_conversation
    
    def get_by_id(self, id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        return self.db.query(Conversation).filter(Conversation.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Conversation]:
        """Get all conversations"""
        return self.db.query(Conversation).offset(skip).limit(limit).all()
    
    def update(self, id: str, title: Optional[str] = None) -> Optional[Conversation]:
        """Update conversation"""
        conversation = self.get_by_id(id)
        if conversation:
            if title is not None:
                conversation.title = title
            conversation.updated_at = now_utc()
            self.db.commit()
            self.db.refresh(conversation)
        return conversation
    
    def delete(self, id: str) -> bool:
        """Delete conversation"""
        conversation = self.get_by_id(id)
        if conversation:
            self.db.delete(conversation)
            self.db.commit()
            return True
        return False


