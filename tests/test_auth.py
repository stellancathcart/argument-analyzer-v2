# tests/test_auth.py

# proves signup returns a bearer token

from tests.conftest import unique_email, create_user_and_token


def test_signup_creates_user_and_returns_token(client):
    payload = {
        "email": unique_email(),
        "password": "supersecret123",
        "full_name": "Test User",
    }

    response = client.post("/auth/signup", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_login_returns_token_for_valid_credentials(client):
    email = unique_email()
    password = "supersecret123"

    signup_payload = {
        "email": email,
        "password": password,
        "full_name": "Test User",
    }

    signup_response = client.post("/auth/signup", json=signup_payload)
    assert signup_response.status_code == 200

    login_payload = {
        "email": email,
        "password": password,
    }

    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_login_rejects_invalid_credentials(client):
    email = unique_email()
    password = "supersecret123"

    signup_payload = {
        "email": email,
        "password": password,
        "full_name": "Test User",
    }

    signup_response = client.post("/auth/signup", json=signup_payload)
    assert signup_response.status_code == 200

    bad_login_payload = {
        "email": email,
        "password": "wrongpassword",
    }

    response = client.post("/auth/login", json=bad_login_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_signup_rejects_duplicate_email(client):
    email = unique_email()

    payload = {
        "email": email,
        "password": "supersecret123",
        "full_name": "Test User",
    }

    first_response = client.post("/auth/signup", json=payload)
    assert first_response.status_code == 200

    second_response = client.post("/auth/signup", json=payload)
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "User already exists"


def test_me_returns_current_user_for_valid_token(client):
    payload, token = create_user_and_token(client)

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == payload["email"]
    assert body["full_name"] == payload["full_name"]
    assert body["is_active"] is True


def test_me_requires_token(client):
    response = client.get("/auth/me")
    assert response.status_code in (401, 403)