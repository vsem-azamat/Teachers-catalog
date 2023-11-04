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
    text = "\ntest <b>asd</b>"
    text = '111'
    q = await detect_bad_symbols(text)
    print(q)
    await msg.answer(text=f"test: {escape(text)}")
