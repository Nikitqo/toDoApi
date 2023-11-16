from fastapi import FastAPI
from app.user.router import router as user_router
from app.tasks.router import router as task_router
from app.boards.router import router as board_router

app = FastAPI(debug=True)

app.include_router(user_router)
app.include_router(task_router)
app.include_router(board_router)
