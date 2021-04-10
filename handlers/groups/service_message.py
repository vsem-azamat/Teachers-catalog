import asyncio

from aiogram import types

from filters import IsGroup
from loader import dp, bot


@dp.message_handler(IsGroup(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    await message.reply(f"Привет, {message.new_chat_members[-1].full_name}")



@dp.message_handler(IsGroup(), content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def push_ban_member(message: types.Message):
    if message.left_chat_member.id == message.from_user.id: #сам вышел
        return
    elif message.from_user.id == (await bot.me).id: #бот забанил
        return
    else:
        await message.reply(f"{message.left_chat_member.full_name} был удалён из чата"
                            f" администратором {message.from_user.full_name}.")


