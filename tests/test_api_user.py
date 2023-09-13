import pytest

from tests.conftest import client


class TestSignUpPositive:

    def test_success_sign_up(self, sign_up):
        assert sign_up.status_code == 200
        assert sign_up.json() == {'data': 'Пользователь: api_test успешно зарегистрирован!'}

    def test_sign_up_has_user(self, sign_up, delete_user):
        assert sign_up.status_code == 400
        assert sign_up.json() == {'detail': [{'error': 'Пользователь с email: api_test@test.com уже существует'}]}


class TestSignUpNegative:
    @pytest.mark.parametrize('email, password',
                             [('api_test@test.com', "1234"),
                              ('api_test', '12345678')])
    def test_sign_up_with_short_password_or_invalid_email(self, email, password):
        response = client.post("/user/create",
                               json={"username": "api_test", "email": email, "password": password})
        assert response.status_code == 422
