from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder 

from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm
from bot.utils.filters import ShowChatsFilter, AboutUsFilter

router = Router()

@router.message(ShowChatsFilter())
async def chats(msg: types.Message):
    user_language = await db.get_user_language(msg.from_user.id)
    text = tm.MainMenu.text_chats.get(user_language, 'ru')
    chats = await db.get_chats()
    builder = InlineKeyboardBuilder()
    for chat in chats:
        builder.button(
            text=chat.name,
            url=chat.link
        )
    builder.adjust(2)
    await msg.answer(text=text, reply_markup=builder.as_markup())


@router.message(AboutUsFilter())
async def chats(msg: types.Message):
    user_language = await db.get_user_language(msg.from_user.id)
    text = tm.MainMenu.text_about_us.get(user_language)
    await msg.answer(text=text, disable_web_page_preview=True)
    