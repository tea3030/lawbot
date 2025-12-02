"""Chat API endpoints"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.chat import ChatRequest, ChatResponse, LawReference, MessageCreate, ConversationCreate
from app.db.database import get_db
from app.repositories.message_repository import MessageRepository
from app.repositories.conversation_repository import ConversationRepository
from app.services.openai_service import get_openai_service
from app.core.exceptions import OpenAIAPIError, InvalidRequestError
from app.mock.law_data import search_laws_by_keyword
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """채팅 메시지 전송 및 응답 생성"""
    # 입력 검증
    if not request.message or not request.message.strip():
        raise InvalidRequestError("질문 내용을 입력해주세요.")
    
    if len(request.message) > 1000:
        raise InvalidRequestError("질문은 1000자 이하로 입력해주세요.")
    
    try:
        # 대화 세션 확인 및 생성
        conversation_id = request.conversation_id
        if not conversation_id:
            # 새 대화 세션 생성
            conversation_repo = ConversationRepository(db)
            new_conversation = conversation_repo.create(
                ConversationCreate(title=request.message[:50])  # 첫 메시지의 일부를 제목으로
            )
            conversation_id = new_conversation.id
        
        # 사용자 메시지 저장
        message_repo = MessageRepository(db)
        user_message = message_repo.create(
            MessageCreate(
                role="user",
                content=request.message,
                conversation_id=conversation_id,
                law_references=None
            )
        )
        
        # 관련 법령 검색
        related_laws = search_laws_by_keyword(request.message)
        
        # 대화 히스토리 가져오기
        previous_messages = message_repo.get_by_conversation_id(conversation_id)
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in previous_messages[-10:]  # 최근 10개만 (현재 메시지 제외)
        ]
        
        # OpenAI 서비스를 사용하여 답변 생성
        try:
            openai_service = get_openai_service()
            response_content = openai_service.ask_question(
                question=request.message,
                conversation_history=conversation_history
            )
        except Exception as e:
            logger.error(f"OpenAI API 호출 실패: {str(e)}")
            raise OpenAIAPIError(f"AI 답변 생성 중 오류가 발생했습니다: {str(e)}")
        
        # 법령 출처 추출
        law_references_data = openai_service.extract_law_references(
            response_content,
            related_laws
        )
        
        # LawReference 객체로 변환
        law_references = [
            LawReference(
                law_id=ref["law_id"],
                title=ref["title"],
                article=ref.get("article")
            )
            for ref in law_references_data
        ]
        
        # 응답 메시지 저장
        bot_message = message_repo.create(
            MessageCreate(
                role="assistant",
                content=response_content,
                conversation_id=conversation_id,
                law_references=law_references
            )
        )
        
        # 대화 세션 업데이트 시간 갱신
        conversation_repo = ConversationRepository(db)
        conversation_repo.update(conversation_id)
        
        return ChatResponse(
            id=str(bot_message.id),
            content=bot_message.content,
            law_references=law_references
        )
    
    except (OpenAIAPIError, InvalidRequestError):
        # 커스텀 예외는 그대로 전파
        raise
    except Exception as e:
        logger.exception(f"메시지 처리 중 예상치 못한 오류: {str(e)}")
        raise


