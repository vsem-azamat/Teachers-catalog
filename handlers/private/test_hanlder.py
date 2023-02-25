from aiogram import Router, types, F, Bot
from aiogram.filters import Command, Filter

from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.gen_button import genButton

router = Router()

# get_university_lessons - test
@router.message(Command(commands=["test"]))
async def category_teachers(msg: types.Message, bot: Bot):
    
    q = await db.get_teacher_profile(10)
    print(f"name: {q.name} - code: {q.id}")
    
    

@router.message(F.photo)
async def image(msg: types.Message):
    await msg.answer(f'{msg.photo[0].file_id}')