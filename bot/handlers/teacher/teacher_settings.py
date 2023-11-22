from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import Optional

from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm
from bot.utils.states import TeacherRegistration
from bot.utils.navigation import *
from bot.utils.filters import TeacherSettingsFilter
from bot.utils.callback_factory import \
    TeacherSettingsMenu, TypeTeacherSettingsMenu, \
    TeacherSettingsEdit, TypeTeacherSettingsEdit, \
    TeacherCatalogLessonsTypes, TypeTeacherCatalogLessonsTypes, \
    TeacherCatalogLessons, TypeLessons

router = Router()


@router.message(TeacherSettingsFilter())
@router.callback_query(TeacherSettingsMenu.filter(F.menu_type == TypeTeacherSettingsMenu.profile_edit))
async def teachers_profile(query: types.Message, state: FSMContext, callback_data: Optional[TeacherSettings] = None):
    """
    Show teacher profile and settings or offer to create new profile.
    """
    user_language = await db.get_user_language(query.from_user.id)
    teacher = await db.get_teacher(teacher_id_tg=query.from_user.id)
    # if teacher profile exists -> Show profile and settings
    if teacher:
        text = tm.MyTeachersProfile.text_your_profile.get(user_language, 'ru')
        text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')

        keyboard = None
        # Teacher has USERNAME -> show profile and settings
        if query.from_user.username:
            teacher_state = bool(teacher.state)

            # Event: callback_query -> update teacher.state
            if callback_data and callback_data.state is not None:
                teacher_state = callback_data.state
                await db.teacher_state_update(teacher_id_tg=teacher.id, state=teacher_state)

            text_teacher_state = tm.MyTeachersProfile.text_teacher_state.get(teacher_state).get(user_language, 'ru')
            builder = tm.MyTeachersProfile.kb_profile_menu(user_language)

            # Add button with teacher.state
            builder.row(
                types.InlineKeyboardButton(
                    text=text_teacher_state,
                    callback_data=TeacherSettingsMenu(
                        menu_type=TypeTeacherSettingsMenu.profile_state,
                        state=not teacher_state
                    ).pack()
                )
            )
            keyboard = builder.as_markup() if builder else None

        # Teacher has not USERNAME -> Request to set USERNAME and set teacher.state=False
        else:
            # Set teacher.state=False
            await db.teacher_state_update(teacher_id_tg=teacher.id, state=False)
            # Text with request to set USERNAME
            text_login_error = tm.MyTeachersProfile.text_login_error.get(user_language, 'ru')
            text += "\n\n" + text_login_error
            await query.answer(text=text)

        if isinstance(query, types.Message):
            text_profile = await teacher_profile_text(teacher=teacher)
            await query.answer(text=text_profile)
            await query.answer(text=text_head + text, reply_markup=keyboard)
        elif isinstance(query, types.CallbackQuery):
            await query.message.edit_text(text=text_head + text, reply_markup=keyboard) # type: ignore
                        
    # If teacher profile does not exist -> Offer to create new profile
    else:
        text = tm.MyTeachersProfile.text_create_new_profile.get(user_language, 'ru')
        builder_reply = tm.MyTeachersProfile.kb_profile_settings()
        keyboard = builder_reply.as_markup(resize_keyboard=True)
        await query.answer(text=text, reply_markup=keyboard)
        await state.set_state(TeacherRegistration.start_registration)


@router.callback_query(TeacherSettingsMenu.filter(F.menu_type == TypeTeacherSettingsMenu.profile_edit))
async def profile_edit(query: types.CallbackQuery, bot: Bot):
    """
    Show menu for edit teacher profile:
        - Edit full teacher profile
        - Edit teacher description
        - Back to main teacher menu
    """
    user_language = await db.get_user_language(query.from_user.id)

    # Text
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_select_edit.get(user_language, 'ru')
    
    # Build buttons
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text=tm.MyTeachersProfile.ti_profile_edit_all.get(user_language, 'ru'),
            callback_data=TeacherSettingsEdit(edit_type=TypeTeacherSettingsEdit.profile_full).pack()
        ),
        types.InlineKeyboardButton(
            text=tm.MyTeachersProfile.ti_profile_edit_description.get(user_language, 'ru'),
            callback_data=TeacherSettingsEdit(edit_type=TypeTeacherSettingsEdit.profile_description).pack()
        ),
        types.InlineKeyboardButton(
            text="↩️",
            callback_data=TeacherSettingsMenu(menu_type=TypeTeacherSettingsMenu.profile_edit).pack()
        ),
    )
    builder.adjust(1)

    # Send message
    await bot.edit_message_text(
        text=text_head + text, 
        chat_id=query.from_user.id, 
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
        )


# TEACHER LESSONS
@router.callback_query(TeacherSettingsMenu.filter(F.menu_type == TypeTeacherSettingsMenu.profile_lessons_add))
async def profile_lessons_category(query: types.CallbackQuery):
    """
    Teacher menu with lessons menu for add/delete from profile:
        - Languages
        - Universities
        - All lessons
        - Back to main teacher menu
    """
    user_language = await db.get_user_language(query.from_user.id)

    # Text
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_lessons.get(user_language, 'ru')

    # Build buttons
    builder = InlineKeyboardBuilder()
    builder.button(
        text=tm.TeachersCategory.ti_universities.get(user_language, 'ru'),
        callback_data=TeacherCatalogLessonsTypes(catalog_type=TypeTeacherCatalogLessonsTypes.universities)
        )
    builder.button(
        text=tm.TeachersCategory.ti_languages.get(user_language, 'ru'),
        callback_data=TeacherCatalogLessonsTypes(catalog_type=TypeTeacherCatalogLessonsTypes.lessons_languages)
        )
    builder.button(
        text=tm.TeachersCategory.ti_lessons.get(user_language, 'ru'),
        callback_data=TeacherCatalogLessonsTypes(catalog_type=TypeTeacherCatalogLessonsTypes.lessons)
        )
    builder.button(
        text="↩️",
        callback_data=TeacherSettingsMenu(menu_type=TypeTeacherSettingsMenu.profile_edit).pack()
    )
    builder.adjust(1)

    # Send message
    await query.message.edit_text(text=text_head + text, reply_markup=builder.as_markup())


@router.callback_query(TeacherCatalogLessonsTypes.filter(F.catalog_type == TypeTeacherCatalogLessonsTypes.universities))
async def list_universities(callback: types.CallbackQuery, bot: Bot):
    """
    Teacher menu: list of universities for select
    """
    # Text
    user_language = await db.get_user_language(callback.from_user.id)
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_lessons_universities.get(user_language, 'ru')
    
    # Build buttons
    universities = await db.get_universities()
    builder = InlineKeyboardBuilder()
    for university in universities:
        builder.button(
            text = university.name,
            callback_data=TeacherCatalogLessons(
                lesson_type=TypeLessons.university,
                lesson_menu_type=TypeTeacherCatalogLessonsTypes.lessons_university,
                lesson_id=university.id,
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

# TODO: Fix CallbackFactory
@router.callback_query(TeacherCatalogLessons.filter())
@router.callback_query(TeacherCatalogLessonsTypes.filter())
async def teacher_catalog_all_lessons(query: types.CallbackQuery, callback_data: TeacherCatalogLessons, bot: Bot):
    """
    Show list of all lessons where teacher can add or remove lesson from profile.
    """
    user_language = await db.get_user_language(query.from_user.id)
    lessons = await db.get_all_lessons()

    # Text
    match callback_data.lesson_menu_type:
        case TypeTeacherCatalogLessonsTypes.lessons:
            text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
            text = tm.MyTeachersProfile.text_profile_lessons_catalog.get(user_language, 'ru')
            current_catalog_type = TypeTeacherCatalogLessonsTypes.lessons
            return_callback = TeacherSettingsMenu(menu_type=TypeTeacherSettingsMenu.profile_lessons_add)

        case TypeTeacherCatalogLessonsTypes.lessons_languages:
            text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
            text = tm.MyTeachersProfile.text_profile_lessons.get(user_language, 'ru')
            lessons = [lesson for lesson in lessons if isinstance(lesson, LessonsLanguage)]
            current_catalog_type = TypeTeacherCatalogLessonsTypes.lessons_languages
            return_callback = TeacherSettingsMenu(menu_type=TypeTeacherSettingsMenu.profile_lessons_add)

        case TypeTeacherCatalogLessonsTypes.lessons_university:
            text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
            text = tm.MyTeachersProfile.text_profile_lessons_universities.get(user_language, 'ru')
            lessons = [lesson for lesson in lessons if isinstance(lesson, LessonsUniversity)]
            current_catalog_type = TypeTeacherCatalogLessonsTypes.lessons_university
            return_callback = TeacherCatalogLessonsTypes(catalog_type=TypeTeacherCatalogLessonsTypes.universities)


    total_rows = len(lessons)    
    rows_per_page = 10
    current_page = callback_data.current_page
    add_lesson = True if callback_data.lesson_id >= 0 else False
    
    teacher = await db.get_teacher(teacher_id_tg=query.from_user.id)
    # If teacher does not exist -> Send message and return to main menu
    if not teacher:
        await query.answer(text="You are not registered as a teacher")
        text = tm.MainMenu.text_main_menu.get(user_language, 'ru')
        keyboard = tm.MainMenu.kb_main_menu(user_language).as_markup(resize_keyboard=True)
        await query.message.answer(
            text=text,
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            reply_markup=keyboard
        )
        await query.message.delete()
        return

    # Add/Remove lesson
    if callback_data.lesson_id:
        match callback_data.lesson_type:
            case TypeLessons.language:
                lesson = await db.get_lesson_of_language(lesson_id=callback_data.lesson_id)
            case TypeLessons.university:
                lesson = await db.get_lesson_of_university(lesson_id=callback_data.lesson_id)
            case _:
                lesson = None
        await db.add_lessons_to_teacher(teacher, lesson, add_lesson)

    lessons = await db.get_all_lessons(current_page=current_page, rows_per_page=rows_per_page, exclude_null_teachers=False)
    lessons_language_id_of_teacher = [lesson.id for lesson in lessons if lesson.id in teacher.lesson_language]
    lessons_university_id_of_teacher = [lesson.id for lesson in lessons if lesson.id in teacher.lesson_university]

    # Build buttons
    builder = InlineKeyboardBuilder()
    for lesson in lessons:
        text_lesson = str(lesson.name)
        add = True
        
        if isinstance(lesson, LessonsLanguage) and lesson.id in lessons_language_id_of_teacher:
            lesson_type = TypeLessons.language
            text_lesson = "✅ " + text_lesson
            add = False
        elif isinstance(lesson, LessonsUniversity) and lesson.id in lessons_university_id_of_teacher:
            lesson_type = TypeLessons.university
            text_lesson = "✅ " + text_lesson
            add = False
        else: continue

        # Button with lesson name and callback_data
        builder.button(
            text=text_lesson,
            callback_data=TeacherSettings(
                catalog_type=TeacherCatalogLessons(
                    lesson_id=lesson.id,
                    lesson_type=lesson_type,
                    lesson_menu_type=TypeTeacherCatalogLessonsTypes.lessons_university,
                    add=add
                )
            )
        )
    builder.adjust(2)
    buttons_next_back = await determine_navigation(
        total_rows=total_rows, current_page=current_page, rows_per_page=rows_per_page,
        back_callback=TeacherCatalogLessons(
            lesson_id=callback_data.lesson_id,
            lesson_type=callback_data.lesson_type,
            lesson_menu_type=current_catalog_type,
            current_page=current_page-1,
            ).pack(),

        next_callback=TeacherCatalogLessons(
            lesson_id=callback_data.lesson_id,
            lesson_type=callback_data.lesson_type,
            lesson_menu_type=current_catalog_type,
            current_page=current_page+1,
            ).pack(),
        return_callback=return_callback.pack()
    )
    builder.row(*buttons_next_back)

    # Send message
    await bot.edit_message_text(
        text=text_head + text,
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
    )
    await query.answer()

