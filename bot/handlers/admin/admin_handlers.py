from aiogram import Router, types, Bot, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.databases.db_postgresql import db
from bot.utils.navigation import *
from bot.utils.callback_factory import AdminLevels, AdminSettings

router = Router()


@router.message(Command('teachers', prefix='!/'))
async def edit_teachers(message: types.Message):
    """
    Edit teachers menu
    """
    teachers = await db.get_all_teachers()
    text = '<b>Список преподавателей:</b>\n\n'
    text += '<b>id_tg : name - login - state - state_admin</b>\n'
    for teacher in teachers:
        text += f'{teacher.id_tg} : {teacher.name} - @{teacher.user.login} - {teacher.state} - {teacher.state_admin}\n'
    await message.answer(text)


@router.message(Command('univ', prefix='!/'))
async def edit_universities(message: types.Message, command: types.BotCommand):
    command_text = command.args

    if command_text is None:
        universitites = await db.get_universities()   
        builder = InlineKeyboardBuilder()
        for university in universitites:
            builder.button(
                text=f'{university.id} : {university.name}',
                callback_data=AdminSettings(
                    pageLevel=AdminLevels.university,
                    university_id=university.id
                )
            )
        builder.adjust(2)
    pass
