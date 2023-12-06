from ast import stmt
from hmac import new
import random

from aiogram import Router, types, F, Bot
from aiogram.filters import Command, Filter
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from html import escape

from bot.databases.db_postgresql import db
from bot.databases.db_declaration import Teachers
from bot.text_assets import TextMenu as tm
from bot.utils.navigation import detect_bad_symbols

from sqlalchemy.dialects.postgresql import insert

router = Router()

@router.message(Command('test'))
async def test(msg: types.Message, bot: Bot):
   
    lessons_of_university = await db.get_all_lessons(exclude_null_teachers=True)
    for lesson in lessons_of_university:
        print(lesson.name)
