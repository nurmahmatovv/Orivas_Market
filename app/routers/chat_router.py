import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.chat import (
    ConversationCreateRequest,
    ConversationResponse,
    MessageCreateRequest,
    MessageResponse,
)
from app.services.chat_service import ChatService

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def start_conversation(
    data: ConversationCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Listing bo'yicha suhbat boshlaydi (yoki mavjudini qaytaradi)."""
    service = ChatService(db)
    return service.get_or_create_conversation(data.listing_id, current_user.id)


@router.get("/conversations", response_model=list[ConversationResponse])
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Joriy foydalanuvchining barcha suhbatlarini ro'yxat qiladi."""
    service = ChatService(db)
    return service.list_my_conversations(current_user.id)


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    conversation_id: uuid.UUID,
    data: MessageCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Suhbatga xabar yuboradi."""
    service = ChatService(db)
    return service.send_message(conversation_id, current_user.id, data.content)


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
def get_messages(
    conversation_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Suhbatdagi barcha xabarlarni qaytaradi."""
    service = ChatService(db)
    return service.get_messages(conversation_id, current_user.id)