from aiogram import types
from aiogram.dispatcher.filters import Command

from texts.texts_main import help_text

from loader import dp


@dp.message_handler(Command('help'))
async def help_command(message: types.Message):
    await message.reply(text=help_text)
