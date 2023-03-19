from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.states import TeacherRegistration
from utils.navigation import *
from utils.callback_factory import *
from utils.filters import TeacherSettingsFilter

router = Router()


# TEACHER: SETTINGS
@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.teacher))
@router.message(TeacherSettingsFilter())
async def teachers_profile(msg: types.Message, state: FSMContext, callback_data: TeacherSettings = None):
    await db.check_exists(id_tg=msg.from_user.id, login=msg.from_user.username)
    user_id_tg = msg.from_user.id
    user_language = await db.get_user_language(user_id_tg)
    teacher = await db.get_teacher_profile(user_id_tg=user_id_tg)
    # if teacher profile exists
    if teacher:
        text = tm.MyTeachersProfile.text_your_profile.get(user_language, 'ru')
        text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
        keyboard = None
        # Teacher has USERNAME
        if msg.from_user.username:

            teacher_state = teacher.state
            # Update teacher state
            if callback_data and callback_data.state is not None:
                teacher_state = callback_data.state
                await db.teacher_state_update(teacher_id=teacher.id, state=teacher_state)

            text_teacher_state = tm.MyTeachersProfile.text_teacher_state.get(teacher_state).get(user_language, 'ru')
            keyboard: InlineKeyboardBuilder = tm.MyTeachersProfile.kb_profile_menu(user_language)
            keyboard.row(
                types.InlineKeyboardButton(
                    text=text_teacher_state,
                    callback_data=TeacherSettings(
                        pageLevel=TeacherLevels.teacher,
                        state=not teacher_state
                    ).pack()
                )
            )
            keyboard = keyboard.as_markup()

        # Teacher has not USERNAME
        else:
            await db.teacher_state_update(teacher_id=teacher.id, state=False)
            text_login_error = tm.MyTeachersProfile.text_login_error.get(user_language, 'ru')
            text += "\n\n" + text_login_error
        if isinstance(msg, types.Message):
            text_profile = await teacher_profile_text(teacher=teacher)
            await msg.answer(text=text_profile)
            await msg.answer(text=text_head + text, reply_markup=keyboard)
        elif isinstance(msg, types.CallbackQuery):
            await msg.message.edit_text(text=text_head + text, reply_markup=keyboard)
                        
    # if teacher profile doen't exist
    else:
        text = tm.MyTeachersProfile.text_create_new_profile.get(user_language, 'ru')
        keyboard = tm.MyTeachersProfile.kb_profile_settings()
        await msg.answer(text=text, reply_markup=keyboard)
        await state.set_state(TeacherRegistration.start_registration)


@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.teacher_edit))
async def profile_edit(query: types.CallbackQuery, bot: Bot):
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_select_edit.get(user_language, 'ru')
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text=tm.MyTeachersProfile.ti_profile_edit_all.get(user_language, 'ru'),
            callback_data=TeacherSettings(pageLevel=TeacherLevels.edit_all).pack()
        ),
        types.InlineKeyboardButton(
            text=tm.MyTeachersProfile.ti_profile_edit_description.get(user_language, 'ru'),
            callback_data=TeacherSettings(pageLevel=TeacherLevels.edit_description).pack()
        ),
        types.InlineKeyboardButton(
            text="↩️",
            callback_data=TeacherSettings(pageLevel=TeacherLevels.teacher).pack()
        ),
    )
    builder.adjust(1)
    await bot.edit_message_text(
        text=text_head + text, 
        chat_id=query.from_user.id, 
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
        )


# TEACHER LESSONS
@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.lessons))
async def profile_lessons_category(msg: types.Message or types.CallbackQuery):
    user_language = await db.get_user_language(msg.from_user.id)
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_lessons.get(user_language, 'ru')
    builder = InlineKeyboardBuilder()
    builder.button(
        text=tm.TeachersCategory.ti_universities.get(user_language, 'ru'),
        callback_data=TeacherSettings(pageLevel=TeacherLevels.universities)
        )
    builder.button(
        text=tm.TeachersCategory.ti_languages.get(user_language, 'ru'),
        callback_data=TeacherSettings(pageLevel=TeacherLevels.lessons_language)
        )
    builder.button(
        text=tm.TeachersCategory.ti_lessons.get(user_language, 'ru'),
        callback_data=TeacherSettings(pageLevel=TeacherLevels.lessons_catalog)
        )
    builder.button(
        text="↩️",
        callback_data=TeacherSettings(pageLevel=TeacherLevels.teacher)
    )
    builder.adjust(1)
    await msg.message.edit_text(text=text_head + text, reply_markup=builder.as_markup())


@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.lessons_catalog))
async def lessons_catalog(query: types.CallbackQuery, callback_data: PageSettings ,bot: Bot):
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_lessons_catalog.get(user_language, 'ru')
    total_rows = await db.get_count_all_lessons(exclude_null_teachers=False)
    rows_per_page = 10
    current_page = callback_data.current_page
    add_lesson = callback_data.add
    teacher = await db.get_teacher(user_id_tg=query.from_user.id)


    # Add/Delete lesson
    if callback_data.lesson_id:
        if callback_data.source == "language":
            table_name = "TeachersLessonsLanguage"
        elif callback_data.source == "university":
            table_name = "TeachersLessonsUniversity"
        await db.add_lessons_to_teacher(
            table_name=table_name,
            teacher_id=teacher.id, 
            lesson_id=callback_data.lesson_id,
            add=add_lesson,
            )

    lessons = await db.get_all_lessons(current_page=current_page, rows_per_page=rows_per_page, exclude_null_teachers=False)
    lessons_language_id_of_teacher = await db.get_lessons_id_of_teacher(table_name='TeachersLessonsLanguage', teacher_id=teacher.id)
    lessons_university_id_of_teacher = await db.get_lessons_id_of_teacher(table_name='TeachersLessonsUniversity', teacher_id=teacher.id)


    if lessons_language_id_of_teacher:
        lessons_language_id_of_teacher = [row.id_lesson for row in lessons_language_id_of_teacher]
    else:
        lessons_language_id_of_teacher = []

    if lessons_university_id_of_teacher:
        lessons_university_id_of_teacher = [row.id_lesson for row in lessons_university_id_of_teacher]
    else:
        lessons_university_id_of_teacher = []

    builder = InlineKeyboardBuilder()
    for lesson in lessons:
        text_lesson = lesson.name
        state = 1

        lesson_source = ""
        if lesson.source: lesson_source = lesson.source

        if lesson_source == 'language' and lesson.id in lessons_language_id_of_teacher:
            text_lesson = "✅ " + text_lesson
            state = 0

        if lesson_source == 'university' and lesson.id in lessons_university_id_of_teacher:
            text_lesson = "✅ " + text_lesson
            state = 0

        builder.button(
            text=text_lesson,
            callback_data=TeacherSettings(
                pageLevel=TeacherLevels.lessons_catalog,
                lesson_id=lesson.id,
                add=state,
                source=lesson_source
            )
        )
    builder.adjust(2)
    buttons_next_back = await determine_navigation(
        total_rows=total_rows, current_page=current_page, rows_per_page=rows_per_page,
        back_button=TeacherSettings(
            pageLevel=TeacherLevels.lessons_catalog,
            current_page=current_page-1,
            ),
        next_button=TeacherSettings(
            pageLevel=TeacherLevels.lessons_catalog,
            current_page=current_page+1,
            ),
        return_button=TeacherSettings(
            pageLevel=TeacherLevels.lessons,
            )
    )
    builder.row(*buttons_next_back)
    await bot.edit_message_text(
        text=text_head + text,
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=builder.as_markup()
    )


# Show list of Languages
@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.lessons_language))
async def list_universities(query: types.CallbackQuery, callback_data: TeacherSettings, bot: Bot):
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_lessons_select.get(user_language, 'ru')
    rows_per_page = PageSettings().rows_per_page
    teacher = await db.get_teacher(user_id_tg=query.from_user.id)
    add_lesson = callback_data.add

    # Add/Delete lesson
    if callback_data.lesson_id:
        await db.add_lessons_to_teacher(
            table_name="TeachersLessonsLanguage",
            teacher_id=teacher.id, 
            lesson_id=callback_data.lesson_id,
            add=add_lesson,
            )
    lessons = await db.get_lessons_languages()
    lessons_id_of_teacher = await db.get_lessons_id_of_teacher(table_name='TeachersLessonsLanguage', teacher_id=teacher.id)

    if lessons_id_of_teacher:
        lessons_id_of_teacher = [row.id_lesson for row in lessons_id_of_teacher]
    else:
        lessons_id_of_teacher = []

    builder = InlineKeyboardBuilder()
    for lesson in lessons:
        text_lesson = lesson.name
        state = 1

        if lesson.id in lessons_id_of_teacher:
            text_lesson = "✅ " + text_lesson
            state = 0
        builder.button(
            text = text_lesson,
            callback_data=TeacherSettings(
                pageLevel=TeacherLevels.lessons_language,
                lesson_id=lesson.id,
                add = state
            )
        )
    builder.adjust(rows_per_page)
    builder.row(types.InlineKeyboardButton(text='↩️', callback_data=TeacherSettings(pageLevel=TeacherLevels.lessons).pack()))
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id, 
        text=text_head + text, 
        reply_markup=builder.as_markup()
        )
    await query.answer()


# UNIVERSITIES 
@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.universities))
async def list_universities(callback: types.CallbackQuery, bot: Bot):
    user_language = await db.get_user_language(callback.from_user.id)
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_lessons_universities.get(user_language, 'ru')
    universities = await db.get_universities()
    builder = InlineKeyboardBuilder()
    for university in universities:
        builder.button(
            text = university.name,
            callback_data=TeacherSettings(
                pageLevel=TeacherLevels.lessons_university,
                university_id=university.id
            )
        )
    rows_per_page = PageSettings().rows_per_page
    builder.adjust(rows_per_page)
    builder.row(types.InlineKeyboardButton(text='↩️', callback_data=TeacherSettings(pageLevel=TeacherLevels.lessons).pack()))
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        text=text_head + text, 
        reply_markup=builder.as_markup()
        )
    await callback.answer()


# Show list of University Lessons
@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.lessons_university))
async def list_universities(query: types.CallbackQuery, callback_data: TeacherSettings, bot: Bot):
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_lessons_select.get(user_language, 'ru')
    rows_per_page = PageSettings().rows_per_page
    university_id = callback_data.university_id
    teacher = await db.get_teacher(user_id_tg=query.from_user.id)
    add_lesson = callback_data.add

    # Add/Delete lesson
    if callback_data.lesson_id:
        await db.add_lessons_to_teacher(
            table_name="TeachersLessonsUniversity",
            teacher_id=teacher.id, 
            lesson_id=callback_data.lesson_id,
            add=add_lesson,
            )
    lessons = await db.get_lessons_of_university(university_id=university_id)
    lessons_id_of_teacher = await db.get_lessons_id_of_teacher(table_name='TeachersLessonsUniversity',teacher_id=teacher.id)

    if lessons_id_of_teacher:
        lessons_id_of_teacher = [row.id_lesson for row in lessons_id_of_teacher]
    else:
        lessons_id_of_teacher = []
    builder = InlineKeyboardBuilder()
    for lesson in lessons:
        text_lesson = lesson.name
        state = 1

        if lesson.id in lessons_id_of_teacher:
            text_lesson = "✅ " + text_lesson
            state = 0
        builder.button(
            text = text_lesson,
            callback_data=TeacherSettings(
                pageLevel=TeacherLevels.lessons_university,
                lesson_id=lesson.id,
               university_id=university_id, 
                add = state
            )
        )
    builder.adjust(rows_per_page)
    builder.row(
        types.InlineKeyboardButton(
            text='↩️', 
            callback_data=TeacherSettings(
                pageLevel=TeacherLevels.universities
            ).pack()
        )
    )
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id, 
        text=text_head + text, 
        reply_markup=builder.as_markup()
        )
    await query.answer()