from tests.conftest import client


class TestSignUpPositive:

    def test_success_sign_up(self, sign_up):
        assert sign_up.status_code == 200
        assert sign_up.json() == {'data': 'Пользователь: api_test успешно зарегистрирован!'}

    def test_sign_up_has_user(self, sign_up, delete_user):
        assert sign_up.status_code == 400
        assert sign_up.json() == {'detail': [{'error': 'Пользователь с email: api_test@test.com уже существует'}]}


class TestSignUpNegative:

    def test_sign_up_short_password(self):
        response_short_password = client.post("/user/create",
                               json={"username": "api_test", "email": "api_test@test.com", "password": "1234"})
        assert response_short_password.status_code == 422

    def test_sign_up_not_valid_email(self):
        response = client.post("/user/create",
                               json={"username": "api_test", "email": "api_test", "password": "12345678"})
        assert response.status_code == 422
