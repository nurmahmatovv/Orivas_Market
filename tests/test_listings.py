def register_and_login(client, phone="+998901112233"):
    client.post(
        "/api/v1/auth/register",
        json={"full_name": "Test Seller", "phone": phone, "password": "testpass123"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"phone": phone, "password": "testpass123"},
    )
    return response.json()["access_token"]


def create_category(client):
    response = client.post(
        "/api/v1/categories",
        json={"name": "Kvartira", "slug": "apartment"},
    )
    return response.json()["id"]


def test_create_listing_requires_auth(client):
    response = client.post(
        "/api/v1/listings",
        json={
            "title": "Test",
            "price": 100000,
            "listing_type": "RENT",
            "category_id": "00000000-0000-0000-0000-000000000000",
            "region_name": "Toshkent",
        },
    )
    assert response.status_code == 403


def test_create_listing_success(client):
    token = register_and_login(client)
    category_id = create_category(client)

    response = client.post(
        "/api/v1/listings",
        json={
            "title": "2 xonali kvartira",
            "price": 300000,
            "currency": "UZS",
            "listing_type": "RENT",
            "category_id": category_id,
            "region_name": "Toshkent",
            "district_name": "Sergeli",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "2 xonali kvartira"
    assert data["status"] == "PENDING_MODERATION"


def test_search_hides_pending_listings(client):
    token = register_and_login(client)
    category_id = create_category(client)

    client.post(
        "/api/v1/listings",
        json={
            "title": "Test listing",
            "price": 100000,
            "listing_type": "SALE",
            "category_id": category_id,
            "region_name": "Toshkent",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get("/api/v1/listings")

    assert response.status_code == 200
    assert response.json()["total"] == 0


def test_search_by_region_includes_district(client, admin_token):
    """Toshkent bo'yicha qidiruv Sergeli listingini ham topishi kerak (hierarchik qidiruv)."""
    token = register_and_login(client)
    category_id = create_category(client)

    create_response = client.post(
        "/api/v1/listings",
        json={
            "title": "Sergeli kvartira",
            "price": 300000,
            "listing_type": "RENT",
            "category_id": category_id,
            "region_name": "Toshkent",
            "district_name": "Sergeli",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    listing_id = create_response.json()["id"]

    # Admin sifatida tasdiqlaymiz
    client.patch(
        f"/api/v1/admin/listings/{listing_id}/approve",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    # Toshkent (region) bo'yicha qidiramiz
    locations_response = client.get("/api/v1/locations")
    toshkent_id = next(
        loc["id"] for loc in locations_response.json() if loc["name"] == "Toshkent"
    )

    search_response = client.get(f"/api/v1/listings?location_id={toshkent_id}")

    assert search_response.status_code == 200
    assert search_response.json()["total"] == 1
    assert search_response.json()["items"][0]["title"] == "Sergeli kvartira"


def test_search_finds_listing_by_exact_district(client, admin_token):
    """Sergeli bo'yicha qidiruv aynan Sergeli listingini topishi kerak."""
    token = register_and_login(client)
    category_id = create_category(client)

    create_response = client.post(
        "/api/v1/listings",
        json={
            "title": "Sergeli kvartira",
            "price": 300000,
            "listing_type": "RENT",
            "category_id": category_id,
            "region_name": "Toshkent",
            "district_name": "Sergeli",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    listing_id = create_response.json()["id"]

    client.patch(
        f"/api/v1/admin/listings/{listing_id}/approve",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    locations_response = client.get("/api/v1/locations")
    sergeli_id = next(
        loc["id"] for loc in locations_response.json() if loc["name"] == "Sergeli"
    )

    search_response = client.get(f"/api/v1/listings?location_id={sergeli_id}")

    assert search_response.status_code == 200
    assert search_response.json()["total"] == 1