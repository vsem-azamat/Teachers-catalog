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
    user_language = await db.get_user_language(callback.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    text = tm.TeachersCategory.text_select_university.get(user_language, 'ru')
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


@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.lessons_university))
async def list_university_lessons(query: types.CallbackQuery, bot: Bot, callback_data: PageSettings):
    """
    Show list Lessons of selected University
    """
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    text = tm.TeachersCategory.text_select_lesson_of_university.get(user_language, 'ru')
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
    columns_per_row = PageSettings().columns_per_row
    builder.adjust(columns_per_row)
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
        text=text_head + text,
        reply_markup=builder.as_markup()
    )
    await query.answer()


@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.teachers_university))
async def teachers_of_university_lessons(query: types.CallbackQuery, bot: Bot, callback_data: PageSettings):
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')

    lesson_id = callback_data.lesson_id
    university_id = callback_data.university_id
    current_page = callback_data.current_page
    rows_per_page = PageSettings().rows_per_page
    columns_per_row = PageSettings().columns_per_row
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
    returnPageLevel = PageLevels.lessons_university
    if callback_data.lesson_catalog: returnPageLevel = PageLevels.lessons_catalog
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
            pageLevel=returnPageLevel,
            lesson_id=lesson_id,
            university_id=university_id,
            current_page = current_page,
            rows_per_page = rows_per_page,
            )
    )
    builder.adjust(columns_per_row)
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
        user_language=user_language,
        current_page=current_page,
        rows_per_page=rows_per_page,
        total_rows=total_rows
    )
    try:
        await bot.edit_message_text(
            text=text, 
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            reply_markup=builder.as_markup()
            )
    except AttributeError:
        await bot.send_message(
            chat_id=query.from_user.id,
            text=text_head + text,
            reply_markup=builder.as_markup()
        )
    await query.answer()


@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.teacher_university))
async def message_show_teacher_profile(query: types.InlineQuery, bot: Bot, callback_data: PageSettings):
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
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
        text=text_head + text,
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
        )
    await query.answer()

