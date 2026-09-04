import re
import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator

from app.models.user import UserRole


class UserRegisterRequest(BaseModel):
    full_name: str
    phone: str
    password: str

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, value: str) -> str:
        """Telefon raqamni har doim +998XXXXXXXXX formatiga keltiradi."""
        digits = re.sub(r"\D", "", value)
        if digits.startswith("998") and len(digits) == 12:
            return f"+{digits}"
        if len(digits) == 9:
            return f"+998{digits}"
        raise ValueError("Telefon raqam noto'g'ri formatda. Masalan: +998901234567")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Parol kamida 8 belgidan iborat bo'lishi kerak")
        return value


class UserLoginRequest(BaseModel):
    phone: str
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    phone: str
    email: str | None
    role: UserRole
    is_active: bool
    phone_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}  # ORM obyektidan to'g'ridan-to'g'ri o'qish uchun


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"