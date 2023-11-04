from aiogram import Router, types, Bot, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from databases.db_postgresql import db
from utils.navigation import *
from utils.callback_factory import AdminLevels, AdminSettings

router = Router()


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
