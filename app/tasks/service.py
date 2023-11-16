from datetime import datetime, timedelta
import bson
from fastapi import HTTPException
from bson import ObjectId
from app.database import tasks
from app.tasks import State
from app.user import verify_user

exception = HTTPException(
                status_code=400,
                detail=[{"error": f'not a valid id, it must be a 12-byte input or a 24-character hex string'}]
            )


async def find_task_by_id(_id):
    task = await tasks.find_one({"_id": ObjectId(_id)})
    if not task:
        raise HTTPException(
            status_code=404,
            detail=[{"message": 'Задача не найдена'}]
        )
    return task


async def find_tasks_by_date(date_from, date_to, user_id):
    date_from_datetime = datetime.strptime(date_from, '%Y-%m-%d')
    date_to_datetime = datetime.strptime(date_to, '%Y-%m-%d')
    task_list = await tasks.find({'user_id': ObjectId(user_id), 'created_at': {'$gte': date_from_datetime, '$lte': date_to_datetime + timedelta(days=1)}}, {"user_id": 0}).to_list(None)
    if not task_list:
        raise HTTPException(
            status_code=404,
            detail=[{"message": 'Задачи не найдены'}]
        )
    return task_list


# main logic
async def add_new_task(task, user_id):
    task_for_insert = {
        **dict(task),
        'state': State.Created,
        'created_at': datetime.utcnow(),
        'user_id': user_id
    }
    task_id = await tasks.insert_one(task_for_insert)
    return await find_task_by_id(task_id.inserted_id)


async def delete_task_by_id(task_id, user_id):
    try:
        task = await find_task_by_id(task_id)
        query = {'_id': ObjectId(task_id)}
        if verify_user(task['user_id'], user_id):
            await tasks.delete_one(query)
            return {"message": f'Задача: {task["name"]} удалена'}
    except bson.errors.InvalidId:
        raise exception


async def update_task_by_id(task_id, data, user_id):
    try:
        task = await find_task_by_id(task_id)
        query = {'_id': ObjectId(task_id)}
        new_values = {"$set": data.model_dump(exclude_none=True)}
        if verify_user(task['user_id'], user_id):
            await tasks.update_one(query, new_values)
            return {"message": f'Задача: {task["name"]} обновлена'}
    except bson.errors.InvalidId:
        raise exception


async def get_task_by_id(task_id, user_id):
    try:
        task = await find_task_by_id(task_id)
        if verify_user(task['user_id'], user_id):
            return task
    except bson.errors.InvalidId:
        raise exception


async def get_list_task_by_date(date_from, date_to, user_id):
    return await find_tasks_by_date(date_from, date_to, user_id)
