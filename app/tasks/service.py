from datetime import datetime

import bson
from fastapi import HTTPException
from bson import ObjectId
from app.database import tasks
from app.tasks import State


def find_task_by_id(_id):
    return tasks.find_one({"_id": ObjectId(_id)})


def verify_user(user_id_from_db, user_id):
    if user_id_from_db != user_id:
        raise HTTPException(
            status_code=403,
            detail=[{"error": 'Доступ запрещен'}]
        )
    return True


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
        if not task:
            raise HTTPException(
                status_code=404,
                detail=[{"error": 'Задача не найдена'}]
            )
        if verify_user(task['user_id'], user_id):
            tasks.delete_one({'_id': ObjectId(task_id)})
            return {"message": f'Задача: {task["name"]} удалена'}
    except bson.errors.InvalidId:
        return HTTPException(
                status_code=400,
                detail=[{f'{task_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'}]
            )
