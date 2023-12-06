import re
import random

from aiogram import Router, types, Bot, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.input_text_message_content import InputTextMessageContent


from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm
from bot.utils.navigation import *

router = Router()


@router.callback_query(F.data == 'lessons')
async def handler_lessons_category(query: types. CallbackQuery, bot: Bot):
    """
    Show menu for catalog of all lessons.

    🏠 Main menu of catalog
    ...
    │
    └── 📑 Menu of of all lessons with categories (THIS HANDLER)
        ├── 📚 Catalog of all lessons
        │   └── 👩‍🏫 Teachers of selected Lesson
        │       └── 👤 Teacher profile
        │
        └── 🔎 Search lessons by name 
            └── 👩‍🏫 Teachers of selected Lesson
                └── 👤 Teacher profile
    """
    # Text
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    text = tm.TeachersCategory.text_lessons_search.get(user_language, 'ru')
    
    # Make buttons
    builder = tm.TeachersCategory.kb_lessons_category(user_language)
    keyboard = builder.as_markup()
    
    # Send message
    await bot.edit_message_text(
        text=text_head + text, 
        chat_id=query.from_user.id, 
        message_id=query.message.message_id, 
        reply_markup=keyboard
        )


@router.callback_query(CatalogGoogle.filter())
async def handler_catalog_lessons(query: types.CallbackQuery, bot: Bot, callback_data: CatalogGoogle):
    """
    Show list of all lessons.

    🏠 Main menu of catalog
    ...
    │
    └── 📑 Menu of of all lessons with categories
        ├── 📚 Catalog of all lessons (THIS HANDLER)
        │   └── 👩‍🏫 Teachers of selected Lesson
        │       └── 👤 Teacher profile
        │
        └── 🔎 Search lessons by name 
            └── 👩‍🏫 Teachers of selected Lesson
                └── 👤 Teacher profile
    """
    # Text
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')

    # Make buttons with lessons
    rows_per_page = 10
    current_page = callback_data.current_page
    lessons = await db.get_all_lessons(exclude_null_teachers=True)
    total_rows = len(lessons)
    lessons = await db._slice_request(lessons, current_page, rows_per_page)
    
    builder = InlineKeyboardBuilder()
    for lesson in lessons:
        if isinstance(lesson, LessonsUniversity):
            lesson_type = TypeLessons.university
        elif isinstance(lesson, LessonsLanguage):
            lesson_type = TypeLessons.language
        else:
            continue

        builder.button(
            text=lesson.name, # type: ignore
            callback_data=CatalogLessons(
                lesson_id=lesson.id, # type: ignore
                lesson_type=lesson_type,
                lesson_return_type=TypeCatalogLessons.lessons_all,
                current_page=current_page,
            )
        )
    builder.adjust(2)

    # Make buttons with navigation
    buttons_next_back = await determine_navigation(
        total_rows=total_rows, 
        current_page=current_page, 
        rows_per_page=rows_per_page,
        back_callback=CatalogGoogle(
            current_page=current_page-1,
            ).pack(),
        next_callback=CatalogGoogle(
            current_page=current_page+1,
            ).pack(),
        return_callback="lessons",
        )
    builder.row(*buttons_next_back)

    # Send message
    await bot.edit_message_text(
        text=text_head,
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
    )


@router.inline_query()
async def show_univerity_teachers(inline_query: types.InlineQuery, bot: Bot) -> None:
    """
    Inline query handler for search lessons by name in inline mode.

    🏠 Main menu of catalog
    ...
    │
    └── 📑 Menu of of all lessons with categories
        ├── 📚 Catalog of all lessons
        │   └── 👩‍🏫 Teachers of selected Lesson
        │       └── 👤 Teacher profile
        │
        └── 🔎 Search lessons by name (THIS HANDLER)
            └── 👩‍🏫 Teachers of selected Lesson
                └── 👤 Teacher profile
    """
    result = await get_inline_query_result(bot, inline_query)
    await inline_query.answer(result, cache_time=10)


def remove_tags(text: str) -> str:
    """
    Remove potential bad symbols/tags from text

    Args:
        text (str): text to remove bad symbols

    Returns:
        str: text without bad symbols
    """
    clean = re.compile('<.*?>')  
    return re.sub(clean, '', text)


async def remove_diacritics(text: str) -> str:
    """
    Remove and replace diacritics from text to normal letters

    Args:
        text (str): text to remove diacritics

    Returns:
        str: text with normal letters
    """
    diacritics = {
        'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e',
        'í': 'i', 'ň': 'n', 'ó': 'o', 'ř': 'r', 'š': 's',
        'ť': 't', 'ú': 'u', 'ů': 'u', 'ý': 'y', 'ž': 'z',
    }
    for diacritic, letter in diacritics.items():
        text = text.lower().replace(diacritic, letter)
    return text


async def generate_deep_link(bot: Bot) -> str:
    bot_user = await bot.get_me()
    bot_username = bot_user.username
    deeplink = f"https://t.me/{bot_username}?start"
    return deeplink


async def get_inline_query_result(bot: Bot, inline_query: types.InlineQuery) -> List[types.InlineQueryResultArticle]:
    """
    Get inline query results for a given bot and inline query.
    
    Args:
        bot (Bot): The bot instance.
        inline_query (types.InlineQuery): The inline query instance.
    
    Returns:
        List[types.InlineQueryResultArticle]: The list of inline query results.
    """
    result = []
    query = inline_query.query
    chat_type = inline_query.chat_type
    query = await remove_diacritics(query)
    lessons = await db.get_all_lessons(exclude_null_teachers=True)
    deep_link = await generate_deep_link(bot)
    for lesson in lessons:
        
        lesson_name = await remove_diacritics(lesson.name.lower())
        lesson_code = str(lesson.code) if isinstance(lesson, LessonsUniversity) and lesson.code is not None else ""

        if not query or query.lower() in lesson_name or query.lower() in lesson_code:

            count_teachers = 0
            teachers = None
            name_university = ""
            # If lesson of university
            if isinstance(lesson, LessonsUniversity):
                teachers = await db.get_teachers_of_university_lesson(lesson.id, exclude_null_teachers=True)
                lesson_type = TypeLessons.university
                name_university = f"\n🏫 School: {', '.join(university.name for university in lesson.university)}" if lesson.university else ""
            
            # If lesson of language
            elif isinstance(lesson, LessonsLanguage):
                teachers = await db.get_teachers_of_language_lesson(lesson.id, exclude_null_teachers=True)
                lesson_type = TypeLessons.language

            else:
                raise ValueError("Unknown lesson type")
            
            count_teachers = teachers.count() if teachers else 0

            builder = InlineKeyboardBuilder()
            
            # If lesson have teachers - add button
            if count_teachers:
                text = "👩‍🏫 Show teachers!"
                # If user search lesson in private chat
                if chat_type == 'sender':
                    builder.button(
                        text=text,
                        callback_data=CatalogLessons(
                            lesson_id=lesson.id,
                            lesson_type=lesson_type,
                            university_id=-1,
                            current_page=1,
                        )
                    )
                # If user search lesson in group chat
                else:
                    builder.button(
                        text=text,
                        url=deep_link
                    )  
            
            # Arcticle data
            title = f"📚 Lesson: {lesson.name}"
            if lesson_code: title += f" - {lesson.code}"
            input_text = f"\n👩‍🏫 Teachers: {count_teachers}" + name_university    
            input_message_content = InputTextMessageContent(message_text=f"📚 <b>Lesson: {lesson.name}</b> {input_text}", parse_mode="HTML")
            thumbnail_url = lesson.university[0].link_image if isinstance(lesson, LessonsUniversity) and lesson.university and lesson.university[0].link_image else None

            # Add query result to list
            result.append(
                types.InlineQueryResultArticle(
                    id=str(random.getrandbits(128)),
                    title=title,
                    input_message_content=input_message_content,
                    description=remove_tags(input_text),
                    thumbnail_url=thumbnail_url,
                    hide_url=True,
                    reply_markup=builder.as_markup()
                    )
                )          
    return result

