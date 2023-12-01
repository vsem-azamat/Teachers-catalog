from aiogram import Router, types, F, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import Tuple

from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm

from bot.utils.navigation import *
from bot.utils.callback_factory import *
from bot.config import catalog_config

router = Router()


@router.callback_query(F.data == 'universities')
async def handler_catalog_universitites(callback: types.CallbackQuery, bot: Bot):
    """
    Show list of Universities.

    🏠 Main menu of catalog
    ├── 🏫 List of Universities (THIS HANDLER)
    │   └── 📚 Lessons of selected University
    │       └── 👩‍🏫 Teachers of selected Lesson
    │           └── 👤 Teacher profile
    ...
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
    columns_per_row = catalog_config.ROWS_PER_PAGE_catalog_universities
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
async def handler_catalog_university_lessons(query: types.CallbackQuery, bot: Bot, callback_data: CatalogUniversity):
    """
    Show list Lessons of selected University.

    🏠 Main menu of catalog
    ├── 🏫 List of Universities (THIS HANDLER)
    │   └── 📚 Lessons of selected University
    │       └── 👩‍🏫 Teachers of selected Lesson
    │           └── 👤 Teacher profile
    ...
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
            callback_data=CatalogLessons(
                lesson_id=lesson.id, # type: ignore
                lesson_type=TypeLessons.university,
                lesson_return_type=TypeCatalogLessons.lessons_university,
                university_id=university_id,
                current_page=current_page,
            )
        )
    columns_per_row = catalog_config.COLUMNS_PER_ROW_catalog_lessons
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
    Show list of Languages.

    🏠 Main menu of catalog
    ├── 🔠 List of Languages (THIS HANDLER)
    │   └── 👩‍🏫 Teachers of selected Language
    │       └── 👤 Teacher profile
    ...
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
            callback_data=CatalogLessons(
                lesson_id=lesson.id, # type: ignore
                lesson_type=TypeLessons.language,
                lesson_return_type=TypeCatalogLessons.lessons_languages,
            ).pack()
        )
    columns_per_row = catalog_config.COLUMNS_PER_ROW_catalog_lessons
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


@router.callback_query(CatalogLessons.filter(F.lesson_type == TypeLessons.university))
@router.callback_query(CatalogLessons.filter(F.lesson_type == TypeLessons.language))
async def handler_catalog_teachers(query: types.CallbackQuery, bot: Bot, callback_data: CatalogLessons):
    """
    Show list of any lessons. Can be called from:
        1. Catalog of all lessons
        2. Catalog of university lessons
        3. Catalog of language lessons
        4. Catalog of search results

    🏠 Main menu of catalog
    ├── 🔠 List of Languages
    │   └── 👩‍🏫 Teachers of selected Language (THIS HANDLER)
    │       └── 👤 Teacher profile
    │
    ├── 🏫 List of Universities
    │   └── 📚 Lessons of selected University
    │       └── 👩‍🏫 Teachers of selected Lesson (THIS HANDLER)
    │           └── 👤 Teacher profile
    │
    └── 📑 Menu of of all lessons with categories
        ├── 📚 Catalog of all lessons
        │   └── 👩‍🏫 Teachers of selected Lesson (THIS HANDLER)
        │       └── 👤 Teacher profile
        │
        └── 🔎 Search lessons by name 
            └── 👩‍🏫 Teachers of selected Lesson (THIS HANDLER)
                └── 👤 Teacher profile
    """
    # Text and buttons
    text, builder = await catalog_teachers(query=query, callback_data=callback_data)
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


async def catalog_teacher_profile(query: types.CallbackQuery, callback_data: CatalogTeacher) ->Tuple[str, InlineKeyboardBuilder]:
    """
    Show Teacher profile. Return text with teacher profile and InlineKeyboardBuilder with return button

    Args:
        query (types.CallbackQuery): CallbackQuery
        callback_data (CatalogTeacher): CallbackData for teacher buttons in catalog

    Returns:
        Tuple[str, InlineKeyboardBuilder]: text with teacher profile and InlineKeyboardBuilder with return button
    """

    # Page settings
    lesson_id = callback_data.lesson_id
    lesson_type = callback_data.lesson_type
    current_page = callback_data.current_page
    university_id=callback_data.university_id
    return_catalog_type = callback_data.lesson_return_type

    #-------------- Return button --------------#
    # Return button -> Catalog of language lessons
    if return_catalog_type == TypeCatalogLessons.lessons_languages:
        return_callback = CatalogLessons(
            lesson_id=lesson_id,
            lesson_type=lesson_type,
            lesson_return_type=TypeCatalogLessons.lessons_languages,
            current_page=current_page,
        ).pack()

    # Return button -> Catalog of university lessons
    elif return_catalog_type == TypeCatalogLessons.lessons_university:
        return_callback = CatalogLessons(
            lesson_id=lesson_id,
            lesson_type=lesson_type,
            lesson_return_type=TypeCatalogLessons.lessons_university,
            university_id=university_id,
            current_page=current_page,
        ).pack()

    # Return button -> Catalog of all lessons
    elif return_catalog_type == TypeCatalogLessons.lessons_all:
        return_callback = CatalogLessons(
            lesson_id=lesson_id,
            lesson_type=lesson_type,
            lesson_return_type=TypeCatalogLessons.lessons_all,
            current_page=current_page,
        ).pack()

    # Return button ->
    # TODO: Add return button for search results
    else:
        return_callback = 'back_menu'
    
    # Build return button
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='↩️', callback_data=return_callback))

    #-------------- Teacher profile --------------#
    # Text head
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    
    # Text teacher
    teacher_id_tg = callback_data.teacher_id_tg
    teacher = await db.get_teacher(teacher_id_tg)
    text_teacher = await teacher_profile_text(teacher)
    
    # Make final text
    text = text_head + text_teacher

    return text, builder
    

@router.callback_query(CatalogTeacher.filter())
async def handler_catalog_teacher_profile(query: types.CallbackQuery, bot: Bot, callback_data: CatalogTeacher):
    """
    Show Teacher profile.

    🏠 Main menu of catalog
    ├── 🔠 List of Languages
    │   └── 👩‍🏫 Teachers of selected Language
    │       └── 👤 Teacher profile (THIS HANDLER)
    │
    ├── 🏫 List of Universities
    │   └── 📚 Lessons of selected University
    │       └── 👩‍🏫 Teachers of selected Lesson
    │           └── 👤 Teacher profile (THIS HANDLER)
    │
    └── 📑 Menu of of all lessons with categories
        ├── 📚 Catalog of all lessons
        │   └── 👩‍🏫 Teachers of selected Lesson
        │       └── 👤 Teacher profile (THIS HANDLER)
        │
        └── 🔎 Search lessons by name 
            └── 👩‍🏫 Teachers of selected Lesson
                └── 👤 Teacher profile (THIS HANDLER)
    """
    text, builder = await catalog_teacher_profile(query=query, callback_data=callback_data)    
    keyboard = builder.as_markup()

    # Send message
    await bot.edit_message_text(
        text=text,
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=keyboard
        )
    await query.answer()
