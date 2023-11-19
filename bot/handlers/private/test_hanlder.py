from aiogram import Router, types, F, Bot
from aiogram.filters import Command, Filter
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from html import escape


from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm
from bot.utils.navigation import detect_bad_symbols

router = Router()


@router.message(Command('test'))
async def test(msg: types.Message, bot: Bot):
    lessons_exc = await db.get_all_lessons(exclude_null_teachers=True)

    text = "Lessons exclude:\n"
    for lesson in lessons_exc:
        text += f"\n{lesson.name}:"
    text += "\n" + str(await db.get_count_all_lessons(True))
    
    text += "\n\nLessons include:\n"
    lessons_inc = await db.get_all_lessons(exclude_null_teachers=False)
    for lesson in lessons_inc:
        text += f"\n{lesson.name}"
    text += "\n" + str(await db.get_count_all_lessons(False))


    await msg.answer(text)
