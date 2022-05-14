from app import main, schemas
from fastapi.testclient import TestClient
from httpx import AsyncClient
from typing import List, Optional
from app.tests.unit.auth import schemas_req
from pydantic import parse_obj_as
from app.tests.unit.auth import token 
import pytest

ACCESS_TOKEN = token.get_super_token()

client = AsyncClient(app=main.app, base_url="http://localhost")

@pytest.mark.anyio
async def test_read_user_username_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/users/test", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(schemas.UserAll, response.json())

@pytest.mark.anyio
async def test_read_user_username_artists_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/users/test/artists", headers=headers)
    assert response.status_code == 200
    assert (parse_obj_as(List[schemas_req.ArtistLikeRequired], response.json()) or not response.json())

@pytest.mark.anyio
async def test_read_user_username_albums_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/users/test/albums", headers=headers)
    assert response.status_code == 200
    assert (parse_obj_as(List[schemas_req.AlbumLikeRequired], response.json()) or not response.json())

@pytest.mark.anyio
async def test_read_user_username_songs_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/users/test/songs", headers=headers)
    assert response.status_code == 200
    assert (parse_obj_as(List[schemas_req.SongLoadedLikeRequired], response.json()) or not response.json())