from aiogram import Router

from .catalog_universities import router as catalog_universities_router
from .catalog_lessons import router as catalog_lessons_router
from .catalog_teachers import router as teachers_teachers_router
from .catalog_teacher_profile import router as teachers_teacher_profile_router

from .catalog_search import router as google_lesson_router

router = Router()

# Google routers
router.include_router(google_lesson_router)

# Catalog routers
router.include_router(catalog_universities_router)
router.include_router(catalog_lessons_router)
router.include_router(teachers_teachers_router)
router.include_router(teachers_teacher_profile_router)
