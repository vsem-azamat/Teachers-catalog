from typing import  Union

from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.states import TeacherRegistration
from utils.navigation import *
from utils.callback_factory import *

router = Router()

# TEACHER: START REGISTRATION
@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.edit_all))
@router.message(TeacherRegistration.start_registration)
async def start_teacher_registration(
    message_or_callback: Union[types.Message, types.CallbackQuery], 
    state: FSMContext,
    bot: Bot, 
    ):
    await db.check_exists(id_tg=message_or_callback.from_user.id, login=message_or_callback.from_user.username)
    user_language = await db.get_user_language(message_or_callback.from_user.id)
    keyboard = True

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
            
            # If Teacher editing existing profile
            teacher = await db.get_teacher_profile(user_id_tg=message_or_callback.from_user.id)
            if teacher:
                builder = ReplyKeyboardBuilder()
                builder.button(text=teacher.name)
                keyboard = builder.as_markup(resize_keyboard=True)

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
    keyboard = None

    # Correct answer
    if 1 < len(msg.text) < 25 and not await detect_bad_symbols(msg.text):
        # If Teacher editing existing profile
        teacher = await db.get_teacher_profile(user_id_tg=msg.from_user.id)
        if teacher:
            builder = ReplyKeyboardBuilder()
            builder.button(text=teacher.location)
            keyboard = builder.as_markup(resize_keyboard=True)

        await state.update_data(name=msg.text)
        await state.set_state(TeacherRegistration.location)
        text = tm.MyTeachersProfile.text_location_write.get(user_language, 'ru')
        # Bad answer. Try again.
    else:
        await state.set_state(TeacherRegistration.name)
        keyboard = True
        text = tm.MyTeachersProfile.text_name_try_again.get(user_language, 'ru')
    await bot.send_message(chat_id=msg.from_user.id, text=text, reply_markup=keyboard)


@router.message(TeacherRegistration.location)
async def profile_location(msg: types.Message, state: FSMContext):
    user_language = await db.get_user_language(msg.from_user.id)
    keyboard = None
    
    # Correct answer
    if 1 < len(msg.text) < 25:
        # If Teacher editing existing profile
        teacher = await db.get_teacher_profile(user_id_tg=msg.from_user.id)
        if teacher:
            builder = ReplyKeyboardBuilder()
            builder.button(text=teacher.price)
            keyboard = builder.as_markup(resize_keyboard=True)

        await state.update_data(location=msg.text)
        await state.set_state(TeacherRegistration.price)
        text = tm.MyTeachersProfile.text_price_write.get(user_language, 'ru')
    # Bad answer. Try again.
    else:
        await state.set_state(TeacherRegistration.location)
        text = tm.MyTeachersProfile.text_location_try_again.get(user_language, 'ru')
    await msg.reply(text=text, reply_markup=keyboard)


@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.edit_description))
@router.message(TeacherRegistration.price)
async def profile_description(
    message_or_callback: Union[types.Message, types.CallbackQuery],
    state: FSMContext,
    bot: Bot,
    ):
    user_language = await db.get_user_language(message_or_callback.from_user.id)
    keyboard = True
    # Correct answer
    if isinstance(message_or_callback, types.CallbackQuery) or 1 < len(message_or_callback.text) < 100:
        # Add location answer
        if isinstance(message_or_callback, types.Message):
            await state.update_data(price=message_or_callback.text)

        # If Teacher editing existing profile
        teacher = await db.get_teacher_profile(user_id_tg=message_or_callback.from_user.id)
        if teacher:
            builder = ReplyKeyboardBuilder()
            builder.button(text=tm.MyTeachersProfile.text_keep.get(user_language))
            keyboard = builder.as_markup(resize_keyboard=True)

        await state.set_state(TeacherRegistration.description_finish)
        text = tm.MyTeachersProfile.text_description_write.get(user_language, 'ru')
    # Bad answer. Try again.
    else:
        await state.set_state(TeacherRegistration.price)
        text = tm.MyTeachersProfile.text_price_try_again.get(user_language, 'ru')
    await bot.send_message(chat_id=message_or_callback.from_user.id, text=text, reply_markup=keyboard)


@router.message(TeacherRegistration.description_finish)
async def profile_finish(msg: types.Message, state: FSMContext):
    user_language = await db.get_user_language(msg.from_user.id)
    keyboard = None
    
    skip_state = msg.text in tm.MyTeachersProfile.text_keep.values()
    # Correct answer
    if 30 < len(msg.text) < 2500 or skip_state:
        data = await state.get_data()
        if not skip_state:
            data['description'] = msg.text
        await db.add_teacher_profile(id_tg=msg.from_user.id, **data)
        teacher = await db.get_teacher_profile(user_id_tg=msg.from_user.id)
        # Editing finish
        if teacher:
            text = tm.MyTeachersProfile.text_profile_edit_finish.get(user_language)
            text_profile = await teacher_profile_text(teacher=teacher)
        # Creating finish
        else:
            text = tm.MyTeachersProfile.text_profile_finish.get(user_language, 'ru')
            text_profile = await teacher_profile_text(teacher_id_tg=msg.from_user.id)

        await state.clear()
        keyboard = tm.MainMenu.kb_main_menu(user_language)    
    
        await msg.answer(text=text_profile)
        
    # Bad answer. Try again.
    else:
        await state.set_state(TeacherRegistration.description_finish)
        text = tm.MyTeachersProfile.text_description_try_again.get(user_language, 'ru')

    await msg.answer(text=text, reply_markup=keyboard)