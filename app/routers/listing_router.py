import uuid
import math
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.listing import ListingType
from app.schemas.listing import ListingCreateRequest, ListingResponse, ListingSearchParams, PaginatedListingResponse
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.repositories.listing_repository import ListingRepository
from app.schemas.listing import ListingCreateRequest, ListingResponse
from app.services.listing_service import ListingService

router = APIRouter(prefix="/api/v1/listings", tags=["Listings"])


@router.post("", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
def create_listing(
    data: ListingCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Yangi listing yaratadi. Faqat login qilgan foydalanuvchilar uchun."""
    service = ListingService(db)
    return service.create_listing(data, seller_id=current_user.id)


@router.get("/{listing_id}", response_model=ListingResponse)
def get_listing(listing_id: uuid.UUID, db: Session = Depends(get_db)):
    """Bitta listingni to'liq ma'lumoti bilan qaytaradi (sotuvchi telefoni bilan)."""
    repository = ListingRepository(db)
    listing = repository.get_by_id(listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing topilmadi")
    return listing


@router.get("", response_model=PaginatedListingResponse)
def search_listings(
    keyword: str | None = None,
    category_id: uuid.UUID | None = None,
    location_id: uuid.UUID | None = None,
    listing_type: ListingType | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
):
    """
    Listinglarni qidiradi va filterlaydi. Faqat ACTIVE statusdagilar chiqadi.
    location_id REGION bo'lsa, uning barcha tumanlari ham qamrab olinadi.
    """
    params = ListingSearchParams(
        keyword=keyword,
        category_id=category_id,
        location_id=location_id,
        listing_type=listing_type,
        min_price=min_price,
        max_price=max_price,
        page=page,
        size=size,
    )
    service = ListingService(db)
    items, total = service.search_listings(params)

    return PaginatedListingResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total > 0 else 0,
    )