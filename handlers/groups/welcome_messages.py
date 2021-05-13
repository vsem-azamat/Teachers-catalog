import asyncio

from aiogram import types

from aiogram.dispatcher.filters import Command
from filters import IsGroup, AdminFilter

from loader import dp, bot
from defs.add_users_chats import add_users_of_chats
from defs.welcome_message import welcome_from_sql, welcome_change


@dp.message_handler(IsGroup(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    id_user = message.new_chat_members[0].id
    add_users_of_chats(id_user)
    text_from_sql = welcome_from_sql(message.chat.id)
    if text_from_sql == None:
        pass
    else:
        await message.reply(text_from_sql)


@dp.message_handler(IsGroup, Command("welcome", prefixes="!/"), AdminFilter())
async def welcome_change(message: types.Message):
    welcome_text = (message.text.split())[1:]
    if len(welcome_text) == 0:
        welcome_change(message.chat.id, "")
    else:
        welcome_text = " ".join(welcome_text)
        message.reply(welcome_change())
