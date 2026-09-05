import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app
from app.models.user import User, UserRole

TEST_DATABASE_URL = "postgresql+psycopg2://orivas_user:07242008KI@localhost:8080/OrivasMarket_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(client, db_session):
    """
    ADMIN rolidagi user yaratadi va uning tokenini qaytaradi.
    Bu orqali testlarda moderatsiya (approve/reject) sinovlarini o'tkazish mumkin.
    """
    client.post(
        "/api/v1/auth/register",
        json={"full_name": "Admin User", "phone": "+998900000000", "password": "adminpass123"},
    )

    # To'g'ridan-to'g'ri database orqali rolni ADMIN qilib qo'yamiz
    user = db_session.query(User).filter(User.phone == "+998900000000").first()
    user.role = UserRole.ADMIN
    db_session.commit()

    login_response = client.post(
        "/api/v1/auth/login",
        json={"phone": "+998900000000", "password": "adminpass123"},
    )
    return login_response.json()["access_token"]