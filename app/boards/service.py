from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
from app.database import boards


async def find_board_by_id(_id):
    board = await boards.find_one({"_id": ObjectId(_id)})
    if not board:
        raise HTTPException(
            status_code=404,
            detail=[{"message": 'Доска не найдена'}]
        )
    return board


# main logic

async def create_board(board, user_id):
    board_for_insert = {
        'name': board.name,
        'description': board.description,
        'visible': board.visible,
        'user_id': user_id,
        'columns': board.columns,
        'company': board.company,
        'created_at': datetime.utcnow()
    }
    board_id = await boards.insert_one(board_for_insert)
    return await find_board_by_id(board_id.inserted_id)
