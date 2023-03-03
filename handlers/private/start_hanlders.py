from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.states import SelectLanguage
from utils.filters import FindTeachersFilter
from utils.callback_factory import *
from utils.states import TeacherRegistration

router = Router()

@router.message(CommandStart(deep_link=False))
async def menu_start_command(msg: types.Message, state: FSMContext):
    user_id_tg = msg.from_user.id
    user = await db.check_exists(id_tg=msg.from_user.id, login=msg.from_user.username)

    # Old user
    if user.language:
        user_language = user.language
        text = tm.MainMenu.text_main_menu[user_language]
        keyboard = tm.MainMenu.kb_main_menu(user_language)

    # New users
    else:
        user_language = msg.from_user.language_code
        user_language = 'ru' # DEBUG
        if user_language not in ['ru', 'en', 'cz']:
            user_language = 'ru'
        await db.update_user_lang(id_tg=user_id_tg, language=user_language)
        text = tm.FirstStart.text_first_select_language[user_language]
        keyboard = tm.FirstStart.kb_first_select_language()
        await state.set_state(SelectLanguage.lang)
        await state.update_data(user_lang=user_language)

    await msg.reply(text=text, reply_markup=keyboard)


@router.message(SelectLanguage.lang)
async def set_user_language(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_lang = user_data['user_lang']
    new_user_lang = msg.text

    # Bad answer. Try again.
    if new_user_lang not in tm.FirstStart.aviable_languages:
        await state.set_state(SelectLanguage.lang)
        text = tm.FirstStart.text_again_select_language[user_lang]
        keyboard = tm.FirstStart.kb_first_select_language()
    
    # Correct Answer. Set `new_user_lang`
    else:
        await db.update_user_lang(id_tg=msg.from_user.id, language=new_user_lang)
        await state.clear()
        text = tm.FirstStart.text_end_select_language[new_user_lang]
        keyboard = tm.MainMenu.kb_main_menu(new_user_lang)
    await msg.answer(text=text, reply_markup=keyboard)


@router.callback_query(F.data == 'back_menu')
@router.message(FindTeachersFilter())
async def category_teachers(msg: types.Message or types.CallbackQuery):
    user_lang = await db.get_user_lang(msg.from_user.id)
    text = tm.FindTeachers.text_find_teachers[user_lang]
    keyboard = tm.FindTeachers.kb_teachers_category(user_lang)
    if isinstance(msg, types.Message):
        await msg.answer(text=text, reply_markup=keyboard)
    elif isinstance(msg, types.CallbackQuery):
        await msg.message.edit_text(text=text, reply_markup=keyboard)
