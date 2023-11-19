from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.databases.db_postgresql import db
from bot.text_assets import TextMenu as tm
from bot.utils.states import SelectLanguage
from bot.utils.filters import FindTeachersFilter
from bot.utils.callback_factory import *

router = Router()


@router.message(Command('language', prefix='!/'))
@router.message(CommandStart(deep_link=False))
async def menu_start_command(message: types.Message, state: FSMContext, command: types.BotCommand):
    """
    Start command handler. If user is new, then select language.
    Or if user is update language, then select language.
    """
    user_id_tg = message.from_user.id
    user = await db.check_exists(id_tg=message.from_user.id, login=message.from_user.username)
    command_text = command.command
    # Old user
    if user.language is not None and not command_text == 'language':
        user_language = str(user.language)
        text = tm.MainMenu.text_main_menu.get(user_language, 'ru')
        keyboard = tm.MainMenu.kb_main_menu(user_language)

    # New users or update language
    else:
        if command_text == 'language':
            user_language = str(user.language)
        else:
            user_language = message.from_user.language_code
            user_language = 'ru' # DEBUG
            if user_language not in tm.FirstStart.td_languages.keys(): user_language = 'ru'
            await db.update_user_language(id_tg=user_id_tg, user_language=user_language)
        
        text = tm.FirstStart.text_first_select_language.get(user_language)

        builder = ReplyKeyboardBuilder()
        for language in tm.FirstStart.td_languages.keys():
            builder.button(text=language)
        keyboard = builder.as_markup(resize_keyboard=True)

        await state.set_state(SelectLanguage.language)
        await state.update_data(user_language=user_language)

    await message.reply(text=text, reply_markup=keyboard)


@router.message(SelectLanguage.language)
async def set_user_language(message: types.Message, state: FSMContext):
    """
    Set user language or update.
    """
    user_data = await state.get_data()
    user_language = user_data.get('user_language', 'ru')
    new_user_lang = tm.FirstStart.td_languages.get(message.text, 'ru') # type: ignore

    # Bad answer. Try again.
    if new_user_lang not in tm.FirstStart.td_languages.values():
        await state.set_state(SelectLanguage.language)
        text = tm.FirstStart.text_again_select_language.get(user_language, 'ru')
        builder = ReplyKeyboardBuilder()
        for language in tm.FirstStart.td_languages.keys():
            builder.button(text=language)
        keyboard = builder.as_markup(resize_keyboard=True)

    # Correct Answer. Set `new_user_lang`s
    else:
        await db.update_user_language(id_tg=message.from_user.id, user_language=new_user_lang)
        await state.clear()
        text = tm.FirstStart.text_end_select_language.get(new_user_lang, 'ru')
        keyboard = tm.MainMenu.kb_main_menu(new_user_lang)
    await message.answer(text=text, reply_markup=keyboard)


# Menu for category of teachers
@router.callback_query(F.data == 'back_menu')
@router.message(FindTeachersFilter())
async def category_teachers(message: types.Message or types.CallbackQuery):
    user_language = await db.get_user_language(message.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    text = tm.TeachersCategory.text_select_category.get(user_language, 'ru')
    keyboard = tm.TeachersCategory.kb_teachers_category(user_language)
    if isinstance(message, types.Message):
        await message.answer(text=text_head + text, reply_markup=keyboard)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text=text_head + text, reply_markup=keyboard) # type: ignore
