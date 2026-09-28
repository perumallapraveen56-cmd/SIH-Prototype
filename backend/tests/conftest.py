import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def auth_headers(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "officer@nexora.gov.in", "password": "Officer@123"}
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
