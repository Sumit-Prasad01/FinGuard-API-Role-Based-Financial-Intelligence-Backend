from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token():
    response = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]


def test_create_record():
    token = get_token()

    response = client.post(
        "/records/",
        json={
            "amount": 1000,
            "type": "expense",
            "category": "food",
            "date": "2026-04-04T10:00:00",
            "notes": "test"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["amount"] == 1000


def test_get_records():
    token = get_token()

    response = client.get(
        "/records/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_record():
    token = get_token()

    create = client.post(
        "/records/",
        json={
            "amount": 500,
            "type": "expense",
            "category": "food",
            "date": "2026-04-04T10:00:00"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    record_id = create.json()["id"]

    response = client.put(
        f"/records/{record_id}",
        json={"amount": 800},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_delete_record():
    token = get_token()

    create = client.post(
        "/records/",
        json={
            "amount": 300,
            "type": "expense",
            "category": "food",
            "date": "2026-04-04T10:00:00"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    record_id = create.json()["id"]

    response = client.delete(
        f"/records/{record_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200