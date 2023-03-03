from aiogram import Router, types, F, Bot, filters
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import KeyboardBuilder, InlineKeyboardBuilder

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
    user_lang = await db.get_user_lang(user_id_tg)
    teacher = await db.get_teacher_profile(user_id_tg=user_id_tg)
    # if teacher profile exists
    if teacher:
        text_profile = await teacher_profile_text(teacher=teacher)
        text = \
            "Ваш профиль:'\n"\
            
        await msg.answer(text=text_profile)
        await msg.answer(
            text=text,
            reply_markup=False
            )
        
    # if teacher profile doen't exist
    else:
        # text = tm.MyTeachersProfile.text_create_new_profile[user_lang]
        text = "У вас еще нет профиля репетитора! Хотите создать?"
        keyboard = tm.MyTeachersProfile.kb_ask_registration(user_lang)
        await msg.answer(text=text, reply_markup=keyboard)
        await state.set_state(TeacherRegistration.start_registration)


@router.message(TeacherRegistration.start_registration)
async def start_teacher_registration(msg: types.Message, state: FSMContext):
    user_language = await db.get_user_lang(msg.from_user.id)

    # Bad answer. Try again.
    if msg.text not in tm.MyTeachersProfile.aviable_create_profile_answers:
        text = tm.MyTeachersProfile.text_try_again_create_profile[user_language]
        keyboard = tm.MyTeachersProfile.kb_ask_registration(user_language)
        await msg.reply(text=text, reply_markup=keyboard)
        await state.set_state(TeacherRegistration.start_registration)

    # Correct Answer.
    else:
        # Answer: No 
        if msg.text == tm.MyTeachersProfile.td_create_profile_no:
            text = tm.MainMenu.text_main_menu[user_language]
            keyboard = tm.MainMenu.kb_main_menu(user_language)
        # Answer: Yes
        else:
            # text = tm.MyTeachersProfile.text_profile_category[user_language]
            # keyboard = tm.MyTeachersProfile.kb_ask_new_profile_category(user_language)

            text = \
                "Ваш профиль будет выглядить подобным образом! (стрелка вверх)\n\n"\
                "Напиши свое имя:"
            text_profile = await teacher_profile_text(example=True)
            await msg.answer(text=text_profile)
            await msg.reply(text=text)
            await state.set_state(TeacherRegistration.name)


@router.message(TeacherRegistration.name)
async def profile_location(msg: types.Message, state: FSMContext):
    user_language = await db.get_user_lang(msg.from_user.id)
    # Correct answer
    if 1 < len(msg.text) < 15:
        await state.update_data(name=msg.text)
        text = \
            "Напиши перечисли кратко где и как проходят занятия!\n"\
            "Пример: Прага, Скайп, Дискорд, Библиотека"
        await msg.reply(text=text)
        await state.set_state(TeacherRegistration.location)

    # Bad answer. Try again.
    else:
        text = tm.MyTeachersProfile.text_try_again_create_profile[user_language]
        await msg.reply(text=text)
        await state.set_state(TeacherRegistration.name)


@router.message(TeacherRegistration.location)
async def profile_location(msg: types.Message, state: FSMContext):
    user_language = await db.get_user_lang(msg.from_user.id)
    # Correct answer
    if 1 < len(msg.text) < 100:
        await state.update_data(location=msg.text)
        text = \
            "Напиши стоимость занятий!\n"\
            "Пример: 150-300 Kc/hod"
        await msg.reply(text=text)
        await state.set_state(TeacherRegistration.price)

    # Bad answer. Try again.
    else:
        text = tm.MyTeachersProfile.text_try_again_create_profile[user_language]
        await msg.reply(text=text)
        await state.set_state(TeacherRegistration.location)


@router.message(TeacherRegistration.price)
async def profile_description(msg: types.Message, state: FSMContext):
    user_language = await db.get_user_lang(msg.from_user.id)
    if 1 < len(msg.text) < 100:
        await state.update_data(price=msg.text)
        text = \
            "Теперь напиши описание к своему профилю!\n"\
            "Учти, что в карусели репетиторов, видно будет только первые 4-5 строк описания."\
            "Остальное при полном открытии профиля."
        await msg.reply(text=text)
        await state.set_state(TeacherRegistration.description)
    else:
        text = tm.MyTeachersProfile.text_try_again_create_profile[user_language]
        await msg.reply(text=text)
        await state.set_state(TeacherRegistration.price)



@router.message(TeacherRegistration.description)
async def profile_finish(msg: types.Message, state: FSMContext):
    user_language = await db.get_user_lang(msg.from_user.id)
    data = await state.get_data()
    name = data.get('name')
    location = data.get('location')
    price = data.get('price')
    description = msg.text
    await db.add_teacher_profile(
        id_tg=msg.from_user.id,
        name=name,
        location=location,
        price=price,
        description=description,
    )
    text_profile = await teacher_profile_text(teacher_id_tg=msg.from_user.id)
    text = \
        "Ваш профиль готов!'\n"\
        "Осталось только завершающая часть - добавить предметы, чтобы вас видно было в каталоге!"
    await msg.answer(text=text_profile)
    await msg.answer(text=text, reply_markup=tm.MainMenu.kb_main_menu()[user_language])
    await state.clear()


# TEACHER LESSONS
@router.callback_query(F.data == 'teacher')
@router.message(Command('te', prefix='!/'))
async def profile_lessons(msg: types.Message or types.CallbackQuery, bot: Bot):
    user_language = await db.get_user_lang(msg.from_user.id)
    if await db.get_teacher(user_id_tg=msg.from_user.id):
        text = "Выберите предметы, чтобы добавить к себе в профиль"
        builder = InlineKeyboardBuilder()
        builder.button(
            text=tm.FindTeachers.ti_universities[user_language],
            callback_data=TeacherSettings(pageLevel=TeacherLevels.universities)
            )
        builder.button(
            text=tm.FindTeachers.ti_lessons[user_language],
            callback_data='lessons_profile' 
            )
        builder.button(
            text=tm.FindTeachers.ti_school[user_language],
            callback_data='school_profile' 
            )
        builder.button(
            text=tm.FindTeachers.ti_languages[user_language],
            callback_data=TeacherSettings(pageLevel=TeacherLevels.lessons_language)
            )
        builder.adjust(2)
        if isinstance(msg, types.Message):
            await msg.answer(text=text, reply_markup=builder.as_markup())
        elif isinstance(msg, types.CallbackQuery):
            await msg.message.edit_text(text=text, reply_markup=builder.as_markup())
    else:
        text = "У вас еще нет профиля нет профиля репетитора! Чтобы создать, нажмите на личный кабинет."
        await msg.answer(text=text)



# Show list of Languages
@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.lessons_language))
async def list_universities(query: types.CallbackQuery, callback_data: TeacherSettings, bot: Bot):
    user_language = await db.get_user_lang(query.from_user.id)
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
    languages = await db.get_lessons_languages()
    languages_id_of_teacher = await db.get_languages_id_of_teacher(teacher_id=teacher.id)
    text = "Выберите Язык, который хочешь добавить к себе профиль"

    if languages_id_of_teacher:
        languages_id_of_teacher = [row.id_lesson for row in languages_id_of_teacher]
    else:
        languages_id_of_teacher = []

    builder = InlineKeyboardBuilder()
    for language in languages:
        text_lesson = language.name
        state = 1

        if language.id in languages_id_of_teacher:
            text_lesson = "✅ " + text_lesson
            state = 0
        builder.button(
            text = text_lesson,
            callback_data=TeacherSettings(
                pageLevel=TeacherLevels.lessons_language,
                lesson_id=language.id,
                add = state
            )
        )
    builder.adjust(rows_per_page)
    builder.row(types.InlineKeyboardButton(text='↩️Назад', callback_data='teacher'))
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id, 
        text=text, 
        reply_markup=builder.as_markup()
        )
    await query.answer()


# UNIVERSITIES 
@router.callback_query(PageSettings.filter(F.pageLevel == TeacherLevels.universities))
async def list_universities(callback: types.CallbackQuery, bot: Bot):
    user_language = await db.get_user_lang(callback.from_user.id)
    text = tm.FindTeachers.ti_universities[user_language]
    universities = await db.get_universities()
    builder = InlineKeyboardBuilder()
    for university in universities:
        builder.button(
            text = university.name,
            callback_data=PageSettings(
                pageLevel=TeacherLevels.lessons_university,
                university_id=university.id
            )
        )
    rows_per_page = PageSettings().rows_per_page
    builder.adjust(rows_per_page)
    builder.row(types.InlineKeyboardButton(text='↩️Назад', callback_data='teacher'))
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id, 
        text=text, 
        reply_markup=builder.as_markup()
        )
    await callback.answer()


# @router.callback_query(
#     TeacherSettings.filter(F.pageLevel == TeacherLevels.lessons_university) or\
#     TeacherSettings.filter(F.pageLevel == TeacherLevels.lesson_university)
#     )
# async def list_universities(query: types.CallbackQuery, callback_data: TeacherSettings, bot: Bot):
#     user_language = await db.get_user_lang(query.from_user.id)
#     rows_per_page = PageSettings().rows_per_page
#     teacher = await db.get_teacher(user_id_tg=query.from_user.id)
#     add_lesson = callback_data.add

#     # Add/Delete lesson
#     if callback_data.lesson_id:
#         await db.add_lessons_to_teacher(
#             teacher_id=teacher.id, 
#             lesson_id=callback_data.lesson_id,
#             add=add_lesson,
#             )
#     languages = await db.get_lessons_languages()
#     languages_id_of_teacher = await db.get_languages_id_of_teacher(teacher_id=teacher.id)
#     text = "Выберите Предмет, который хочешь добавить к себе профиль"

#     if languages_id_of_teacher:
#         languages_id_of_teacher = [row.id_lesson for row in languages_id_of_teacher]
#     else:
#         languages_id_of_teacher = []

#     builder = InlineKeyboardBuilder()
#     for language in languages:
#         text_lesson = language.name
#         state = 1

#         if language.id in languages_id_of_teacher:
#             text_lesson = "✅ " + text_lesson
#             state = 0
#         builder.button(
#             text = text_lesson,
#             callback_data=TeacherSettings(
#                 pageLevel=TeacherLevels.lesson_language,
#                 lesson_id=language.id,
#                 add = state
#             )
#         )
#     builder.adjust(rows_per_page)
#     builder.row(types.InlineKeyboardButton(text='↩️Назад', callback_data='teacher'))
#     await bot.edit_message_text(
#         chat_id=query.from_user.id,
#         message_id=query.message.message_id, 
#         text=text, 
#         reply_markup=builder.as_markup()
#         )
#     await query.answer()
