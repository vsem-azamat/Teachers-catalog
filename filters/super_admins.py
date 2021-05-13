from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

list_super_amins = [268388996]


class SuperAdmins(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in list_super_amins
