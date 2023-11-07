from typing import Annotated
from fastapi import APIRouter, Depends
from app.boards import Board, Visible, CreateBoard, create_board
from app.user import get_current_user

router = APIRouter(
    prefix='/board',
    tags=['Board']
)

Auth = Annotated[dict, Depends(get_current_user)]


@router.post("/create", response_model=Board)
async def create_new_board(board: CreateBoard, auth: Auth):
    return await create_board(board, auth)

