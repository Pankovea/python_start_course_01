# Переменные для пользователей
users = []
user_mode = {}


def reset_mode(cid):
    user_mode.pop(cid, None)


def get_user_mode(cid):
    return user_mode.get(cid, None)