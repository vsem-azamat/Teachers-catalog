from aiogram.fsm.state import StatesGroup, State


class SelectLanguage(StatesGroup):
    new_lang = State()
    language = State()


class TeacherRegistration(StatesGroup):
    start_registration = State()
    name = State()
    location = State()
    price = State()
    description_finish = State()
