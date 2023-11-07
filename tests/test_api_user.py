import pytest
from httpx import AsyncClient
from tests.users import test_user


class TestSignUp:

    @pytest.mark.anyio
    async def test_success_sign_up(self, client: AsyncClient):
        response = await client.post("/user/create", json=test_user)
        assert response.status_code == 200
        assert response.json() == {'message': 'Пользователь: api_test успешно зарегистрирован!'}

    @pytest.mark.anyio
    async def test_sign_up_has_user(self, client: AsyncClient, delete_user):
        response = await client.post("/user/create", json=test_user)
        assert response.status_code == 400
        assert response.json() == {'detail': [{'error': 'Пользователь с email: api_test@test.com уже существует'}]}

    @pytest.mark.anyio
    @pytest.mark.parametrize('email, password',
                             [('api_test@test.com', "1234"),
                              ('api_test', '12345678')])
    async def test_sign_up_with_short_password_or_invalid_email(self, client: AsyncClient, email, password):
        response = await client.post("/user/create",
                                     json={"username": "api_test", "email": email, "password": password})
        assert response.status_code == 422
