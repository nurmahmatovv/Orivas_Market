from fastapi import HTTPException, status


class AlreadyFavoritedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu listing allaqachon sevimlilar ro'yxatida",
        )


class FavoriteNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bu listing sevimlilar ro'yxatida topilmadi",
        )