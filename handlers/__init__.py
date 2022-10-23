from aiogram import Router

from .private import router as router_private

main_router = Router()

main_router.include_router(router_private)
