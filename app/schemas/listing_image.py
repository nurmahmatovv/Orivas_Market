import uuid

from pydantic import BaseModel


class ListingImageResponse(BaseModel):
    id: uuid.UUID
    listing_id: uuid.UUID
    url: str
    order_index: int

    model_config = {"from_attributes": True}