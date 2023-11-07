from typing import Annotated
from fastapi import APIRouter, Depends
from app.boards import Board, Visible, CreateBoard, create_board, delete_board_by_id
from app.user import get_current_user

router = APIRouter(
    prefix='/board',
    tags=['Board']
)

Auth = Annotated[dict, Depends(get_current_user)]


@router.post("/create", response_model=Board)
async def create_new_board(board: CreateBoard, auth: Auth):
    return await create_board(board, auth)


@router.delete("/{id}/delete")
async def delete_board(board_id, auth: Auth):
    return await delete_board_by_id(board_id, auth)