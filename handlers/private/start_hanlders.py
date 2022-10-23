from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from databases.mongodb import mongodb
from text_assets import TextMenu as tm

router = Router()


class Form(StatesGroup):
    new_lang = State()
    lang = State()


@router.message(CommandStart())
async def menu_start_command(msg: types.Message, state: FSMContext) -> None:
    user_id_tg = msg.from_user.id
    user_lang = mongodb.get_user_lang(msg.from_user.id)

    if not user_lang:
        user_lang = msg.from_user.language_code
        if user_lang not in ['ru', 'cz']:
            user_lang = 'ru'

    state_new_user = mongodb.new_user(user_id_tg, user_lang)
    # Old user
    if state_new_user:
        user_lang = mongodb.get_user_lang(user_id_tg)

        text = tm.MainMenu.text_main_menu[user_lang]
        keyboard = tm.MainMenu.kb_main_menu(user_lang)
        await msg.answer(text=text, reply_markup=keyboard)
    # New users
    else:
        text = tm.FirstStart.text_first_select_language[user_lang]
        keyboard = tm.FirstStart.kb_first_select_language()
        await state.set_state(Form.lang)
        await state.update_data(user_lang=user_lang)

        await msg.answer(text=text, reply_markup=keyboard)


@router.message(Form.lang)
async def set_user_language(msg: types.Message, state: FSMContext):
    new_user_lang = msg.text
    user_data = await state.get_data()
    user_lang = user_data['user_lang']

    # Bad answer. Try again.
    if new_user_lang not in tm.FirstStart.aviable_languages:

        await state.set_state(Form.lang)
        text = tm.FirstStart.text_again_select_language[user_lang]
        keyboard = tm.FirstStart.kb_first_select_language()
        await msg.answer(text=text, reply_markup=keyboard)

    # Correct Answer. Set `new_user_lang`
    else:
        await state.clear()
        mongodb.update_user_lang(id_tg=msg.from_user.id, lang=new_user_lang)
        text = tm.FirstStart.text_end_select_language[new_user_lang]
        keyboard = tm.MainMenu.kb_main_menu(new_user_lang)
        await msg.answer(text=text, reply_markup=keyboard)

