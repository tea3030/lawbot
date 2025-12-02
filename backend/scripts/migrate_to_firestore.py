"""SQLite에서 Firestore로 데이터 마이그레이션 스크립트"""
import sys
import os
import json
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import get_db
from app.db.models import Conversation, Message
from app.core.config import settings
import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    """Firebase 초기화"""
    if not settings.firebase_credentials_path:
        raise ValueError("FIREBASE_CREDENTIALS_PATH 환경 변수가 설정되지 않았습니다.")
    
    if not os.path.exists(settings.firebase_credentials_path):
        raise FileNotFoundError(f"Firebase 인증서 파일을 찾을 수 없습니다: {settings.firebase_credentials_path}")
    
    cred = credentials.Certificate(settings.firebase_credentials_path)
    firebase_admin.initialize_app(cred)
    return firestore.client()

def migrate_conversations(db_session, firestore_db):
    """대화 세션 마이그레이션"""
    conversations = db_session.query(Conversation).all()
    print(f"마이그레이션할 대화 세션 수: {len(conversations)}")
    
    for conv in conversations:
        doc_ref = firestore_db.collection('conversations').document(conv.id)
        doc_ref.set({
            'id': conv.id,
            'title': conv.title,
            'created_at': conv.created_at.isoformat() if conv.created_at else None,
            'updated_at': conv.updated_at.isoformat() if conv.updated_at else None,
        })
        print(f"  ✓ 대화 세션 마이그레이션: {conv.id}")
    
    return len(conversations)

def migrate_messages(db_session, firestore_db):
    """메시지 마이그레이션"""
    messages = db_session.query(Message).all()
    print(f"마이그레이션할 메시지 수: {len(messages)}")
    
    for msg in messages:
        doc_ref = firestore_db.collection('messages').document(msg.id)
        
        # law_references 파싱
        law_refs = None
        if msg.law_references:
            try:
                law_refs = json.loads(msg.law_references)
            except:
                pass
        
        doc_ref.set({
            'id': msg.id,
            'conversation_id': msg.conversation_id,
            'role': msg.role,
            'content': msg.content,
            'law_references': law_refs,
            'created_at': msg.created_at.isoformat() if msg.created_at else None,
        })
        print(f"  ✓ 메시지 마이그레이션: {msg.id}")
    
    return len(messages)

def main():
    """메인 마이그레이션 함수"""
    print("=" * 50)
    print("SQLite → Firestore 마이그레이션 시작")
    print("=" * 50)
    
    # Firebase 초기화
    try:
        firestore_db = init_firebase()
        print("✓ Firebase 초기화 완료")
    except Exception as e:
        print(f"✗ Firebase 초기화 실패: {e}")
        return 1
    
    # SQLite 데이터베이스 연결
    try:
        db_session = next(get_db())
        print("✓ SQLite 데이터베이스 연결 완료")
    except Exception as e:
        print(f"✗ SQLite 데이터베이스 연결 실패: {e}")
        return 1
    
    # 마이그레이션 실행
    try:
        conv_count = migrate_conversations(db_session, firestore_db)
        msg_count = migrate_messages(db_session, firestore_db)
        
        print("=" * 50)
        print("마이그레이션 완료!")
        print(f"  - 대화 세션: {conv_count}개")
        print(f"  - 메시지: {msg_count}개")
        print("=" * 50)
        
        return 0
    except Exception as e:
        print(f"✗ 마이그레이션 실패: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        db_session.close()

if __name__ == "__main__":
    exit(main())

