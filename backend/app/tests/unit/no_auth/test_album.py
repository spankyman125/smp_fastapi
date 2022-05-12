from app import main, schemas
from fastapi.testclient import TestClient
from pydantic import parse_obj_as
from typing import List, Optional


client = TestClient(main.app)

def test_read_album_200():
    response = client.get("/albums/1")
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 200
    assert parse_obj_as(schemas.AlbumLoaded, response.json())

def test_read_album_404_not_found():
    response = client.get("/albums/0")
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 404
    assert response.json() == { "detail": "Item not found" }

def test_read_album_422_validation_error():
    response = client.get("/albums/abc")
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 422

def test_read_albums_200():
    response = client.get("/albums/")
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 200
    assert parse_obj_as(List[schemas.AlbumLoaded], response.json())

def test_read_albums_422_validation_error():
    response = client.get("/albums/", params={"skip": "abc"})
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 422

def test_like_album_401_no_auth():
    response = client.put("/albums/1/like")
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 401
    assert response.json() == { "detail": "Not authenticated" }
    