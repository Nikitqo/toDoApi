from app.database.service import add_new_user, find_user


def add_user(user):
    if add_new_user(user):
        return {"data": "Вы успешно зарегистрированы"}
    else:
        return {"data": "Пользователь с данным email уже зарегистрирован"}
