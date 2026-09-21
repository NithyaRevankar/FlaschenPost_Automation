#Public Billing API Test Suite

This project contains an automated test suite for verifying the  Public Billing API. 
Since direct access to the live API requires business credentials, this suite uses a **local mock server** to simulate the API's behavior.

## Prerequisites

- Python 3.8+
- `pip`

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Start the Mock Server
The tests run against a local mock server. You must start it before running the tests.

```bash
python mock_server.py
```
The server will start at `http://0.0.0.0:8000`.

### 2. Run the Tests
Open a new terminal window (keep the server running in the first one) and run:

```bash
pytest
```

To see detailed output:
```bash
pytest -v
```

## Test Structure

- `tests/test_auth.py`: Verifies valid and invalid token handling.
- `tests/test_structure.py`: Checks response schemas for invoices and products.
- `tests/test_edge_cases.py`: Tests rate limiting (2 rq/s) and invalid parameters.

## Expanding the Suite for Real API
To run these tests against the real IONOS API:
1.  Update the `BASE_URL` in `tests/conftest.py` to point to the real API endpoint.
2.  Update the `VALID_TOKEN` in `tests/conftest.py` with your real Bearer token.
