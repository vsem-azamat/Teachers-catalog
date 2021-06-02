from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsPrivate

from loader import dp, bot


@dp.message_handler(Command("aboba", prefixes='!/'))
async def aboba(message: types.Message):
    await message.reply(text='И вам абоба, уважаемый!')

