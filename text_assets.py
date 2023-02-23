from dataclasses import dataclass

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, \
    InlineKeyboardBuilder

from utils.callback_factory import CategoryTeachersCallbackFactory
from utils.gen_button import genButton

@dataclass
class TextMenu:
    """
    Collection of texts for messages, buttons with language variants.

    text_ : text from message
    td_: text for default buttons
    ti_: text for inline buttons
    """

    class FirstStart:
        """
        /start - Fist user start.

        Default buttons.
        """
        text_first_select_language = {
            "ru": "Привет! Для начала выбери язык, на котором ты хочешь со мной общаться!"
        }
        text_again_select_language = {
            "ru": "Выбери язык, нажав на кнопки ниже!"
        }
        text_end_select_language = {
            "ru": "Язык выбран!"
        }

        td_selest_ru = "ru"
        td_select_en = "en"

        aviable_languages = [td_selest_ru, td_select_en, ]

        @staticmethod
        def kb_first_select_language() -> ReplyKeyboardMarkup:
            builder = ReplyKeyboardBuilder()
            builder.row(
                KeyboardButton(text=TextMenu.FirstStart.td_selest_ru),
                KeyboardButton(text=TextMenu.FirstStart.td_select_en)
            )
            return builder.as_markup(resize_keyboard=True)

    class MainMenu:
        """
        /start - Main user menu.

        Default buttons.
        """
        text_main_menu = {
            "ru": "Главное меню.\n\nТут инструкция к боту."
        }

        td_find_teachers = {
            'ru': 'Найти репетитора.'
        }
        td_chats_for_university = {
            'ru': 'Чаты по ВУЗ-ам'
        }
        td_about_us = {
            'ru': 'О нас'
        }
        td_my_teachers_profile = {
            'ru': 'Личный кабинет репетитора'
        }

        @staticmethod
        def kb_main_menu(lang: str) -> ReplyKeyboardMarkup:
            builder = ReplyKeyboardBuilder()
            builder.row(
                KeyboardButton(text=TextMenu.MainMenu.td_find_teachers[lang])
            )
            builder.row(
                KeyboardButton(text=TextMenu.MainMenu.td_chats_for_university[lang]),
                KeyboardButton(text=TextMenu.MainMenu.td_about_us[lang])
            )
            builder.row(
                KeyboardButton(text=TextMenu.MainMenu.td_my_teachers_profile[lang])
            )
            return builder.as_markup(resize_keyboard=True)

    class FindTeachers:
        """
        Inline buttons.
        """
        text_find_teachers = {
            "ru": "Выбери нужный раздел с репетиторами!"
        }

        ti_for_university = {
            'ru': 'По ВУЗ-ам'
        }
        ti_for_lessons = {
            'ru': 'По предметам'
        }
        ti_exams = {
            'ru': 'Вступительным'
        }
        ti_nostr = {
            'ru': 'Нострификации'
        }

        @staticmethod
        def kb_teachers_category(lang: str) -> InlineKeyboardMarkup:
            buider = InlineKeyboardBuilder()
            buider.button(
                text=TextMenu.FindTeachers.ti_for_university[lang],
                callback_data='univ'
            )
            buider.button(
                text=TextMenu.FindTeachers.ti_for_lessons[lang],
                switch_inline_query_current_chat=" 📚"
            )
            buider.button(
                text=TextMenu.FindTeachers.ti_exams[lang],
                switch_inline_query_current_chat="📝"
            )
            buider.button(
                text=TextMenu.FindTeachers.ti_nostr[lang],
                switch_inline_query_current_chat="📓"
            )
            buider.adjust(2)
            return buider.as_markup()


    class MyTeachersProfile:
        """
        Default buttons.
        """
        text_create_new_profile = {
            "ru": "У вас еще нет профиля репетитора! Хотите создать?"
        }

        td_create_profile_yes = "✅"
        td_create_profile_no = "❌"

        aviable_create_profile_answers = [td_create_profile_no, td_create_profile_yes]

        text_try_again_create_profile = {
            "ru": "Нажмите на одну из кнопок ниже!"
        }

        @staticmethod
        def kb_ask_registration(lang: str) -> ReplyKeyboardMarkup:
            builder = ReplyKeyboardBuilder()
            builder.row(
                KeyboardButton(text=TextMenu.MyTeachersProfile.td_create_profile_yes),
                KeyboardButton(text=TextMenu.MyTeachersProfile.td_create_profile_no)
            )
            return builder.as_markup(resize_keyboard=True)

        text_profile_category = {
            "ru": "Для большей гибкости мы разделили систему для поступающих и для студентов.\n\n"
                  "Выбери какой профиль ты хочешь создать для начала!"
        }

        td_create_profile_for_students = {
            "ru": "Для студентов"
        }

        td_create_profile_for_schools = {
            "ru": "Для поступающих"
        }

        aviable_profile_category_answers = [
            td_create_profile_for_schools["ru"], td_create_profile_for_students["ru"]
        ]

        @staticmethod
        def kb_ask_new_profile_category(lang: str) -> ReplyKeyboardMarkup:
            builder = ReplyKeyboardBuilder()
            builder.row(
                KeyboardButton(text=TextMenu.MyTeachersProfile.td_create_profile_for_students[lang]),
                KeyboardButton(text=TextMenu.MyTeachersProfile.td_create_profile_for_schools[lang])
            )
            return builder.as_markup(resize_keyboard=True)

    