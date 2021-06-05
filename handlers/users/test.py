from aiogram import types
from aiogram.types.message import ParseMode
from aiogram.utils.markdown import hlink
from filters.super_admins import SuperAdmins

from keyboards.inline.button_school import test1
from loader import dp, bot
from aiogram.dispatcher.filters import Command
from db.sq_lite import cursor, conn


@dp.message_handler(Command('test', prefixes='!/'), SuperAdmins())
async def test(message: types.Message):
    text = hlink('test', 'https://soundcloud.com/discover')
    await message.reply(text)



