def test_register_success(client):
    """Yangi user muvaffaqiyatli ro'yxatdan o'tishi kerak."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "phone": "+998901112233",
            "password": "testpass123",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["phone"] == "+998901112233"
    assert data["role"] == "USER"
    assert "password_hash" not in data  # xavfsizlik: hash hech qachon chiqmasligi kerak


def test_register_duplicate_phone_fails(client):
    """Bir xil telefon raqam bilan ikkinchi marta ro'yxatdan o'tish rad etilishi kerak."""
    payload = {
        "full_name": "Test User",
        "phone": "+998901112233",
        "password": "testpass123",
    }
    client.post("/api/v1/auth/register", json=payload)

    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 409


def test_login_success(client):
    """To'g'ri telefon va parol bilan login muvaffaqiyatli bo'lishi kerak."""
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "phone": "+998901112233",
            "password": "testpass123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"phone": "+998901112233", "password": "testpass123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password_fails(client):
    """Noto'g'ri parol bilan login rad etilishi kerak."""
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "phone": "+998901112233",
            "password": "testpass123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"phone": "+998901112233", "password": "wrongpassword"},
    )

    assert response.status_code == 401


def test_get_me_requires_auth(client):
    """Token bo'lmasa /me endpoint rad etishi kerak."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 403


def test_get_me_with_valid_token(client):
    """To'g'ri token bilan /me joriy userni qaytarishi kerak."""
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "phone": "+998901112233",
            "password": "testpass123",
        },
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"phone": "+998901112233", "password": "testpass123"},
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["phone"] == "+998901112233"