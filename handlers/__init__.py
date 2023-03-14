from aiogram import Router

from utils.filters import ChatTypeFilter
from .private import router as router_private

main_router = Router()

router_private.message.filter(ChatTypeFilter(chat_type=['private']))
main_router.include_router(router_private)

