from aiogram import Router, types, F, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import cnfg_catalog
from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm
from bot.utils.callback_factory import CatalogUniversity, CatalogLessons, TypeLessons, TypeCatalogLessons


router = Router()


@router.callback_query(CatalogUniversity.filter())
async def handler_catalog_university_lessons(query: types.CallbackQuery, bot: Bot, callback_data: CatalogUniversity):
    """
    Show list Lessons of selected University.

    🏠 Main menu of catalog
    ├── 🏫 List of Universities
    │   └── 📚 Lessons of selected University (THIS HANDLER)
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
    columns_per_row = cnfg_catalog.COLUMNS_PER_ROW_catalog_lessons
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
    columns_per_row = cnfg_catalog.COLUMNS_PER_ROW_catalog_lessons
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
