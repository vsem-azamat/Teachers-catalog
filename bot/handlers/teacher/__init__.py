from aiogram import Router

from .teacher_registration import router as teacher_registration_router
from .teacher_settings import router as teacher_settings_router
from .teacher_lessons import router as teacher_lessons_router

router = Router()

router.include_router(teacher_registration_router)
router.include_router(teacher_settings_router)
router.include_router(teacher_lessons_router)