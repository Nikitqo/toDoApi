from typing import List
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette import status
from app.user.models import CreateUser, UserLogIn
import app.tasks.models as models
from app.mongo_db_script import add_new_user, find_user

app = FastAPI()

# пока ручки болванки
@app.post("/user/create",
          summary='Создает нового пользователя',
          status_code=status.HTTP_200_OK)
def add_user(user: CreateUser):
    encode_user = jsonable_encoder(user)
    add_new_user(encode_user)
    return {"data": "Вы успешно зарегистрированы"}


@app.post("/user/login",
          summary='Авторизация пользователя',
          status_code=status.HTTP_200_OK)
def login_user(login: UserLogIn):
    encode_user = jsonable_encoder(login)
    result = find_user(encode_user["email"])
    return {"data": result}


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


@app.get("/task/list",
         summary='Получение списка задач',
         status_code=status.HTTP_200_OK,
         response_model=List[models.Task])
def get_list(from_date, to_date):
    return {List[models.Task]}


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
