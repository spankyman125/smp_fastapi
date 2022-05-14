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
async def test_read_tags_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/tags/", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(List[schemas.Tag], response.json())

@pytest.mark.anyio
async def test_read_songs_by_tags_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = await client.get("/tags/songs", headers=headers, params={"tags":"metal"})
    assert response.status_code == 200
    assert parse_obj_as(List[schemas_req.SongTaggedLikeRequired], response.json())
