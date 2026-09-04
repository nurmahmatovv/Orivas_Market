import enum
import uuid

from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class LocationLevel(str, enum.Enum):
    REGION = "REGION"
    DISTRICT = "DISTRICT"


class Location(Base):
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(255), nullable=False)
    level = Column(Enum(LocationLevel), nullable=False)

    parent_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=True, index=True)

    # Self-referencing relationship: bitta region ko'p district'larga ega bo'ladi
    children = relationship("Location", backref="parent", remote_side=[id])