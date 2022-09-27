from aiogram import types, Dispatcher

from tgbot.misc.throttling_function import rate_limit
from tgbot.services.db_api import db_commands as commands


@rate_limit(5)
async def bot_start(message: types.Message):
    new_user = await commands.add_user(id=message.from_user.id, name=message.from_user.full_name)
    if new_user is True:
        await message.answer(f"Здравствуйте, {message.from_user.full_name}!\n"
                             f"Для прохождения аутентификации в боте используйте команду <b>/auth</b>")
    else:
        await message.answer("Вы уже зарегистрированы в бд")


def register_process_bot_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands="start", state="*")
