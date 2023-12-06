from aiogram import Router, types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import Tuple

from bot.databases.db_postgresql import db
from bot.databases.db_declaration import Teachers
from bot.text_assets import TextMenu as tm
from bot.utils.callback_factory import CatalogTeacher, CatalogLessons, TypeCatalogLessons


router = Router()


async def teacher_profile_text(teacher: Teachers) -> str:
    """
    Generate text for teacher profile

    Args:
        teacher (Teachers): Teacher

    Returns:
        str: Text for teacher profile
    """
    # Lessons
    lessons_university = "\n📚" + ", ".join([lesson.name for lesson in teacher.lesson_university]) + "\n" if teacher.lesson_university else ""
    lessons_language = "🔠" + ", ".join([lesson.name for lesson in teacher.lesson_language]) + "\n" if teacher.lesson_language else ""

    # Text body
    try:
        result = \
            "👩‍🏫 <b>{name} - @{login}</b>\n"\
            "{lessons_university}"\
            "{lessons_language}"\
            "\n📍 {location}\n"\
            "💳 {price}\n\n"\
            "📝 {description}\n\n"\
            .format(
                name = teacher.name,
                login = teacher.user.login,
                lessons_university = lessons_university,
                lessons_language = lessons_language,
                location = teacher.location,
                description = teacher.description,
                price = teacher.price,
            )
    except Exception as e:
        raise e
    
    return result


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
