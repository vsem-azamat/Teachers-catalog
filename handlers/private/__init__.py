from aiogram import Router

from .find_teachers_handlers import router as router_find_teachers
from .start_hanlders import router as router_start
from .test_hanlder import router as router_test

router = Router()

router.include_router(router_find_teachers)
router.include_router(router_test)
router.include_router(router_start)
