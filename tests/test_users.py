from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_admin_token():
    # Ensure admin user exists in DB
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "admin123"
    })
    return response.json()["access_token"]


def test_get_all_users():
    token = get_admin_token(token)

    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id():
    token = get_admin_token()

    response = client.get(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [200, 404]