from aiogram.fsm.state import StatesGroup, State




class SelectLanguage(StatesGroup):
    new_lang = State()
    lang = State()


class TeacherRegistration(StatesGroup):
    start_registration = State()
    profile_category = State()

    name = State()
    lessons = State()
    universities = State()
