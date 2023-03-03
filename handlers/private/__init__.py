from aiogram import Router

from .google_lesson import router as google_lesson_router
from .teacher_settings import router as teacher_settings_router
from .teachers_university import router as teachers_university_router
from .teachers_language import router as teachers_language_router
from .start_hanlders import router as router_start
from .test_hanlder import router as router_test

router = Router()

router.include_router(google_lesson_router)
router.include_router(teacher_settings_router)
router.include_router(teachers_university_router)
router.include_router(teachers_language_router)
router.include_router(router_test)
router.include_router(router_start)
