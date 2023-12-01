import math
from html import escape
from typing import Union, List, Optional, Tuple

from aiogram import types
from sqlalchemy.orm import Query
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.text_assets import TextMenu as tm
from bot.databases.db_postgresql import db
from bot.databases.db_declaration import *
from bot.utils.callback_factory import *

EMOJI_NUMBERS = {
        "0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣", 
        "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"
        }


async def int_to_emoji(number: int) -> str:
    """
    Convert number to emoji

    Args:
        number (int): Number to convert

    Returns:
        str: Emoji number
    """
    return ''.join([EMOJI_NUMBERS.get(i, '?') for i in str(number)])


def detect_bad_symbols(text: str) -> bool:
    """
    Detect special symbols in text which don't allowed in bot

    Args:
        text (str): Text to check

    Returns:
        bool: True if bad symbols detected
    """
    bad_symbols = ['`', '[', ']', '~', '#', '+', '=', '|', '{', '}', '<', '>', ':']
    return any(char in text for char in bad_symbols)


async def truncate_text(text: str, max_length: int = 225, max_lines: int = 4) -> str:
    """
    Truncate text to max_length and max_lines

    Args:
        text (str): Text to truncate
        max_length (int, optional): Max length of text. Defaults to 225.
        max_lines (int, optional): Max lines of text. Defaults to 4.

    Returns:
        str: Truncated text
    """
    lines = text.split('\n')
    if len(lines) > max_lines:
        text = '\n'.join(lines[:max_lines]) + '.....'
        lines = text.split('\n')
    for i, line in enumerate(lines):
        if len(line) > max_length:
            lines[i] = line[:max_length-3] + '.....'
    return '\n'.join(lines)

# TODO: Re-write this function
async def determine_navigation(
    total_rows: int = 1, current_page: int = 1, rows_per_page: int = 1,
    back_callback: Optional[str] = None, next_callback: Optional[str] = None, return_callback: Optional[str] = None
    ) -> List[types.InlineKeyboardButton]:
    """
    Build navigation buttons for catalog. Determine if is back or next buttons needed with current_page and total_rows

    Args:
        total_rows (int, optional): Total rows in query. Defaults to 1.
        current_page (int, optional): Current page. Defaults to 1.
        rows_per_page (int, optional): Rows per page. Defaults to 1.

        back_button (Optional[str], optional): Callback data for back button. Defaults to None.
        next_button (Optional[str], optional): Callback data for next button. Defaults to None.
        return_button (Optional[str], optional): Callback data for return button. Defaults to None.
    
    Returns:
        List[types.InlineKeyboardButton]: List of navigation buttons
    """
    total_pages = total_rows // rows_per_page + (1 if total_rows % rows_per_page != 0 else 0)
    back = f"◀️{current_page-1}" if current_page > 1 else False
    next = f"{current_page+1}▶️" if current_page < total_pages else False 
    buttons = []
    if back and back_callback:
        buttons.append(
            types.InlineKeyboardButton(
                text=back,
                callback_data=back_callback
            )
        )
    if return_callback:
        buttons.append(
            types.InlineKeyboardButton(
                text="↩️",
                callback_data=return_callback
            )
        )
    if next and next_callback:
        buttons.append(
            types.InlineKeyboardButton(
                text=next,
                callback_data=next_callback
            )
        )
    return buttons


async def teachers_catalog_text(
    teachers: Query[Teachers], lesson: Union[LessonsUniversity, LessonsLanguage], user_language: str,
    total_rows: int, current_page: int = 1, rows_per_page: int = 3
    ) -> str:
    """
    Generate text for teachers catalog

    Args:
        teachers (Query[Teachers]): Teachers
        lesson (Union[LessonsUniversity, LessonsLanguage]): Lesson which selected for catalog of teachers
        user_language (str): User language
        total_rows (int): Total rows in query
        current_page (int, optional): Current page. Defaults to 1.

    Returns:
        str: Text for teachers catalog
    """
    text_body = tm.TeachersCategory.text_show_teachers.get(user_language, 'ru') + " {lesson_name}\n\n".format(lesson_name=lesson.name)
    for i, teacher in enumerate(teachers, start=1):    
        teacher_number = (current_page-1)*rows_per_page+i
        teacher_number_emoji = await int_to_emoji(teacher_number)
        lessons = ", ".join([lesson.name for lesson in teacher.lesson_language] + [lesson.name for lesson in teacher.lesson_university])
        description = await truncate_text(teacher.description) # type: ignore
        text = \
            "{line}\n"\
            "👩‍🏫 <b>{name} - @{login}</b>\n"\
            "📚 {lessons} \n"\
            "📍 {location}\n"\
            "💳 {price} Kč/hod\n\n"\
            "📝 {description}\n\n"
        text_body += text.format(
            line = f"{teacher_number_emoji}〰️〰️〰️〰️〰️〰️〰️〰️"[:15],
            name = escape(str(teacher.name)),
            login = escape(str(teacher.user.login)),
            lessons = escape(str(lessons)),
            location = escape(str(teacher.location)),
            price = escape(str(teacher.price)),
            description = escape(description),
            )
    text_end = "<b>Page:</b> {current_page}/{total_rows}".format(
        current_page=current_page, 
        total_rows=math.ceil(total_rows/rows_per_page)
        )
    return text_body + text_end    


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


    
