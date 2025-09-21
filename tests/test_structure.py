import pytest
import requests

def test_invoices_structure(base_url, auth_headers):
    """Test that the invoices endpoint returns the expected JSON structure."""
    response = requests.get(f"{base_url}/invoices", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    assert "items" in data
    assert "meta" in data
    assert isinstance(data["items"], list)
    
    # Check structure of the first invoice
    if len(data["items"]) > 0:
        inv = data["items"][0]
        assert "id" in inv
        assert "date" in inv
        assert "amount" in inv
        assert "currency" in inv
        assert isinstance(inv["amount"], (int, float))

def test_products_structure(base_url, auth_headers):
    """Test that the products endpoint returns the expected JSON structure."""
    response = requests.get(f"{base_url}/products", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    assert "products" in data
    assert isinstance(data["products"], list)
    
    if len(data["products"]) > 0:
        prod = data["products"][0]
        assert "id" in prod
        assert "name" in prod
        assert "price_per_hour" in prod or "price_per_gb" in prod
