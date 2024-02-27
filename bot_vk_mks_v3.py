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

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat


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

@dp.message(Command('start_reply'))
async def cmd_start(message: types.Message):
    await message.reply(reply_to_message_id=message.message_id, f' reply , {message.from_user.full_name}!\n{hello_text}')

@dp.message(Command('start_reply_to'))
async def cmd_start(message: types.Message):
    await message.reply_to(reply_to_message_id=message.message_id, f' reply_to , {message.from_user.full_name}!\n{hello_text}')

@dp.message(Command('start_reply_to_m'))
async def cmd_start(message: types.Message):
    await message.reply_to_message(reply_to_message_id=message.message_id, f' reply_to_message  , {message.from_user.full_name}!\n{hello_text}')


@dp.message(Command('startt'))
async def cmd_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\n{hello_text}')

@dp.message(Command('stopp'))
async def cmd_stop(message: types.Message):
    await message.answer(f'stopppp  ')
    await dp.start_polling(bot)


@dp.message()
async def correct_punctuation(message: types.Message):
    # bot.reply_to(message, f"ответ: {giga_answer} " )
    await message.answer(gigachat_correction(message.text))
    

# @bot.message_handler(func=lambda message: True)
# def handle_text(message):
#     order_number = message.text.strip()
#     print(order_number)
#     # giga_answer = order_number
#     giga_answer = gigachat_correction(message.text)
#     # Загружаем данные из Excel-таблицы
#     #orders_df = load_orders()

#     # Ищем статус заказа по номеру
#     #status = orders_df.loc[orders_df['Номер заказа'] == order_number, 'Статус'].values
#     status = '111'

#     if len(status) > 0:
#         # bot.reply_to(message, f"Статус заказа {order_number}: {status[0]}")
#         bot.reply_to(message, f"ответ: {giga_answer} " ) 
#     else:
#         bot.reply_to(message, f" Нененене {order_number} не найден.")


if __name__ == '__main__':
    asyncio.run(main())
