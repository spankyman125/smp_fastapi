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
async def test_home_random_albums_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/home/random/albums", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(List[schemas_req.AlbumLikeRequired], response.json())

@pytest.mark.anyio
async def test_home_random_songs_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/home/random/songs", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(List[schemas_req.SongLoadedLikeRequired], response.json())

@pytest.mark.anyio
async def test_home_random_artists_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/home/random/artists", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(List[schemas_req.ArtistLikeRequired], response.json())

@pytest.mark.anyio
async def test_home_last_album_releases():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/home/last-album-releases", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(List[schemas_req.AlbumLikeRequired], response.json())
