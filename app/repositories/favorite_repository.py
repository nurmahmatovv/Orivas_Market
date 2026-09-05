import uuid

from sqlalchemy.orm import Session, joinedload

from app.models.favorite import Favorite
from app.models.listing import Listing


class FavoriteRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists(self, user_id: uuid.UUID, listing_id: uuid.UUID) -> bool:
        return (
            self.db.query(Favorite)
            .filter(Favorite.user_id == user_id, Favorite.listing_id == listing_id)
            .first()
            is not None
        )

    def create(self, favorite: Favorite) -> Favorite:
        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)
        return favorite

    def get(self, user_id: uuid.UUID, listing_id: uuid.UUID) -> Favorite | None:
        return (
            self.db.query(Favorite)
            .filter(Favorite.user_id == user_id, Favorite.listing_id == listing_id)
            .first()
        )

    def delete(self, favorite: Favorite) -> None:
        self.db.delete(favorite)
        self.db.commit()

    def list_by_user(self, user_id: uuid.UUID) -> list[Favorite]:
        return (
            self.db.query(Favorite)
            .options(joinedload(Favorite.listing).joinedload(Listing.seller))
            .filter(Favorite.user_id == user_id)
            .all()
        )