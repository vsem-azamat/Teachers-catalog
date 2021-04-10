import asyncio
import datetime
import re

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest

from filters import IsGroup, AdminFilter
from loader import dp, bot


#MUTE and UNMUTE
@dp.message_handler(IsGroup(), Command("mute",prefixes='!/'), AdminFilter())
async def mute_member(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    command_parse = re.compile(r"(!mute|/mute) ?(\d+)? ?([\w+\D ]+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)
    if not time:
        time = int(5)
    else:
        time = int(time)
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)

    ReadOnlyPremissions = types.ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=False
    )
    try:
        await bot.restrict_chat_member(chat_id, user_id=member_id, permissions=ReadOnlyPremissions,
                                       until_date=until_date)
        await message.reply(f"Пользователь {member.get_mention(as_html=True)} в муте на {time} минут. \nПричина: {comment}")
    except BadRequest:
        await message.answer("Пользователь является администратором")


@dp.message_handler(IsGroup(), Command("unmute", prefixes="!/"), AdminFilter())
async def unmute_member(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id

    ReadOnlyPremissions = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True
    )
    try:
        await message.chat.restrict(user_id=member_id, permissions=ReadOnlyPremissions, until_date=0)
        await message.reply(f"Пользователь {member.get_mention(as_html=True)} размучен")
    except BadRequest:
        await message.answer("Ошибка размута")

    await asyncio.sleep(300)
    await message.delete()


#BAN and UNBAN
@dp.message_handler(IsGroup(), Command("ban", prefixes="!/"), AdminFilter())
async def ban_member(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.kick(user_id=member_id)
    await message.reply(f"Пользователь {member.get_mention(as_html=True)} забанен")
    await asyncio.sleep(300)
    await message.delete()


@dp.message_handler(IsGroup(), Command("unban", prefixes="!/"), AdminFilter())
async def ban_member(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.unban(user_id=member_id)
    await message.reply(f"Пользователь {member.get_mention(as_html=True)} разбанен")
    await asyncio.sleep(300)
    await message.delete()