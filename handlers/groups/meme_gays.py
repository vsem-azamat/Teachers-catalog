from random import randint

from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), Command("gay", prefixes="!/"))
async def gay_detektor(message: types.Message):
    procent = randint(0, 100)

    if procent < 50:
        welcome = 'Чел, обдумай еще раз своё поступление в ЧВУТ'
        await message.reply(f"Пользователь 🏳️‍🌈 на {procent}%\n", welcome)
    else:
        welcome = 'Добро пожаловать. Здесь тебе рады.'
        await message.reply(f"Пользователь 🏳️‍🌈 на {procent}%\n", welcome)
