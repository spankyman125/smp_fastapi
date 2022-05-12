from email import header
from app import main, schemas
from fastapi.testclient import TestClient
from typing import List, Optional

from app.tests.unit.auth.test_token import test_get_token
from app.tests.unit.auth import schemas_req
from pydantic import parse_obj_as

client = TestClient(main.app)

def test_read_album_200():
    token = test_get_token()
    headers = {"Authorization":"Bearer " + token["access_token"]}
    response = client.get("/albums/1", headers=headers)
    with open("time.txt", "a") as text_file:
        text_file.write(f"AUTH:{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 200
    assert parse_obj_as(schemas_req.AlbumLoadedLikeRequired, response.json())

def test_read_album_404_not_found():
    token = test_get_token()
    headers = {"Authorization":"Bearer " + token["access_token"]}
    response = client.get("/albums/0", headers=headers)
    with open("time.txt", "a") as text_file:
        text_file.write(f"AUTH:{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 404
    assert response.json() == { "detail": "Item not found" }

def test_read_album_422_validation_error():
    token = test_get_token()
    headers = {"Authorization":"Bearer " + token["access_token"]}
    response = client.get("/albums/abc", headers=headers)
    with open("time.txt", "a") as text_file:
        text_file.write(f"AUTH:{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 422

def test_read_albums_200():
    token = test_get_token()
    headers = {"Authorization":"Bearer " + token["access_token"]}
    response = client.get("/albums/", headers=headers)
    with open("time.txt", "a") as text_file:
        text_file.write(f"AUTH:{response.url}: {response.elapsed.total_seconds()}\n")
    assert response.status_code == 200
    assert parse_obj_as(List[schemas_req.AlbumLoadedLikeRequired], response.json())

# def test_read_albums_422_validation_error():
#     response = client.get("/albums/", params={"skip": "abc"})
#     assert response.status_code == 422

# def test_like_album_401_no_auth():
#     response = client.put("/albums/1/like")
#     assert response.status_code == 401
#     assert response.json() == { "detail": "Not authenticated" }
