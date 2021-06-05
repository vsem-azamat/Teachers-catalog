from aiogram import types
from aiogram.types.message import ParseMode
from aiogram.utils.markdown import hlink
from filters.super_admins import SuperAdmins

from aiogram.types import InputFile
from keyboards.inline.button_school import test1
from loader import dp, bot
from aiogram.dispatcher.filters import Command
from db.sq_lite import cursor, conn
from texts.texts_main import start_msg


@dp.message_handler(Command('test', prefixes='!/'), SuperAdmins())
async def test(message: types.Message):
    photo = InputFile(path_or_bytesio="Images/start.jpg")
    await bot.send_photo(message.from_user.id, photo=photo, caption=start_msg)
