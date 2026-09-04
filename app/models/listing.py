import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class ListingType(str, enum.Enum):
    SALE = "SALE"
    RENT = "RENT"


class ListingStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SOLD = "SOLD"
    RENTED = "RENTED"
    PENDING_MODERATION = "PENDING_MODERATION"
    REJECTED = "REJECTED"


class Currency(str, enum.Enum):
    UZS = "UZS"
    USD = "USD"


class Listing(Base):
    __tablename__ = "listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    price = Column(Numeric(14, 2), nullable=False)
    currency = Column(Enum(Currency), default=Currency.UZS, nullable=False)

    listing_type = Column(Enum(ListingType), nullable=False)
    status = Column(Enum(ListingStatus), default=ListingStatus.PENDING_MODERATION, nullable=False)

    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False, index=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    seller = relationship("User", backref="listings")
    category = relationship("Category", backref="listings")
    location = relationship("Location", backref="listings")