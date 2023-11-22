from enum import Enum
from typing import Optional
from aiogram.filters.callback_data import CallbackData


ROWS_PER_PAGE = 5


# CallbackData for CATALOG
class CatalogUniversity(CallbackData, prefix='uni'):
    """
    CallbackData for university buttons in catalog
    """
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
    """
    CallbackData for lessons buttons in catalog
    """
    lesson_id: int
    lesson_type: TypeLessons
    university_id: Optional[int] = 0
    
    # Page settings
    columns_per_row: int = 2
    current_page: int = 1
    total_pages: int = 0
    rows_per_page: int = ROWS_PER_PAGE


class CatalogTeacher(CallbackData, prefix='ct'):
    """
    CallbackData for teacher buttons in catalog
    """
    lesson_id: int
    lesson_type: TypeLessons
    teacher_id_tg: int
    university_id: Optional[int] = 0

    # Page settings
    current_page: int = 1
    total_pages: int = 0
    rows_per_page: int = ROWS_PER_PAGE


class CatalogGoogle(CallbackData, prefix='cg'):
    """
    CallbackData for google buttons after searching in inline mode
    """
    # Page settings
    current_page: int = 1
    total_pages: int = 0
    rows_per_page: int = ROWS_PER_PAGE

#########################################################################
# CallbackData for TEACHER SETTINGS
class TypeTeacherSettingsMenu(str, Enum):
    profile_edit = "profile_edit"
    profile_lessons_add = "profile_lessons_add"
    profile_state = "profile_state"

class TeacherSettingsMenu(CallbackData, prefix='tsm'):
    """
    CallbackData for teacher settings buttons:
        - Edit profile
        - Add/Remove lessons
        - Activate/Deactivate profile
    """
    menu_type: TypeTeacherSettingsMenu
    state: Optional[bool] = None


class TypeTeacherSettingsEdit(str, Enum):
    profile_full = "profile_full"
    profile_description = "profile_descr"

class TeacherSettingsEdit(CallbackData, prefix='tse'):
    """
    CallbackData for teacher settings buttons for edit profile:
        - Edit full profile
        - Edit description
    """
    edit_type: TypeTeacherSettingsEdit


class TypeTeacherCatalogLessonsTypes(str, Enum):
    universities = "universities"
    lessons_university = "l_university"
    lessons_languages = "l_languages"
    lessons = "l_all"

class TeacherCatalogLessonsTypes(CallbackData, prefix='reg'):
    """
    CallbackData for teacher settings buttons for edit lessons:
        - universities (list of universities)
        - lesson of university
        - lesson of language
        - all lessons
    """
    catalog_type: TypeTeacherCatalogLessonsTypes


class TeacherCatalogLessons(CatalogLessons, prefix='clt'):
    """
    CallbackData for operations with lessons in teacher profile:
        - lesson
        - lesson
        ...
    """
    add: bool = True
    lesson_menu_type: TypeTeacherCatalogLessonsTypes













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
    catalog_type: TeacherLevels
    
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