from aiogram import Router, types, F, Bot
from aiogram.filters import Command, Filter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.gen_button import genButton
from enum import Enum

class LessonLevels(str, Enum):
    languages = "languages"
    teachers = "teachers"
    teacher = "teacher"


class LanguagePageSettings(CallbackData, prefix='lang'):
    lessonLevel: LessonLevels = ''
    lesson_id: int = 0
    teacher_id: int = 0
    current_page: int = 1
    total_pages: int = 0
    rows_per_page: int = 2

q = LanguagePageSettings().rows_per_page
print(q)

inline_keyboard=[
    [
        InlineKeyboardButton(
            text='1️⃣', 
            url=None, 
            callback_data='lang::10:40:1:0:2', 
            web_app=None, 
            login_url=None, 
            switch_inline_query=None, 
            switch_inline_query_current_chat=None, 
            callback_game=None, pay=None
            ), 
        InlineKeyboardButton(
            text='2️⃣', url=None, callback_data='lang::10:10:1:0:2', web_app=None, login_url=None, switch_inline_query=None, switch_inline_query_current_chat=None, callback_game=None, pay=None)]]