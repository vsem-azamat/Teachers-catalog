from enum import Enum
from aiogram.filters.callback_data import CallbackData


class PageLevels(str, Enum):
    lessons_language = "lessons_language"
    teachers_language = "teachers_languages"
    
    universities = "universities"
    lessons_university = "lessons_university"
    teachers_university = "teachers_universities"
    
    teacher_language = "teacher_language"
    teacher_university = "teacher_university"

    teacher = "teacher"

    lessons = "lessons"
    lessons_catalog = "lessons_catalog"
    google = "google"


class PageSettings(CallbackData, prefix='fub'):
    pageLevel: PageLevels = ''
    university_id: int = 0
    lesson_id: int = 0
    teacher_id: int = 0
    current_page: int = 1
    total_pages: int = 0

    lesson_catalog:int = 0
    rows_per_page: int = 2
    # source: LessonsSource = ''



    
class TeacherLevels(str, Enum):
    lessons_language = "lessons_language"
    
    universities = "universities"
    lessons_university = "lessons_university"

    teacher = "teacher"
    # google = "google"


class TeacherSettings(CallbackData, prefix='reg'):
    pageLevel: TeacherLevels = ''
    university_id: int = 0
    lesson_id: int = 0

    current_page: int = 1
    total_pages: int = 0
    rows_per_page: int = 2

    # True - add lesson to teacher profile
    # False - delete lesson from teacher profile
    add: bool = True 
    