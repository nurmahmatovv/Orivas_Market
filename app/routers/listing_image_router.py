import uuid

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.listing_image import ListingImageResponse
from app.services.listing_image_service import ListingImageService

router = APIRouter(prefix="/api/v1/listings/{listing_id}/images", tags=["Listing Images"])


@router.post("", response_model=ListingImageResponse, status_code=201)
def upload_image(
    listing_id: uuid.UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Listing uchun rasm yuklaydi. Faqat listing egasi uchun."""
    service = ListingImageService(db)
    return service.upload_image(listing_id, file, current_user.id)


@router.get("", response_model=list[ListingImageResponse])
def list_images(listing_id: uuid.UUID, db: Session = Depends(get_db)):
    """Listingning barcha rasmlarini ro'yxat qiladi."""
    service = ListingImageService(db)
    return service.list_images(listing_id)