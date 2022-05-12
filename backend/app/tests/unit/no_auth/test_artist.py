from app import main, schemas
from fastapi.testclient import TestClient
from pydantic import parse_obj_as
from typing import List, Optional


client = TestClient(main.app)

def test_read_artist_200():
    response = client.get("/artists/1")
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 200
    assert parse_obj_as(schemas.ArtistLoaded, response.json())

def test_read_artist_404_not_found():
    response = client.get("/artists/0")
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 404
    assert response.json() == { "detail": "Item not found" }

def test_read_artist_422_validation_error():
    response = client.get("/artists/abc")
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 422

def test_read_artists_200():
    response = client.get("/artists/")
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 200
    assert parse_obj_as(List[schemas.ArtistLoaded], response.json())

def test_read_artists_422_validation_error():
    response = client.get("/artists/", params={"skip": "abc"})
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 422

def test_like_artist_401_no_auth():
    response = client.put("/artists/1/like")
    with open("time.txt", "a") as text_file:
        text_file.write(f"{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 401
    assert response.json() == { "detail": "Not authenticated" }
    