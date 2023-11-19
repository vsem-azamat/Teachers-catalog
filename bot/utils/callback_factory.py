from enum import Enum
from typing import Optional
from aiogram.filters.callback_data import CallbackData

ROWS_PER_PAGE = 5

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
    """
    Settings for navigation between pages

    Attributes:
        # TODO: write description for attributes
    """

    targetpageLevel: Optional[PageLevels] = None
    backPageLevel: Optional[PageLevels] = None
    university_id: int = 0
    lesson_id: int = 0
    teacher_id: int = 0
    current_page: int = 1
    total_pages: int = 0

    lesson_catalog:int = 0
    rows_per_page: int = ROWS_PER_PAGE
    columns_per_row: int = 2
    # source: LessonsSource = ''


# CallbackData for CATALOG
class CatalogUniversity(CallbackData, prefix='uni'):
    university_id: int = 0
    
    # Page settings
    columns_per_row: int = 2
    current_page: int = 1
    total_pages: int = 0
    rows_per_page: int = ROWS_PER_PAGE


class TypeLessons(str, Enum):
    language = "language"
    university = "university"


class CatalogLessons(CallbackData, prefix='clu'):
    lesson_id: int
    lesson_type: TypeLessons
    university_id: Optional[int] = 0
    
    # Page settings
    columns_per_row: int = 2
    current_page: int = 1
    total_pages: int = 0
    rows_per_page: int = ROWS_PER_PAGE


class CatalogTeacher(CallbackData, prefix='ct'):
    lesson_id: int
    lesson_type: TypeLessons
    teacher_id_tg: int
    university_id: Optional[int] = 0

    # Page settings
    current_page: int = 1
    total_pages: int = 0
    rows_per_page: int = ROWS_PER_PAGE


class CatalogGoogle(CallbackData, prefix='cg'):
    # Page settings
    current_page: int = 1
    total_pages: int = 0
    rows_per_page: int = ROWS_PER_PAGE


# CallbackData for TEACHERS SETTINGS
class TeacherLevels(str, Enum):
    lessons_language = "lessons_language"
    
    universities = "universities"
    lessons_university = "lessons_university"

    lessons_catalog = "lessons_catalog"

    lessons = "lessons"

    teacher = "teacher"
    teacher_edit = "teacher_edit"
    
    edit_all = "edit_all"
    edit_description = "edit_description"


class TeacherSettings(CallbackData, prefix='reg'):
    pageLevel: TeacherLevels = ''
    source: str = " "
    university_id: int = 0
    lesson_id: int = 0

    current_page: int = 1
    total_pages: int = 0
    rows_per_page: int = 2
    
    state: bool = None

    # True - add lesson to teacher profile
    # False - delete lesson from teacher profile
    add: bool = True 
    

class AdminLevels(str, Enum):
    universities = "universities"
    university = "university"


class AdminSettings(CallbackData, prefix='adm'):
    pageLevel: AdminLevels = ''
    university_id: int = 0