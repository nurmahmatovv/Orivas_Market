import uuid

from sqlalchemy.orm import Session

from app.models.listing import Listing, ListingStatus
from app.models.location import LocationLevel
from app.repositories.listing_repository import ListingRepository
from app.schemas.listing import ListingCreateRequest
from app.services.location_service import LocationService


class ListingService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ListingRepository(db)
        self.location_service = LocationService(db)

    def create_listing(self, data: ListingCreateRequest, seller_id: uuid.UUID) -> Listing:
        # 1-qadam: manzil matnidan location_id topamiz yoki yaratamiz
        region = self.location_service.get_or_create(
            name=data.region_name,
            level=LocationLevel.REGION,
            parent_id=None,
        )

        location_id = region.id
        if data.district_name:
            district = self.location_service.get_or_create(
                name=data.district_name,
                level=LocationLevel.DISTRICT,
                parent_id=region.id,
            )
            location_id = district.id

        # 2-qadam: listing yaratamiz
        listing = Listing(
            title=data.title,
            description=data.description,
            price=data.price,
            currency=data.currency,
            listing_type=data.listing_type,
            status=ListingStatus.PENDING_MODERATION,
            seller_id=seller_id,
            category_id=data.category_id,
            location_id=location_id,
        )
        return self.repository.create(listing)

    def search_listings(self, params) -> tuple[list[Listing], int]:
        from app.repositories.location_repository import LocationRepository

        location_ids = None
        if params.location_id:
            location_repo = LocationRepository(self.db)
            location_ids = location_repo.get_ids_including_children(params.location_id)

        return self.repository.search(
            keyword=params.keyword,
            category_id=params.category_id,
            location_ids=location_ids,
            listing_type=params.listing_type,
            min_price=params.min_price,
            max_price=params.max_price,
            page=params.page,
            size=params.size,
        )