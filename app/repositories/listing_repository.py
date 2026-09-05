import uuid
from decimal import Decimal

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.listing import Listing, ListingStatus, ListingType


class ListingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, listing_id: uuid.UUID) -> Listing | None:
        return (
            self.db.query(Listing)
            .options(joinedload(Listing.seller))
            .filter(Listing.id == listing_id)
            .first()
        )

    def create(self, listing: Listing) -> Listing:
        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing

    def list_by_seller(self, seller_id: uuid.UUID) -> list[Listing]:
        return (
            self.db.query(Listing)
            .options(joinedload(Listing.seller))
            .filter(Listing.seller_id == seller_id)
            .all()
        )

    def update(self, listing: Listing) -> Listing:
        self.db.commit()
        self.db.refresh(listing)
        return listing

    def delete(self, listing: Listing) -> None:
        self.db.delete(listing)
        self.db.commit()

    def search(
        self,
        keyword: str | None = None,
        category_id: uuid.UUID | None = None,
        location_ids: list[uuid.UUID] | None = None,
        listing_type: ListingType | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[Listing], int]:
        """
        Filterlangan, sahifalangan listing ro'yxatini qaytaradi.
        Faqat ACTIVE statusdagi listinglar ko'rsatiladi (moderatsiyadan
        o'tmagan yoki bekor qilinganlar qidiruvda chiqmaydi).
        """
        query = self.db.query(Listing).options(joinedload(Listing.seller))

        query = query.filter(Listing.status == ListingStatus.ACTIVE)

        if keyword:
            query = query.filter(
                or_(
                    Listing.title.ilike(f"%{keyword}%"),
                    Listing.description.ilike(f"%{keyword}%"),
                )
            )

        if category_id:
            query = query.filter(Listing.category_id == category_id)

        if location_ids:
            query = query.filter(Listing.location_id.in_(location_ids))

        if listing_type:
            query = query.filter(Listing.listing_type == listing_type)

        if min_price is not None:
            query = query.filter(Listing.price >= min_price)

        if max_price is not None:
            query = query.filter(Listing.price <= max_price)

        total = query.count()

        items = (
            query.order_by(Listing.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )

        return items, total