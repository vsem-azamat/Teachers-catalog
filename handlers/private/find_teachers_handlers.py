from aiogram import Router, types, F
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from databases.mongodb import mongodb
from text_assets import TextMenu as tm
from utils.filters import FindTeachersFilter
from utils.callback_factory import CategoryTeachersCallbackFactory
import random

router = Router()


@router.message(FindTeachersFilter())
async def category_teachers(msg: types.Message):
    user_lang = mongodb.get_user_lang(msg.from_user.id)

    text = tm.FindTeachers.text_find_teachers[user_lang]
    keyboard = tm.FindTeachers.kb_teachers_category(user_lang)
    await msg.answer(text=text, reply_markup=keyboard)


@router.inline_query(F.query == "university")
async def show_univerity_teachers(inline_query: types.InlineQuery):
    result = []
    univ_list = ['cvut', 'czu', 'vse']
    for i in univ_list:
        result.append(InlineQueryResultArticle(
            id=random.getrandbits(128),
            title=f"Title: {i}",
            desciption=f"Desciption: {i}",
            input_message_content=InputTextMessageContent(
                message_text=f"input_message_content: {i}"
            )
        ))
    await inline_query.answer(result, is_personal=True)

# @router.callback_query(CategoryTeachersCallbackFactory.filter())
# async def inline_category_list(
#         callback: types.CallbackQuery,
#         callback_data: CategoryTeachersCallbackFactory
# ):
#     category = callback_data.category
#     match category:
#         case "university":
#             print(1)
#         case _:
#             print('pass')
