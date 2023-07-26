from passlib.context import CryptContext
from app.database.mongo_db import users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def add_new_user(data, collection=users):
    email = data['email']
    if not list(find_user(email)):
        user_for_insert = {
            'username': data['username'],
            'password_hash': get_password_hash(data['password'].get_secret_value()),
            'email': data['email']
        }
        return collection.insert_one(user_for_insert)
    else:
        return False


def find_user(mail, collection=users):
    json_data = collection.find({"email": mail})
    return json_data