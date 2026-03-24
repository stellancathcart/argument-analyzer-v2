# tests/conftest.py

import uuid
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db import Base, engine


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def unique_email() -> str:
    return f"test-{uuid.uuid4().hex[:8]}@example.com"


def create_user_and_token(client):
    payload = {
        "email": unique_email(),
        "password": "supersecret123",
        "full_name": "Test User",
    }

    response = client.post("/auth/signup", json=payload)
    assert response.status_code == 200

    token = response.json()["access_token"]
    return payload, token