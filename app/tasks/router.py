from typing import List
from fastapi import APIRouter
from app.tasks import CreateTask, UpdateTask, Task

router = APIRouter(
    prefix='/task',
    tags=['Task']
)


@router.post("/create")
def create_task(create: CreateTask):
    return {"message": create}


@router.patch("/{id}")
def update_task(id, update: UpdateTask):
    return {"info": update}


@router.get("/list")
def get_list(from_date, to_date):
    return {List[Task]}


@router.get("/{task_id}")
def get_task(task_id):
    return {"task_id": task_id}


@router.delete("/{task_id}")
def delete_task(task_id):
    return {"message": f'Задача: {Task.name} - удалена'}
