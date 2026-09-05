import uuid
from datetime import datetime

from pydantic import BaseModel


class MessageCreateRequest(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    sender_id: uuid.UUID
    content: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationCreateRequest(BaseModel):
    listing_id: uuid.UUID


class ConversationResponse(BaseModel):
    id: uuid.UUID
    listing_id: uuid.UUID
    buyer_id: uuid.UUID
    seller_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
    
