from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command

from typing import  Union
from pydantic import BaseModel, validator, Field

from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm
from bot.utils.states import TeacherRegistration
from bot.utils.navigation import *
from bot.utils.callback_factory import *

router = Router()

class TeacherNameError(Exception):
    def __init__(self, name):
        self.name = name
        super().__init__(f'Invalid name: {name}')


class TeacherLocationError(Exception):
    def __init__(self, location):
        self.location = location
        super().__init__(f'Invalid location: {location}')

class TeacherPriceError(Exception):
    def __init__(self, price):
        self.price = price
        super().__init__(f'Invalid price: {price}')

class TeacherDescriptionError(Exception):
    def __init__(self, description):
        self.description = description
        super().__init__(f'Invalid description: {description}')


class TeacherValidator(BaseModel):
    id_tg: int = Field(None)
    name: str = Field(None)
    location: str = Field(None)
    price: str = Field(None)
    description: str = Field(None)

    @validator("name")
    def name_validator(cls, name):
        if not 1 < len(name) < 25 or detect_bad_symbols(name):
            raise TeacherNameError(name)
        return name
    
    @validator("location")
    def location_validator(cls, location):
        if not 1 < len(location) < 100 or detect_bad_symbols(location):
            raise TeacherLocationError(location)
        return location
    
    @validator("price")
    def price_validator(cls, price):
        if not 1 < len(price) < 100 or detect_bad_symbols(price):
            raise TeacherPriceError(price)
        return price
    
    @validator("description")
    def description_validator(cls, description):
        if not 30 < len(description) < 2500 or detect_bad_symbols(description):
            raise TeacherDescriptionError(description)
        return description


@router.message(Command('cancel'))
async def cancel(msg: types.Message, state: FSMContext):
    """
    Cancel teacher registration.
    """
    user_language = await db.get_user_language(msg.from_user.id)
    await state.clear()
    text = tm.MyTeachersProfile.text_cancel_registration.get(user_language)
    keyboard = tm.MainMenu.kb_main_menu(user_language).as_markup(resize_keyboard=True)
    await msg.answer(text=text, reply_markup=keyboard)


@router.message(TeacherRegistration.start_registration)
async def start_teacher_registration(message: types.Message, state: FSMContext, bot: Bot):
    """
    Start first teacher registration. 
    Method catch message from Main menu. Answers: Yes or No.
    """
    await db.check_exists(id_tg=message.from_user.id, login=message.from_user.username)
    user_language = await db.get_user_language(message.from_user.id)
    message_text = message.text
    
    # Message == Yes -> Create new profile
    if message_text == tm.MyTeachersProfile.td_create_profile_yes:
    
        # Check if Teacher already has profile -> Strange situation -> Return to Main menu
        teacher = await db.get_teacher(teacher_id_tg=message.from_user.id)
        if teacher:
            text = tm.MainMenu.text_main_menu.get(user_language)
            keyboard = tm.MainMenu.kb_main_menu(user_language).as_markup(resize_keyboard=True)
            await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=keyboard)
            await state.clear()
            return
        
        # Teacher has not profile -> Create new profile
        else:
            text = tm.MyTeachersProfile.text_teacher_write_me_you_name.get(user_language)
            await state.set_state(TeacherRegistration.name)
            await bot.send_message(chat_id=message.from_user.id, text=text)
            return
    
    # Answer == No -> Return to Main menu
    elif message.text == tm.MyTeachersProfile.td_create_profile_no:
        text = tm.MainMenu.text_main_menu.get(user_language)
        keyboard = tm.MainMenu.kb_main_menu(user_language).as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=keyboard)
        await state.clear()
        return

    # Answer is not correct -> Try again -> Return to Main menu
    if message_text not in tm.MyTeachersProfile.aviable_create_profile_answers:
        await state.set_state(TeacherRegistration.start_registration)
        text = tm.MyTeachersProfile.text_try_again_create_profile.get(user_language)
        builder = tm.MyTeachersProfile.kb_profile_settings()
        keyboard = builder.as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=keyboard)


@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.edit_all))
async def teacher_profile_edit(query: types.CallbackQuery, bot: Bot, state: FSMContext):
    """
    Edit teacher profile.
    Method catch callback from teacher menu (Edit all profile)
    """
    user_language = await db.get_user_language(query.from_user.id)
    teacher = await db.get_teacher(teacher_id_tg=query.from_user.id)

    # Check if Teacher already has profile -> Send message
    if teacher:
        builder = ReplyKeyboardBuilder()
        builder.button(text=teacher.name)
        keyboard = builder.as_markup(resize_keyboard=True)

        text = tm.MyTeachersProfile.text_teacher_write_me_you_name.get(user_language)
        await bot.send_message(chat_id=query.from_user.id, text=text, reply_markup=keyboard)
        await state.set_state(TeacherRegistration.name)
        await query.message.delete()

    # Teacher has not profile -> Strange situation -> Return to Main menu
    else:
        text = tm.MainMenu.text_main_menu.get(user_language)
        keyboard = tm.MainMenu.kb_main_menu(user_language).as_markup(resize_keyboard=True)
        await bot.send_message(chat_id=query.from_user.id, text=text, reply_markup=keyboard)
        await state.clear()


@router.message(TeacherRegistration.name)
async def teacher_name_location(message: types.Message, state: FSMContext, bot: Bot):
    """
    Catch teacher name. Send message with request location.
    """
    user_language = await db.get_user_language(message.from_user.id)
    try:
        TeacherValidator(name=message.text)
        keyboard = None
        teacher = await db.get_teacher(teacher_id_tg=message.from_user.id)
        # If Teacher editing existing profile -> Offer old location
        if teacher:
            builder = ReplyKeyboardBuilder()
            builder.button(text=teacher.location)
            keyboard = builder.as_markup(resize_keyboard=True)
        
        text = tm.MyTeachersProfile.text_location_write.get(user_language)
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=keyboard)
        await state.update_data(name=message.text)
        await state.set_state(TeacherRegistration.location)

    # Uncorrect answer
    except TeacherNameError:
        await state.set_state(TeacherRegistration.name)
        text = tm.MyTeachersProfile.text_name_try_again.get(user_language)
        await bot.send_message(chat_id=message.from_user.id, text=text)


@router.message(TeacherRegistration.location)
async def teacher_location_price(message: types.Message, state: FSMContext):
    """
    Catch teacher location. Send message with request price.
    """
    user_language = await db.get_user_language(message.from_user.id)
    try:
        TeacherValidator(location=message.text)
        keyboard = None
        teacher = await db.get_teacher(teacher_id_tg=message.from_user.id)
        # If Teacher editing existing profile -> Offer old price
        if teacher:
            builder = ReplyKeyboardBuilder()
            builder.button(text=teacher.price)
            keyboard = builder.as_markup(resize_keyboard=True)

        text = tm.MyTeachersProfile.text_price_write.get(user_language)
        await message.answer(text=text, reply_markup=keyboard)
        await state.update_data(location=message.text)
        await state.set_state(TeacherRegistration.price)

    # Uncorrect answer
    except TeacherLocationError:
        await state.set_state(TeacherRegistration.location)
        text = tm.MyTeachersProfile.text_location_try_again.get(user_language)
        await message.answer(text=text)


@router.callback_query(TeacherSettings.filter(F.pageLevel == TeacherLevels.edit_description))
@router.message(TeacherRegistration.price)
async def profile_description(message_or_callback: Union[types.Message, types.CallbackQuery], state: FSMContext, bot: Bot):
    """
    Catch teacher price. Send message with request description.
    Can be called from:
        - Message -> This is an ongoing registration
        - CallbackQuery -> Edit description
    """
    user_language = await db.get_user_language(message_or_callback.from_user.id)
    try:
        TeacherValidator(price=message_or_callback.text)
        keyboard = None

        # Event: Message -> This is an ongoing registration -> Update price
        if isinstance(message_or_callback, types.Message):
            await state.update_data(price=message_or_callback.text)

        # If Teacher exists -> Offer old description
        teacher = await db.get_teacher(teacher_id_tg=message_or_callback.from_user.id)
        if teacher:
            builder = ReplyKeyboardBuilder()
            builder.button(text=teacher.description)
            keyboard = builder.as_markup(resize_keyboard=True)

        text = tm.MyTeachersProfile.text_description_write.get(user_language)
        await message_or_callback.answer(text=text, reply_markup=keyboard)
        await state.set_state(TeacherRegistration.description_finish)

    # Uncorrect answer
    except TeacherPriceError:
        await state.set_state(TeacherRegistration.price)
        text = tm.MyTeachersProfile.text_price_try_again.get(user_language)
        await message_or_callback.answer(text=text)


@router.message(TeacherRegistration.description_finish)
async def profile_finish(msg: types.Message, state: FSMContext):
    user_language = await db.get_user_language(msg.from_user.id)
    
    try:
        TeacherDescriptionError(description=msg.text)
        await state.update_data(description=msg.text)
        data = await state.get_data()
        
        # Finish editing of existing profile -> Text: Profile edited
        if await db.get_teacher(teacher_id_tg=msg.from_user.id):
            text = tm.MyTeachersProfile.text_profile_edit_finish.get(user_language)

        # Finish creating of new profile -> Text: Profile created
        else:
            text = tm.MyTeachersProfile.text_profile_finish.get(user_language)
        
        teacher = Teachers(**data)
        teacher.id_tg = msg.from_user.id
        await db.upset_teacher_profile(new_teacher=teacher)
        
        text_profile = await teacher_profile_text(teacher)
        keyboard = tm.MainMenu.kb_main_menu(user_language).as_markup(resize_keyboard=True)
        await msg.answer(text=text_profile, reply_markup=keyboard)
        await state.clear()
        
    # Uncorrect answer
    except TeacherDescriptionError:
        await state.set_state(TeacherRegistration.description_finish)
        text = tm.MyTeachersProfile.text_description_try_again.get(user_language)
        await msg.answer(text=text)

