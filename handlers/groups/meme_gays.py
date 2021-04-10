from random import randint
import re

from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsGroup, AdminFilter
from loader import dp


@dp.message_handler(IsGroup(), Command("gay", prefixes="!/"), AdminFilter())
async def gay_detektor(message: types.Message):
    procent = randint(0,100)

    if procent < 50:
        welcome = ('Чел, обдумай еще раз своё поступление в ЧВУТ')
        await message.reply(f"🏳️‍🌈Пользователь гей на {procent}%\n", welcome)
    else:
        welcome = ('Добро пожаловать. Здесь тебе рады.')
        await message.reply(f"🏳️‍🌈Пользователь гей на {procent}%\n", welcome)
