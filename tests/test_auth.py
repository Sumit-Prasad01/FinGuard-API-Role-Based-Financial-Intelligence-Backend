import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register():
    unique_email = f"user_{uuid.uuid4()}@test.com"

    response = client.post("/auth/register", json={
        "name": "user",
        "email": unique_email,
        "password": "password123"
    })
    assert response.status_code in [200, 201]
    data = response.json()
    assert "email" in data


def test_login():
    response = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_token():
    login = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "password123"
    })
    refresh_token = login.json()["refresh_token"]

    response = client.post("/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert response.status_code == 200
    assert "access_token" in response.json()