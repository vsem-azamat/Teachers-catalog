from aiogram import Dispatcher


from .admins import AdminFilter
from .group_chat import IsGroup
from .user_chat import IsPrivate
from .dict_list import DictList
from .next_back_univ_less import NextBackUL
from .super_admins import SuperAdmins
from .start_button import Start_button


def setup(dp: Dispatcher):
    pass
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(DictList)
    dp.filters_factory.bind(NextBackUL)
    dp.filters_factory.bind(SuperAdmins)
    dp.filters_factory.bind(Start_button)
