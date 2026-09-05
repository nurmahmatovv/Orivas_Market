import uuid

from sqlalchemy.orm import Session

from app.models.location import Location, LocationLevel


class LocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, location_id: uuid.UUID) -> Location | None:
        return self.db.query(Location).filter(Location.id == location_id).first()

    def get_by_name_and_parent(self, name: str, parent_id: uuid.UUID | None) -> Location | None:
        return (
            self.db.query(Location)
            .filter(Location.name == name, Location.parent_id == parent_id)
            .first()
        )

    def list_all(self, level: LocationLevel | None = None) -> list[Location]:
        query = self.db.query(Location)
        if level:
            query = query.filter(Location.level == level)
        return query.order_by(Location.name).all()

    def get_children(self, parent_id: uuid.UUID) -> list[Location]:
        return self.db.query(Location).filter(Location.parent_id == parent_id).all()

    def get_ids_including_children(self, location_id: uuid.UUID) -> list[uuid.UUID]:
        """
        Berilgan location ID'ni va uning barcha bevosita farzandlari ID'larini qaytaradi.
        Masalan: Toshkent ID berilsa -> [Toshkent_id, Sergeli_id, Chilonzor_id, ...]
        Sergeli ID berilsa -> [Sergeli_id] (chunki uning farzandi yo'q)

        Bu orqali "Toshkent" bo'yicha qidiruv butun viloyatni,
        "Sergeli" bo'yicha qidiruv faqat o'sha tumanni qamrab oladi.
        """
        ids = [location_id]
        children = self.get_children(location_id)
        ids.extend([child.id for child in children])
        return ids

    def create(self, location: Location) -> Location:
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location