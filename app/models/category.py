import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    icon = Column(String(255), nullable=True)

    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True, index=True)

    # Self-referencing: bitta parent category ko'p child category'ga ega bo'lishi mumkin
    children = relationship("Category", backref="parent", remote_side=[id])