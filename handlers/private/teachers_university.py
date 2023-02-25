import math
from aiogram import Router, types, F, Bot

from databases.db_postgresql import db
from text_assets import TextMenu as tm

from utils.filters import FindTeachersFilter
from utils.gen_button import genButton
from utils.desh_args import get_desh_args 
from utils.navigation import determine_navigation, teachers_page

router = Router()



@router.callback_query(F.data == 'universities')
async def list_universities(callback: types.CallbackQuery, bot: Bot):
    user_lang = await db.get_user_lang(callback.from_user.id)
    text = tm.FindTeachers.ti_universities[user_lang]
    universities = await db.get_universities()
    universities_name = [university.name for university in universities]
    universities_id_inline = [f'university_id-{university.id}' for university in universities]
    keyboard = await genButton.inline_b(universities_name, universities_id_inline, 2)
    keyboard['inline_keyboard'].append([{'text': '↩️Назад', 'callback_data': 'back_menu'}])
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        text=text, 
        reply_markup=keyboard
        )
    await callback.answer()


@router.callback_query(F.data.regexp(r'^university_id'))
async def list_university_lessons(callback: types.CallbackQuery, bot: Bot):
    """
    Show list of selected Lessons University
    """
    data = await get_desh_args(callback.data)
    university_id = data.get('university_id',)
    lessons = await db.get_lessons_of_university(university_id)
    lessons_name = [lesson.name for lesson in lessons]
    lessons_id_inline = [
        f'less_univ-1--lesson_id-{lesson.id}--current_page-1--university_id-{university_id}' for lesson in lessons
        ]
    keyboard = await genButton.inline_b(lessons_name, lessons_id_inline, 2)
    keyboard['inline_keyboard'].append([{'text': '↩️Назад', 'callback_data': 'universities'}])
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Lessons of university',
        reply_markup=keyboard
    )
    await callback.answer()


@router.callback_query(F.data.regexp(r'^less_univ'))
async def teachers_of_university_lessons(callback: types.CallbackQuery, bot: Bot):
    data = await get_desh_args(callback.data)
    lesson_id = data.get('lesson_id',)
    current_page = data.get('current_page', 1)
    rows_per_page = 2
    total_rows = await db.get_count_teachers_of_university_lesson(lesson_id=lesson_id)
    buttons_next_back = await determine_navigation(
        total_rows=total_rows,
        current_page=current_page,
        rows_per_page=rows_per_page,
        prefix='less_univ-1',
        params={'lesson_id': lesson_id},
        button_return_callback=f"university_id-{lesson_id}",
        )
    teachers_of_university_lesson = await db.get_teachers_of_university_lesson(
        lesson_id=lesson_id,
        current_page=current_page,
        rows_per_page=rows_per_page
        )
    lesson = await db.get_lesson_of_university(lesson_id=lesson_id)
    text, buttons_teachers = await teachers_page(
        teachers=teachers_of_university_lesson,
        lesson=lesson, 
        prefix="teacher_university-1",
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


@router.callback_query(F.data.regexp(r'^teacher_university'))
async def message_show_teacher_profile(callback: types.InlineQuery, bot: Bot):
    data = await get_desh_args(callback.data[19:])
    lesson_id = data.get('lesson_id',)
    current_page = data.get('current_page',)
    teacher_id = data.get('teacher_id',)
    button_return = [
        types.InlineKeyboardButton(
        text="RETURN",
        callback_data="less_univ-lesson_id-{lesson_id}--current_page-{current_page}".format(
            lesson_id=lesson_id,
            current_page=current_page,
            )
        )
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[button_return])
    text = ""
    await bot.edit_message_text(
        text=text,
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=keyboard
        )
    await callback.answer()


##########################
