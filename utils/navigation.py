import math
from aiogram import types
from databases.db_postgresql import db


async def determine_navigation(
    total_rows: int, current_page, rows_per_page, 
    prefix: str = '', params: dict = {}, button_return_callback: str = None
    ):
    total_pages = total_rows // rows_per_page + (1 if total_rows % rows_per_page != 0 else 0)
    back_button = current_page > 1
    next_button = current_page < total_pages 
    data = "--".join([f"{i}-{j}" for i, j in zip(params.keys(), params.values())])
    buttons = []
    if back_button:
        buttons.append(
            types.InlineKeyboardButton(text=f"◀️{current_page-1}", callback_data=f"{prefix}--current_page-{current_page-1}--{data}")
        )
    if button_return_callback is not None:
        buttons.append(
            types.InlineKeyboardButton(text="↩️Назад", callback_data=button_return_callback)
    )
    if next_button:
        buttons.append(
            types.InlineKeyboardButton(text=f"{current_page+1}▶️", callback_data=f"{prefix}--current_page-{current_page+1}--{data}")
        )
    return buttons


async def truncate_text(text, max_length: int, max_lines: int) -> str:
    lines = text.splitlines()[:max_lines]
    truncated_length = sum(len(line) for line in lines)
    if truncated_length > max_length:
        last_line = lines[-1] if lines[-1] != '' else lines[-2]
        truncated_length -= len(last_line)
        truncated_text = ''
        for line in lines:
            if truncated_length + len(line) <= max_length:
                truncated_text += line + '\n'
                truncated_length += len(line)
            else:
                break
    else:
        truncated_text = '\n'.join(lines) + '.....'
    return truncated_text


async def teachers_page(
    teachers, lesson,
    prefix: str,
    total_rows: int, current_page: int = 1, rows_per_page: int = 3
    ) -> str and list:
    
    result = "<b>Репетиторы по предмету:</b> {lesson_name}\n\n".format(lesson_name=lesson.name)
    numbers = {
        "0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣", 
        "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"
        }
    buttons = []
    for i, teacher in enumerate(teachers):    
        number_emoji = ''.join([numbers.get(i) for i in str(current_page*rows_per_page+i-1)])
        buttons.append(
            types.InlineKeyboardButton(
                text=number_emoji, 
                callback_data='{prefix}--teacher_id-{teacher_id}--lesson_id-{lesson_id}--current_page-{current_page}'.\
                    format(
                        prefix=prefix,
                        teacher_id=teacher.id,
                        lesson_id=lesson.id,
                        current_page=current_page,
                    )
            )
        )
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
            name = teacher.name,
            login = teacher.login,
            lessons = teacher.lessons,
            location = teacher.location,
            description = description,
            price = teacher.price,
            )
    end = "<b>Page:</b> {current_page}/{total_rows}".format(
        current_page=current_page, 
        total_rows=math.ceil(total_rows/rows_per_page)
        )
    return result + end, buttons


async def teacher_profile(teacher_id: int) -> str:
    teacher = await db.get_teacher_profile(teacher_id)
    result = \
        "👩‍🏫 <b>{name} - @{login}</b>\n"\
        "📚 {lessons} \n"\
        "📍 {location}\n"\
        "💳 {price} Kč/hod\n\n"\
        "📝 {description}\n\n"\
        .format(
            name = teacher.name,
            login = teacher.login,
            lessons = teacher.lessons_university,
            location = teacher.location,
            description = teacher.description,
            price = teacher.price,
        ) 
    return result   
    

    

