import pytest
import requests

def test_auth_success(base_url, auth_headers):
    """Test that valid credentials return a 200 OK response."""
    response = requests.get(f"{base_url}/products", headers=auth_headers)
    assert response.status_code == 200

def test_auth_missing_token(base_url):
    """Test that missing authentication header returns 401."""
    response = requests.get(f"{base_url}/products")
    assert response.status_code == 401
    assert "detail" in response.json()

def test_auth_invalid_token(base_url):
    """Test that an invalid token returns 401."""
    headers = {"Authorization": "Bearer invalid-token"}
    response = requests.get(f"{base_url}/products", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized: Invalid token"

def test_auth_malformed_header(base_url):
    """Test that a malformed Authorization header returns 401."""
    headers = {"Authorization": "Basic 12345"}
    response = requests.get(f"{base_url}/products", headers=headers)
    assert response.status_code == 401
