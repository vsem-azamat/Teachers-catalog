from aiogram import Router

from .profile_settings_handlers import router as router_profile_settings

router = Router()

router.include_router(router_profile_settings)
