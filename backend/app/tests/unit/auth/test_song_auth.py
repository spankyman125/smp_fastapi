from email import header
from app import main, schemas
from fastapi.testclient import TestClient
from typing import List, Optional

from app.tests.unit.auth.test_token import test_get_token
from app.tests.unit.auth import schemas_req
from pydantic import parse_obj_as

from app.tests.unit.auth import token 
import pytest
from httpx import AsyncClient

client = AsyncClient(app=main.app, base_url="http://localhost")
ACCESS_TOKEN = token.get_super_token()

@pytest.mark.anyio
async def test_read_song_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/songs/1", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(schemas_req.SongLoadedLikeRequired, response.json())

@pytest.mark.anyio
async def test_read_song_404_not_found():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/songs/0", headers=headers)
    assert response.status_code == 404
    assert response.json() == { "detail": "Item not found" }

@pytest.mark.anyio
async def test_read_song_422_validation_error():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/songs/abc", headers=headers)
    assert response.status_code == 422

@pytest.mark.anyio
async def test_read_songs_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/songs/", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(List[schemas_req.SongLoadedLikeRequired], response.json())

@pytest.mark.anyio
async def test_like_song_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.put("/songs/1/like", headers=headers)
    assert response.status_code == 200

# @pytest.mark.anyio
# async def test_read_artist_200():
#     response = await client.get("/artists/1")
#     assert response.status_code == 200
#     assert parse_obj_as(schemas.ArtistLoaded, response.json())

# @pytest.mark.anyio
# async def test_read_artist_404_not_found():
#     response = await client.get("/artists/0")
#     assert response.status_code == 404
#     assert response.json() == { "detail": "Item not found" }

# @pytest.mark.anyio
# async def test_read_artist_422_validation_error():
#     response = await client.get("/artists/abc")
#     assert response.status_code == 422

# @pytest.mark.anyio
# async def test_read_artists_200():
#     response = await client.get("/artists/")
#     assert response.status_code == 200
#     assert parse_obj_as(List[schemas.ArtistLoaded], response.json())

# @pytest.mark.anyio
# async def test_read_artists_422_validation_error():
#     response = await client.get("/artists/", params={"skip": "abc"})
#     assert response.status_code == 422

# @pytest.mark.anyio
# async def test_like_artist_401_no_auth():
#     response = await client.put("/artists/1/like")
#     assert response.status_code == 401
#     assert response.json() == { "detail": "Not authenticated" }
    