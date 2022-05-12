from email import header
from app import main, schemas
from fastapi.testclient import TestClient
from pydantic import parse_obj_as
from typing import List, Optional


client = TestClient(main.app)

def test_user_create_200_or_400():
    response = client.post(
        "/users/",
        json = {"username":"test", "password":"test"},
    )
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert (response.status_code == 200 or response.status_code == 400) 
    if response.status_code == 200:
        assert parse_obj_as(schemas.UserAll, response.json())
    elif response.status_code == 400:
        assert response.json() == { "detail": "Username already registered"}

def test_user_create_422_validation_error():
    response = client.post(
        "/users/",
        json = {"username":"!@#$%^&*()", "password":"test"},
    )
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 422 