from aiogram import Router, types, F, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import Optional, Tuple

from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm
from bot.utils.navigation import *
from bot.handlers.private.start import main_menu_start
from bot.utils.callback_factory import \
    TeacherSettingsMenu, TypeTeacherSettingsMenu, \
    TeacherCatalogLessonsTypes, TypeCatalogLessons, \
    TeacherCatalogLessons, TypeLessons

router = Router()


@router.callback_query(TeacherSettingsMenu.filter(F.menu_type == TypeTeacherSettingsMenu.profile_lessons_add))
async def handler_profile_lessons_category(query: types.CallbackQuery):
    """
    Teacher menu with lessons menu for add/delete from profile.

    ⚙️ Main menu of teacher profile
    ...
    │
    ├── 🛒 Add/Remove lessons (THIS HANDLER)
    │   ├── 🔠 Languages
    │   ├── 🏫 Universities
    │   │   └── 📚 Lessons of university
    │   │
    │   ├── 📚 All lessons
    │   └── ↩️ Back to main menu
    │
    ...
    """
    user_language = await db.get_user_language(query.from_user.id)

    # Text
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_lessons.get(user_language, 'ru')

    # Build buttons
    builder = InlineKeyboardBuilder()
    # 🏫 Universities
    builder.button(
        text=tm.TeachersCategory.ti_universities.get(user_language, 'ru'),
        callback_data=TeacherCatalogLessonsTypes(catalog_type=TypeCatalogLessons.universities)
        )
    # 🔠 Languages
    builder.button(
        text=tm.TeachersCategory.ti_languages.get(user_language, 'ru'),
        callback_data=TeacherCatalogLessonsTypes(catalog_type=TypeCatalogLessons.lessons_languages)
        )
    # 📚 All lessons
    builder.button(
        text=tm.TeachersCategory.ti_lessons.get(user_language, 'ru'),
        callback_data=TeacherCatalogLessonsTypes(catalog_type=TypeCatalogLessons.lessons_all)
        )
    # ↩️ Back to main menu
    builder.button(
        text="↩️",
        callback_data=TeacherSettingsMenu(menu_type=TypeTeacherSettingsMenu.profile).pack()
    )
    builder.adjust(1)

    # Send message
    await query.message.edit_text(text=text_head + text, reply_markup=builder.as_markup())


@router.callback_query(TeacherCatalogLessonsTypes.filter(F.catalog_type == TypeCatalogLessons.universities))
async def list_universities(callback: types.CallbackQuery, bot: Bot):
    """
    Teacher menu: list of universities for select.

    ⚙️ Main menu of teacher profile
    ...
    │
    ├── 🛒 Add/Remove lessons
    │   ├── 🔠 Languages
    │   ├── 🏫 Universities (THIS HANDLER)
    │   │   └── 📚 Lessons of university
    │   │
    │   ├── 📚 All lessons
    │   └── ↩️ Back to main menu
    │
    ...
    """
    # Text
    user_language = await db.get_user_language(callback.from_user.id)
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language,)
    text = tm.MyTeachersProfile.text_profile_list_universities.get(user_language)
    
    # Build buttons
    universities = await db.get_universities()
    builder = InlineKeyboardBuilder()
    for university in universities:
        builder.button(
            text = university.name, # type: ignore
            callback_data=TeacherCatalogLessons(
                lesson_type=TypeLessons.university,
                lesson_menu_type=TypeCatalogLessons.lessons_university,
                university_id=university.id, # type: ignore
            ).pack()
        )
    builder.adjust(2)
    builder.row(types.InlineKeyboardButton(text='↩️', callback_data=TeacherSettingsMenu(menu_type=TypeTeacherSettingsMenu.profile_lessons_add).pack()))
    
    # Send message
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        text=text_head + text, 
        reply_markup=builder.as_markup()
        )
    await callback.answer()


async def teacher_catalog_add_lesson(query: types.CallbackQuery, callback_data: TeacherCatalogLessons) -> None:
    """
    Add lesson to teacher profile.

    Args:
        query (types.CallbackQuery): CallbackQuery
        callback_data (TeacherCatalogLessons): CallbackData for operations with lessons in teacher profile:
            - lesson
            - lesson
            ...
    
    Returns:
        None
    """
    if callback_data.lesson_id:
        match callback_data.lesson_type:
            case TypeLessons.language:
                lesson = await db.get_lesson_of_language(lesson_id=callback_data.lesson_id)
            case TypeLessons.university:
                lesson = await db.get_lesson_of_university(lesson_id=callback_data.lesson_id)
            case _:
                return
        add_lesson = callback_data.add
        teacher_id_tg = query.from_user.id
        await db.add_lessons_to_teacher(teacher_id_tg, lesson, add_lesson)


async def teacher_catalog_lessons(query: types.CallbackQuery, callback_data: TeacherCatalogLessons) -> Optional[Tuple[str, InlineKeyboardBuilder]]:
    """
    Show list of all lessons where teacher can add or remove lesson from profile.

    Args:
        query (types.CallbackQuery): CallbackQuery
        callback_data (TeacherCatalogLessons): CallbackData for operations with lessons in teacher profile:
            - lesson
            - lesson
            ...

    Returns:
        Optional[Tuple[str, InlineKeyboardBuilder]]: Text and InlineKeyboardBuilder
    """

    user_language = await db.get_user_language(query.from_user.id)
    teacher = await db.get_teacher(teacher_id_tg=query.from_user.id)
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')

    # If teacher does not exist -> Send message and return to main menu
    if not teacher:
        await query.answer(text="You are not registered as a teacher")
        await main_menu_start(query.message, user_language)
        await query.message.delete()
        return


    return_callback = None
    lessons_language_of_teacher = []
    lessons_university_of_teacher = []
    match callback_data.lesson_menu_type:
        case TypeCatalogLessons.lessons_all:
            text_menu = tm.MyTeachersProfile.text_profile_lessons_catalog.get(user_language)
            lessons = await db.get_all_lessons()
            lessons_language_of_teacher = teacher.lesson_language
            lessons_university_of_teacher = teacher.lesson_university     
            return_callback = TeacherSettingsMenu(menu_type=TypeTeacherSettingsMenu.profile_lessons_add).pack()

        case TypeCatalogLessons.lessons_university:
            text_menu = tm.MyTeachersProfile.text_profile_lessons_universities.get(user_language)
            university_id = callback_data.university_id
            lessons = await db.get_lessons_of_university(university_id=university_id)
            lessons_university_of_teacher = teacher.lesson_university
            return_callback = TeacherCatalogLessonsTypes(catalog_type=TypeCatalogLessons.universities).pack()

        case TypeCatalogLessons.lessons_languages:
            text_menu = tm.MyTeachersProfile.text_profile_lessons_languages.get(user_language)
            lessons = await db.get_lessons_of_languages()
            lessons_language_of_teacher = teacher.lesson_language
            return_callback = TeacherSettingsMenu(menu_type=TypeTeacherSettingsMenu.profile_lessons_add).pack()

        case _:
            await query.answer(text="Error: Unknown type of catalog")
            return
    print(lessons_language_of_teacher)
    print(lessons_university_of_teacher)

    # Pagination and navigation buttons
    total_rows = len(lessons) if isinstance(lessons, list) else lessons.count()
    rows_per_page = 10
    current_page = callback_data.current_page

    # Build buttons
    builder = InlineKeyboardBuilder()
    for lesson in lessons:
        lesson_name = str(lesson.name)
        lesson_type = TypeLessons.university if isinstance(lesson, LessonsUniversity) else TypeLessons.language
        add = True

        if isinstance(lesson, LessonsLanguage) and lesson.id in lessons_language_of_teacher:
            lesson_name = "✅ " + lesson_name
            add = False
        elif isinstance(lesson, LessonsUniversity) and lesson.id in lessons_university_of_teacher:
            lesson_name = "✅ " + lesson_name
            add = False
        else: 
            pass

        # Button with lesson name and callback_data
        builder.button(
            text=lesson_name,
            callback_data=TeacherCatalogLessons(
                lesson_id=lesson.id,
                lesson_type=lesson_type,
                lesson_menu_type=callback_data.lesson_menu_type,
                current_page=current_page,
                add=add
                ).pack()
            )
    builder.adjust(2)

    # Navigation buttons
    buttons_next_back = await determine_navigation(
        total_rows=total_rows, current_page=current_page, rows_per_page=rows_per_page,
        back_callback=TeacherCatalogLessons(
            lesson_id=callback_data.lesson_id,
            lesson_type=callback_data.lesson_type,
            lesson_menu_type=callback_data.lesson_menu_type,
            current_page=current_page-1,
            ).pack(),
        next_callback=TeacherCatalogLessons(
            lesson_id=callback_data.lesson_id,
            lesson_type=callback_data.lesson_type,
            lesson_menu_type=callback_data.lesson_menu_type,
            current_page=current_page+1,
            ).pack(),       
        return_callback=return_callback
        )
        
    builder.row(*buttons_next_back)
            
    return text_head + text_menu, builder



@router.callback_query(TeacherCatalogLessons.filter())
async def handler_teacher_catalog_lessons(query: types.CallbackQuery, callback_data: TeacherCatalogLessons, bot: Bot):
    """
    Show list of all lessons where teacher can add or remove lesson from profile.

    ⚙️ Main menu of teacher profile
    ...
    │
    ├── 🛒 Add/Remove lessons
    │   ├── 🔠 Languages (THIS HANDLER)
    │   ├── 🏫 Universities
    │   │   └── 📚 Lessons of university (THIS HANDLER)
    │   │
    │   ├── 📚 All lessons (THIS HANDLER)
    │   └── ↩️ Back to main menu
    │
    ...
    """
    await teacher_catalog_add_lesson(query, callback_data)
    text_bulder =  await teacher_catalog_lessons(query, callback_data)
    if not text_bulder: return
    text, builder = text_bulder

    # Send message
    await bot.edit_message_text(
        text=text,
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
    )
    await query.answer()
