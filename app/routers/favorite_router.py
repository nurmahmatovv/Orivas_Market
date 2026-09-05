import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.listing import ListingResponse
from app.services.favorite_service import FavoriteService

router = APIRouter(prefix="/api/v1/favorites", tags=["Favorites"])


@router.post("/{listing_id}", status_code=status.HTTP_201_CREATED)
def add_favorite(
    listing_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Listingni sevimlilar ro'yxatiga qo'shadi."""
    service = FavoriteService(db)
    service.add_favorite(current_user.id, listing_id)
    return {"success": True, "message": "Sevimlilarga qo'shildi"}


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    listing_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Listingni sevimlilar ro'yxatidan o'chiradi."""
    service = FavoriteService(db)
    service.remove_favorite(current_user.id, listing_id)


@router.get("", response_model=list[ListingResponse])
def list_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Joriy foydalanuvchining barcha sevimli listinglarini qaytaradi."""
    service = FavoriteService(db)
    favorites = service.list_favorites(current_user.id)
    return [fav.listing for fav in favorites]