import pytest
from fastapi.testclient import TestClient
from app.api import app


client = TestClient(app)


def get_auth_headers(credentials):
    response = client.post("/user/login", data=credentials)
    print(credentials)
    token = response.json()
    print(token)
    return {'authorization': f'{token["token_type"]} {token["access_token"]}'}


@pytest.fixture(scope='function')
def sign_up():
    response = client.post("/user/create",
                           json={"username": "api_test", "email": 'api_test@test.com', "password": "12345678"})
    return response


@pytest.fixture(scope='function')
def delete_user():
    credentials = {'username': 'api_test@test.com', 'password': '12345678'}
    headers = get_auth_headers(credentials)
    params = {'email': credentials['username']}
    yield
    client.delete("/user/delete", params=params, headers=headers)