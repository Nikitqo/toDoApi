from typing import List, Annotated
from fastapi import APIRouter, Depends
from app.tasks import CreateTask, UpdateTask, Task, add_new_task
from app.user import get_current_user

router = APIRouter(
    prefix='/task',
    tags=['Task']
)

Auth = Annotated[dict, Depends(get_current_user)]


@router.post("/create")
def create_task(task: CreateTask, auth: Auth):
    user_id = auth['_id']
    return add_new_task(task, user_id)

# пример объекта из auth:
# {'_id': ObjectId('64c3c43a5362fa9473b6ab79'), 'username': 'string', 'password_hash':
# '$2b$12$L7Yu92/k8u4w4TIeHZyiseLi668jx/UxmAD79tgKAGItB41JHzn.u', 'email': 'usertest@example.com'}

# @router.patch("/{id}")
# def update_task(id, update: UpdateTask):
#     return {"info": update}
#
#
# @router.get("/list")
# def get_list(from_date, to_date):
#     return {List[Task]}
#
#
# @router.get("/{task_id}")
# def get_task(task_id):
#     return {"task_id": task_id}
#
#
# @router.delete("/{task_id}")
# def delete_task(task_id):
#     return {"message": f'Задача: {Task.name} - удалена'}
