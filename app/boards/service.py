from datetime import datetime
import bson
from fastapi import HTTPException
from bson import ObjectId
from app.database import boards
from app.user import verify_user

exception = HTTPException(
                status_code=400,
                detail=[{"error": f'not a valid id, it must be a 12-byte input or a 24-character hex string'}]
            )


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


async def delete_board_by_id(board_id, user_id):
    try:
        task = await find_board_by_id(board_id)
        query = {'_id': ObjectId(board_id)}
        if verify_user(task['user_id'], user_id):
            await boards.delete_one(query)
            return {"message": f'Доска: {task["name"]} удалена'}
    except bson.errors.InvalidId:
        raise exception
