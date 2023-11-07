from datetime import datetime
import pytest
from httpx import AsyncClient
from random_object_id import generate
from app.tasks import State


class TestCrudTask:

    @pytest.mark.anyio
    async def test_create_task(self, create_user, prepare_task):
        # response = await client.post("/task/create",
        #                   json={"name": "test task", "description": "test descriprion",
        #                         "deadline": str(datetime.now())}, headers=get_auth_headers)
        assert prepare_task.status_code == 200
        assert prepare_task.json()['name'] == 'test task'

    @pytest.mark.anyio
    async def test_get_task(self, client: AsyncClient, get_auth_headers: dict, prepare_task):
        params = {'task_id': prepare_task.json()['_id']}
        response = await client.get("/task/{id}/get", params=params, headers=get_auth_headers)
        assert response.status_code == 200
        assert response.json() == prepare_task.json()

    @pytest.mark.anyio
    async def test_update_task(self, client: AsyncClient, get_auth_headers: dict, prepare_task):
        params = {'task_id': prepare_task.json()['_id']}
        response = await client.patch("/task/{id}/update", json={"name": "new name", "description": "new descriprion",
                                 "deadline": str(datetime.now()), "state": State.Finished}, params=params, headers=get_auth_headers)
        assert prepare_task.status_code == 200
        assert response.json() == {'message': 'Задача: test task обновлена'}

    @pytest.mark.anyio
    async def test_get_list_task(self, client: AsyncClient, get_auth_headers: dict, prepare_task):
        date_str = prepare_task.json()['created_at']
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        date = str(date_obj.date())
        params = {'date_from': date, 'date_to': date}
        response = await client.get("/task/list/by-date", params=params, headers=get_auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

    @pytest.mark.anyio
    async def test_delete_task(self, client: AsyncClient, get_auth_headers: dict, prepare_task):
        task_id = prepare_task.json()['_id']
        params = {'task_id': task_id}
        response = await client.delete("/task/{id}/delete", params=params, headers=get_auth_headers)
        assert response.status_code == 200
        assert response.json() == {'message': 'Задача: test task удалена'}

    @pytest.mark.anyio
    async def test_get_not_found_task(self, client: AsyncClient, get_auth_headers: dict):
        params = {'task_id': generate()}
        print(params)
        response = await client.get("/task/{id}/get", params=params, headers=get_auth_headers)
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_update_not_found_task(self, client: AsyncClient, get_auth_headers: dict):
        params = {'task_id': generate()}
        response = await client.patch("/task/{id}/update", json={"name": "new name", "description": "new descriprion",
                                 "deadline": str(datetime.now()), "state": State.Finished}, params=params, headers=get_auth_headers)
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_list_not_found_task(self, client: AsyncClient, get_auth_headers: dict):
        date_obj = datetime.now()
        date = str(date_obj.date())
        params = {'date_from': date, 'date_to': date}
        response = await client.get("/task/list/by-date", params=params, headers=get_auth_headers)
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_delete_not_found_task(self, client: AsyncClient, get_auth_headers: dict, delete_user):
        params = {'task_id': generate()}
        response = await client.delete("/task/{id}/delete", params=params, headers=get_auth_headers)
        assert response.status_code == 404
