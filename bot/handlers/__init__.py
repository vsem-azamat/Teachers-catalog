from aiogram import Router

from bot.utils.filters import ChatTypeFilter
from .private import router as router_private
from .admin import router as router_admin
from .catalog import router as router_catalog
from .teacher import router as router_teacher

router_private.message.filter(ChatTypeFilter(chat_type=['private']))
router_catalog.message.filter(ChatTypeFilter(chat_type=['private']))
router_teacher.message.filter(ChatTypeFilter(chat_type=['private']))

main_router = Router()

main_router.include_router(router_admin)
main_router.include_router(router_private)
main_router.include_router(router_catalog)
main_router.include_router(router_teacher)
