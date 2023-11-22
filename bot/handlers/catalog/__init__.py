from aiogram import Router

from .catalog_teachers import router as teachers_university_router
from .catalog_search import router as google_lesson_router

router = Router()

router.include_router(google_lesson_router)
router.include_router(teachers_university_router)
