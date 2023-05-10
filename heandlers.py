from aiogram import types, Dispatcher
from response_processor import response
from aiogram.types import InputFile
import matplotlib.pyplot as plt
import numpy as np
from create_bot import bot
import os
from create_bot import access_list



async def command_start(message: types.Message):
    try:
        print(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Привет, я Telegram-бот для помощи с математикой. Я умею:\n'
                                                     '  - решать уравнения с одной переменной;\n'
                                                     '  - упрощать выражения;\n'
                                                     '  - рисовать графики функций;\n'
                                                     '  - давать определение понятию.\n'
                                                     'Спроси меня, и я попробую решить твой математический вопрос!')
    except:
        await message.reply('Что то пошло не так')


async def command_help(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Список команд:\n'
                                                     '/start - начать диалог\n'
                                                     '/graphic <уравнение> - построить график уравнения\n'
                                                     'Примеры запросов:\n'
                                                     '● pеши уравнение x+1 = 10\n'
                                                     '● что такое число')
    except:
        await message.reply('Что то пошло не так')


async def echo(message: types.Message):
    if message.from_user.id in access_list:

        answer = response(message.text)
        if answer.startswith('img'):
            photo = InputFile(answer)
            await bot.send_photo(message.from_user.id, photo=photo)
            os.remove(answer)
        else:
            await bot.send_message(message.from_user.id, answer)
        #await message.reply('Что то пошло не так')
    else:
        await message.reply('Нет доступа')



def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(echo)
