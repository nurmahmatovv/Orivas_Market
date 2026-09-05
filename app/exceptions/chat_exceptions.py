from fastapi import HTTPException, status


class CannotMessageOwnListingException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O'z e'loningizga xabar yubora olmaysiz",
        )


class ConversationNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suhbat topilmadi",
        )


class NotConversationParticipantException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Siz bu suhbatning ishtirokchisi emassiz",
        )