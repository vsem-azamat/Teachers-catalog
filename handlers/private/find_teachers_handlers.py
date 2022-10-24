from aiogram import Router, types, F, Bot, filters
from aiogram.filters import CommandStart
from aiogram.types import InputTextMessageContent

from databases.mongodb import mongodb
from text_assets import TextMenu as tm
from utils.filters import FindTeachersFilter

router = Router()


@router.message(FindTeachersFilter())
async def category_teachers(msg: types.Message):
    user_lang = mongodb.get_user_lang(msg.from_user.id)

    text = tm.FindTeachers.text_find_teachers[user_lang]
    keyboard = tm.FindTeachers.kb_teachers_category(user_lang)
    await msg.answer(text=text, reply_markup=keyboard)


@router.inline_query(F.query == 'univ')
async def show_univerity_teachers(inline_query: types.InlineQuery, bot: Bot):
    result = await get_inline_query_result(bot)
    await inline_query.answer(result)


async def get_inline_query_result(bot: Bot):
    result = []
    univ_list = ['cvut', 'czu', 'vse']
    for index, univ in enumerate(univ_list, start=0):
        deep_link = await generate_deep_link(bot)
        input_content = InputTextMessageContent(
            message_text=f"input_message_content: {univ}"
        )
        result.append(types.InlineQueryResultArticle(
            id=random.getrandbits(128),
            title=f"title: {univ}",
            input_message_content=input_content,
            description=f"description: {univ}",
            thumb_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/How_to_use_icon.svg/2214px-How_to_use_icon.svg.png',
            url=deep_link
        ))
    return result


async def generate_deep_link(bot: Bot):
    bot_user = await bot.get_me()
    bot_username = bot_user.username
    deeplink = f"https://t.me/{bot_username}?start=item_12345"
    return deeplink

@router.message(CommandStart(deep_link=True))
async def answer_deep_link(msg: types.Message, bot: Bot):

