import pytest
import requests
import time

def test_invalid_date_param(base_url, auth_headers):
    """Test that sending an invalid date format returns a 400 Bad Request."""
    params = {"start_date": "invalid-date-format"}
    response = requests.get(f"{base_url}/utilization", headers=auth_headers, params=params)
    assert response.status_code == 400
    assert "Invalid date format" in response.json()["detail"]

def test_rate_limit_utilization(base_url, auth_headers):
    """
    Test rate limiting on the utilization endpoint.
    The mock server allows 2 requests per second.
    """
    # Reset limit logic by waiting a bit if needed (mock logic is simple time-window)
    time.sleep(1.1)
    
    # Send 2 allowed requests
    r1 = requests.get(f"{base_url}/utilization", headers=auth_headers)
    assert r1.status_code == 200
    
    r2 = requests.get(f"{base_url}/utilization", headers=auth_headers)
    assert r2.status_code == 200
    
    # Send 3rd request immediately - should fail
    r3 = requests.get(f"{base_url}/utilization", headers=auth_headers)
    assert r3.status_code == 429
    assert "Too Many Requests" in r3.json()["detail"]
