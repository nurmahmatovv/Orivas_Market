import uuid

from sqlalchemy.orm import Session

from app.models.listing_image import ListingImage


class ListingImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, image: ListingImage) -> ListingImage:
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def list_by_listing(self, listing_id: uuid.UUID) -> list[ListingImage]:
        return (
            self.db.query(ListingImage)
            .filter(ListingImage.listing_id == listing_id)
            .order_by(ListingImage.order_index)
            .all()
        )

    def count_by_listing(self, listing_id: uuid.UUID) -> int:
        return self.db.query(ListingImage).filter(ListingImage.listing_id == listing_id).count()

    def get_by_id(self, image_id: uuid.UUID) -> ListingImage | None:
        return self.db.query(ListingImage).filter(ListingImage.id == image_id).first()

    def delete(self, image: ListingImage) -> None:
        self.db.delete(image)
        self.db.commit()