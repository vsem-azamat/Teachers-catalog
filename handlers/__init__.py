from aiogram import Router

from utils.filters import ChatTypeFilter
from .private import router as router_private
from .admin import router as router_admin

router_private.message.filter(ChatTypeFilter(chat_type=['private']))

main_router = Router()

main_router.include_router(router_admin)
main_router.include_router(router_private)

