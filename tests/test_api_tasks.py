from datetime import datetime
from app.tasks import State
from tests.conftest import client
from random_object_id import generate


class TestCrudTask:

    def test_create_task(self, sign_up, prepare_task):
        assert prepare_task.status_code == 200
        assert prepare_task.json()['name'] == 'test task'

    def test_get_task(self, login_user, prepare_task):
        params = {'task_id': prepare_task.json()['_id']}
        response = client.get("/task/{id}/get", params=params, headers=login_user)
        assert prepare_task.status_code == 200
        assert response.json() == prepare_task.json()

    def test_update_task(self, login_user, prepare_task):
        params = {'task_id': prepare_task.json()['_id']}
        response = client.patch("/task/{id}/update", json={"name": "new name", "description": "new descriprion",
                                 "deadline": str(datetime.now()), "state": State.Finished}, params=params, headers=login_user)
        assert prepare_task.status_code == 200
        assert response.json() == {'message': 'Задача: test task обновлена'}

    def test_get_list_task(self, login_user, prepare_task):
        date_str = prepare_task.json()['created_at']
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        date = str(date_obj.date())
        params = {'date_from': date, 'date_to': date}
        response = client.get("/task/list/by-date", params=params, headers=login_user)
        assert response.status_code == 200
        assert response.json() == [prepare_task.json()]

    def test_delete_task(self, login_user, prepare_task):
        task_id = prepare_task.json()['_id']
        params = {'task_id': task_id}
        response = client.delete("/task/{id}/delete", params=params, headers=login_user)
        assert response.status_code == 200
        assert response.json() == {'message': 'Задача: test task удалена'}

    def test_get_not_found_task(self, login_user):
        params = {'task_id': generate()}
        response = client.get("/task/{id}/get", params=params, headers=login_user)
        assert response.status_code == 404

    def test_update_not_found_task(self, login_user):
        params = {'task_id': generate()}
        response = client.patch("/task/{id}/update", json={"name": "new name", "description": "new descriprion",
                                 "deadline": str(datetime.now()), "state": State.Finished}, params=params, headers=login_user)
        assert response.status_code == 404

    def test_get_list_not_found_task(self, login_user):
        date_obj = datetime.now()
        date = str(date_obj.date())
        params = {'date_from': date, 'date_to': date}
        response = client.get("/task/list/by-date", params=params, headers=login_user)
        assert response.status_code == 404

    def test_delete_not_found_task(self, login_user, delete_user):
        params = {'task_id': generate()}
        response = client.delete("/task/{id}/delete", params=params, headers=login_user)
        assert response.status_code == 404
