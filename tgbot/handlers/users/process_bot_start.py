from aiogram import types, Dispatcher


async def bot_start(message: types.Message):
        await message.answer(f"Здравствуйте, {message.from_user.full_name}!\n"
                             f"Для прохождения аутентификации в боте используйте команду <b>/auth</b>")


def register_process_bot_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands="start", state="*")
