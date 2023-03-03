from aiogram import Router, types, F, Bot
from aiogram.filters import Command, Filter
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.gen_button import genButton

router = Router()


class MyCallback(CallbackData, prefix="my"):
    value: int
    action: str

@router.message(Command(commands=["test"]))
async def category_teachers(msg: types.Message, bot: Bot):
    text = "test"
    builder = InlineKeyboardBuilder()
    teacher = await db.get_teacher(user_id_tg=msg.from_user.id)
    print(teacher.id)
    print(teacher.id)
    

# @router.callback_query(MyCallback.filter(F.action == "page"))
# async def test_callback(query: types.CallbackQuery, callback_data: MyCallback):
#     print(callback_data.action)    
#     print(1)
#     await query.answer()
