from typing import List
from fastapi import FastAPI
from starlette import status
from app.user.models import CreateUser, UserLogIn
import app.tasks.models as models

app = FastAPI()


@app.post("/user/create",
          summary='Создает нового пользователя',
          status_code=status.HTTP_200_OK)
def add_user(user: CreateUser):
    return {"message": user}


@app.post("/user/login",
          summary='Авторизация пользователя',
          status_code=status.HTTP_200_OK)
def login_user(login: UserLogIn):
    return {"message": "Вы успешно авторизованы"}


@app.post("/task/create",
          summary='Создание новой задачи',
          status_code=status.HTTP_200_OK)
def create_task(create: models.CreateTask):
    return {"message": create}


@app.patch("/task/{id}",
           summary='Обновление задачи',
           status_code=status.HTTP_200_OK,
           response_model=models.UpdateTask)
def update_task(id, update: models.UpdateTask):
    return {"info": update}


@app.get("/task",
         summary='Получение списка задач',
         status_code=status.HTTP_200_OK,
         response_model=List[models.Task])
def get_list(from_date, to_date):
    return {models.Task}


@app.get("/task/{task_id}",
         summary='Получение задачи',
         status_code=status.HTTP_200_OK,
         response_model=models.Task)
def get_task(task_id):
    return {"task_id": task_id}


@app.delete("/task/{task_id}",
            summary='Удаление задачи',
            status_code=status.HTTP_200_OK)
def delete_task(task_id):
    return {"message": f'Задача: {models.Task.name} - удалена'}
