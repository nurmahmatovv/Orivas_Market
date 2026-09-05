import os
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.exceptions.image_exceptions import (
    ImageTooLargeException,
    InvalidImageFormatException,
    ListingNotFoundException,
    NotListingOwnerException,
)
from app.models.listing_image import ListingImage
from app.repositories.listing_image_repository import ListingImageRepository
from app.repositories.listing_repository import ListingRepository

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class ListingImageService:
    def __init__(self, db: Session):
        self.image_repository = ListingImageRepository(db)
        self.listing_repository = ListingRepository(db)

    def upload_image(self, listing_id: uuid.UUID, file: UploadFile, current_user_id: uuid.UUID) -> ListingImage:
        listing = self.listing_repository.get_by_id(listing_id)
        if listing is None:
            raise ListingNotFoundException()

        if listing.seller_id != current_user_id:
            raise NotListingOwnerException()

        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise InvalidImageFormatException()

        file.file.seek(0, os.SEEK_END)
        size_bytes = file.file.tell()
        file.file.seek(0)

        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if size_bytes > max_bytes:
            raise ImageTooLargeException(settings.MAX_UPLOAD_SIZE_MB)

        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        order_index = self.image_repository.count_by_listing(listing_id)

        image = ListingImage(
            listing_id=listing_id,
            url=f"/{settings.UPLOAD_DIR}/{unique_filename}",
            order_index=order_index,
        )
        return self.image_repository.create(image)

    def list_images(self, listing_id: uuid.UUID) -> list[ListingImage]:
        return self.image_repository.list_by_listing(listing_id)