import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="session")
def token():
    email = "user@test.com"

    client.post("/auth/register", json={
        "name": "user",
        "email": email,
        "password": "password123"
    })

    response = client.post("/auth/login", json={
        "email": email,
        "password": "password123"
    })

    return response.json()["access_token"]