from aiogram import Router

from .admin_handlers import router as router_admin
from .test_hanlder import router as router_test

router = Router()

router.include_router(router_admin)
router.include_router(router_test)
