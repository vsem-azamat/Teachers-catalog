from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from databases.db_postgresql import db
from text_assets import TextMenu as tm
from utils.states import SelectLanguage

router = Router()


@router.message(CommandStart(deep_link=False))
async def menu_start_command(msg: types.Message, state: FSMContext):
    user_id_tg = msg.from_user.id
    user_lang = await db.get_user_lang(msg.from_user.id)

    if not user_lang:
        user_lang = msg.from_user.language_code
        user_lang = 'ru'
        if user_lang not in ['ru', 'cz', 'en']:
            user_lang = 'ru'

    state_new_user = await db.check_exists(user_id_tg)
    # Old user
    if state_new_user:
        user_lang = await db.get_user_lang(user_id_tg)
        text = tm.MainMenu.text_main_menu[user_lang]
        keyboard = tm.MainMenu.kb_main_menu(user_lang)

    # New users
    else:
        text = tm.FirstStart.text_first_select_language[user_lang]
        keyboard = tm.FirstStart.kb_first_select_language()
        await db.new_user(user_id_tg, msg.from_user.username)
        await state.set_state(SelectLanguage.lang)
        await state.update_data(user_lang=user_lang)

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
        await db.update_user_lang(id_tg=msg.from_user.id, lang=new_user_lang)
        await state.clear()
        text = tm.FirstStart.text_end_select_language[new_user_lang]
        keyboard = tm.MainMenu.kb_main_menu(new_user_lang)
    await msg.answer(text=text, reply_markup=keyboard)


@router.message(Command('t'))
async def test(msg: types.Message):
    lang = await db.get_user_lang(msg.from_user.id)
    await msg.answer(f'{lang}')
    
