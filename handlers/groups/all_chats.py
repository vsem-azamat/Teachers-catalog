from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsGroup
from keyboards.inline.button_chat import school_chat

from loader import dp, bot
from texts.texts_main import start_list_chat


@dp.message_handler(IsGroup(), Command('chats', prefixes='!/'))
async def chats(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=start_list_chat,
                           reply_markup=school_chat)
