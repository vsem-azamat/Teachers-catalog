from aiogram import types, md
from loader import dp, bot
from aiogram.dispatcher.filters import Command


@dp.message_handler(Command('test', prefixes='!/'))
async def test(message: types.CallbackQuery):
    id_user = 268388996
    text = md.hlink(title=message.from_user.full_name, url=message.from_user.url)
    await bot.send_message(text=text, chat_id=message.from_user.id)
