from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from app.api import app
from tests.users import test_user

client = TestClient(app)


def get_auth_headers():
    credentials = {'username': test_user['email'], 'password': test_user['password']}
    response = client.post("/user/login", data=credentials)
    token = response.json()
    return {'authorization': f'{token["token_type"]} {token["access_token"]}'}


@pytest.fixture(scope='function')
def sign_up():
    response = client.post("/user/create",
                           json=test_user)
    return response


@pytest.fixture(scope='function')
def delete_user():
    headers = get_auth_headers()
    params = {'email': test_user['email']}
    yield
    client.delete("/user/delete", params=params, headers=headers)


@pytest.fixture(scope='function')
def login_user():
    credentials = {'username': test_user['email'], 'password': test_user['password']}
    response = client.post("/user/login", data=credentials)
    token = response.json()
    return {'authorization': f'{token["token_type"]} {token["access_token"]}'}


@pytest.fixture(scope='function')
def prepare_task():
    headers = get_auth_headers()
    response = client.post("/task/create",
                           json={"name": "test task", "description": "test descriprion",
                                 "deadline": str(datetime.now())}, headers=headers)
    yield response
    params = {'task_id': response.json()['_id']}
    client.delete("/task/{id}/delete", params=params, headers=headers)
