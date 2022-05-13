from app import main
from fastapi.testclient import TestClient


client = TestClient(main.app)

def get_super_token():
    response_token = client.post(
        "/auth/token",
        data = {"username":"test", "password":"test"},
    )
    return response_token.json()["access_token"]
