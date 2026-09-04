from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenResponse, UserLoginRequest, UserRegisterRequest
from app.exceptions.auth_exceptions import InvalidCredentialsException, PhoneAlreadyExistsException


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register(self, data: UserRegisterRequest) -> User:
        if self.user_repository.exists_by_phone(data.phone):
            raise PhoneAlreadyExistsException(data.phone)

        user = User(
            full_name=data.full_name,
            phone=data.phone,
            password_hash=hash_password(data.password),
        )
        return self.user_repository.create(user)

    def login(self, data: UserLoginRequest) -> TokenResponse:
        user = self.user_repository.get_by_phone(data.phone)

        if not user or not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsException()

        access_token = create_access_token(subject=str(user.id), role=user.role.value)
        refresh_token = create_refresh_token(subject=str(user.id))

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
