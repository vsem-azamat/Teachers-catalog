from aiogram import Router

from .start import router as router_start
from .help import router as router_help

router = Router()

router.include_router(router_start)
router.include_router(router_help)