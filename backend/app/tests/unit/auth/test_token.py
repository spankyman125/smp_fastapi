from app import main, schemas
from fastapi.testclient import TestClient
from pydantic import parse_obj_as


client = TestClient(main.app)

def test_get_token():
    client.post(
        "/users/",
        json = {"username":"test", "password":"test"},
    )
    response_token = client.post(
        "/auth/token",
        data = {"username":"test", "password":"test"},
    )
    # assert response_token.status_code == 200
    # assert parse_obj_as(schemas.Token, response_token.json())
    return response_token.json()

# def auth_decorator(function):
#     def wrap_function(*args, **kwargs):
#         token = get_token()
#         kwargs['headers'] = {"Authorization":"Bearer "+ token["access_token"]}
#         return function(*args, **kwargs)
#     return wrap_function
