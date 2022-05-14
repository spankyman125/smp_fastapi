from app import main, schemas
from fastapi.testclient import TestClient
from httpx import AsyncClient
from typing import List, Optional
from app.tests.unit.auth import schemas_req
from pydantic import parse_obj_as
from app.tests.unit.auth import token 

ACCESS_TOKEN = token.get_super_token()

client = TestClient(app=main.app, base_url="http://localhost")

# def test_search_songs_200():
#     headers = {"Authorization":"Bearer " + ACCESS_TOKEN}
#     response = client.get("/search/songs", headers=headers, params={"name":"song"})
#     assert response.status_code == 200
#     assert parse_obj_as(List[schemas_req.SongLoadedLikeRequired], response.json())
