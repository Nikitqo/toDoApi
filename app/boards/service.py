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


async def find_board_by_id(id):
    board = await boards.find_one({"_id": ObjectId(id)})
    if not board:
        raise HTTPException(
            status_code=404,
            detail=[{"message": 'Доска не найдена'}]
        )
    return board


# main logic

async def create_board(board, user_id):
    board_for_insert = board.model_dump()
    board_for_insert.update({'created_at': datetime.utcnow(), 'user_id': user_id})
    new_board = await boards.insert_one(board_for_insert)
    return await find_board_by_id(new_board.inserted_id)


async def delete_board_by_id(board_id, user_id):
    try:
        task = await find_board_by_id(board_id)
        query = {'_id': ObjectId(board_id)}
        if verify_user(task['user_id'], user_id):
            await boards.delete_one(query)
            return {"message": f'Доска: {task["name"]} удалена'}
    except bson.errors.InvalidId:
        raise exception
