from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserRegisterRequest, db: Session = Depends(get_db)):
    """Yangi foydalanuvchini ro'yxatdan o'tkazadi."""
    service = AuthService(db)
    user = service.register(data)
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: UserLoginRequest, db: Session = Depends(get_db)):
    """Login qiladi va access/refresh token qaytaradi."""
    service = AuthService(db)
    return service.login(data)
from app.core.dependencies import get_current_user

# ... mavjud kodlar tepada qoladi, faqat pastga shuni qo'shing:

@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    """Joriy login qilgan foydalanuvchi ma'lumotini qaytaradi."""
    return current_user