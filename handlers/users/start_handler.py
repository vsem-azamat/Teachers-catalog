from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsPrivate
from keyboards.default import start_menu
from keyboards.default.start_menu import bt11, bt12, bt21, bt22, bt32
from keyboards.inline.button_abous_us import about_us
from keyboards.inline.button_chat import school_chat
from keyboards.inline.button_school import school_teacher1
from loader import dp
from texts.texts_main import start_msg, start_about_us, start_list_univ, start_list_chat, start_channels, start_offer


@dp.message_handler(IsPrivate(), Command('start'))
async def start_message(msg: types.Message):
    await msg.reply(text=start_msg,
                    reply_markup=start_menu)


@dp.message_handler(IsPrivate())
async def start_menu_message(message: types.Message):
    if message.text == bt11:
        await message.reply(text=start_list_chat,
                            reply_markup=school_chat)

    if message.text == bt21:
        await message.reply(text=start_channels)

    if message.text == bt12:
        await message.reply(text=start_list_univ,
                            reply_markup=school_teacher1)

    if message.text == bt22:
        await message.reply(text=start_offer)

    # if message.text == bt31:
    #     await message.reply(text=start_offer)

    if message.text == bt32:
        await message.reply(text=start_about_us,
                            reply_markup=about_us)
