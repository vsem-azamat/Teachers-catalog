from aiogram import Router, types
from aiogram.filters import CommandStart

from databases.mongodb import mongodb
from text_assets import TextMenu as tm

router = Router()


@router.message(commands=["test"])
async def category_teachers(msg: types.Message):
    text = mongodb.get_university()
    text = [coll for coll in text]
    # await msg.answer(text=text)
    print(text)
