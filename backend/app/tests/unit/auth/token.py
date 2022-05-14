from app import main, schemas
from fastapi.testclient import TestClient
from pydantic import parse_obj_as

client = TestClient(main.app)

def get_super_token():
    client.post(
        "/users/",
        json = {"username":"test", "password":"test"},
    )
    response_token = client.post(
        "/auth/token",
        data = {"username":"test", "password":"test"},
    )
    return response_token.json()["access_token"]
