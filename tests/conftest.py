import pytest
import requests
import os
import shutil
import time
import subprocess

# Default to the local mock server
BASE_URL = "http://localhost:8000"
VALID_TOKEN = "valid-token-123"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def auth_headers():
    return {"Authorization": f"Bearer {VALID_TOKEN}"}

@pytest.fixture(scope="session", autouse=True)
def ensure_server_running():
    """
    Ideally, we would start the mock server here if it's not running.
    For this simple task, we'll assume the user checks the README or we start it separately.
    However, we can try to do a health check.
    """
    try:
        # Check if server is reachable
        requests.get(f"{BASE_URL}/docs", timeout=1)
    except requests.exceptions.ConnectionError:
        print("\nWARNING: Mock server is not running on localhost:8000. Tests may fail.")
        print("Please run `python mock_server.py` in a separate terminal.\n")
