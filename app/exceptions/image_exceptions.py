from fastapi import HTTPException, status


class InvalidImageFormatException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Faqat JPG, JPEG, PNG formatidagi rasmlar qabul qilinadi",
        )


class ImageTooLargeException(HTTPException):
    def __init__(self, max_size_mb: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rasm hajmi {max_size_mb}MB dan oshmasligi kerak",
        )


class ListingNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing topilmadi",
        )


class NotListingOwnerException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Faqat listing egasi rasm qo'sha oladi",
        )