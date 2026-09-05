from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreateRequest, CategoryResponse

router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreateRequest, db: Session = Depends(get_db)):
    """
    Yangi category yaratadi. Hozircha ochiq — keyinchalik faqat ADMIN
    uchun cheklaymiz (moderatsiya bosqichida).
    """
    repository = CategoryRepository(db)
    category = Category(**data.model_dump())
    return repository.create(category)


@router.get("", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """Barcha category'larni ro'yxat qiladi."""
    repository = CategoryRepository(db)
    return repository.list_all()