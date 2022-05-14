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
async def test_read_album_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/albums/1", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(schemas_req.AlbumLoadedLikeRequired, response.json())

@pytest.mark.anyio
async def test_read_album_404_not_found():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/albums/0", headers=headers)
    assert response.status_code == 404
    assert response.json() == { "detail": "Item not found" }

@pytest.mark.anyio
async def test_read_album_422_validation_error():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/albums/abc", headers=headers)
    assert response.status_code == 422

@pytest.mark.anyio
async def test_read_albums_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/albums/", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(List[schemas_req.AlbumLoadedLikeRequired], response.json())

@pytest.mark.anyio 
async def test_read_albums_422_validation_error():
    response = await client.get("/albums/", params={"skip": "abc"})
    assert response.status_code == 422

@pytest.mark.anyio
async def test_like_albums_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.put("/albums/1/like", headers=headers)
    assert response.status_code == 200

