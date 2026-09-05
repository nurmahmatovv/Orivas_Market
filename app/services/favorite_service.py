import uuid

from sqlalchemy.orm import Session

from app.exceptions.favorite_exceptions import AlreadyFavoritedException, FavoriteNotFoundException
from app.models.favorite import Favorite
from app.repositories.favorite_repository import FavoriteRepository


class FavoriteService:
    def __init__(self, db: Session):
        self.repository = FavoriteRepository(db)

    def add_favorite(self, user_id: uuid.UUID, listing_id: uuid.UUID) -> Favorite:
        if self.repository.exists(user_id, listing_id):
            raise AlreadyFavoritedException()

        favorite = Favorite(user_id=user_id, listing_id=listing_id)
        return self.repository.create(favorite)

    def remove_favorite(self, user_id: uuid.UUID, listing_id: uuid.UUID) -> None:
        favorite = self.repository.get(user_id, listing_id)
        if favorite is None:
            raise FavoriteNotFoundException()

        self.repository.delete(favorite)

    def list_favorites(self, user_id: uuid.UUID) -> list[Favorite]:
        return self.repository.list_by_user(user_id)