from aiogram import Router

from .start import router as router_start
from .test_hanlder import router as router_test
from .help import router as help_handlers_router

router = Router()

router.include_router(router_start)
router.include_router(help_handlers_router)
router.include_router(router_test)