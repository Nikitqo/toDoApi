from datetime import datetime
import bson
from fastapi import HTTPException
from bson import ObjectId
from app.database import tasks
from app.tasks import State
from app.user import verify_user

exceptions = HTTPException(
                status_code=400,
                detail=[{"error": f'not a valid id, it must be a 12-byte input or a 24-character hex string'}]
            )


def find_task_by_id(_id):
    task = tasks.find_one({"_id": ObjectId(_id)})
    if not task:
        raise HTTPException(
            status_code=404,
            detail=[{"error": 'Задача не найдена'}]
        )
    return task


# main logic
def add_new_task(task, user_id):
    task_for_insert = {
        **task.__dict__,
        'state': State.Created,
        'created_at': datetime.utcnow(),
        'user_id': user_id
    }
    tasks.insert_one(task_for_insert)
    return {"message": f'Задача: {task.name} создана'}


def delete_task_by_id(task_id, user_id):
    try:
        task = find_task_by_id(task_id)
        query = {'_id': ObjectId(task_id)}
        if verify_user(task['user_id'], user_id):
            tasks.delete_one(query)
            return {"message": f'Задача: {task["name"]} удалена'}
    except bson.errors.InvalidId:
        raise exceptions


def update_task_by_id(task_id, data, user_id):
    try:
        task = find_task_by_id(task_id)
        query = {'_id': ObjectId(task_id)}
        new_values = {"$set": data.__dict__}
        if verify_user(task['user_id'], user_id):
            tasks.update_one(query, new_values)
            return {"message": f'Задача: {task["name"]} обновлена'}
    except bson.errors.InvalidId:
        raise exceptions


def get_task_by_id(task_id, user_id):
    try:
        task = find_task_by_id(task_id)
        if verify_user(task['user_id'], user_id):
            result = {'id': task_id, **task}
            return result
    except bson.errors.InvalidId:
        raise exceptions
