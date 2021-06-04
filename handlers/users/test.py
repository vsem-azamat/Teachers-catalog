from aiogram import types
from aiogram.types.message import ParseMode
from filters.super_admins import SuperAdmins

from keyboards.inline.button_school import test1
from loader import dp, bot
from aiogram.dispatcher.filters import Command
from db.sq_lite import cursor, conn


@dp.message_handler(Command('test', prefixes='!/'), SuperAdmins())
async def test(message: types.Message):
    sql = """
    SELECT * FROM all_texts
    """
    cursor.execute(sql)
    catalog = cursor.fetchall()
    if len(catalog) == 0:
        await bot.send_message(chat_id=message.chat.id, text='0')
    else:
        texts = catalog[0][1]
        # await bot.send_message(chat_id=message.chat.id, text=catalog[0][1], parse_mode='HTML')
        await bot.send_message(chat_id=message.chat.id, text=texts)


@dp.message_handler(Command('add', prefixes='!/'), SuperAdmins())
async def run(message: types.Message):
    message_text = message.text.partition(" ")[1]
    sql = """
    INSERT INTO all_texts
    (all_text)
    VALUES (?)
    """
    cursor.execute(sql, [message_text])
    conn.commit()
    await bot.send_message(chat_id=message.chat.id, text=message_text)


@dp.message_handler(Command('test1', prefixes='!/'), SuperAdmins())
async def call(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='hope', reply_markup=test1)


@dp.callback_query_handler(regexp=r"^aboba")
async def cull(call: types.CallbackQuery):
    message = call.data.split()[1]
    await bot.send_message(chat_id=call.message.chat.id, text=message)
    await bot.answer_callback_query(call.id)




