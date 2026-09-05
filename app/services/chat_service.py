import uuid

from sqlalchemy.orm import Session

from app.exceptions.chat_exceptions import (
    CannotMessageOwnListingException,
    ConversationNotFoundException,
    NotConversationParticipantException,
)
from app.models.conversation import Conversation
from app.models.message import Message
from app.repositories.chat_repository import ChatRepository
from app.repositories.listing_repository import ListingRepository


class ChatService:
    def __init__(self, db: Session):
        self.repository = ChatRepository(db)
        self.listing_repository = ListingRepository(db)

    def get_or_create_conversation(self, listing_id: uuid.UUID, buyer_id: uuid.UUID) -> Conversation:
        listing = self.listing_repository.get_by_id(listing_id)
        if listing is None:
            raise ConversationNotFoundException()

        if listing.seller_id == buyer_id:
            raise CannotMessageOwnListingException()

        existing = self.repository.get_conversation_by_listing_and_buyer(listing_id, buyer_id)
        if existing:
            return existing

        conversation = Conversation(
            listing_id=listing_id,
            buyer_id=buyer_id,
            seller_id=listing.seller_id,
        )
        return self.repository.create_conversation(conversation)

    def send_message(self, conversation_id: uuid.UUID, sender_id: uuid.UUID, content: str) -> Message:
        conversation = self.repository.get_conversation_by_id(conversation_id)
        if conversation is None:
            raise ConversationNotFoundException()

        if sender_id not in (conversation.buyer_id, conversation.seller_id):
            raise NotConversationParticipantException()

        message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content,
        )
        return self.repository.create_message(message)

    def get_messages(self, conversation_id: uuid.UUID, user_id: uuid.UUID) -> list[Message]:
        conversation = self.repository.get_conversation_by_id(conversation_id)
        if conversation is None:
            raise ConversationNotFoundException()

        if user_id not in (conversation.buyer_id, conversation.seller_id):
            raise NotConversationParticipantException()

        return self.repository.list_messages(conversation_id)

    def list_my_conversations(self, user_id: uuid.UUID) -> list[Conversation]:
        return self.repository.list_conversations_for_user(user_id)