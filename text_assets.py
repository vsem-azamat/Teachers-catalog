from dataclasses import dataclass

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, \
    InlineKeyboardBuilder

from utils.callback_factory import PageLevels, PageSettings, TeacherLevels, TeacherSettings

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
            "ru": "Привет! Для начала выбери язык, на котором ты хочешь со мной общаться!",
            "cz": "Ahoj! Pro začátek vyber jazyk, ve kterém chceš se mnou komunikovat!",
            "en": "Hello! To start, select the language in which you want to communicate with me!",
            "ua": "Привіт! На початку виберіть мову, на якій ви хочете спілкуватися зі мною!"
        }
        text_again_select_language = {
            "ru": "Выбери язык, нажав на кнопки ниже!",
            "cz": "Zvolte jazyk stisknutím tlačítek níže!",
            "en": "Select a language by pressing the buttons below!",
            "ua": "Оберіть мову, натиснувши кнопки нижче!"
        }
        text_end_select_language = {
            "ru": "Язык выбран!",
            "cz": "Jazyk zvolen!",
            "en": "Language selected!",
            "ua": "Мова вибрана!"
        }

        td_selest_ru = "ru"
        td_select_en = "en"
        td_select_cz = "cz"
        td_select_ua = "ua"

        aviable_languages = [td_selest_ru, td_select_en, td_select_cz, td_select_ua]

        @staticmethod
        def kb_first_select_language() -> ReplyKeyboardMarkup:
            builder = ReplyKeyboardBuilder()
            builder.row(
                KeyboardButton(text=TextMenu.FirstStart.td_selest_ru),
                KeyboardButton(text=TextMenu.FirstStart.td_select_cz),
                KeyboardButton(text=TextMenu.FirstStart.td_select_ua),
                KeyboardButton(text=TextMenu.FirstStart.td_select_en),
            )
            return builder.as_markup(resize_keyboard=True)

    class MainMenu:
        """
        /start - Main user menu.

        Default buttons.
        """
        text_main_menu = {
            "ru": 
                "Привет Я бот КОННЕКТ! 🤖\n\n"\
                
                "Я нужен, что бы помочь тебе сориентироваться в нашем пространстве.\n\n"\
                
                "Здесь ты сможешь найти себе репетитора или предложить свои услуги."\
                "На данный момент моя база только пополняется :)\n\n"\
                
                "<b>Здесь ты можешь:</b>\n"\
                "📍 Найти репетитора и помощь\n"
                "📍 Бесплатно попасть в каталог репетиторов\n"\
                "📍 Найти студенческие чаты/каналы\n"\
                "📍 Предложить сотрудничество\n",
        }

        td_find_teachers = {
            'ru': 'Найти репетитора.',
            'cz': 'Najít učitele.',
            'en': 'Find a tutor.',
            'ua': 'Знайти репетитора.'
        }
        td_chats_for_university = {
            'ru': 'Чаты по ВУЗ-ам',
            'cz': 'Chaty podle VŠ',
            'en': 'Chats by universities',
            'ua': 'Чати за ВНЗ'
        }
        td_about_us = {
            'ru': 'Обо мне',
            'cz': 'O nás',
            'en': 'About us',
            'ua': 'Про нас'
        }
        td_my_teachers_profile = {
            'ru': 'Личный кабинет репетитора',
            'cz': 'Můj profil učitele',
            'en': 'My tutor profile',
            'ua': 'Мій профіль репетитора'
        }

        @staticmethod
        def kb_main_menu(language: str) -> ReplyKeyboardMarkup:
            builder = ReplyKeyboardBuilder()
            builder.row(
                KeyboardButton(text=TextMenu.MainMenu.td_find_teachers[language])
            )
            builder.row(
                KeyboardButton(text=TextMenu.MainMenu.td_chats_for_university[language]),
                KeyboardButton(text=TextMenu.MainMenu.td_about_us[language])
            )
            builder.row(
                KeyboardButton(text=TextMenu.MainMenu.td_my_teachers_profile[language])
            )
            return builder.as_markup(resize_keyboard=True)

    class TeachersCategory:
        """
        Inline buttons.
        """


        text_select_category = {
            "ru": "👩‍🏫 <b>Выбери нужный раздел!</b>",
            "cz": "👩‍🏫 <b>Vyberte požadovanou sekci!</b>",
            "en": "👩‍🏫 <b>Select the required section!</b>",
            "ua": "👩‍🏫 <b>Виберіть потрібний розділ!</b>"
        }

        ti_universities = {
            'ru': '🏫 По ВУЗ-ам',
            'cz': '🏫 Podle VŠ',
            'en': '🏫 By universities',
            'ua': '🏫 За ВНЗ'
        }
        ti_languages = {
            'ru': '🔠 Языки',
            'cz': '🔠 Jazyky',
            'en': '🔠 Languages',
            'ua': '🔠 Мови'
        }
        ti_lessons = {
            'ru': '📚 По предметам',
            'cz': '📚 Podle předmětů',
            'en': '📚 By subjects',
            'ua': '📚 За предметами'
        }


        @staticmethod
        def kb_teachers_category(language: str) -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()
            builder.button(
                text=TextMenu.TeachersCategory.ti_universities[language],
                callback_data="universities"
            )
            builder.button(
                text=TextMenu.TeachersCategory.ti_languages[language],
                callback_data="languages"
            )
            builder.button(
                text=TextMenu.TeachersCategory.ti_lessons[language],
                callback_data="lessons"
            )
            builder.adjust(2)
            return builder.as_markup()

        text_select_head = {
            "ru": 
                "🟰🟰🟰🟰🔎🟰🟰🟰🟰\n"\
                "<b>-> Поиск репетитора</b>\n\n",
            "cz":
                "🟰🟰🟰🟰🔎🟰🟰🟰🟰\n"
                "<b>-> Vyhledávání doučujícího</b>\n\n",
            "en":
                "🟰🟰🟰🟰🔎🟰🟰🟰🟰\n"
                "<b>-> Tutor search</b>\n\n",
            "ua":
                "🟰🟰🟰🟰🔎🟰🟰🟰🟰\n"
                "<b>-> Пошук репетитора</b>\n\n"  
        }

        text_select_university = {
            'ru': '🏫 <b>Сортировка предметов по ВУЗ-ам:</b>',
            'cz': '🏫 <b>Třídit předměty podle VŠ:</b>',
            'en': '🏫 <b>Sort subjects by universities:</b>',
            'ua': '🏫 <b>Сортування предметів за ВНЗ:</b>'
        }
        text_select_lesson_of_university = {
            'ru': '📚 <b>Сортировка репетиторов по предметам:</b>',
            'en': '📚 <b>Sorting tutors by subjects:</b>',
            'cz': '📚 <b>Třídění lektorů podle předmětů:</b>',
            'ua': '📚 <b>Сортування репетиторів за предметами:</b>'
            }

        text_select_language = {
            'ru': '🔠 <b>Сортировка предметов по Языкам:</b>',
            'en': '🔠 <b>Sorting subjects by Languages:</b>',
            'cz': '🔠 <b>Třídění předmětů podle jazyků:</b>',
            'ua': '🔠 <b>Сортування предметів за Мовами:</b>'
            }

        text_show_teachers = {
            'ru': '<b>📚 Репетиторы по предмету:</b>',
            'en': '<b>📚 Tutors by subject:</b>',
            'cz': '<b>📚 Lektoři podle předmětu:</b>',
            'ua': '<b>📚 Репетитори за предметом:</b>'
            }

        text_lessons_search = {
            'ru': '📚 Выберите способ поиска репетиторов по предмету:',
            'en': '📚 Choose a way to search for tutors by subject:',
            'cz': '📚 Vyberte způsob vyhledávání lektorů podle předmětu:',
            'ua': '📚 Виберіть спосіб пошуку репетиторів за предметом:'
            }

        ti_lessons_search_with_catalog = {
            'ru': '🗂 Каталог всех предметов',
            'en': '🗂 Catalog of all subjects',
            'cz': '🗂 Katalog všech předmětů',
            'ua': '🗂 Каталог усіх предметів'
            }
        ti_lessons_search_with_google = {
            'ru': '🔎 Поиск предмета по названию',
            'en': '🔎 Search for a subject by name',
            'cz': '🔎 Vyhledávání předmětu podle názvu',
            'ua': '🔎 Пошук предмету за назвою'
            }

        @staticmethod
        def kb_lessons_category(language: str) -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(
                    text=TextMenu.TeachersCategory.ti_lessons_search_with_catalog.get(language, 'ru'),
                    callback_data=PageSettings(
                        pageLevel=PageLevels.lessons_catalog,
                        ).pack()
                    ),
                InlineKeyboardButton(
                    text=TextMenu.TeachersCategory.ti_lessons_search_with_google.get(language, 'ru'),
                    switch_inline_query_current_chat=""
                    ),
                InlineKeyboardButton(
                    text='↩️', 
                    callback_data='back_menu'
                    )
                )
            builder.adjust(1)
            return builder.as_markup()

    class MyTeachersProfile:
        """
        Default buttons.
        """
        text_create_new_profile = {
            "ru": "У вас еще нет профиля репетитора! Хотите создать?",
            "en": "You do not have a tutor profile yet! Would you like to create one?",
            "cz": "Nemáte ještě profil učitele! Chcete vytvořit profil?",
            "ua": "У вас ще немає профілю репетитора! Хочете створити?"
            }

        text_your_profile = {
            'ru': '<b>Ваш профиль</b> ⬆️',
            'en': '<b>Your Profile</b> ⬆️',
            'cz': '<b>Váš profil</b> ⬆️',
            'ua': '<b>Ваш профіль</b> ⬆️'
            }

        td_create_profile_yes = "✅"
        td_create_profile_no = "❌"

        aviable_create_profile_answers = [td_create_profile_no, td_create_profile_yes]

        text_try_again_create_profile = {
            "ru": "Нажмите на одну из кнопок ниже!",
            "en": "Click on one of the buttons below!",
            "cz": "Klikněte na jedno z tlačítek níže!",
            "ua": "Натисніть на одну з кнопок нижче!"
            }

        @staticmethod
        def kb_profile_settings() -> ReplyKeyboardMarkup:
            builder = ReplyKeyboardBuilder()
            builder.row(
                KeyboardButton(text=TextMenu.MyTeachersProfile.td_create_profile_yes),
                KeyboardButton(text=TextMenu.MyTeachersProfile.td_create_profile_no)
            )
            return builder.as_markup(resize_keyboard=True)

        text_name_write = {
            'ru': "<b>Ваш профиль будет выглядить подобным образом!</b> ⬆️\n"
                "Рекомундую заполнять всё латиницей, кроме описания профиля!"
                "Можете не бояться сделать ошибку, у вас всегда будет возможность потом подправить свои данные!\n\n"
                "<b>Помните, что данные не должны содержать спец символы:</b> /\>[_*...:\n\n"
                "Напишите свое имя:",
            'en': "<b>Your profile will look similar to this!</b> ⬆️\n"
                "I recommend filling everything in Latin script except for the profile description! "
                "Don't be afraid to make a mistake, you will always have the opportunity to correct your data later!\n\n"
                "<b>Remember, data should not contain special characters:</b> /\>[_*...:\n\n"
                "Write your name:",
            'cs': "<b>Váš profil bude vypadat podobně!</b> ⬆️\n"
                "Doporučuji vyplnit všechno latinkou kromě popisu profilu! "
                "Nebojte se udělat chybu, později budete mít vždy možnost opravit svá data!\n\n"
                "<b>Pamatujte si, že data by neměla obsahovat speciální znaky:</b> /\>[_*...:\n\n"
                "Napište své jméno:",
            'uk': "<b>Ваш профіль виглядатиме наступним чином!</b> ⬆️\n"
                "Рекомендую заповнювати все латиницею, крім опису профілю! "
                "Не бійтеся робити помилку, у вас завжди буде можливість потім виправити свої дані!\n\n"
                "<b>Пам'ятайте, що дані не повинні містити спеціальні символи:</b> /\>[_*...:\n\n"
                "Напишіть своє ім'я:"
                }

        text_name_try_again = {
            'ru': 
                "Попробуйте еще раз, вы что-то ввели неккоректно\n"\
                " - имя должно быть от 2 до 25 символов\n",
            'en':
                "Try again, you entered something incorrectly\n"
                " - name must be between 2 and 25 characters long\n",
            'cz':
                'Zkuste to znovu, zadal jste něco špatně\n'
                '- jméno musí být 2 až 25 znaků dlouhé\n',
            'ua':
                "Спробуйте ще раз, ви щось ввели неправильно\n"
                " - ім'я повинно бути від 2 до 25 символів\n"
        }


        text_location_write = {
            'ru': 
                "Перечислите кратко где и как проходят занятия!\n"\
                "Пример: Прага, Скайп, Дискорд, Библиотека",
            'cz':
                "Stručně vyjmenujte, kde a jak probíhají lekce!\n"\
                "Příklad: Praha, Skype, Discord, knihovna",
            'en':
                "List briefly where and how the lessons take place!\n"\
                "Example: Prague, Skype, Discord, library",
            'ua':
                "Перелічіть коротко де і як проходять заняття!\n"\
                "Приклад: Прага, Скайп, Дискорд, Бібліотека"
            }

        text_location_try_again = {
            "ru":
                "Попробуйте еще раз, вы что-то ввели некорректно\n"\
                " - текст должен быть от 2 до 100 символов\n",
            'cz':
                "Zkuste to znovu, něco jste zadal(a) nesprávně\n"\
                " - text by měl mít délku od 2 do 100 znaků\n",
            'en':
                "Try again, you entered something incorrectly\n"\
                " - the text should be from 2 to 100 characters long\n",
            'ua':
                "Спробуйте ще раз, ви щось ввели неправильно\n"\
                " - текст повинен бути від 2 до 100 символів\n"
                }


        text_price_write = {
            "ru":
                "Напишите стоимость занятий!\n"\
                "Пример: 300-500 Kč/час",
            "cz":
                "Napište cenu lekcí!\n"\
                "Příklad: 300-500 Kč/hod",
            "en":
                "Write down the price of the lessons!\n"\
                "Example: 300-500 CZK/hour",
            "ua":
                "Напишіть вартість занять!\n"\
                "Приклад: 300-500 Kč/год"
            }

        text_price_try_again = {
            "ru":
                "Попробуйте еще раз, вы что-то ввели некорректно\n"\
                " - текст должен быть от 2 до 25 символов\n",
            "cz":
                "Zkuste to znovu, něco jste zadal(a) nesprávně\n"\
                " - text by měl mít délku od 2 do 25 znaků\n",
            "en":
                "Try again, you entered something incorrectly\n"\
                " - the text should be from 2 to 25 characters long\n",
            "ua":
                "Спробуйте ще раз, ви щось ввели неправильно\n"\
                " - текст повинен бути від 2 до 25 символів\n"
            }


        text_description_write = {
            "ru": 
                "Напишите описание к своему профилю!\n"\
                "Учтите, что в каталоге репетиторов, видно будет только первые 4-5 строк описания.\n"\
                "Полный текст будет виден человека при полном открытии профиля.",
            "cz": 
                "Napište popis svého profilu!\n"\
                "V katalogu lektorů bude vidět pouze prvních 4-5 řádků popisu.\n"\
                "Celý text bude viditelný pro osobu při úplném otevření profilu.",
            "en": 
                "Write a description for your profile!\n"\
                "Note that in the tutor directory, only the first 4-5 lines of the description will be visible.\n"\
                "The full text will be visible to a person when the profile is fully opened.",
            "uk": 
                "Напишіть опис до свого профілю!\n"\
                "Зверніть увагу, що в каталозі репетиторів, буде видно тільки перші 4-5 рядків опису.\n"\
                "Повний текст буде видно людині при повному відкритті профілю."
            }
        
        text_description_try_again = {
            "ru":
                "Попробуйте еще раз, вы что-то ввели неккоректно\n"\
                " - текст описания должен быть от 30 до 2500 символов\n",
            "cz":
                "Zkuste to znovu, něco jste zadal nesprávně\n"\
                " - popis textu by měl být od 30 do 2500 znaků\n",
            "en":
                "Please try again, you entered something incorrectly\n"\
                " - description text should be between 30 and 2500 characters\n",
            "ua":
                "Спробуйте ще раз, ви щось ввели неправильно\n"\
                " - текст опису має бути від 30 до 2500 символів\n"
            }


        text_profile_finish = {
            "ru": 
                "<b>Ваш профиль почти готов!</b> ⬆️\n"
                "Осталось только выбрать предметы, чтобы ваш профиль было видно в соответствующих каталогах.\n\n"
                "Чтобы это сделать, используйте комманду /teacher"
        }

        text_profile_menu = {
            "ru":
                "Здесь вы можете самостоятельно редактировать свои профиль репетитора:"
        }

        text_profile_lessons_head = {
            "ru": 
                "🟰🟰🟰🟰🎓🟰🟰🟰🟰\n"\
                "<b>-> Вы в меню репетитора!</b>\n\n"
        }
        text_profile_lessons = {
            "ru": 
                "Предметы отсорторованы в приведенных ниже категориях."\
                "Выберите предмет, который хотите добавить себе, чтобы ваш профиль отображался в каталоге!"\
        }

        text_profile_lessons_profile_doesnt_exists = {
            "ru": 
                "У вас еще нет профиля нет профиля репетитора! Чтобы создать, нажмите на <b>Личный кабинет.</b>"
        }

        text_profile_lessons_universities = {
            "ru":
                "Сортировка предметов по ВУЗ-ам:"
        }

        text_profile_lessons_select = {
            "ru":
                "Выберите  предмет, который хотите добавить к себе профиль:"
        }
        
        text_profile_lessons_catalog = {
            "ru": 
                "Каталог всех предметов!"
        }
        

        text_profile_select_edit = {
            "ru": 
                "<b>Редактировать:</b>"
        }

        ti_profile_lessons_add_delete = {
            "ru":
                "📚 Добавить/Убрать предметы"
        }
        ti_profile_edit = {
            "ru":
                "✍ Редактировать профиль"
        }
        @staticmethod
        def kb_profile_menu(language: str) -> InlineKeyboardMarkup:
            builder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(
                    text=TextMenu.MyTeachersProfile.ti_profile_edit.get(language, 'ru'),
                    callback_data=TeacherSettings(
                        pageLevel=TeacherLevels.teacher_edit,
                        ).pack()
                    ),
                InlineKeyboardButton(
                    text=TextMenu.MyTeachersProfile.ti_profile_lessons_add_delete.get(language, 'ru'),
                    callback_data=TeacherSettings(
                        pageLevel=TeacherLevels.lessons
                        ).pack()
                    )
                )
            builder.adjust(1)
            return builder.as_markup()