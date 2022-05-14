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

client = TestClient(app=main.app)
ACCESS_TOKEN = token.get_super_token()

def home_random_albums_200():
    headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
    response = client.get("/home/random/albums", headers=headers)
    assert response.status_code == 200
    assert parse_obj_as(List[schemas_req.AlbumLikeRequired], response.json())


