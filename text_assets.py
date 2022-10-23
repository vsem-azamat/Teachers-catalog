from dataclasses import dataclass

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, \
        InlineKeyboardBuilder

from utils.callback_factory import CategoryTeachersCallbackFactory


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
        td_my_profile = {
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
                KeyboardButton(text=TextMenu.MainMenu.td_my_profile[lang])
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
            'ru': 'Подготовка к вступительным'
        }
        ti_nostr = {
            'ru': 'Подготовка к нострификации'
        }

        @staticmethod
        def kb_teachers_category(lang: str) -> InlineKeyboardMarkup:
            buider = InlineKeyboardBuilder()
            buider.button(
                    text=TextMenu.FindTeachers.ti_for_university[lang],
                    # callback_data=CategoryTeachersCallbackFactory(category="university")
                    switch_inline_query_current_chat="🏫"
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
