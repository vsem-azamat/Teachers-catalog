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


#-------------------------------CallbackData for Teacher settings-------------------------------#
class TypeTeacherSettingsMenu(str, Enum):
    profile_edit = "prof_edit"
    profile_lessons_add = "prof_lessons_add"
    profile_activate = "prof_activate"

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
    add: bool = True
    lesson_menu_type: TypeCatalogLessons



















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