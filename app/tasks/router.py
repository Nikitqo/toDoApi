from typing import List, Annotated
from fastapi import APIRouter, Depends
from app.tasks import CreateTask, UpdateTask, Task, TaskList, add_new_task, \
    delete_task_by_id, update_task_by_id, get_task_by_id, get_list_task_by_date
from app.user import get_current_user

router = APIRouter(
    prefix='/task',
    tags=['Task']
)

Auth = Annotated[dict, Depends(get_current_user)]


@router.post("/create")
def create_task(task: CreateTask, auth: Auth):
    return add_new_task(task, auth)


@router.patch("/{task_id}/update")
def update_task(task_id, update_data: UpdateTask, auth: Auth):
    return update_task_by_id(task_id, update_data, auth)


@router.delete("/{_id}/delete")
def delete_task(task_id, auth: Auth):
    return delete_task_by_id(task_id, auth)


@router.get("/{task_id}/get", response_model=Task)
def get_task(task_id, auth: Auth):
    return get_task_by_id(task_id, auth)


@router.get("/list/by-date")
def get_list_task(from_date, to_date, auth: Auth):
    return get_list_task_by_date(from_date, to_date, auth)

# пример объекта из auth:
# {'_id': ObjectId('64c3c43a5362fa9473b6ab79'), 'username': 'string', 'password_hash':
# '$2b$12$L7Yu92/k8u4w4TIeHZyiseLi668jx/UxmAD79tgKAGItB41JHzn.u', 'email': 'usertest@example.com'}
