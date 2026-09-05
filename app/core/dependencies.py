from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Authorization headerdagi Bearer tokenni tekshiradi va joriy userni qaytaradi.
    Har qanday himoyalangan endpoint shu dependency'ni ishlatadi.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token yaroqsiz yoki muddati o'tgan",
    )

    try:
        payload = decode_token(credentials.credentials)
        user_id: str = payload.get("sub")
        if user_id is None or payload.get("type") != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = UserRepository(db).get_by_id(UUID(user_id))
    if user is None:
        raise credentials_exception

    return user
from app.models.user import UserRole


def require_role(*allowed_roles: UserRole):
    """
    Faqat berilgan rollardan biriga ega bo'lgan userlarga ruxsat beradigan dependency factory.
    Masalan: Depends(require_role(UserRole.ADMIN))
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bu amal uchun ruxsatingiz yo'q",
            )
        return current_user

    return role_checker