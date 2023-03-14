import re
import random

from aiogram import Router, types, Bot, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.input_text_message_content import InputTextMessageContent


from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.callback_factory import PageSettings, PageLevels
from utils.navigation import *

router = Router()

@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.lessons))
@router.callback_query(F.data == 'lessons')
async def lessons(query: types. CallbackQuery, bot: Bot):
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    text = tm.TeachersCategory.text_lessons_search.get(user_language, 'ru')
    keyboard = tm.TeachersCategory.kb_lessons_category(user_language)
    await bot.edit_message_text(
        text=text_head + text, 
        chat_id=query.from_user.id, 
        message_id=query.message.message_id, 
        reply_markup=keyboard
        )


@router.callback_query(PageSettings.filter(F.pageLevel == PageLevels.lessons_catalog))
async def lessons_catalog(query: types.CallbackQuery, callback_data: PageSettings, bot: Bot):
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')

    rows_per_page = 10
    current_page = callback_data.current_page

    lessons = await db.get_all_lessons(current_page=current_page, rows_per_page=rows_per_page, exclude_null_teachers=True)
    total_rows = await db.get_count_all_lessons(exclude_null_teachers=True)
    builder = InlineKeyboardBuilder()
    # ДОДЕЛАТЬ
    for lesson in lessons:
        if lesson.source == 'university':
            source = PageLevels.teachers_university
        else:
            source = PageLevels.teachers_language

        builder.button(
            text=lesson.name,
            callback_data=PageSettings(
                pageLevel=source,
                lesson_id=lesson.id,
                current_page=current_page,
                lesson_catalog=1
            )
        )
    builder.adjust(2)
    buttons_next_back = await determine_navigation(
        total_rows=total_rows, 
        current_page=current_page, 
        rows_per_page=rows_per_page,
        back_button=PageSettings(
            pageLevel=PageLevels.lessons_catalog,
            current_page=current_page-1,
            ),
        next_button=PageSettings(
            pageLevel=PageLevels.lessons_catalog,
            current_page=current_page+1,
            ),
        return_button=PageSettings(
            pageLevel=PageLevels.lessons,
            )
    )
    builder.row(*buttons_next_back)
    await bot.edit_message_text(
        text=text_head,
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
    )


# @router.message(ViaMessageFilter())
# async def read(msg: types.Message, bot: Bot):
#     pass


@router.inline_query()
async def show_univerity_teachers(inline_query: types.InlineQuery, bot: Bot,):
    result = await get_inline_query_result(bot, inline_query)
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
    deeplink = f"https://t.me/{bot_username}?start"
    return deeplink

async def get_inline_query_result(bot: Bot, inline_query: str = "", ):
    result = []
    query = inline_query.query
    chat_type = inline_query.chat_type
    query = await remove_diacritics(query)
    lessons = await db.get_all_lessons(exclude_null_teachers=True)
    deep_link = await generate_deep_link(bot)
    if chat_type == 'sender':
        pass
    for lesson in lessons:
        
        lesson_name = await remove_diacritics(lesson.name.lower())
        lesson_code = ""
        if lesson.code: lesson_code = await remove_diacritics(lesson.code.lower())

        if not query or \
            query.lower() in lesson_name or query.lower() in lesson_code:

            if lesson.source == "university":
                count_teachers = await db.get_count_teachers_of_university_lesson(lesson.id)
                pageLevel = PageLevels.teachers_university
            elif lesson.source == "language":
                count_teachers = await db.get_count_teachers_of_language_lesson(lesson.id)
                pageLevel = PageLevels.teachers_language
            else:
                count_teachers = 0

            name_university = ""
            if lesson.name_university: name_university = f"\n🏫 School: {lesson.name_university}"


            lesson_code = ""
            if lesson.code: lesson_code = f" - {lesson.code}"
            input_text = f"\n👩‍🏫 Teachers: {count_teachers}" + name_university
    
            input_content = InputTextMessageContent(message_text=f"📚 <b>Lesson: {lesson.name}</b> {input_text}", parse_mode="HTML")
            builder = InlineKeyboardBuilder()
            if count_teachers:
                text = "Show teachers!"
                if chat_type == 'sender':
                    builder.button(
                            text=text,
                            callback_data=PageSettings(
                                pageLevel=pageLevel,
                                lesson_id=lesson.id
                                )
                            )
                else:
                    builder.button(
                        text=text,
                        url=deep_link
                    )
            result.append(
                types.InlineQueryResultArticle(
                    id=random.getrandbits(128),
                    title=f"📚 Lesson: {lesson.name}" + lesson_code,
                    input_message_content= input_content,
                    description=remove_tags(input_text),
                    thumb_url=lesson.link_image,
                    hide_url=True,
                    reply_markup=builder.as_markup()
                    )
                )          
    return result

