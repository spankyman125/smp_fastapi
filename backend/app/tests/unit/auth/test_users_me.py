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
async def test_read_user_me_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(schemas.UserAll, response.json())

@pytest.mark.anyio
async def test_update_user_about_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    json_about = {
        "name": "string",
        "surname": "string",
        "about": "string",
        "email": "string"
    }
    response = await client.post("/users/me", headers=headers, json=json_about)
    assert response.status_code == 200
    assert parse_obj_as(schemas.UserAbout, response.json())
    assert response.json() == json_about

@pytest.mark.anyio
async def test_read_user_me_artists_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/users/me/artists", headers=headers)
    assert response.status_code == 200
    assert (parse_obj_as(List[schemas_req.ArtistLikeRequired], response.json()) or not response.json())

@pytest.mark.anyio
async def test_read_user_me_albums_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/users/me/albums", headers=headers)
    assert response.status_code == 200
    assert (parse_obj_as(List[schemas_req.AlbumLikeRequired], response.json()) or not response.json())

@pytest.mark.anyio
async def test_read_user_me_songs_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/users/me/songs", headers=headers)
    assert response.status_code == 200
    assert (parse_obj_as(List[schemas_req.SongLoadedLikeRequired], response.json()) or not response.json())