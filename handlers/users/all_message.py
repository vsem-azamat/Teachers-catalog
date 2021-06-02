from aiogram import types
from aiogram.dispatcher.filters import Command

from db.sq_lite import cursor
from filters import SuperAdmins
from loader import dp, bot


@dp.message_handler(Command('notify', prefixes='!/'), SuperAdmins())
async def notify(message: types.Message):
    text = " ".join(message.text.split()[1:])
    if len(text.split()) != 0:
        sql = """
            SELECT * FROM start_users
        """
        cursor.execute(sql)
        catalog = cursor.fetchall()
        i = 0
        for _ in catalog:
            await bot.send_message(chat_id=catalog[i][0], text=text)
            i += 1
    else:
        await bot.send_message(chat_id=message.chat.id, text="Что-то пошло не так")
        pass
