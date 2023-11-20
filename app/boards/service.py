from datetime import datetime
import bson
from fastapi import HTTPException
from bson import ObjectId
from app.database import boards
from app.user import verify_user, find_user_by_id
from .models import Roles

not_valid_id_exception = HTTPException(
                status_code=400,
                detail=[{"error": f'not a valid id, it must be a 12-byte input or a 24-character hex string'}]
            )

has_admin_exception = HTTPException(
                status_code=400,
                detail=[{"message": 'Обновляемый пользователь имеет роль Admin'}]
            )

access_exception = HTTPException(
                    status_code=403,
                    detail=[{"error": 'Доступ запрещен'}]
                )

has_user_exception = HTTPException(
            status_code=400,
            detail=[{"error": 'Пользователь уже добавлен'}]
        )

nof_found_user_exception = HTTPException(
            status_code=404,
            detail=[{"error": 'Пользователь не найден'}]
        )

has_task_list_exception = HTTPException(
                status_code=400,
                detail=[{"message": 'Список задач с таким названием уже существует'}]
            )


async def find_board_by_id(board_id):
    board = await boards.find_one({"_id": ObjectId(board_id)})
    if not board:
        raise HTTPException(
            status_code=404,
            detail=[{"message": 'Доска не найдена'}]
        )
    return board


def is_user_admin_in_board(board, user_id):
    for i in board["users"]:
        if i["id"] == str(user_id) and i["role"] == "Admin":
            return True
    raise access_exception


def is_user_in_board(board, user_id):
    for i in board["users"]:
        if str(i["id"]) == str(user_id):
            return True
    return False


def is_task_list_in_board(board, name):
    for i in board["task_list"]:
        if str(i["name"]) == str(name):
            raise has_task_list_exception


# main logic

async def create_board(board, user_id):
    board_for_insert = board.model_dump()
    board_for_insert.update({'created_at': datetime.utcnow(), 'user_id': user_id, 'users': [{'id': str(user_id), 'role': Roles.Admin}], 'task_list': []})
    new_board = await boards.insert_one(board_for_insert)
    return await find_board_by_id(new_board.inserted_id)


async def delete_board_by_id(board_id, user_id):
    try:
        board = await find_board_by_id(board_id)
        query = {'_id': ObjectId(board_id)}
        if verify_user(board['user_id'], user_id):
            await boards.delete_one(query)
            return {"message": f'Доска: {board["name"]} удалена'}
    except bson.errors.InvalidId:
        raise not_valid_id_exception


async def add_user_to_board(board_id, data, user_id):
    try:
        board = await find_board_by_id(board_id)
        query = {'_id': ObjectId(board_id)}
        new_user = {"$push": {"users": {"id": data.id, "role": data.role}}}
        if is_user_admin_in_board(board, user_id) and await find_user_by_id(data.id) and not is_user_in_board(board, data.id):
            await boards.update_one(query, new_user)
            return {"message": 'Пользователь успешно добавлен'}
        raise has_user_exception
    except bson.errors.InvalidId:
        raise not_valid_id_exception


async def update_board_user_role(board_id, data, user_id):
    try:
        board = await find_board_by_id(board_id)
        update_user_role_query = {'_id': ObjectId(board_id), "users.id": data.id}
        update_user_role = {"$set": {"users.$.role": data.role}}
        if is_user_admin_in_board(board, user_id):
            if str(board["user_id"]) == str(data.id):
                raise has_admin_exception
            elif is_user_in_board(board, data.id):
                await boards.update_one(update_user_role_query, update_user_role)
                return {"message": 'Роль обновлена'}
            raise nof_found_user_exception
    except bson.errors.InvalidId:
        raise not_valid_id_exception


async def add_task_list_to_board(board_id, data, user_id):
    try:
        board = await find_board_by_id(board_id)
        query = {'_id': ObjectId(board_id)}
        new_task_list = {"$push": {"task_list": {"name": data.name, "tasks": []}}}
        if is_user_admin_in_board(board, user_id) and await find_user_by_id(user_id) and not is_task_list_in_board(board, data.name):
            await boards.update_one(query, new_task_list)
            return {"message": f'Список задач {data.name} успешно добавлен'}
    except bson.errors.InvalidId:
        raise not_valid_id_exception

