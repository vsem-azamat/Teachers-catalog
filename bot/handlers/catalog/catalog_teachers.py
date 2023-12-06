from aiogram import Router, types, F, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import Tuple

from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm
from bot.utils.callback_factory import CatalogTeacher, CatalogLessons, TypeCatalogLessons, TypeLessons, CatalogGoogle, CatalogUniversity
from bot.utils.navigation import determine_navigation, teachers_catalog_text, EMOJI_NUMBERS

router = Router()


async def catalog_teachers(query: types.CallbackQuery, callback_data: CatalogLessons) -> Tuple[str, InlineKeyboardBuilder]:
    """
    Show catalog of teachers of selected lesson (university or language) for selected page

    Args:
        query (types.CallbackQuery): Callback query
        callback_data (Union[CatalogLessonUniversity, CatalogLessonLanguage]): Callback data

    Returns:
        Tuple[str, InlineKeyboardBuilder]: Text and buttons    
    """
    # Text
    user_language = await db.get_user_language(query.from_user.id)
    
    # Make buttons with teachers
    lesson_id = callback_data.lesson_id
    current_page = callback_data.current_page
    rows_per_page = callback_data.rows_per_page

    # Determine lesson type
    if callback_data.lesson_type == TypeLessons.university:
        selected_lessons = await db.get_lesson_of_university(lesson_id=lesson_id)
        university_id = callback_data.university_id
        teachers = await db.get_teachers_of_university_lesson(
            lesson_id=lesson_id,
            current_page=current_page,
            rows_per_page=rows_per_page,
            exclude_null_teachers=True,
            )
    elif callback_data.lesson_type == TypeLessons.language:
        selected_lessons = await db.get_lesson_of_language(lesson_id=lesson_id)
        university_id = None
        teachers = await db.get_teachers_of_language_lesson(
            lesson_id=lesson_id,
            current_page=current_page,
            rows_per_page=rows_per_page,
            exclude_null_teachers=True,
            )
    else:
        raise TypeError("callback_data must be CatalogLessonUniversity or CatalogLessonLanguage")
    
    total_rows = teachers.count()
    builder = InlineKeyboardBuilder()

    # Build buttons with teachers
    for idx, teacher in enumerate(teachers, start=1):
        builder.button(
            text="".join([EMOJI_NUMBERS.get(i, '?') for i in str((current_page-1)*rows_per_page+idx)]),
            callback_data=CatalogTeacher(
                lesson_id=lesson_id,
                lesson_type=callback_data.lesson_type,
                lesson_return_type=callback_data.lesson_return_type,
                university_id=university_id,
                current_page=current_page,
                teacher_id_tg=teacher.id_tg, # type: ignore
            )
        )

    # Build return button
    return_callback = None
    # Return -> List of lessons of university
    if callback_data.lesson_return_type == TypeCatalogLessons.lessons_university and callback_data.university_id:
        return_callback = CatalogUniversity(
            university_id=callback_data.university_id
            ).pack()
    # Return -> List of lessons of language
    elif callback_data.lesson_return_type == TypeCatalogLessons.lessons_languages:
        return_callback = "languages"
    # Return -> List of all lessons
    elif callback_data.lesson_return_type == TypeCatalogLessons.lessons_all:
        return_callback = CatalogGoogle(
            current_page=callback_data.current_page,
            ).pack()        

    # Build buttons with navigation
    navigation_buttons = await determine_navigation(
        total_rows=total_rows,
        current_page=current_page,
        rows_per_page=rows_per_page,

        back_callback=CatalogLessons(
            lesson_id=lesson_id,
            lesson_type=callback_data.lesson_type,
            university_id=university_id,
            current_page=current_page-1,
            ).pack(),
        next_callback=CatalogLessons(
            lesson_id=lesson_id,
            lesson_type=callback_data.lesson_type,
            university_id=university_id,
            current_page=current_page+1,
            ).pack(),
        return_callback=return_callback,
        )
    builder.row(*navigation_buttons)
    
    # Build text
    text = await teachers_catalog_text(
        teachers=teachers,
        lesson=selected_lessons,
        user_language=user_language,
        current_page=current_page,
        rows_per_page=rows_per_page,
        total_rows=total_rows,
        )
    
    return text, builder



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

