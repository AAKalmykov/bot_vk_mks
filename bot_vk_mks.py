# Бот для Телеги
# Отвечает как Космоснавт на МКС
# by Artem
# используется библиотеки
# - TeleGram
# - GigaChat

import pandas as pd
import telebot
import os


# Создаем экземпляр бота
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
# bot = telebot.TeleBot('string my token')

# Обработчик команды /start или приветствия
@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.reply_to(message, "Привет! Я бот. Для получения статуса заказа отправьте его номер.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    order_number = message.text.strip()

    # Загружаем данные из Excel-таблицы
    #orders_df = load_orders()

    # Ищем статус заказа по номеру
    #status = orders_df.loc[orders_df['Номер заказа'] == order_number, 'Статус'].values
    status = 0

    if len(status) > 0:
        bot.reply_to(message, f"Статус заказа {order_number}: {status[0]}")
    else:
        bot.reply_to(message, f"Заказ с номером {order_number} не найден.")


# Запускаем бота
bot.polling()



