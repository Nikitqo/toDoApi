import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.user import delete_user_by_email


client = TestClient(app)


@pytest.fixture(scope='function')
def sign_up():
    response = client.post("/user/create",
                           json={"username": "api_test", "email": 'api_test@test.com', "password": "12345678"})
    return response


@pytest.fixture(scope='function')
def delete_user():
    email = 'api_test@test.com'
    yield
    delete_user_by_email(email)
