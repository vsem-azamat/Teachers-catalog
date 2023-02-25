import random
from aiogram import Router, types, Bot, F
from aiogram.types import InputTextMessageContent, InputMediaPhoto
from aiogram.filters import CommandStart

from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.gen_button import genButton

router = Router()


@router.inline_query()
async def show_univerity_teachers(inline_query: types.InlineQuery, bot: Bot):
    result = await get_inline_query_result(inline_query.query)
    await inline_query.answer(result)


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
    result = []
    query = await remove_diacritics(query)
    lessons = await db.get_all_lessons()
    for lesson in lessons:
        if not query or query.lower() in lesson.name.lower() or lesson.code and query.lower() in lesson.code.lower():
            input_content = InputTextMessageContent(
                message_text=f"input_message_content: {lesson.id}"
            )
            lesson_code = ""
            if lesson.code: lesson_code = f" - {lesson.code}"
            result.append(
                types.InlineQueryResultArticle(
                    id=random.getrandbits(128),
                    title=f"Предмет: {lesson.name}" + lesson_code,
                    input_message_content=input_content,
                    description=f"description: {lesson.code}",
                    thumb_url=lesson.link_image,
                    hide_url=True,
                    reply_markup=types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                types.InlineKeyboardButton(
                                    text="TEST",
                                    callback_data="test",
                                    )
                            ]
                            
                        ]
                    )
                    )
                )
    return result

