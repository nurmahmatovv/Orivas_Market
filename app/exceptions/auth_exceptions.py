from fastapi import HTTPException, status


class PhoneAlreadyExistsException(HTTPException):
    def __init__(self, phone: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bu telefon raqam allaqachon ro'yxatdan o'tgan: {phone}",
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Telefon raqam yoki parol noto'g'ri",
        )