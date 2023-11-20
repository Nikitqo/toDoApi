from typing import Annotated
from fastapi import APIRouter, Depends
from app.boards import Board, BaseBoard, create_board, delete_board_by_id, add_user_to_board, BoardUsers, \
    update_board_user_role, add_task_list_to_board, BoardTasks
from app.user import get_current_user

router = APIRouter(
    prefix='/board',
    tags=['Board']
)

Auth = Annotated[dict, Depends(get_current_user)]


@router.post("/create", response_model=Board)
async def create_new_board(board: BaseBoard, auth: Auth):
    return await create_board(board, auth)


@router.delete("/{id}/delete")
async def delete_board(board_id, auth: Auth):
    return await delete_board_by_id(board_id, auth)


@router.patch("/add_user_to_board")
async def add_user(board_id, user_data: BoardUsers, auth: Auth):
    return await add_user_to_board(board_id, user_data, auth)


@router.patch("/update_user_role")
async def update_role(board_id, user_data: BoardUsers, auth: Auth):
    return await update_board_user_role(board_id, user_data, auth)


@router.patch("/add_task_list_to_board")
async def add_task_list(board_id, data: BoardTasks, auth: Auth):
    return await add_task_list_to_board(board_id, data, auth)
