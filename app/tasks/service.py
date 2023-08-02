from datetime import datetime
from app.database import tasks
from app.tasks import State


# main logic
def add_new_task(data, user_id):
    task_for_insert = {
        'name': data.name,
        'description': data.description,
        'deadline': data.deadline,
        'state': State.Created,
        'created_at': datetime.utcnow(),
        'user_id': user_id
    }
    tasks.insert_one(task_for_insert)
    return {"data": f'Задача: {data.name} создана'}
