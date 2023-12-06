from enum import Enum
from typing import Optional
from aiogram.filters.callback_data import CallbackData


ROWS_PER_PAGE = 5


#-------------------------------CallbackData for Catalog of Teachers------------------------------#
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
    language = "lang"
    university = "univ"


class TypeCatalogLessons(str, Enum):
    """
    CallbackData for return buttons in catalog
        - universities: return to list of universities
        - lessons_university: return to list of lessons of university
        - lessons_languages: return to list of lessons of language
        - lessons_all: return to list of all lessons
    """
    universities = "univ"
    lessons_university = "l_univ"
    lessons_languages = "l_lang"
    lessons_all = "l_all"


class CatalogLessons(CallbackData, prefix='clu'):
    """
    CallbackData for lessons buttons in catalog
    """
    lesson_id: int
    lesson_type: TypeLessons
    lesson_return_type: Optional[TypeCatalogLessons] = None
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
    lesson_return_type: Optional[TypeCatalogLessons] = None
    teacher_id_tg: int
    university_id: Optional[int] = None

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


# TODO: Complete this class. And use it in all catalog callbacks.
# Why? Because we need to save state of catalog menu, and I can't do it with different callbacks
# For example, we need to save current page of lessons in catalog lessons, teachers, etc.
class CatalogCallback(CallbackData, prefix='ctn'):
    # ------ Catalog: universities ------ #
    university_id: int = 0

    # ------ Catalog: Lessons ------ #
    lesson_type: Optional[TypeLessons] = None 
    lesson_id: int = 0

    # Page settings
    lesson_total_pages: int = 0
    lesson_current_page: int = 1
    lesson_rows_per_page: int = ROWS_PER_PAGE
    
    # ------ Catalog: Teachers ------ #
    teacher_id_tg: int = 0

    # Page settings
    teacher_total_pages: int = 0
    teacher_current_page: int = 1
    teacher_rows_per_page: int = ROWS_PER_PAGE
    
    
    


#-------------------------------CallbackData for Teacher settings-------------------------------#
class TypeTeacherSettingsMenu(str, Enum):
    profile = "prof"
    profile_edit = "prof_edit"
    profile_lessons_add = "prof_lessons_add"
    profile_activate = "prof_activate"

class TeacherSettingsMenu(CallbackData, prefix='tsm'):
    """
    CallbackData for teacher settings buttons:
        - Profile (return to profile)
        - Edit profile
        - Add/Remove lessons
        - Activate/Deactivate profile
    """
    menu_type: TypeTeacherSettingsMenu
    state: Optional[bool] = None


class TypeTeacherSettingsEdit(str, Enum):
    profile_edit_full = "prof_edit_full"
    profile_edit_description = "prof_edit_descr"

class TeacherSettingsEdit(CallbackData, prefix='tse'):
    """
    CallbackData for teacher settings buttons for edit profile:
        - Edit full profile
        - Edit description
    """
    edit_type: TypeTeacherSettingsEdit


class TeacherCatalogLessonsTypes(CallbackData, prefix='reg'):
    """
    CallbackData for teacher settings buttons for edit lessons:
        - universities (list of universities)
        - lesson of university
        - lesson of language
        - all lessons
    """
    catalog_type: TypeCatalogLessons


class TeacherCatalogLessons(CatalogLessons, prefix='clt'):
    """
    CallbackData for operations with lessons in teacher profile:
        - lesson
        - lesson
        ...
    """
    lesson_id: int = 0
    add: bool = True
    lesson_menu_type: TypeCatalogLessons


#-------------------------------CallbackData for Admin settings-------------------------------#
class AdminLevels(str, Enum):
    universities = "universities"
    university = "university"


class AdminSettings(CallbackData, prefix='adm'):
    pageLevel: Optional[AdminLevels] = None
    university_id: int = 0