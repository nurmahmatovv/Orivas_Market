from pydantic import BaseModel


class RejectListingRequest(BaseModel):
    reason: str | None = None