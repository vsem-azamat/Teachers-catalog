import math
from html import escape

from aiogram import types

from text_assets import TextMenu as tm
from databases.db_postgresql import db

emoji_numbers = {
        "0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣", 
        "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"
        }


async def determine_navigation(
    total_rows: int = 1, current_page: int = 1, rows_per_page: int = 1,
    back_button = False, next_button = False, return_button = False
    ):
    total_pages = total_rows // rows_per_page + (1 if total_rows % rows_per_page != 0 else 0)
    back = f"◀️{current_page-1}" if current_page > 1 else False
    next = f"{current_page+1}▶️" if current_page < total_pages else False 
    buttons = []
    if back and back_button:
        buttons.append(
            types.InlineKeyboardButton(
                text=back,
                callback_data=back_button.pack()
            )
        )
    if return_button:
        buttons.append(
            types.InlineKeyboardButton(
                text="↩️",
                callback_data=return_button.pack()
            )
        )
    if next and next_button:
        buttons.append(
            types.InlineKeyboardButton(
                text=next,
                callback_data=next_button.pack()
            )
        )
    return buttons


async def truncate_text(text: str, max_length: int, max_lines: int) -> str:
    lines = text.split('\n')
    if len(lines) > max_lines:
        text = '\n'.join(lines[:max_lines]) + '.....'
        lines = text.split('\n')
    for i, line in enumerate(lines):
        if len(line) > max_length:
            lines[i] = line[:max_length-3] + '.....'
    return '\n'.join(lines)


async def teachers_page_text(
    teachers, lesson, user_language: str,
    total_rows: int, current_page: int = 1, rows_per_page: int = 3
    ) -> str:
    result = tm.TeachersCategory.text_show_teachers.get(user_language, 'ru') + "{lesson_name}\n\n".format(lesson_name=lesson.name)
    for i, teacher in enumerate(teachers, start=1):    
        number_emoji = ''.join([emoji_numbers.get(i) for i in str((current_page-1)*rows_per_page+i)])
        description = await truncate_text(teacher.description, 225, 4)
        text = \
            "{line}\n"\
            "👩‍🏫 <b>{name} - @{login}</b>\n"\
            "📚 {lessons} \n"\
            "📍 {location}\n"\
            "💳 {price} Kč/hod\n\n"\
            "📝 {description}\n\n"
        result += text.format(
            line = f"{number_emoji}〰️〰️〰️〰️〰️〰️〰️〰️"[:15],
            name = escape(teacher.name),
            login = escape(teacher.login),
            lessons = escape(teacher.lessons),
            location = escape(teacher.location),
            description = escape(description),
            price = escape(teacher.price),
            )
    end = "<b>Page:</b> {current_page}/{total_rows}".format(
        current_page=current_page, 
        total_rows=math.ceil(total_rows/rows_per_page)
        )
    return result + end


async def teacher_profile_text(
        teacher_id: int = 0, teacher_id_tg: int = 0, 
        teacher = False, example: bool = False) -> str:
    if example:
        teacher_id = 1

    if not teacher:
        try:
            teacher = await db.get_teacher_profile(teacher_id, teacher_id_tg)
        except Exception:
            return False

    try:
        lessons_university = "\n📚" + teacher.lessons_university
    except TypeError:
        lessons_university = ""
    except AttributeError:
        lessons_university = ""
    try:
        lessons_language = "\n🔠" + teacher.lessons_language
    except TypeError:
        lessons_language = ""
    except AttributeError:
        lessons_language = ""

    try:
        result = \
            "👩‍🏫 <b>{name} - @{login}</b>"\
            "{lessons_university}"\
            "{lessons_language}"\
            "\n📍 {location}\n"\
            "💳 {price}\n\n"\
            "📝 {description}\n\n"\
            .format(
                name = teacher.name,
                login = teacher.login,
                lessons_university = lessons_university,
                lessons_language = lessons_language,
                location = teacher.location,
                description = teacher.description,
                price = teacher.price,
            ) 
    except AttributeError:
        return "Teacher Error"
    return result


async def detect_bad_symbols(text: str):
    bad_symbols = ['`', '[', ']', '~', '#', '+', '=', '|', '{', '}', '<', '>', ':']
    return any(char in text for char in bad_symbols)

