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

def test_openapi_security_scheme(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    security_schemes = schema.get("components", {}).get("securitySchemes", {})
    assert "HTTPBearer" in security_schemes
    assert security_schemes["HTTPBearer"]["type"] == "http"
    assert security_schemes["HTTPBearer"]["scheme"] == "bearer"
    assert "OAuth2PasswordBearer" not in security_schemes
    # Verify protected route has HTTPBearer security requirement
    me_security = schema["paths"]["/api/auth/me"]["get"].get("security", [])
    assert {"HTTPBearer": []} in me_security

