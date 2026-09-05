import uuid

from pydantic import BaseModel


class CategoryCreateRequest(BaseModel):
    name: str
    slug: str
    parent_id: uuid.UUID | None = None
    icon: str | None = None


class CategoryResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    parent_id: uuid.UUID | None
    icon: str | None

    model_config = {"from_attributes": True}