from typing import Union

from aiogram import types, Bot
from aiogram.filters import BaseFilter

from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm


class ChatTypeFilter(BaseFilter): 
    def __init__(self, chat_type: Union[str, list]):
        self.chat_type = chat_type

    async def __call__(self, message: types.Message) -> bool: 
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


class FindTeachersFilter(BaseFilter):
    async def __call__(self, msg: types.Message) -> bool:
        return msg.text in tm.MainMenu.td_find_teachers.values()


class ShowChatsFilter(BaseFilter):
    async def __call__(self, msg: types.Message) -> bool:
        return msg.text in tm.MainMenu.td_chats.values()


class AboutUsFilter(BaseFilter):
    async def __call__(self, msg: types.Message) -> bool:
        return msg.text in tm.MainMenu.td_about_us.values()


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