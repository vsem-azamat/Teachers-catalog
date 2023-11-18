from aiogram import Router, types, F, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm

from bot.utils.navigation import *
from bot.utils.callback_factory import *

router = Router()


@router.callback_query(F.data == 'universities')
async def catalog_universitites(callback: types.CallbackQuery, bot: Bot):
    """
    Show list of Universities
    """
    # Text
    user_language = await db.get_user_language(callback.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    text = tm.TeachersCategory.text_select_university.get(user_language, 'ru')
    
    # Make buttons with universities
    universities = await db.get_universities(exclude_null_teachers=True)
    builder = InlineKeyboardBuilder()
    for university in universities:
        builder.button(
            text = university.name, # type: ignore
            callback_data=CatalogUniversity(
                university_id=university.id, # type: ignore
                current_page=1,
            )
        )
    columns_per_row = PageSettings().columns_per_row
    builder.adjust(columns_per_row)
    builder.row(types.InlineKeyboardButton(text='↩️', callback_data='back_menu'))
    # Send message
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        text=text_head + text, 
        reply_markup=builder.as_markup()
        )
    await callback.answer()


@router.callback_query(CatalogUniversity.filter())
async def catalog_university_lessons(query: types.CallbackQuery, bot: Bot, callback_data: CatalogUniversity):
    """
    Show list Lessons of selected University
    """
    # Text
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    text = tm.TeachersCategory.text_select_lesson_of_university.get(user_language, 'ru')
    
    # Make buttons with lessons
    university_id = callback_data.university_id
    current_page = callback_data.current_page
    lessons = await db.get_lessons_of_university(university_id=university_id, exclude_null_teachers=True)
    builder = InlineKeyboardBuilder()
    for lesson in lessons:
        builder.button(
            text=lesson.name, # type: ignore
            callback_data=CatalogLessonUniversity(
                university_id=university_id,
                lesson_id=lesson.id, # type: ignore
                current_page=current_page,
            )
        )
    columns_per_row = PageSettings().columns_per_row
    builder.adjust(columns_per_row)
    builder.row(types.InlineKeyboardButton(text='↩️', callback_data='universities'))

    # Send message
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=text_head + text,
        reply_markup=builder.as_markup()
    )
    await query.answer()


@router.callback_query(F.data == 'languages')
async def catalog_language_lessons(query: types.CallbackQuery, bot: Bot):
    """
    Show list of Languages
    """
    # Text
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    text = tm.TeachersCategory.text_select_language.get(user_language, 'ru')

    # Make buttons with languages
    lessons = await db.get_lessons_of_languages(exclude_null_teachers=True)
    builder = InlineKeyboardBuilder()
    for lesson in lessons:
        builder.button(
            text = lesson.name, # type: ignore
            callback_data=CatalogLessonLanguage(
                lesson_id=lesson.id, # type: ignore
            ).pack()
        )
    columns_per_row = PageSettings().columns_per_row
    builder.adjust(columns_per_row)
    builder.row(types.InlineKeyboardButton(text='↩️', callback_data='back_menu'))

    # Send message
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id, 
        text=text_head + text, 
        reply_markup=builder.as_markup()
        )
    await query.answer()


@router.callback_query(CatalogLessonUniversity.filter())
@router.callback_query(CatalogLessonLanguage.filter())
async def catalog_teachers(query: types.CallbackQuery, bot: Bot, callback_data: Union[CatalogLessonUniversity, CatalogLessonLanguage]):
    """
    Show list of Teachers of selected University Lesson
    """
    # Text and buttons
    text, builder = await teachers_catalog(query=query, callback_data=callback_data)
    # Send message
    try:
        await bot.edit_message_text(
            text=text, 
            chat_id=query.from_user.id,
            message_id=query.message.message_id, 
            reply_markup=builder.as_markup()
            )
    except AttributeError:
        user_language = await db.get_user_language(query.from_user.id)
        text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
        await bot.send_message(
            chat_id=query.from_user.id,
            text=text_head + text,
            reply_markup=builder.as_markup()
        )
    await query.answer()


@router.callback_query(CatalogTeacher.filter())
async def catalog_teacher_profile(query: types.InlineQuery, bot: Bot, callback_data: CatalogTeacher):
    """
    Show Teacher profile
    """
    # Send message
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')

    lesson_id = callback_data.lesson_id
    current_page = callback_data.current_page
    teacher_id_tg = callback_data.teacher_id_tg
    university_id=callback_data.university_id

    # Make return button
    builder = InlineKeyboardBuilder()

    callback_data_return = None
    # If user select teacher from lessons of university
    if callback_data.lesson_language:
        callback_data_return = CatalogLessonLanguage(
            lesson_id=lesson_id,
            current_page=current_page,
        ).pack()
    
    elif callback_data.lesson_university:
        callback_data_return = CatalogLessonUniversity(
            university_id=university_id,
            lesson_id=lesson_id,
            current_page=current_page,
        ).pack()

    # Make keyboard
    if callback_data_return:
        builder.add(types.InlineKeyboardButton(text='↩️', callback_data=callback_data_return))
        keyboard = builder.as_markup()

    # If callback_data_return is None, then it is a first page
    # This variant is used when user use google search
    else:
        callback_data_return = tm.TeachersCategory.kb_teachers_category(user_language)
        keyboard = callback_data_return

    # Text
    teacher = await db.get_teacher(teacher_id_tg)
    text = await teacher_profile_text(teacher)

    # Send message
    await bot.edit_message_text(
        text=text_head + text,
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=keyboard
        )
    await query.answer()
