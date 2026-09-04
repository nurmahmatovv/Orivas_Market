from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Butun ilova uchun markazlashgan konfiguratsiya.
    Barcha qiymatlar .env fayldan o'qiladi, hech narsa kodga hardcode qilinmaydi.
    """

    # App
    APP_NAME: str = "Orivas Market"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Butun ilova bo'ylab shu bitta instance ishlatiladi (singleton pattern)
settings = Settings()
