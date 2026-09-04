import uuid

from pydantic import BaseModel

from app.models.location import LocationLevel


class LocationCreateRequest(BaseModel):
    name: str
    level: LocationLevel
    parent_id: uuid.UUID | None = None


class LocationResponse(BaseModel):
    id: uuid.UUID
    name: str
    level: LocationLevel
    parent_id: uuid.UUID | None

    model_config = {"from_attributes": True}