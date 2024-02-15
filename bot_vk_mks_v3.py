import asyncio
import logging
import re
# import pandas as pd
import os
# from joblib import load
# from navec import Navec
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from keep_alive import keep_alive


keep_alive()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GIGACHAT_TOKEN = os.environ.get('sber_auth_code')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)

def gigachat_correction(text):
    print(text)
    # Авторизация в сервисе GigaChat
    chat = GigaChat(model='GigaChat:latest',
                    credentials=GIGACHAT_TOKEN,
                    verify_ssl_certs=False)

    messages = [SystemMessage(content="Ты космонавт который живет на МКС, на орбите Земли. Отвечай коротко, используя космический лексикон."),
                HumanMessage(content='Что ты думаешь про: \n' + text)]
    answer = chat.invoke(messages).content
    print(answer)

    return answer


hello_text = 'Отправь мне текстовое сообщение и я расскажу про это.'

@dp.message(Command('startt'))
async def cmd_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\n{hello_text}')


@dp.message()
async def correct_punctuation(message: types.Message):
    await message.answer(gigachat_correction(message.text))


if __name__ == '__main__':
    asyncio.run(main())
