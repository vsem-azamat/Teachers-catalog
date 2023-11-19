from aiogram import Router

from .catalogSearch import router as google_lesson_router
from .teacher_settings import router as teacher_settings_router
from .teacher_registration import router as teacher_registration_router
from .catalogTeachers import router as teachers_university_router
from .start_hanlders import router as router_start
from .test_hanlder import router as router_test
from .help_handlers import router as help_handlers_router

router = Router()

# Base
router.include_router(router_start)
router.include_router(help_handlers_router)
router.include_router(router_test)

# Catalog
router.include_router(google_lesson_router)
router.include_router(teachers_university_router)

# Settings
router.include_router(teacher_registration_router)
router.include_router(teacher_settings_router)