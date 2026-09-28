def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OPERATIONAL"
    assert data["ps_id"] == "SIH26017"
    assert data["team"] == "NEXORA_TAU"

def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

def test_auth_me_success(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "officer@nexora.gov.in"
    assert data["role"] == "Officer"

def test_auth_invalid_token(client):
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid.token.value"})
    assert response.status_code == 401
    assert "Invalid or expired token" in response.json()["detail"]
