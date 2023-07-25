from fastapi import FastAPI
from app.user.router import router as user_router
from app.tasks.router import router as task_router

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)
