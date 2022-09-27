import argparse

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


from tgbot.config import load_config
from tgbot.services.youtube.auth import GoogleAuth
from tgbot.services.youtube.youtube import YouTube, like_video


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
    else:
        auth_key = message.text
        try:
            config = load_config(".env")
            auth = GoogleAuth(CLIENT_ID=config.misc.client_id, CLIENT_SECRET=config.misc.client_secret)
            auth.Auth(auth_key)
            auth.SaveCredentialsFile("creds.json")
            with open("creds.json", "r") as f:
                cred_data = f.read()

            # await save_auth_data(cred_data=cred_data)
            await message.answer("Авторизация пройдена и её данные успешно сохранены!")
        except Exception as e:
            print(e)
            await message.answer("ERROR")
    await state.finish()


async def save_auth_data(cred_data: str):
    try:
        config = load_config(".env")
        with open("creds.json", "a+") as f:
            f.writelines(f"{cred_data}\n")
        auth = GoogleAuth(CLIENT_ID=config.misc.client_id, CLIENT_SECRET=config.misc.client_secret)
        auth.LoadCredentialsFile("creds.json")
        auth.authorize()
    except Exception as e:
        print(e)


async def like_video_by_url(url: str = "C-Cdk4BqnRc"):
    """

    Функция, которая будет вызываться внутри хендлеров бота

    """

    config = load_config(".env")
    auth = GoogleAuth(CLIENT_ID=config.misc.client_id, CLIENT_SECRET=config.misc.client_secret)
    auth.LoadCredentialsFile("creds.json")

    ratings = ('like', 'dislike', 'none')
    parser = argparse.ArgumentParser()
    parser.add_argument('--videoId', default=f'{url}',
                        help='ID of video to like.')
    parser.add_argument('--rating', default='like',
                        choices=ratings,
                        help='Indicates whether the rating is "like", "dislike", or "none".')
    args = parser.parse_args()

    like_video(youtube=auth.authorize(), args=args)


async def likee(message: types.Message):
    await like_video_by_url()
    await message.answer("Отлично")


def register_process_ytapi_test(dp: Dispatcher):
    dp.register_message_handler(auth_start, commands="auth", state="*")
    dp.register_message_handler(authentication_yt, content_types=types.ContentType.TEXT, state="auth_step_1")
    # dp.register_message_handler(save_auth_data, commands="save", state="*")
    dp.register_message_handler(likee, commands="likevid", state="*")
