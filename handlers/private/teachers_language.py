from aiogram import Router, types, F, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from databases.db_postgresql import db
from text_assets import TextMenu as tm

from utils.callback_factory import *
from utils.navigation import *

router = Router()


# Show list of Languages
@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.lessons_language))
@router.callback_query(F.data == 'languages')
async def list_universities(callback: types.CallbackQuery, bot: Bot):
    user_language = await db.get_user_language(callback.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    text = tm.TeachersCategory.text_select_language.get(user_language, 'ru')
    languages = await db.get_lessons_languages()

    builder = InlineKeyboardBuilder()
    for language in languages:
        builder.button(
            text = language.name,
            callback_data=PageSettings(
                pageLevel=PageLevels.teachers_language,
                lesson_id=language.id,
            )
        )
    columns_per_row = PageSettings().columns_per_row
    builder.adjust(columns_per_row)
    builder.row(types.InlineKeyboardButton(text='↩️', callback_data='back_menu'))
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        text=text_head + text, 
        reply_markup=builder.as_markup()
        )
    await callback.answer()


# Show list of Teachers
@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.teachers_language))
async def teachers_of_language_lessons(query: types.CallbackQuery, callback_data: PageSettings, bot: Bot):
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    lesson_id = callback_data.lesson_id
    current_page = callback_data.current_page
    rows_per_page = PageSettings().rows_per_page
    columns_per_row = PageSettings().columns_per_row
    total_rows = await db.get_count_teachers_of_language_lesson(lesson_id=lesson_id,)
    
    builder = InlineKeyboardBuilder()
    teachers_of_language_lesson = await db.get_teachers_of_language_lesson(
        lesson_id=lesson_id,
        current_page=current_page,
        rows_per_page=rows_per_page
        )
    for i, teacher in enumerate(teachers_of_language_lesson):
        builder.button(
            text = ''.join([numbers.get(i) for i in str(current_page*rows_per_page+i-1)]),
            callback_data=PageSettings(
                pageLevel=PageLevels.teacher_language,
                lesson_id=lesson_id,  
                current_page=current_page,  
                teacher_id=teacher.id,   
            )
        )
    buttons_next_back = await determine_navigation(
        total_rows=total_rows, 
        current_page=current_page, 
        rows_per_page=rows_per_page,
        back_button=PageSettings(
            pageLevel=PageLevels.teachers_language,
            current_page=current_page-1,
            lesson_id=lesson_id,
            ),
        next_button=PageSettings(
            pageLevel=PageLevels.teachers_language,
            current_page=current_page+1,
            lesson_id=lesson_id
            ),
        return_button=PageSettings(
            pageLevel=PageLevels.lessons_language,
            lesson_id=lesson_id,
            current_page = current_page,
            ),
        )
    builder.adjust(columns_per_row)
    builder.row(*buttons_next_back)
    lesson = await db.get_lesson_of_language(lesson_id=lesson_id)
    teachers_of_language_lesson = await db.get_teachers_of_language_lesson(
        lesson_id=lesson_id,
        current_page=current_page,
        rows_per_page=rows_per_page
        )
    text = await teachers_page_text(
        teachers=teachers_of_language_lesson,
        lesson=lesson,
        user_language=user_language,
        current_page=current_page,
        rows_per_page=rows_per_page,
        total_rows=total_rows,
        )
    try:
        await bot.edit_message_text(
            text=text, 
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            reply_markup=builder.as_markup(),
        )
    except AttributeError:
        await bot.send_message(
            chat_id=query.from_user.id,
            text=text_head + text,
            reply_markup=builder.as_markup(),
        )
    await query.answer()


# Show a teacher
@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.teacher_language))
async def message_show_teacher_profile(query: types.InlineQuery, bot: Bot, callback_data: PageSettings):
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    lesson_id = callback_data.lesson_id
    current_page = callback_data.current_page
    teacher_id = callback_data.teacher_id
    builder = InlineKeyboardBuilder()
    button_return = await determine_navigation(
        return_button=PageSettings(
            pageLevel=PageLevels.teachers_language,
            lesson_id=lesson_id,
            current_page=current_page
        )
    )
    builder.row(*button_return)
    text = await teacher_profile_text(teacher_id=teacher_id)
    await bot.edit_message_text(
        text=text_head + text,
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
        )
    await query.answer()

