from datetime import datetime
import pytest
from httpx import AsyncClient
from app.api import app
from tests.users import test_user


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope='session')
async def get_auth_headers(client):
    credentials = {'username': test_user['email'], 'password': test_user['password']}
    response = await client.post("/user/login", data=credentials)
    token = response.json()
    return {'authorization': f'{token["token_type"]} {token["access_token"]}'}


@pytest.fixture(scope='session')
async def delete_user(client: AsyncClient, get_auth_headers: dict):
    params = {'email': test_user['email']}
    yield
    await client.delete("/user/delete", params=params, headers=get_auth_headers)


@pytest.fixture(scope='session')
async def create_user(client: AsyncClient):
    await client.post("/user/create", json=test_user)


@pytest.fixture
async def prepare_task(client: AsyncClient, get_auth_headers: dict):
    response = await client.post("/task/create",
                           json={"name": "test task", "description": "test descriprion",
                                 "deadline": str
                                 (datetime.now())}, headers=get_auth_headers)
    params = {'task_id': response.json()['_id']}
    yield response
    await client.delete("/task/{id}/delete", params=params, headers=get_auth_headers)
