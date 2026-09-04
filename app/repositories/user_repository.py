import uuid

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Faqat database bilan ishlaydigan qatlam.
    Hech qanday business logic bu yerda bo'lmaydi — faqat CRUD operatsiyalar.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_phone(self, phone: str) -> User | None:
        return self.db.query(User).filter(User.phone == phone).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def exists_by_phone(self, phone: str) -> bool:
        return self.db.query(User).filter(User.phone == phone).first() is not None