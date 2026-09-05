import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.listing import ListingStatus
from app.models.user import User, UserRole
from app.repositories.listing_repository import ListingRepository
from app.schemas.admin import RejectListingRequest
from app.schemas.listing import ListingResponse

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.patch("/listings/{listing_id}/approve", response_model=ListingResponse)
def approve_listing(
    listing_id: uuid.UUID,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.ADMIN)),
):
    """Listingni tasdiqlaydi va ACTIVE holatiga o'tkazadi. Faqat ADMIN uchun."""
    repository = ListingRepository(db)
    listing = repository.get_by_id(listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing topilmadi")

    listing.status = ListingStatus.ACTIVE
    return repository.update(listing)


@router.patch("/listings/{listing_id}/reject", response_model=ListingResponse)
def reject_listing(
    listing_id: uuid.UUID,
    data: RejectListingRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.ADMIN)),
):
    """Listingni rad etadi. Faqat ADMIN uchun."""
    repository = ListingRepository(db)
    listing = repository.get_by_id(listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing topilmadi")

    listing.status = ListingStatus.REJECTED
    return repository.update(listing)