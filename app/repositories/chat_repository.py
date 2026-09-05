import uuid

from sqlalchemy.orm import Session, joinedload

from app.models.conversation import Conversation
from app.models.message import Message


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_conversation_by_listing_and_buyer(
        self, listing_id: uuid.UUID, buyer_id: uuid.UUID
    ) -> Conversation | None:
        return (
            self.db.query(Conversation)
            .filter(Conversation.listing_id == listing_id, Conversation.buyer_id == buyer_id)
            .first()
        )

    def create_conversation(self, conversation: Conversation) -> Conversation:
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, conversation_id: uuid.UUID) -> Conversation | None:
        return (
            self.db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

    def list_conversations_for_user(self, user_id: uuid.UUID) -> list[Conversation]:
        return (
            self.db.query(Conversation)
            .options(joinedload(Conversation.listing))
            .filter(
                (Conversation.buyer_id == user_id) | (Conversation.seller_id == user_id)
            )
            .order_by(Conversation.created_at.desc())
            .all()
        )

    def create_message(self, message: Message) -> Message:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def list_messages(self, conversation_id: uuid.UUID) -> list[Message]:
        return (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )
    