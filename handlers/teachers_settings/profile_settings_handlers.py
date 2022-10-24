from aiogram import Router, types, F, Bot, filters
from aiogram.fsm.context import FSMContext

from databases.mongodb import mongodb
from text_assets import TextMenu as tm
from utils.states import TeacherRegistration

router = Router()


@router.message(F.text in tm.MainMenu.td_my_teachers_profile.values())
async def my_teachers_profile(msg: types.Message, state: FSMContext):
    user_lang = mongodb.get_user_lang(msg.from_user.id)
    teachers_profile = mongodb.get_my_teachers_profile(msg.from_user.id)

    # if teacher profile exists
    if teachers_profile:
        pass
    # if teacher profile doen't exist
    else:
        text = tm.MyTeachersProfile.text_create_new_profile[user_lang]
        keyboard = tm.MyTeachersProfile.kb_ask_registration(user_lang)
        await msg.answer(text=text, reply_markup=keyboard)
        await state.set_state(TeacherRegistration.start_registration)


@router.message(TeacherRegistration.start_registration)
async def start_teacher_registration(msg: types.Message, state: FSMContext):
    user_lang = mongodb.get_user_lang(msg.from_user.id)
    if msg.text not in tm.MyTeachersProfile.aviable_create_profile_answers:
        text = tm.MyTeachersProfile.text_try_again_create_profile[user_lang]
        keyboard = tm.MyTeachersProfile.kb_ask_registration(user_lang)
        await msg.reply(text=text, reply_markup=keyboard)
        await state.set_state(TeacherRegistration.start_registration)

    else:
        pass
