import math
import random
from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import InputTextMessageContent

from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.filters import FindTeachersFilter, UnivLessonsFilter
from utils.gen_button import genButton

router = Router()


async def get_desh_args(text: str) -> list:
    """
    {key: value, key: values} 
     
    key-values--key-values
    """
    return {x.split('-')[0]: int(x.split('-')[1]) for x in text.split('--')}


@router.callback_query(F.data == 'back_menu')
@router.message(FindTeachersFilter())
async def category_teachers(msg: types.Message or types.CallbackQuery):
    user_lang = await db.get_user_lang(msg.from_user.id)
    text = tm.FindTeachers.text_find_teachers[user_lang]
    keyboard = tm.FindTeachers.kb_teachers_category(user_lang)
    if isinstance(msg, types.Message):
        await msg.answer(text=text, reply_markup=keyboard)
    elif isinstance(msg, types.CallbackQuery):
        await msg.message.edit_text(text=text, reply_markup=keyboard)


@router.inline_query(F.query == 'univ')
async def show_univerity_teachers(inline_query: types.InlineQuery, bot: Bot):
    result = await get_inline_query_result(bot)
    await inline_query.answer(result)


async def get_inline_query_result(bot: Bot):
    result = []
    univ_list = await db.get_universities()
    for univ in univ_list:
        deep_link = await generate_deep_link(bot)
        input_content = InputTextMessageContent(
            message_text=f"input_message_content: {univ}"
        )
        result.append(types.InlineQueryResultArticle(
            id=random.getrandbits(128),
            title=f"title: {univ}",
            input_message_content=input_content,
            description=f"description: {univ}",
            # thumb_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/How_to_use_icon.svg/2214px-How_to_use_icon.svg.png',
            thumb_url='https://i.imgur.com/wWRsfS5.jpeg',
            url=deep_link,
            hide_url=True
        ))
    return result


async def generate_deep_link(bot: Bot):
    bot_user = await bot.get_me()
    bot_username = bot_user.username
    deeplink = f"https://t.me/{bot_username}?start=item_12345"
    return deeplink


@router.callback_query(F.data == 'univ')
async def list_universities(callback: types.CallbackQuery, bot: Bot):
    await callback.answer()
    user_lang = await db.get_user_lang(callback.from_user.id)
    text = tm.FindTeachers.ti_for_university[user_lang]
    record = await db.get_universities()
    universities_name = [row.name for row in record]
    universities_id_inline = [f'univ_id-{row.id}' for row in record]
    keyboard = await genButton.inline_b(universities_name, universities_id_inline, 2)
    keyboard['inline_keyboard'].append([{'text': 'НАЗАД', 'callback_data': 'back_menu'}])
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        text=text, 
        reply_markup=keyboard
        )


@router.callback_query(F.data.regexp(r'^univ_'))
async def list_university_lessons(callback: types.CallbackQuery, bot: Bot):
    """
    Show list of selected Lessons University
    """
    await callback.answer()
    univ_id = int(callback.data[8:])
    lessons = await db.get_university_lessons(univ_id)
    lessons_name = [lesson.name for lesson in lessons]
    lessons_id_inline = [f'lesson_univ_lesson_id-{lesson.id}--page-1' for lesson in lessons]
    keyboard = await genButton.inline_b(lessons_name, lessons_id_inline, 2)
    keyboard['inline_keyboard'].append([{'text': 'НАЗАД', 'callback_data': 'univ'}])
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Lessons of university',
        reply_markup=keyboard
    )





@router.callback_query(F.data.regexp(r'^lesson_univ'))
async def list_lesson_teachers(callback: types.CallbackQuery, bot: Bot):
    await callback.answer()
    data = await get_desh_args(callback.data[12:])
    lesson_id = data.get('lesson_id')
    current_page = data.get('page', 1)
    rows_per_page = 2
    total_rows = await db.get_teachers_univ_profiles_count(
        lesson_id=lesson_id,
        )
    keyboard = await determine_navigation(
        total_rows=total_rows,
        current_page=current_page,
        rows_per_page=rows_per_page,
        prefix='lesson_univ_',
        params={'lesson_id': lesson_id}
        )
    text = await get_teachers_page(
        lesson_id=lesson_id, 
        current_page=current_page,
        rows_per_page=rows_per_page,
        total_rows=total_rows
        )
    
    await bot.edit_message_text(
        text=text, 
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[keyboard]),
        )


async def determine_navigation(
    total_rows: int, current_page, rows_per_page, 
    prefix: str = '', params: dict = {}, menu: dict = {}
    ):
    total_pages = total_rows // rows_per_page + (1 if total_rows % rows_per_page != 0 else 0)
    back_button = current_page > 1
    next_button = current_page < total_pages 
    data = "--".join([f"{i}-{j}" for i, j in zip(params.keys(), params.values())])
    buttons = []
    if back_button:
        buttons.append(
            types.InlineKeyboardButton(text=f"◀️{current_page-1}", callback_data=f"{prefix}page-{current_page-1}--{data}")
        )
    if next_button:
        buttons.append(
            types.InlineKeyboardButton(text=f"{current_page+1}▶️", callback_data=f"{prefix}page-{current_page+1}--{data}")
        )
    return buttons



async def get_teachers_page(lesson_id: int, total_rows: int, current_page: int = 1, rows_per_page: int = 3) -> str:
    lesson_info = await db.get_lesson_info(lesson_id=lesson_id)
    teachers = await db.get_teachers_univ_profiles(
        lesson_id=lesson_id, 
        page=current_page, 
        rows=rows_per_page)
    result = "<b>Репетиторы по предмету:</b> {lesson_name}\n\n".format(lesson_name=lesson_info.name)
    for teacher in teachers:    
        link = "https://t.me/testing_people_bot?start=teacher_id-{teacher_id}--lesson_id-{lesson_id}--page-{current_page}".\
            format(teacher_id=teacher.id, lesson_id=lesson_info.id, current_page=current_page)
        description_univ = await truncate_text(teacher.description_univ, 225, 4)
        text = \
            "〰️〰️〰️〰️1️⃣〰️〰️〰️〰️\n"\
            "👩‍🏫 <b>{name} - @{login}</b>\n"\
            "📚 {lessons} \n"\
            "📍 Прага, дискорд\n"\
            "💳 {price} Kč/hod\n\n"\
            "📝 {description}\n"\
            "<b><a href='{link}'>Подробнее</a></b>\n\n"
        result += text.format(
            name = teacher.name,
            login = teacher.login,
            lessons = teacher.lessons,
            description = description_univ,
            price = teacher.price,
            link = link,
            )
    end = "<b>Page:</b> {current_page}/{total_rows}".format(
        current_page=current_page, 
        total_rows=math.ceil(total_rows/rows_per_page)
        )
    return result + end


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


@router.message(CommandStart(deep_link=True))
async def message_show_teacher_profile(msg: types.Message, command: CommandObject):
    deep_link = command.args
    args = await get_desh_args(deep_link)



@router.message(Command('q'))
async def q_test(msg: types.Message):
    # q = await get_teachers_page(10)
    # await msg.answer(q)
    t = "Я занимаюсь репетиторством уже более 5 лет и за это время помог многим\nученикам достичь успеха в учебе. Я предлагаю индивидуальный подход и\nгибкий график занятий. Я занимаюсь репетиторством уже более 5 лет и за\nэто время помог многим"
    await msg.answer(t)
