import uuid

from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def list_all(self) -> list[Category]:
        return self.db.query(Category).order_by(Category.name).all()

    def get_by_id(self, category_id: uuid.UUID) -> Category | None:
        return self.db.query(Category).filter(Category.id == category_id).first()
    