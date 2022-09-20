from typing import List

from asyncpg import UniqueViolationError

from tgbot.services.db_api.db_gino import db
from tgbot.models.user import User


async def add_user(id: int, name: str, authenticated: str = "False", auth_key: str = "None"):
    try:
        user = User(id=id, name=name, authenticated=authenticated, auth_key=auth_key)
        await user.create()
        return True
    except UniqueViolationError:
        print("Пользователь уже есть в базе данных!")
        return False


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total


async def update_user_auth_status(id: int, status: str = "True"):
    user = await User.query.where(User.id == id).gino.first()
    await user.update(authenticated=status).apply()


async def save_user_auth_key(id: int, auth_key: str):
    user = await User.query.where(User.id == id).gino.first()
    await user.update(auth_key=auth_key).apply()
