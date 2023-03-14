from typing import List, Optional, Any, Union, Dict

from aiogram import Router, types, F, Bot, filters
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.states import TeacherRegistration
from utils.filters import TeacherSettingsFilter
from utils.navigation import *
from utils.callback_factory import *

router = Router()


@router.message(TeacherSettingsFilter())
async def teachers_profile(msg: types.Message, state: FSMContext):
    user_id_tg = msg.from_user.id
    user_language = await db.get_user_language(user_id_tg)
    teacher = await db.get_teacher_profile(user_id_tg=user_id_tg)
    # if teacher profile exists
    if teacher:
        text_profile = await teacher_profile_text(teacher=teacher)
        text = tm.MyTeachersProfile.text_your_profile.get(user_language, 'ru')
            
        await msg.answer(text=text_profile)
        await msg.answer(text=text,reply_markup=False)
        
    # if teacher profile doen't exist
    else:
        text = tm.MyTeachersProfile.text_create_new_profile.get(user_language, 'ru')
        keyboard = tm.MyTeachersProfile.kb_profile_settings()
        await msg.answer(text=text, reply_markup=keyboard)
        await state.set_state(TeacherRegistration.start_registration)


@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.edit_all))
@router.message(TeacherRegistration.start_registration)
async def start_teacher_registration(
    message_or_callback: Union[types.Message, types.CallbackQuery], 
    state: FSMContext,
    bot: Bot, 
    ):
    user_language = await db.get_user_language(message_or_callback.from_user.id)
    keyboard = None

    # First registration 
    if isinstance(message_or_callback, types.Message):
        message_text = message_or_callback.text

    # Bad answer. Try again.
    if isinstance(message_or_callback, types.Message) and message_text not in tm.MyTeachersProfile.aviable_create_profile_answers:
        await state.set_state(TeacherRegistration.start_registration)
        text = tm.MyTeachersProfile.text_try_again_create_profile.get(user_language, 'ru')
        keyboard = tm.MyTeachersProfile.kb_profile_settings(user_language)
    
    # Correct Answer.
    else:
        # Answer: Yes
        if isinstance(message_or_callback, types.CallbackQuery) or message_text == tm.MyTeachersProfile.td_create_profile_yes:
            text_profile_example = await teacher_profile_text(example=True)
            text = tm.MyTeachersProfile.text_name_write.get(user_language, 'ru')
            await bot.send_message(chat_id=message_or_callback.from_user.id, text=text_profile_example)
            await state.set_state(TeacherRegistration.name)

        # Answer: No -> Return to Main menu
        elif message_or_callback.text == tm.MyTeachersProfile.td_create_profile_no:
            text = tm.MainMenu.text_main_menu.get(user_language, 'ru')
            keyboard = tm.MainMenu.kb_main_menu(user_language)    

    await bot.send_message(chat_id=message_or_callback.from_user.id, text=text, reply_markup=keyboard)


@router.message(TeacherRegistration.name)
async def profile_location(
    msg: types.Message, 
    state: FSMContext, 
    bot: Bot
    ):
    user_language = await db.get_user_language(msg.from_user.id)

    # Correct answer
    if 1 < len(msg.text) < 25:
        await state.update_data(name=msg.text)
        await state.set_state(TeacherRegistration.location)
        text = tm.MyTeachersProfile.text_location_write.get(user_language, 'ru')
        # Bad answer. Try again.
    else:
        await state.set_state(TeacherRegistration.name)
        text = tm.MyTeachersProfile.text_name_try_again.get(user_language, 'ru')
    await bot.send_message(chat_id=msg.from_user.id, text=text)


@router.message(TeacherRegistration.location)
async def profile_location(msg: types.Message, state: FSMContext):
    user_language = await db.get_user_language(msg.from_user.id)
    # Correct answer
    if 1 < len(msg.text) < 25:
        await state.update_data(location=msg.text)
        await state.set_state(TeacherRegistration.price)
        text = tm.MyTeachersProfile.text_price_write.get(user_language, 'ru')
    # Bad answer. Try again.
    else:
        await state.set_state(TeacherRegistration.location)
        text = tm.MyTeachersProfile.text_location_try_again.get(user_language, 'ru')
    await msg.reply(text=text)


@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.edit_description))
@router.message(TeacherRegistration.price)
async def profile_description(
    message_or_callback: Union[types.Message, types.CallbackQuery],
    state: FSMContext,
    bot: Bot,
    ):
    user_language = await db.get_user_language(message_or_callback.from_user.id)
    # Correct answer
    if isinstance(message_or_callback, types.CallbackQuery) or 1 < len(message_or_callback.text) < 100:
        # Add location answer
        if isinstance(message_or_callback, types.Message):
            await state.update_data(price=message_or_callback.text)
        await state.set_state(TeacherRegistration.description_finish)
        text = tm.MyTeachersProfile.text_description_write.get(user_language, 'ru')
    # Bad answer. Try again.
    else:
        await state.set_state(TeacherRegistration.price)
        text = tm.MyTeachersProfile.text_price_try_again.get(user_language, 'ru')
    await bot.send_message(chat_id=message_or_callback.from_user.id, text=text)


@router.message(TeacherRegistration.description_finish)
async def profile_finish(msg: types.Message, state: FSMContext):
    user_language = await db.get_user_language(msg.from_user.id)
    keyboard = None

    # Correct answer
    if 30 < len(msg.text) < 2500:
        data = await state.get_data()
        data['description'] = msg.text
        await db.add_teacher_profile(id_tg=msg.from_user.id, **data)
        await state.clear()
        text_profile = await teacher_profile_text(teacher_id_tg=msg.from_user.id)
        text = tm.MyTeachersProfile.text_profile_finish.get(user_language, 'ru')
        keyboard = tm.MainMenu.kb_main_menu(user_language)    
    
        await msg.answer(text=text_profile)
        
    # Bad answer. Try again.
    else:
        await state.set_state(TeacherRegistration.description_finish)
        text = tm.MyTeachersProfile.text_description_try_again.get(user_language, 'ru')

    await msg.answer(text=text, reply_markup=keyboard)


# TEACHER SETTINGS
@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.teacher))
@router.message(Command('te', prefix='!/'))
async def profile_lessons(msg: types.Message or types.CallbackQuery):
    user_language = await db.get_user_language(msg.from_user.id)
    if await db.get_teacher(user_id_tg=msg.from_user.id):
        text = tm.MyTeachersProfile.text_profile_menu.get(user_language, 'ru')
        text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
        keyboard = tm.MyTeachersProfile.kb_profile_menu(user_language)
        if isinstance(msg, types.Message):
            await msg.answer(text=text_head + text, reply_markup=keyboard)
        elif isinstance(msg, types.CallbackQuery):
            await msg.message.edit_text(text=text_head + text, reply_markup=keyboard)
    else:
        text = tm.MyTeachersProfile.text_profile_lessons_profile_doesnt_exists.get(user_language, 'ru')
        await msg.answer(text=text)



@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.teacher_edit))
async def profile_edit(query: types.CallbackQuery, bot: Bot):
    user_language = await db.get_user_language(query.from_user.id)
    text_head = tm.MyTeachersProfile.text_profile_lessons_head.get(user_language, 'ru')
    text = tm.MyTeachersProfile.text_profile_select_edit.get(user_language, 'ru')
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="👩‍🏫 Всё",
            callback_data=TeacherSettings(pageLevel=TeacherLevels.edit_all).pack()
        ),
        types.InlineKeyboardButton(
            text="📝 Описание",
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
async def profile_lessons(msg: types.Message or types.CallbackQuery):
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

    lessons = await db.get_all_lessons(current_page=current_page, rows_per_page=rows_per_page)
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
    builder.row(types.InlineKeyboardButton(text='↩️', callback_data='teacher'))
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
    builder.row(types.InlineKeyboardButton(text='↩️', callback_data='teacher'))
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