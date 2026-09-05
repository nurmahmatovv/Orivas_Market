import uuid

from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    listing_id = Column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False, index=True)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    listing = relationship("Listing", backref="conversations")
    buyer = relationship("User", foreign_keys=[buyer_id], backref="conversations_as_buyer")
    seller = relationship("User", foreign_keys=[seller_id], backref="conversations_as_seller")

    __table_args__ = (
        UniqueConstraint("listing_id", "buyer_id", name="uq_listing_buyer_conversation"),
    )