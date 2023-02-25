from aiogram import Router

from .google_lesson_hanlders import router as google_lesson
from .teachers_university import router as teachers_university_router
from .teachers_language import router as teachers_language_router
from .start_hanlders import router as router_start
from .test_hanlder import router as router_test

router = Router()

router.include_router(google_lesson)
router.include_router(teachers_university_router)
router.include_router(teachers_language_router)
router.include_router(router_test)
router.include_router(router_start)
