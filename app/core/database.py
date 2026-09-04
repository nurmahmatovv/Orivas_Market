from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Database bilan bog'lanish uchun engine
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Har bir request uchun alohida session yaratadigan factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Barcha SQLAlchemy modellar shu Base'dan meros oladi
Base = declarative_base()


def get_db():
    """
    FastAPI dependency: har bir request uchun DB session ochadi
    va request tugagach albatta yopadi (connection leak bo'lmasligi uchun).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
