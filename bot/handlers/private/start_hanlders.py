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
async def menu_start_command(msg: types.Message, state: FSMContext, command: types.BotCommand):
    user_id_tg = msg.from_user.id
    user = await db.check_exists(id_tg=msg.from_user.id, login=msg.from_user.username)
    command_text = command.command
    # Old user
    if user.language and not command_text == 'language':
        user_language = str(user.language)
        text = tm.MainMenu.text_main_menu.get(user_language, 'ru')
        keyboard = tm.MainMenu.kb_main_menu(user_language)

    # New users or update language
    else:
        if command_text == 'language':
            user_language = user.language
        else:
            user_language = msg.from_user.language_code
            user_language = 'ru' # DEBUG
            if user_language not in tm.FirstStart.td_languages.keys(): user_language = 'ru'
            await db.update_user_language(id_tg=user_id_tg, user_language=user_language)
        
        text = tm.FirstStart.text_first_select_language.get(user_language, 'ru')

        builder = ReplyKeyboardBuilder()
        for language in tm.FirstStart.td_languages.keys():
            builder.button(text=language)
        keyboard = builder.as_markup(resize_keyboard=True)

        await state.set_state(SelectLanguage.language)
        await state.update_data(user_language=user_language)

    await msg.reply(text=text, reply_markup=keyboard)



@router.message(SelectLanguage.language)
async def set_user_language(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_language = user_data.get('user_language', 'ru')
    new_user_lang = tm.FirstStart.td_languages.get(msg.text, False)

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
        await db.update_user_language(id_tg=msg.from_user.id, user_language=new_user_lang)
        await state.clear()
        text = tm.FirstStart.text_end_select_language.get(new_user_lang, 'ru')
        keyboard = tm.MainMenu.kb_main_menu(new_user_lang)
    await msg.answer(text=text, reply_markup=keyboard)


# Menu for category of teachers
@router.callback_query(F.data == 'back_menu')
@router.message(FindTeachersFilter())
async def category_teachers(msg: types.Message or types.CallbackQuery):
    user_language = await db.get_user_language(msg.from_user.id)
    text_head = tm.TeachersCategory.text_select_head.get(user_language, 'ru')
    text = tm.TeachersCategory.text_select_category.get(user_language, 'ru')
    keyboard = tm.TeachersCategory.kb_teachers_category(user_language)
    if isinstance(msg, types.Message):
        await msg.answer(text=text_head + text, reply_markup=keyboard)
    elif isinstance(msg, types.CallbackQuery):
        await msg.message.edit_text(text=text_head + text, reply_markup=keyboard)
