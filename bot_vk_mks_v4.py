import os
import logging
import random
# from background import keep_alive  #импорт функции для поддержки работоспособности
from keep_alive import keep_alive
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat



# Настройка журналирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)



BOT_TOKEN = os.environ.get('BOT_TOKEN')
GIGACHAT_TOKEN = os.environ.get('sber_auth_code')

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

keep_alive()  #запускаем flask-сервер в отдельном потоке


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


@dp.message()
async def correct_punctuation(message: types.Message):
    # bot.reply_to(message, f"ответ: {giga_answer} " )
    await message.answer(gigachat_correction(message.text))
    

@dp.message(Command('startt'))
async def cmd_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\n{hello_text}')

@dp.message(Command('stopp'))
async def cmd_stop(message: types.Message):
    await message.answer(f'stopppp  ')
    await dp.start_polling(bot)

# Функция для выбора случайного сообщения из файла
def get_random_message():
  with open('words.txt', 'r') as file:
    lines = file.readlines()
    message = random.choice(lines)
  return message.strip()


# Функция для сохранения сообщений в файле
def save_message_to_file(message):
  if message.startswith('/'):
    return  # не сохраняем команды в файле

  with open('words.txt', 'a') as file:
    file.write(message + '\n')


# Функция для сохранения слов в файле
def save_words_to_file(words):
  with open('words.txt', 'a') as file:
    file.write('\n'.join(words) + '\n')


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
  """Команда /start"""
  await message.reply('Привет, я Бот!')


# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
  """Команда /help"""
  await message.reply(
      'Вы можете отправлять мне сообщения, и я буду их повторять. Администраторы могут удалить сообщения с помощью команды /delete.'
  )


# Обработчик команды /delete для удаления сообщений (только для администраторов)
@dp.message_handler(commands=['delete'])
async def cmd_delete(message: types.Message):
  chat_id = message.chat.id
  message_id = message.reply_to_message.message_id

  if message.from_user.id in [
      admin.user.id
      for admin in await bot.get_chat_administrators(chat_id=chat_id)
  ]:
    # Если пользователь, отправивший команду, является администратором, удаляем сообщение
    try:
      await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
      # Если бот не может удалить сообщение, сообщаем пользователю об ошибке
      await bot.send_message(chat_id=chat_id,
                             text=f'Не удалось удалить сообщение: {e}')
  else:
    # Если пользователь не является администратором, сообщаем ему об ошибке
    await bot.send_message(
        chat_id=chat_id,
        text=
        'Вы не являетесь администратором этого чата, поэтому вы не можете удалять сообщения.'
    )


# Обработчик команды /clear для очистки файла words.txt
@dp.message_handler(commands=['clear'])
async def cmd_clear(message: types.Message):
  chat_id = message.chat.id

  if message.from_user.id in [
      admin.user.id
      for admin in await bot.get_chat_administrators(chat_id=chat_id)
  ]:
    # Если пользователь, отправивший команду, является администратором, очищаем файл
    with open('words.txt', 'w') as file:
      file.write('')
    await bot.send_message(chat_id=chat_id, text='Файл words.txt был очищен.')
  else:
    # Если пользователь не является администратором, сообщаем ему об ошибке
    await bot.send_message(
        chat_id=chat_id,
        text=
        'Вы не являетесь администратором этого чата, поэтому вы не можете очищать файл words.txt.'
    )


# Обработчик команды /view для просмотра содержимого файла words.txt
@dp.message_handler(commands=['view'])
async def cmd_view(message: types.Message):
  chat_id = message.chat.id

  if message.from_user.id in [
      admin.user.id
      for admin in await bot.get_chat_administrators(chat_id=chat_id)
  ]:
    # Если пользователь, отправивший команду, является администратором, читаем содержимое файла
    with open('words.txt', 'r') as file:
      content = file.read()
    await bot.send_message(chat_id=chat_id,
                           text=f'Содержимое файла words.txt:\n\n{content}')
  else:
    # Если пользователь не является администратором, сообщаем ему об ошибке
    await bot.send_message(
        chat_id=chat_id,
        text=
        'Вы не являетесь администратором этого чата, поэтому вы не можете просматривать файл words.txt.'
    )


@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo(message: types.Message):
  text = message.text
  save_message_to_file(text)  # Сохраняем сообщение в файле

  # Получаем случайное сообщение из файла
  random_message = get_random_message()

  await message.answer(random_message)


# Запуск бота
if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
