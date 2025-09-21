from fastapi import FastAPI, HTTPException, Header, Query, Request
from fastapi.responses import JSONResponse
import uvicorn
import time
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="IONOS Billing API Mock")

# In-memory storage for rate limiting
# Key: client_ip, Value: list of timestamps
rate_limit_store = {}

# Constants
MOCK_TOKEN = "valid-token-123"
RATE_LIMIT_WINDOW = 1.0  # 1 second
RATE_LIMIT_MAX_REQUESTS = 2

def check_rate_limit(request: Request):
    client_ip = request.client.host
    now = time.time()
    
    if client_ip not in rate_limit_store:
        rate_limit_store[client_ip] = []
    
    # Clean up old timestamps
    rate_limit_store[client_ip] = [ts for ts in rate_limit_store[client_ip] if now - ts < RATE_LIMIT_WINDOW]
    
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Too Many Requests")
    
    rate_limit_store[client_ip].append(now)

def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized: No token provided")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token format")
        
    token = authorization.split(" ")[1]
    if token != MOCK_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

@app.get("/invoices")
async def get_invoices(authorization: Optional[str] = Header(None)):
    verify_token(authorization)
    return {
        "items": [
            {
                "id": "inv-001",
                "date": "2023-10-01T12:00:00Z",
                "amount": 120.50,
                "currency": "EUR",
                "status": "PAID"
            },
            {
                "id": "inv-002",
                "date": "2023-11-01T12:00:00Z",
                "amount": 135.00,
                "currency": "EUR",
                "status": "PENDING"
            }
        ],
        "meta": {
            "total_count": 2
        }
    }

@app.get("/products")
async def get_products(authorization: Optional[str] = Header(None)):
    verify_token(authorization)
    return {
        "products": [
            {"id": "p1", "name": "Compute Engine M", "price_per_hour": 0.05},
            {"id": "p2", "name": "Storage 100GB", "price_per_gb": 0.02}
        ]
    }

@app.get("/utilization")
async def get_utilization(
    request: Request,
    authorization: Optional[str] = Header(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    verify_token(authorization)
    check_rate_limit(request)
    
    # Edge case: Invalid date format simulation
    if start_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    return {
        "status": "OK",
        "utilization_data": [
            {"resource_id": "res-1", "usage_hours": 240, "cost": 12.00},
            {"resource_id": "res-2", "usage_hours": 720, "cost": 36.00}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
