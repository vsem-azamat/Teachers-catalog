from typing import Union

from aiogram import types
from aiogram.filters import BaseFilter

from databases.mongodb import mongodb
from text_assets import TextMenu as tm


class FindTeachersFilter(BaseFilter):

    async def __call__(self, msg: types.Message) -> bool:
        return msg.text in tm.MainMenu.td_find_teachers.values()

