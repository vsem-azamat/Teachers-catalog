from aiogram import Router, types, F, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command


from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.gen_button import genButton
from utils.desh_args import get_desh_args
from utils.navigation import *

router = Router()


@router.callback_query(F.data == 'languages')
async def list_universities(callback: types.CallbackQuery, bot: Bot):
    user_lang = await db.get_user_lang(callback.from_user.id)
    text = "Выберите Язык, чтобы показать репетиторов"
    languages = await db.get_languages()
    for language in languages:
        buttons = [

        ]


    languages_name = [language.name for language in languages]
    languages_id_inline = [f'less_lang-1--lesson_id-{language.id}' for language in languages]
    keyboard = await genButton.inline_b(languages_name, languages_id_inline, 2)
    keyboard['inline_keyboard'].append([{'text': '↩️Назад', 'callback_data': 'back_menu'}])
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        text=text, 
        reply_markup=keyboard
        )
    await callback.answer()


@router.callback_query(F.data.regexp(r'^less_lang'))
async def teachers_of_language_lessons(callback: types.CallbackQuery, bot: Bot):
    data = await get_desh_args(callback.data)
    lesson_id = data.get('lesson_id',)
    current_page = data.get('current_page', 1)
    rows_per_page = 2
    total_rows = await db.get_count_teachers_of_language_lesson(lesson_id=lesson_id,)
    buttons_next_back = await determine_navigation(
        total_rows=total_rows,
        current_page=current_page,
        rows_per_page=rows_per_page,
        prefix='less_lang-1',
        params={'lesson_id': lesson_id},
        button_return_callback=f"languages",
        )
    teachers_of_language_lesson = await db.get_teachers_of_language_lesson(
        lesson_id=lesson_id,
        current_page=current_page,
        rows_per_page=rows_per_page
        )
    lesson = await db.get_lesson_of_language(lesson_id=lesson_id)
    text, buttons_teachers = await teachers_page(
        teachers=teachers_of_language_lesson,
        lesson=lesson,
        prefix="teacher_language-1",
        current_page=current_page,
        rows_per_page=rows_per_page,
        total_rows=total_rows,
        )
    await bot.edit_message_text(
        text=text, 
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[buttons_teachers, buttons_next_back]),
        )
    await callback.answer()


@router.callback_query(F.data.regexp(r'^teacher_language-1'))
async def message_show_teacher_profile(callback: types.InlineQuery, bot: Bot):
    data = await get_desh_args(callback.data)
    lesson_id = data.get('lesson_id',)
    current_page = data.get('current_page',)
    teacher_id = data.get('teacher_id',)
    button_return = [
        types.InlineKeyboardButton(
        text="↩️Назад",
        callback_data="less_lang-1--lesson_id-{lesson_id}--current_page-{current_page}".format(
            lesson_id=lesson_id,
            current_page=current_page,
            )
        )
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[button_return])
    text = await teacher_profile(teacher_id=teacher_id)
    await bot.edit_message_text(
        text=text,
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=keyboard
        )
    await callback.answer()
