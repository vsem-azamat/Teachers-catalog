from aiogram import types, Bot
from aiogram.filters import BaseFilter
from databases.db_postgresql import db

from text_assets import TextMenu as tm


class FindTeachersFilter(BaseFilter):
    async def __call__(self, msg: types.Message) -> bool:
        return msg.text in tm.MainMenu.td_find_teachers.values()

class UnivLessonsFilter(BaseFilter):
    async def __call__(self, msg: types.Message) -> bool:
        return msg.text in tm.MainMenu.td_find_teachers.values()

class TeacherSettingsFilter(BaseFilter):
    async def __call__(self, msg: types.Message) -> bool:
        return msg.text in tm.MainMenu.td_my_teachers_profile.values()
    

class ViaMessageFilter(BaseFilter):
    async def __call__(self, msg: types.Message, bot: Bot) -> bool:
        bot = await bot.get_me()
        if msg.via_bot:
            return msg.via_bot.username == bot.username
        return False