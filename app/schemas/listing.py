import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator, model_validator

from app.models.listing import Currency, ListingStatus, ListingType


class ListingCreateRequest(BaseModel):
    title: str
    description: str | None = None

    price: Decimal
    currency: Currency = Currency.UZS

    listing_type: ListingType
    category_id: uuid.UUID

    region_name: str
    district_name: str | None = None

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("Narx musbat son bo'lishi kerak")
        return value


class ListingResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    price: Decimal
    currency: Currency
    listing_type: ListingType
    status: ListingStatus
    seller_id: uuid.UUID
    category_id: uuid.UUID
    location_id: uuid.UUID
    created_at: datetime

    seller_name: str
    seller_phone: str

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def extract_seller_info(cls, obj):
        """
        Listing modelidagi `seller` relationship'idan ism va telefonni chiqarib,
        tekis (flat) response'ga joylashtiradi — client'ga ikki marta so'rov
        yubormasdan, bitta javobda barcha kerakli ma'lumot beriladi.
        """
        if hasattr(obj, "seller") and obj.seller is not None:
            obj.seller_name = obj.seller.full_name
            obj.seller_phone = obj.seller.phone
        return obj


class ListingSearchParams(BaseModel):
    keyword: str | None = None
    category_id: uuid.UUID | None = None
    location_id: uuid.UUID | None = None
    listing_type: ListingType | None = None
    min_price: Decimal | None = None
    max_price: Decimal | None = None
    page: int = 1
    size: int = 20


class PaginatedListingResponse(BaseModel):
    items: list[ListingResponse]
    total: int
    page: int
    size: int
    pages: int