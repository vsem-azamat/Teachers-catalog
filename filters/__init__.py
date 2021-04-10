from aiogram import Dispatcher


from .admins import AdminFilter
from .group_chat import IsGroup
from .user_chat import IsPrivate


def setup(dp: Dispatcher):
    pass
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)