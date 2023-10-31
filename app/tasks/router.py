from typing import Annotated
from fastapi import APIRouter, Depends
from app.tasks import CreateTask, UpdateTask, Task, add_new_task, \
    delete_task_by_id, update_task_by_id, get_task_by_id, get_list_task_by_date, MessageResponse
from app.user import get_current_user

router = APIRouter(
    prefix='/task',
    tags=['Task']
)

Auth = Annotated[dict, Depends(get_current_user)]


@router.post("/create", response_model=Task)
async def create_task(task: CreateTask, auth: Auth):
    return await add_new_task(task, auth)


@router.patch("/{id}/update", response_model=MessageResponse)
async def update_task(task_id, update_data: UpdateTask, auth: Auth):
    return await update_task_by_id(task_id, update_data, auth)


@router.get("/{id}/get", response_model=Task)
async def get_task(task_id, auth: Auth):
    return await get_task_by_id(task_id, auth)


@router.get("/list/by-date", response_model=list[Task])
async def get_list_task(date_from, date_to, auth: Auth):
    return await get_list_task_by_date(date_from, date_to, auth)


@router.delete("/{id}/delete", response_model=MessageResponse)
async def delete_task(task_id, auth: Auth):
    return await delete_task_by_id(task_id, auth)
