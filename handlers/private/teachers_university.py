from aiogram import Router, types, F, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from databases.db_postgresql import db
from text_assets import TextMenu as tm

from utils.navigation import *
from utils.callback_factory import *

router = Router()


@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.universities))
@router.callback_query(F.data == 'universities')
async def list_universities(callback: types.CallbackQuery, bot: Bot):
    user_lang = await db.get_user_lang(callback.from_user.id)
    text = tm.FindTeachers.ti_universities[user_lang]
    universities = await db.get_universities()
    builder = InlineKeyboardBuilder()
    for university in universities:
        builder.button(
            text = university.name,
            callback_data=PageSettings(
                pageLevel=PageLevels.lessons_university,
                university_id=university.id
            )
        )
    rows_per_page = PageSettings().rows_per_page
    builder.adjust(rows_per_page)
    builder.row(types.InlineKeyboardButton(text='↩️Назад', callback_data='back_menu'))
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        text=text, 
        reply_markup=builder.as_markup()
        )
    await callback.answer()


@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.lessons_university))
async def list_university_lessons(query: types.CallbackQuery, bot: Bot, callback_data: PageSettings):
    """
    Show list of selected Lessons University
    """
    university_id = callback_data.university_id
    current_page = callback_data.current_page
    lessons = await db.get_lessons_of_university(university_id)
    builder = InlineKeyboardBuilder()
    for lesson in lessons:
        builder.button(
            text=lesson.name,
            callback_data=PageSettings(
                pageLevel=PageLevels.teachers_university,
                lesson_id=lesson.id, 
                current_page=current_page,
                university_id=university_id
            )
        )
    rows_per_page = PageSettings().rows_per_page
    builder.adjust(rows_per_page)
    builder.row(*
        await determine_navigation(
            return_button=(
                PageSettings(
                    pageLevel=PageLevels.universities
                )
            )
        )
    )
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text='Lessons of university',
        reply_markup=builder.as_markup()
    )
    await query.answer()


@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.teachers_university))
async def teachers_of_university_lessons(query: types.CallbackQuery, bot: Bot, callback_data: PageSettings):
    lesson_id = callback_data.lesson_id
    university_id = callback_data.university_id
    current_page = callback_data.current_page
    rows_per_page = PageSettings().rows_per_page
    total_rows = await db.get_count_teachers_of_university_lesson(lesson_id=lesson_id)

    builder = InlineKeyboardBuilder()
    teachers = await db.get_teachers_of_university_lesson(
        lesson_id=lesson_id,
        current_page=current_page,
        rows_per_page=rows_per_page,
        )
    for i, teacher in enumerate(teachers):
        builder.button(
            text=''.join([numbers.get(i) for i in str(current_page*rows_per_page+i-1)]),
            callback_data=PageSettings(
                pageLevel=PageLevels.teacher_university,
                lesson_id=lesson_id,
                university_id=university_id,
                current_page=current_page,
                teacher_id=teacher.id
            )
        )
    buttons_next_back = await determine_navigation(
        total_rows=total_rows, 
        current_page=current_page, 
        rows_per_page=rows_per_page,
        back_button=PageSettings(
            pageLevel=PageLevels.teachers_university,
            university_id=university_id,
            current_page=current_page-1,
            lesson_id=lesson_id,
            ),
        next_button=PageSettings(
            pageLevel=PageLevels.teachers_university,
            university_id=university_id,
            current_page=current_page+1,
            lesson_id=lesson_id
            ),
        return_button=PageSettings(
            pageLevel=PageLevels.lessons_university,
            lesson_id=lesson_id,
            university_id=university_id,
            current_page = current_page,
            rows_per_page = rows_per_page,
            )
    )
    builder.adjust(rows_per_page)
    builder.row(*buttons_next_back)
    lesson = await db.get_lesson_of_university(lesson_id=lesson_id)
    teachers = await db.get_teachers_of_university_lesson(
        lesson_id=lesson_id,
        current_page=current_page,
        rows_per_page=rows_per_page,
        )    
    text = await teachers_page_text(
        teachers=teachers,
        lesson=lesson,
        current_page=current_page,
        rows_per_page=rows_per_page,
        total_rows=total_rows
    )
    await bot.edit_message_text(
        text=text, 
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
        )
    await query.answer()


@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.teacher_university))
async def message_show_teacher_profile(query: types.InlineQuery, bot: Bot, callback_data: PageSettings):
    lesson_id = callback_data.lesson_id
    current_page = callback_data.current_page
    teacher_id = callback_data.teacher_id
    university_id=callback_data.university_id
    builder = InlineKeyboardBuilder()
    button_return = await determine_navigation(
        return_button=PageSettings(
            pageLevel=PageLevels.teachers_university,
            lesson_id=lesson_id,
            university_id=university_id,
            current_page=current_page
        )
    )
    builder.row(*button_return)
    text = await teacher_profile_text(teacher_id=teacher_id)
    await bot.edit_message_text(
        text=text,
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
        )
    await query.answer()
