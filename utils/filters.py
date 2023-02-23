from aiogram import types
from aiogram.filters import BaseFilter
from databases.db_postgresql import db

from text_assets import TextMenu as tm


class FindTeachersFilter(BaseFilter):
    async def __call__(self, msg: types.Message) -> bool:
        return msg.text in tm.MainMenu.td_find_teachers.values()

class UnivLessonsFilter(BaseFilter):
    async def __call__(self, msg: types.Message) -> bool:
        return msg.text in tm.MainMenu.td_find_teachers.values()

