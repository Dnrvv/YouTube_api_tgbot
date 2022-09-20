from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


from tgbot.config import load_config
from tgbot.services.db_api import db_commands
from tgbot.services.youtube.auth import GoogleAuth


async def auth_start(message: types.Message, state: FSMContext):
    config = load_config(".env")
    auth = GoogleAuth(CLIENT_ID=config.misc.client_id, CLIENT_SECRET=config.misc.client_secret)
    url = auth.GetAuthUrl()
    await message.answer(f"Для авторизации в боте пройдите по <b><a href='{url}'>ссылке</a></b>, "
                         f"а затем скопируйте и отправьте боту ваш <b>уникальный код</b>.")
    await state.set_state("auth_step_1")


async def authentication_yt(message: types.Message, state: FSMContext):
    if len(message.text) < 20:
        await message.answer("В сообщении отсутствует код, либо код неверный!")
        return
    else:
        code = message.text  # code = auth_key в gino.db
        try:
            config = load_config(".env")
            auth = GoogleAuth(CLIENT_ID=config.misc.client_id, CLIENT_SECRET=config.misc.client_secret)
            auth.Auth(code)
            # auth.SaveCredentialsFile("credentials.json")
            await db_commands.update_user_auth_status(id=message.from_user.id)  # По умолчанию status = "True
            await db_commands.save_user_auth_key(id=message.from_user.id, auth_key=code)
            await message.answer("Авторизация пройдена!")

            # with open("credentials.json", "r") as f:
            #     cred_data = f.read()
        except Exception as e:
            print(e)
    await state.finish()


# async def save_auth_data(message: types.Message):
#     auth_data = message.reply_to_message.text
#     try:
#         with open("credentials.json", "w") as f:
#             f.write(auth_data)
#         config = load_config(".env")
#         auth = GoogleAuth(CLIENT_ID=config.misc.client_id, CLIENT_SECRET=config.misc.client_secret)
#         auth.LoadCredentialsFile("credentials.json")
#         auth.authorize()
#     except Exception as e:
#         print(e)


# async def send_video_url(message: types.Message, state: FSMContext):
#     await message.answer("Отправьте ссылку на видео:")
#     await state.set_state("get_vid_url")


def register_process_ytapi_test(dp: Dispatcher):
    dp.register_message_handler(auth_start, commands="auth", state="*")
    dp.register_message_handler(authentication_yt, content_types=types.ContentType.TEXT, state="auth_step_1")
