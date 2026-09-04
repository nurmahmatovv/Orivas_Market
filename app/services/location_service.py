from app.models.location import Location, LocationLevel
from app.repositories.location_repository import LocationRepository
from app.schemas.location import LocationResponse


class LocationService:
    def __init__(self, db):
        self.repository = LocationRepository(db)

    def list_locations(self, level: LocationLevel | None = None) -> list[LocationResponse]:
        locations = self.repository.list_all(level)
        return [LocationResponse.model_validate(loc) for loc in locations]

    def get_or_create(self, name: str, level: LocationLevel, parent_id=None) -> Location:
        """
        Sotuvchi manzil kiritganda ishlatiladi: agar shu nomdagi location
        (aynan shu ota ostida) mavjud bo'lsa, o'shani qaytaradi;
        bo'lmasa, yangisini yaratadi.

        Bu orqali baza faqat haqiqatan ishlatilayotgan joylashuvlar bilan to'ladi,
        oldindan butun O'zbekiston ro'yxatini qo'lda kiritish shart emas.
        """
        existing = self.repository.get_by_name_and_parent(name, parent_id)
        if existing:
            return existing

        new_location = Location(name=name, level=level, parent_id=parent_id)
        return self.repository.create(new_location)