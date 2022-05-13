from email import header
from app import main, schemas
from fastapi.testclient import TestClient
from typing import List, Optional

from app.tests.unit.auth.test_token import test_get_token
from app.tests.unit.auth import schemas_req
from pydantic import parse_obj_as

client = TestClient(main.app)

def test_read_song_200():
    token = test_get_token()
    headers = {"Authorization":"Bearer " + token["access_token"]}
    response = client.get("/songs/1", headers=headers)
    with open("time.txt", "a") as text_file:
        text_file.write(f"AUTH:{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 200
    assert parse_obj_as(schemas_req.SongLoadedLikeRequired, response.json())

def test_read_song_404_not_found():
    token = test_get_token()
    headers = {"Authorization":"Bearer " + token["access_token"]}
    response = client.get("/songs/0", headers=headers)
    with open("time.txt", "a") as text_file:
        text_file.write(f"AUTH:{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 404
    assert response.json() == { "detail": "Item not found" }

def test_read_song_422_validation_error():
    token = test_get_token()
    headers = {"Authorization":"Bearer " + token["access_token"]}
    response = client.get("/songs/abc", headers=headers)
    with open("time.txt", "a") as text_file:
        text_file.write(f"AUTH:{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 422

def test_read_songs_200():
    token = test_get_token()
    headers = {"Authorization":"Bearer " + token["access_token"]}
    response = client.get("/songs/", headers=headers)
    with open("time.txt", "a") as text_file:
        text_file.write(f"AUTH:{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 200
    assert parse_obj_as(List[schemas_req.SongLoadedLikeRequired], response.json())


# def test_read_artist_200():
#     response = client.get("/artists/1")
#     assert response.status_code == 200
#     assert parse_obj_as(schemas.ArtistLoaded, response.json())

# def test_read_artist_404_not_found():
#     response = client.get("/artists/0")
#     assert response.status_code == 404
#     assert response.json() == { "detail": "Item not found" }

# def test_read_artist_422_validation_error():
#     response = client.get("/artists/abc")
#     assert response.status_code == 422

# def test_read_artists_200():
#     response = client.get("/artists/")
#     assert response.status_code == 200
#     assert parse_obj_as(List[schemas.ArtistLoaded], response.json())

# def test_read_artists_422_validation_error():
#     response = client.get("/artists/", params={"skip": "abc"})
#     assert response.status_code == 422

# def test_like_artist_401_no_auth():
#     response = client.put("/artists/1/like")
#     assert response.status_code == 401
#     assert response.json() == { "detail": "Not authenticated" }
    