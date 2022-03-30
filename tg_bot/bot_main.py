#!venv/bin/python
import logging


import conf, keyboards
from aiogram import Bot, Dispatcher, executor, types


import requests
import json

import numpy as np

# Объект бота
bot = Bot(token=conf.TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

global true_dict
true_dict = {}


@dp.message_handler(commands='start')
async def process_hi1_command(message: types.Message):
    await message.reply('Привет', reply_markup=keyboards.greet_kb)


@dp.message_handler(text='Привет! 👋')
async def process_command_2(message: types.Message):
    hello_string = '''Привет!\n
Я бот, с которым можно посоревноваться в угадывании оригинальности текста из произведений Солженицына.\n
А еще я могу определять, принадлежит ли введенная тобой фраза Александру Исаевичу)\n
Кстати, текст можешь вводить любым способом!
Я умею обрабатывать и скриншоты, и голосовые😜😜😜'''
    await message.answer(hello_string, reply_markup=keyboards.inline_kb_full)


# @dp.message_handler(text='Привет! 👋')
# async def cmd_test1(message: types.Message):
#     chat_id = message.chat.id  # работает и для приватного(лс) чата и для общих чатов (групп)
#     await message.reply(chat_id)


@dp.callback_query_handler(text='compete')
async def send_random_value(call: types.CallbackQuery):
    chat_id = call.from_user.id
    print(1)
    answer = requests.get('https://d00f-37-204-7-129.ngrok.io/get_answers', timeout=10)

    phrase_id = answer.json().keys()
    true_dict[chat_id] = phrase_id
    await call.message.answer(list(answer.json().values())[0], reply_markup=keyboards.inline_yesno)


@dp.callback_query_handler(text=['1', '0'])
async def checker(call: types.CallbackQuery):
    chat_id = call.from_user.id
    answer = call.data
    user_answer = {'answer': answer, 'user': chat_id, 'text_id': list(true_dict[chat_id])[0]}
    data_json = json.dumps(user_answer)
    answer = requests.post('https://d00f-37-204-7-129.ngrok.io/to_base', json=data_json, timeout=10) #to the server
    print(answer.json()['next_text'])
    if answer.json()['next_text'] == 1:
        await send_random_value(call=call)
    else:
        await call.message.answer(f'Игра завершена!\n {answer.json()["result"]} \nВсего побед: {answer.json()["wins"]}\nВсего игр сыграно: {answer.json()["average"]}\nХочешь сыграть еще?)',
                                  reply_markup=keyboards.inline_contno,
                                  )



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
