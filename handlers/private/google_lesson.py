import re
import random
from aiogram import Router, types, Bot, F
from aiogram.types import InputTextMessageContent, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.filters import ViaMessageFilter
from utils.callback_factory import PageSettings, PageLevels


router = Router()


@router.message(ViaMessageFilter())
async def read(msg: types.Message, bot: Bot):
    pass

@router.inline_query()
async def show_univerity_teachers(inline_query: types.InlineQuery, bot: Bot):
    result = await get_inline_query_result(inline_query.query)
    await inline_query.answer(result, cache_time=10)


def remove_tags(text):
    clean = re.compile('<.*?>')  
    return re.sub(clean, '', text)


async def remove_diacritics(text):
    diacritics = {
        'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e',
        'í': 'i', 'ň': 'n', 'ó': 'o', 'ř': 'r', 'š': 's',
        'ť': 't', 'ú': 'u', 'ů': 'u', 'ý': 'y', 'ž': 'z',
    }
    for diacritic, letter in diacritics.items():
        text = text.lower().replace(diacritic, letter)
    return text


async def generate_deep_link(bot: Bot):
    bot_user = await bot.get_me()
    bot_username = bot_user.username
    deeplink = f"https://t.me/{bot_username}?start=item_12345"
    return deeplink


async def get_inline_query_result(query: str = ""):
    print(query)
    result = []
    query = await remove_diacritics(query)
    lessons = await db.get_all_lessons()
    for lesson in lessons:
        if not query or query.lower() in lesson.name.lower() or lesson.code and query.lower() in lesson.code.lower():

            if lesson.source == "university":
                count_teachers = await db.get_count_teachers_of_university_lesson(lesson.id)
            elif lesson.source == "language":
                count_teachers = await db.get_count_teachers_of_language_lesson(lesson.id)
            else:
                count_teachers = 0

            name_university = ""
            if lesson.name_university: name_university = f"<b>ВУЗ:</b> {lesson.name_university}"
            
            lesson_code = ""
            if lesson.code: lesson_code = f" - {lesson.code}"
            input_text = \
                f"<b>Предмет:</b> {lesson.name}{lesson_code}"\
                f"\n<b>Репетиторов по предмету:</b> {count_teachers}"\
                f"\n{name_university}"
            input_content = InputTextMessageContent(message_text=input_text, parse_mode="HTML")
            builder = InlineKeyboardBuilder()
            if count_teachers:
                builder.button(
                        text="Показать всех",
                        callback_data=PageSettings(
                            pageLevel=PageLevels.google,
                            source=lesson.source,
                            lesson_id=lesson.id
                            )
                        )
            result.append(
                types.InlineQueryResultArticle(
                    id=random.getrandbits(128),
                    title=f"Предмет: {lesson.name}" + lesson_code,
                    input_message_content=input_content,
                    description=remove_tags(input_text),
                    thumb_url=lesson.link_image,
                    hide_url=True,
                    reply_markup=builder.as_markup()
                    )
                )          
    return result

