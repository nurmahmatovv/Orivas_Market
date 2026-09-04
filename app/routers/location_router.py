from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.location import LocationLevel
from app.schemas.location import LocationResponse
from app.services.location_service import LocationService

router = APIRouter(prefix="/api/v1/locations", tags=["Locations"])


@router.get("", response_model=list[LocationResponse])
def list_locations(
    level: LocationLevel | None = Query(default=None, description="REGION yoki DISTRICT bo'yicha filter"),
    db: Session = Depends(get_db),
):
    """Barcha joylashuvlarni ro'yxat qiladi, ixtiyoriy ravishda level bo'yicha filterlaydi."""
    service = LocationService(db)
    return service.list_locations(level)