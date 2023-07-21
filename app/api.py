from fastapi import FastAPI
from starlette import status

app = FastAPI()


@app.post("/user/create",
          summary='Создает нового пользователя',
          status_code=status.HTTP_200_OK)
def root():
    return {"message": "Hello World"}


@app.post("/user/login",
          summary='Авторизация пользователя',
          status_code=status.HTTP_200_OK)
def root():
    return {"message": "Hello World"}


@app.post("/task/create",
          summary='Создание новой задачи',
          status_code=status.HTTP_200_OK)
def root():
    return {"message": "Hello World"}


@app.patch("/task/{id}",
           summary='Обновление задачи',
           status_code=status.HTTP_200_OK)
def update_task(task_id):
    return {"task_id": task_id}


@app.get("/task",
            summary='Получение списка задач',
            status_code=status.HTTP_200_OK)
def get_list(from_date, to_date):
    return {"from_date": from_date, "to_date": to_date}


@app.get("/task/{task_id}",
            summary='Получение задачи',
            status_code=status.HTTP_200_OK)
def get_task(task_id):
    return {"task_id": task_id}


@app.delete("/task/{task_id}",
            summary='Удаление задачи',
            status_code=status.HTTP_200_OK)
def delete_task(task_id):
    return {"task_id": task_id}
