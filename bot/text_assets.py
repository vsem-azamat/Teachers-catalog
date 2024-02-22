from dataclasses import dataclass

from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.utils.callback_factory import *

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
            "ru": "🌍 <b>Привет! Для начала выбери язык, на котором ты хочешь со мной общаться!</b>",
            "cz": "🌍 <b>Ahoj! Pro začátek vyber jazyk, ve kterém chceš se mnou komunikovat!</b>",
            "en": "🌍 <b>Hello! To start, select the language in which you want to communicate with me!</b>",
            "ua": "🌍 <b>Привіт! На початку виберіть мову, на якій ви хочете спілкуватися зі мною!</b>"
        }
 
        text_again_select_language = {
            "ru": "🌍 <b>Выбери язык, нажав на кнопки ниже!</b>",
            "cz": "🌍 <b>Zvolte jazyk stisknutím tlačítek níže!</b>",
            "en": "🌍 <b>Select a language by pressing the buttons below!</b>",
            "ua": "🌍 <b>Оберіть мову, натиснувши кнопки нижче!</b>"
        }

        text_end_select_language = {
            "ru": "🌍 <b>Язык выбран!</b>",
            "cz": "🌍 <b>Jazyk zvolen!</b>",
            "en": "🌍 <b>Language selected!</b>",
            "ua": "🌍 <b>Мова вибрана!</b>"
        }

        td_languages = {
            "🇷🇺": "ru",
            "🇬🇧": "en",
            "🇨🇿": "cz",
            "🇺🇦": "ua"
        }
        

    class MainMenu:
        """
        /start - Main user menu.

        Default buttons.
        """
        text_main_menu = {
            "ru": 
                "<b>Привет Я бот КОННЕКТ!</b> 🤖\n\n"\
                
                "📚Я нужен, что бы помочь тебе в учебе!\n\n"\
                
                "Помогу тебе найти репетитора или студентов."\
                "На данный момент моя база только пополняется :)\n\n"\
                
                "<b>Со мной ты можешь:</b>\n"\
                "📍 Найти репетитора и помощь\n"
                "📍 Бесплатно попасть в каталог репетиторов\n"\
                "📍 Найти студенческие чаты/каналы\n"\
                "📍 Предложить сотрудничество\n\n"
                
                "<b>💬 Мои команды:</b>\n"
                "/start - Обновить меню\n"
                "/language - Поменять язык\n\n"

                "<b>Если что-то не понятно/не работает,то смело пишите ему!</b>\n"
                "<b>Dev:</b> @vsem_azamat\n",
            
            "cz":
                "<b>Ahoj Jsem bot CONNECT!</b> 🤖\n\n"\
                
                "📚Potřebuji vám pomoci se studiem!\n\n"\
                
                "Pomůžu vám najít učitele nebo studenty."\
                "V současné době se můj seznam pouze doplňuje :)\n\n"\
                
                "<b>Semnou můžete:</b>\n"\
                "📍 Najít učitele a pomoc\n"
                "📍 Zdarma se dostanete do katalogu učitelů\n"\
                "📍 Najděte studentské chaty / kanály\n"\
                "📍 Navrhněte spolupráci\n\n"
                
                "<b>💬 Moje příkazy:</b>\n"
                "/start - Aktualizovat menu\n"
                "/language - Změnit jazyk\n\n"

                "<b>Pokud něco nerozumíte / nefunguje, napište mu!</b>\n"
                "<b>Dev:</b> @vsem_azamat\n",

            "en":
                "<b>Hello I'm bot CONNECT!</b> 🤖\n\n"\
                
                "📚I need to help you with your studies!\n\n"\
                
                "I will help you find a tutor or students."\
                "At the moment, my list is only being replenished :)\n\n"\
                
                "<b>With me you can:</b>\n"\
                "📍 Find a tutor and help\n"
                "📍 Get into the catalog of tutors for free\n"\
                "📍 Find student chats / channels\n"\
                "📍 Offer cooperation\n\n"
                
                "<b>💬 My commands:</b>\n"
                "/start - Update menu\n"
                "/language - Change language\n\n"

                "<b>If something is not clear / does not work, write to him!</b>\n"
                "<b>Dev:</b> @vsem_azamat\n",

            "ua":
                "<b>Привіт Я бот КОННЕКТ!</b> 🤖\n\n"\
                
                "📚Я потрібен, щоб допомогти тобі в навчанні!\n\n"\
                
                "Допоможу тобі знайти репетитора або студентів."\
                "На даний момент мій список тільки поповнюється :)\n\n"\
                
                "<b>Зі мною ти можеш:</b>\n"\
                "📍 Знайти репетитора і допомогу\n"
                "📍 Безкоштовно потрапити в каталог репетиторів\n"\
                "📍 Знайти студентські чати / канали\n"\
                "📍 Запропонувати співпрацю\n\n"
                
                "<b>💬 Мої команди:</b>\n"
                "/start - Оновити меню\n"
                "/language - Змінити мову\n\n"

                "<b>Якщо щось незрозуміло / не працює, то сміливо пиши йому!</b>\n"
                "<b>Dev:</b> @vsem_azamat\n"
        }
          

        td_find_teachers = {
            'ru': '🔎Найти репетитора.',
            'cz': '🔎Najít učitele.',
            'en': '🔎Find a tutor.',
            'ua': '🔎Знайти репетитора.'
        }
        td_chats = {
            'ru': '💬Чаты студенческие',
            'en': '💬Student chats',
            'cz': '💬Studentské chaty',
            'ua': '💬Студентські чати',
        }
        td_about_us = {
            'ru': 'ℹ️Обо мне',
            'cz': 'ℹ️O nás',
            'en': 'ℹ️About us',
            'ua': 'ℹ️Про нас'
        }
        td_my_teachers_profile = {
            'ru': '👨‍🏫Личный кабинет репетитора',
            'cz': '👨‍🏫Můj profil učitele',
            'en': '👨‍🏫My tutor profile',
            'ua': '👨‍🏫Мій профіль репетитора'
        }

        text_chats = {
            "ru": 
                "💬<b>Чешские чаты для студентов из СНГ:</b>\n\n"
                "Пожалуйста, будьте внимательны к правилам в чатах, которые обычно закреплены!",
            "cz": 
                "💬<b>České chaty pro studenty z SNĚ:</b>\n\n"
                "Prosím, pozor na pravidla v chatování, která jsou obvykle připnutá!",
            "en": 
                "💬<b>Czech chats for students from CIS:</b>\n\n"
                "Please be attentive to the rules in chats, which are usually pinned!",
            "ua": 
                "💬<b>Чеські чати для студентів з СНД:</b>\n\n"
                "Будь ласка, уважно дотримуйтесь правил в чатах, які зазвичай закріплені!"
        }

        text_about_us = {
            "ru":
                "<b>Я бот для репетиторов</b>🤖\n\n"
                "Если есть замечания или вопросы по работе бота, то можете писать в <b>Dev!</b>\n"
                "<b>Dev:</b> t.me/vsem_azamat\n"
                "<b>Сотрудничество:</b> t.me/CzechMedia_bot",
            "cz":
                "<b>Jsem chatbot pro doučování</b>🤖\n\n"
                "Pokud máte nápady nebo dotazy na práci tohoto chatbota, můžete psát na <b>Dev!</b>\n"
                "<b>Dev:</b> t.me/vsem_azamat\n"
                "<b>Spolupráce:</b> t.me/CzechMedia_bot",
            "en":
                "<b>I'm a chatbot for tutors</b>🤖\n\n"
                "If you have any feedback or questions about this chatbot's work, please contact <b>Dev!</b>\n"
                "<b>Dev:</b> t.me/vsem_azamat\n"
                "<b>Cooperation:</b> t.me/CzechMedia_bot",
            "ua":
                "<b>Я чат-бот для репетиторів</b>🤖\n\n"
                "Якщо у вас є зауваження або питання щодо роботи цього чат-бота, зверніться до <b>Dev!</b>\n"
                "<b>Dev:</b> t.me/vsem_azamat\n"
                "<b>Співпраця:</b> t.me/CzechMedia_bot"
        }

        @staticmethod
        def kb_main_menu(language: str) -> ReplyKeyboardBuilder:
            builder = ReplyKeyboardBuilder()
            builder.row(
                KeyboardButton(text=TextMenu.MainMenu.td_find_teachers[language])
            )
            builder.row(
                KeyboardButton(text=TextMenu.MainMenu.td_chats[language]),
                KeyboardButton(text=TextMenu.MainMenu.td_about_us[language])
            )
            builder.row(
                KeyboardButton(text=TextMenu.MainMenu.td_my_teachers_profile[language])
            )
            return builder

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
            'en': '📚 By lessons',
            'ua': '📚 За предметами'
        }


        @staticmethod
        def kb_teachers_category(language: str) -> InlineKeyboardBuilder:
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
                text=TextMenu.TeachersCategory.ti_lessons_search_with_catalog.get(language, 'ru'),
                callback_data=CatalogGoogle().pack()
            )
            builder.button(
                text=TextMenu.TeachersCategory.ti_lessons_search_with_google.get(language, 'ru'),
                switch_inline_query_current_chat=""
            )
            builder.adjust(1)
            return builder

        text_select_head = {
            "ru": 
                "🟰🟰🟰🟰🟰🔎🟰🟰🟰🟰🟰\n"\
                "<b>-> Поиск репетитора</b>\n\n",
            "cz":
                "🟰🟰🟰🟰🟰🔎🟰🟰🟰🟰🟰\n"
                "<b>-> Vyhledávání doučujícího</b>\n\n",
            "en":
                "🟰🟰🟰🟰🟰🔎🟰🟰🟰🟰🟰\n"
                "<b>-> Tutor search</b>\n\n",
            "ua":
                "🟰🟰🟰🟰🟰🔎🟰🟰🟰🟰🟰\n"
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
            'en': '📚 <b>Sorting tutors by lessons:</b>',
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
            'ru': '📚 <b>Репетиторы по предмету:</b>',
            'en': '📚 <b>Tutors by lessons:</b>',
            'cz': '📚 <b>Lektoři podle předmětu:</b>',
            'ua': '📚 <b>Репетитори за предметом:</b>'
            }

        text_lessons_search = {
            'ru': '📚 <b>Выберите способ поиска репетиторов по предмету:</b>',
            'en': '📚 <b>Choose a way to search for tutors by lessons:</b>',
            'cz': '📚 <b>Vyberte způsob vyhledávání lektorů podle předmětu:</b>',
            'ua': '📚 <b>Виберіть спосіб пошуку репетиторів за предметом:</b>'
            }

        ti_lessons_search_with_catalog = {
            'ru': '🗂 Каталог всех предметов',
            'en': '🗂 Catalog of all lessons',
            'cz': '🗂 Katalog všech předmětů',
            'ua': '🗂 Каталог усіх предметів'
            }
        ti_lessons_search_with_google = {
            'ru': '🔎 Поиск по названию',
            'en': '🔎 Search by name',
            'cz': '🔎 Vyhledávání podle názvu',
            'ua': '🔎 Пошук за назвою'
            }

        @staticmethod
        def kb_lessons_category(language: str) -> InlineKeyboardBuilder:
            builder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(
                    text=TextMenu.TeachersCategory.ti_lessons_search_with_catalog.get(language, 'ru'),
                    callback_data=CatalogGoogle().pack()
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
            return builder

    class MyTeachersProfile:
        """
        Default buttons.
        """
        text_create_new_profile = {
            "ru": "🧑‍🏫 <b>У вас еще нет профиля репетитора! Хотите создать?</b>",
            "en": "🧑‍🏫 <b>You do not have a tutor profile yet! Would you like to create one?</b>",
            "cz": "🧑‍🏫 <b>Nemáte ještě profil učitele! Chcete vytvořit profil?</b>",
            "ua": "🧑‍🏫 <b>У вас ще немає профілю репетитора! Хочете створити?</b>"
            }

        text_your_profile = {
            'ru': '⬆️ <b>Ваш профиль:</b> ⬆️',
            'en': '⬆️ <b>Your Profile:</b> ⬆️',
            'cz': '⬆️ <b>Váš profil:</b> ⬆️',
            'ua': '⬆️ <b>Ваш профіль:</b> ⬆️'
            }
        
        td_create_profile_yes = "✅"
        td_create_profile_no = "❌"

        aviable_create_profile_answers = [td_create_profile_no, td_create_profile_yes]

        text_try_again_create_profile = {
            "ru": "⚠️ <b>Нажмите на одну из кнопок ниже!</b>",
            "en": "⚠️ <b>Click on one of the buttons below!</b>",
            "cz": "⚠️ <b>Klikněte na jedno z tlačítek níže!</b>",
            "ua": "⚠️ <b>Натисніть на одну з кнопок нижче!</b>"
            }

        @staticmethod
        def kb_profile_settings() -> ReplyKeyboardBuilder:
            builder = ReplyKeyboardBuilder()
            builder.row(
                KeyboardButton(text=TextMenu.MyTeachersProfile.td_create_profile_yes),
                KeyboardButton(text=TextMenu.MyTeachersProfile.td_create_profile_no)
            )
            return builder

        text_teacher_write_me_you_name = {
            'ru': 
                "⬆️ <b>Ваш профиль будет выглядить подобным образом!</b> ⬆️\n"
                "Рекомендую заполнять всё латиницей, кроме описания профиля!\n\n"
                "Можете не бояться сделать ошибку, у вас всегда будет возможность потом подправить свои данные!\n\n"
                "<b>Помните, что данные не должны содержать спец символы:</b> /\>[_*...:\n\n"
                "❌ <b>Отменить регистрацию:</b> /cancel\n\n"
                "⬇️ <b>Напишите свое имя:</b> ⬇️",

            'cz':
                "⬆️ <b>Váš profil bude vypadat takto!</b> ⬆️\n"
                "Nemusíte se bát udělat chybu, vždy budete mít možnost později opravit své údaje!\n\n"
                "<b>Pamatujte, že údaje nesmí obsahovat speciální znaky:</b> /\>[_*...:\n\n"
                "❌ <b>Zrušit registraci:</b> /cancel\n\n"
                "⬇️ <b>Napište své jméno:</b> ⬇️",

            'en':
                "⬆️ <b>Your profile will look like this!</b> ⬆️\n"
                "You don't have to be afraid to make a mistake, you will always have the opportunity to correct your data later!\n\n"
                "<b>Remember that the data must not contain special characters:</b> /\>[_*...:\n\n"
                "❌ <b>Cancel registration:</b> /cancel\n\n"
                "⬇️ <b>Write your name:</b> ⬇️",

            'ua':
                "⬆️ <b>Ваш профіль буде виглядати так!</b> ⬆️\n"
                "Ви не повинні боятися зробити помилку, у вас завжди буде можливість потім виправити свої дані!\n\n"
                "<b>Пам'ятайте, що дані не повинні містити спеціальні символи:</b> /\>[_*...:\n\n"
                "❌ <b>Скасувати реєстрацію:</b> /cancel\n\n"
                "⬇️ <b>Напишіть своє ім'я:</b> ⬇️"
                }

        text_name_try_again = {
            'ru': 
                "↪️ <b>Введите имя еще раз, вы что-то ввели неккоректно.</b>\n\n"
                "⚠️ <b>Имя должно быть от 2 до 25 символов!</b>",

            'cz':
                "↪️ <b>Zadejte jméno znovu, něco jste zadal(a) nesprávně.</b>\n\n"
                "⚠️ <b>Jméno by mělo mít délku od 2 do 25 znaků!</b>",

            'en':
                "↪️ <b>Enter your name again, you entered something incorrectly.</b>\n\n"
                "⚠️ <b>The name should be from 2 to 25 characters long!</b>",
            
            'ua':
                "↪️ <b>Введіть ім'я ще раз, ви щось ввели неправильно.</b>\n\n"
                "⚠️ <b>Ім'я повинно бути від 2 до 25 символів!</b>"
            }   

        td_keep = {
            "ru": "⏩ Пропустить",
            "en": "⏩ Skip",
            "cz": "⏩ Přeskočit",
            "ua": "⏩ Пропустити",
            }

        text_location_write = {
            'ru': 
                "📍<b>Перечислите кратко где и как проходят занятия!</b>\n\n"
                "❌ <b>Отменить регистрацию:</b> /cancel\n\n"
                "<b>Пример:</b> Прага, Скайп, Дискорд, Библиотека",
            'cz':
                "📍<b>Stručně vyjmenujte, kde a jak probíhají lekce!</b>\n"
                "❌ <b>Zrušit registraci:</b> /cancel\n\n"
                "<b>Příklad:</b> Praha, Skype, Discord, knihovna",
            'en':
                "📍<b>List briefly where and how the lessons take place!</b>\n\n"
                "❌ <b>Cancel registration:</b> /cancel\n\n"
                "<b>Example:</b> Prague, Skype, Discord, library",
            'ua':
                "📍<b>Перелічіть коротко де і як проходять заняття!</b>\n\n"
                "❌ <b>Скасувати реєстрацію:</b> /cancel\n\n"
                "<b>Приклад:</b> Прага, Скайп, Дискорд, Бібліотека"
            }

        text_location_try_again = {
            "ru":
                "↪️ <b>Попробуйте еще раз, вы что-то ввели некорректно</b>\n\n"
                "⚠️ <b>Текст должен быть от 2 до 100 символов</b>\n",

            "cz":
                "↪️ <b>Zkuste to znovu, něco jste zadal(a) nesprávně</b>\n\n"
                "⚠️ <b>Text by měl mít délku od 2 do 100 znaků</b>\n",

            "en":
                "↪️ <b>Try again, you entered something incorrectly</b>\n\n"
                "⚠️ <b>The text should be from 2 to 100 characters long</b>\n",

            "ua":
                "↪️ <b>Спробуйте ще раз, ви щось ввели неправильно</b>\n\n"
                "⚠️ <b>Текст повинен бути від 2 до 100 символів</b>\n"
                }

        text_price_write = {
            "ru":
                "💳 <b>Напишите стоимость занятий!</b>\n\n"
                "❌ <b>Отменить регистрацию:</b> /cancel\n\n"
                "<b>Пример:</b> 300-500 Kč/час",
            "cz":
                "💳 <b>Napište cenu lekcí!</b>\n\n"
                "❌ <b>Zrušit registraci:</b> /cancel\n\n"
                "<b>Příklad:</b> 300-500 Kč/hod",
            "en":
                "💳 <b>Write down the price of the lessons!</b>\n\n"
                "❌ <b>Cancel registration:</b> /cancel\n\n"
                "<b>Example:</b> 300-500 CZK/hour",
            "ua":
                "💳 <b>Напишіть вартість занять!</b>\n\n"
                "❌ <b>Скасувати реєстрацію:</b> /cancel\n\n"
                "<b>Приклад:</b> 300-500 Kč/год"
            }

        text_price_try_again = {
            "ru":
                "↪️ <b>Попробуйте еще раз, вы что-то ввели некорректно</b>\n\n"
                "⚠️ <b>Текст должен быть от 2 до 25 символов</b>\n",
        
            "cz":
                "↪️ <b>Zkuste to znovu, něco jste zadal(a) nesprávně</b>\n\n"
                "⚠️ <b>Text by měl mít délku od 2 do 25 znaků</b>\n",
            "en":
                "↪️ <b>Try again, you entered something incorrectly</b>\n\n"
                "⚠️ <b>The text should be from 2 to 25 characters long</b>\n",
            "ua":
                "↪️ <b>Спробуйте ще раз, ви щось ввели неправильно</b>\n\n"
                "⚠️ <b>Текст повинен бути від 2 до 25 символів</b>\n"
            }


        text_description_write = {
            "ru": 
                "📝 <b>Напишите описание к своему профилю!</b>\n\n"
                "Учтите, что в каталоге репетиторов, видно будет только первые 4-5 строк описания.\n"
                "Полный текст будет виден человека при полном открытии профиля.",

            "cz":
                "📝 <b>Napište popis svého profilu!</b>\n\n"
                "Vezměte prosím na vědomí, že v katalogu lektorů budou vidět pouze první 4-5 řádků popisu.\n"
                "Plný text bude vidět člověk při úplném otevření profilu.",

            "en":
                "📝 <b>Write a description for your profile!</b>\n\n"
                "Please note that in the catalog of tutors, only the first 4-5 lines of the description will be visible.\n"
                "The full text will be visible to a person when the profile is fully opened.",

            "ua":
                "📝 <b>Напишіть опис до свого профілю!</b>\n\n"
                "Врахуйте, що в каталозі репетиторів, видно буде тільки перші 4-5 рядків опису.\n"
                "Повний текст буде видно людині при повному відкритті профілю."
            }
        
        td_keep_old_description ={
            "ru":
                "⏩ Оставить как есть",
            "cz":
                "⏩ Ponechat jak je",
            "en":
                "⏩ Leave as is",
            "ua":
                "⏩ Залишити як є"
            }
        
        text_description_try_again = {
            "ru":
                "↪️ <b>Попробуйте еще раз, вы что-то ввели неккоректно</b>\n\n"\
                "⚠️ <b>Текст описания должен быть от 30 до 2500 символов</b>\n",

            "cz":
                "↪️ <b>Zkuste to znovu, něco jste zadal(a) nesprávně</b>\n\n"\
                "⚠️ <b>Text popisu by měl mít délku od 30 do 2500 znaků</b>\n",

            "en":
                "↪️ <b>Try again, you entered something incorrectly</b>\n\n"\
                "⚠️ <b>The description text should be from 30 to 2500 characters long</b>\n",

            "ua":
                "↪️ <b>Спробуйте ще раз, ви щось ввели неправильно</b>\n\n"\
                "⚠️ <b>Текст опису повинен бути від 30 до 2500 символів</b>\n"
            }

        text_cancel_registration = {
            "ru": "❌ <b>Вы отменили регистрацию!</b>",
            "en": "❌ <b>You have canceled registration!</b>",
            "cz": "❌ <b>Zrušili jste registraci!</b>",
            "ua": "❌ <b>Ви скасували реєстрацію!</b>"
            }

        text_profile_finish = {
            "ru": 
                "⬆️ <b>Ваш профиль репетитора готов!</b> ⬆️\n\n"
                "<b> Что-бы перейти в личный кабинет, из главного меню (start) нажмите на кнопку:</b>\n"
                "👨‍🏫 <i>Личный кабинет репетитора</i>\n\n"
                "<b>Теперь вам нужно:</b>"
                    "📍 Выбрать предметы, которые вы будете преподавать, чтобы ваш профиль отображался в каталоге\n"
                    "📍 Иметь логин (username) в Telegram\n"
                    "📍 Активировать профиль, нажав на 3-ю кнопку в личном кабинете \n(✅Профиль активирован/❌Профиль деактивирован) \n\n"
                "Если у вас что-то не получается или есть вопросы, то смело пишите мне: @vsem_azamat",

            "cz":
                "⬆️ <b>Váš profil učitele je připraven!</b> ⬆️\n\n"
                "<b>Chcete-li přejít do osobního účtu, z hlavní nabídky (start) klikněte na tlačítko:</b>\n"
                "👨‍🏫 <i>Můj profil učitele</i>\n\n"
                "<b>Nyní musíte:</b>"
                    "📍 Vyberte předměty, které budete vyučovat, aby se váš profil zobrazoval v katalogu\n"
                    "📍 Mít přihlašovací jméno (username) v Telegramu\n"
                    "📍 Aktivujte profil kliknutím na 3. tlačítko v osobním účtu \n(✅Profil aktivován/❌Profil deaktivován) \n\n"
                "Pokud se vám něco nedaří nebo máte nějaké dotazy, napište mi: @vsem_azamat",

            "en":
                "⬆️ <b>Your tutor profile is ready!</b> ⬆️\n\n"
                "<b>To go to your personal account, from the main menu (start) click on the button:</b>\n"
                "👨‍🏫 <i>My tutor profile</i>\n\n"
                "<b>Now you need:</b>"
                    "📍 Select the subjects you will teach to make your profile visible in the catalog\n"
                    "📍 Have a login (username) in Telegram\n"
                    "📍 Activate the profile by clicking on the 3rd button in the personal account \n(✅Profile activated/❌Profile deactivated) \n\n"
                "If you can't do something or have any questions, feel free to write to me: @vsem_azamat",

            "ua":
                "⬆️ <b>Ваш профіль репетитора готовий!</b> ⬆️\n\n"
                "<b>Щоб перейти в особистий кабінет, з головного меню (start) натисніть на кнопку:</b>\n"
                "👨‍🏫 <i>Особистий кабінет репетитора</i>\n\n"
                "<b>Тепер вам потрібно:</b>"
                    "📍 Вибрати предмети, які ви будете викладати, щоб ваш профіль відображався в каталозі\n"
                    "📍 Мати логін (username) в Telegram\n"
                    "📍 Активувати профіль, натиснувши на 3-ю кнопку в особистому кабінеті \n(✅Профіль активований/❌Профіль деактивований) \n\n"
                "Якщо у вас щось не виходить або є питання, то сміливо пишіть мені: @vsem_azamat"
            }

        text_profile_edit_finish = {
            "ru": "⬆️ <b>Изменения внесены в ваш профиль:</b> ⬆️",
            "en": "⬆️ <b>Changes have been made to your profile:</b> ⬆️",
            "ua": "⬆️ <b>Зміни внесені до вашого профілю:</b> ⬆️",
            "cz": "⬆️ <b>Změny byly provedeny ve vašem profilu:</b> ⬆️"
            }

        text_profile_menu = {
            "ru": "✍️ <b>Здесь вы можете самостоятельно редактировать свой профиль репетитора:</b>",
            "cz": "✍️ <b>Zde si můžete upravit svůj profil učitele:</b>",
            "en": "✍️ <b>Here you can edit your tutor profile yourself:</b>",
            "ua": "✍️ <b>Тут ви можете самостійно редагувати свій профіль репетитора:</b>"
            }

        text_profile_lessons_head = {
            "ru":
                "🟰🟰🟰🟰🟰⚙️🎓🟰🟰🟰🟰🟰\n"
                "<b>-> Вы в меню репетитора!</b>\n\n",
            "cz":
                "🟰🟰🟰🟰🟰⚙️🎓🟰🟰🟰🟰🟰\n"
                "<b>-> Jste v menu učitele!</b>\n\n",
            "en":
                "🟰🟰🟰🟰🟰⚙️🎓🟰🟰🟰🟰🟰\n"
                "<b>-> You are in the tutor menu!</b>\n\n",
            "ua":
                "🟰🟰🟰🟰🟰⚙️🎓🟰🟰🟰🟰🟰\n"
                "<b>-> Ви в меню репетитора!</b>\n\n"
            }
        
        text_profile_lessons = {
            "ru":
                "📚 <b>Предметы отсортированы по категориям, указанным ниже.</b>\n\n"
                "Отмечайте предметы, чтобы ваш профиль отображался в каталогах выбранных предметов",
            "cz":
                "📚 <b>Předměty jsou seřazeny podle níže uvedených kategorií.</b>\n\n"
                "Označte předměty, aby se váš profil zobrazoval v katalozích vybraných předmětů",
            "en":
                "📚 <b>Subjects are sorted by the categories below.</b>\n\n"
                "Check the subjects for your profile to be displayed in the catalogs of selected subjects",
            "ua":
                "📚 <b>Предмети відсортовані за категоріями, зазначеними нижче.</b>\n\n"
                "Відмічайте предмети, щоб ваш профіль відображався в каталогах обраних предметів"
            }

        text_profile_lessons_profile_doesnt_exists = {
            "ru": "⚠️ У вас еще нет профиля репетитора! Чтобы создать, нажмите на <b>Личный кабинет.</b>",
            "cz": "⚠️ Ještě nemáte vytvořený profil učitele! Abyste jej vytvořili, klepněte na <b>Osobní účet.</b>",
            "en": "⚠️ You don't have a tutor profile yet! To create one, click on <b>Personal Account.</b>",
            "ua": "⚠️ У вас ще немає профілю репетитора! Щоб створити профіль, натисніть <b>Особистий кабінет.</b>"
            }

        text_profile_list_universities = {
            "ru": "🏫 <b>Список ВУЗ-ов:</b>",
            "cz": "🏫 <b>Seznam VŠ:</b>",
            "en": "🏫 <b>List of universities:</b>",
            "ua": "🏫 <b>Список ВНЗ:</b>"
            }

        text_profile_list_universities = {
            "ru":
                "🏫 <b>Список ВУЗ-ов:</b>",
            "cz":
                "🏫 <b>Seznam VŠ:</b>",
            "en":
                "🏫 <b>List of universities:</b>",
            "ua":
                "🏫 <b>Список ВНЗ:</b>"
        }

        text_profile_lessons_universities = {
            "ru": "🏫 <b>Сортировка предметов по ВУЗ-ам:</b>",
            "cz": "🏫 <b>Třídění předmětů podle vysokých škol:</b>",
            "en": "🏫 <b>Sorting subjects by universities:</b>",
            "ua": "🏫 <b>Сортування предметів за ВУЗ-ами:</b>"
            }

        text_profile_lessons_languages = {
            "ru": "🔠 <b>Сортировка предметов по Языкам:</b>",
            "cz": "🔠 <b>Třídění předmětů podle jazyků:</b>",
            "en": "🔠 <b>Sorting subjects by languages:</b>",
            "ua": "🔠 <b>Сортування предметів за Мовами:</b>"
            }

        text_profile_lessons_select = {
            "ru": "📚🛒 <b>Выберите предмет, который хотите добавить к себе профиль:</b>",
            "cz": "📚🛒 <b>Vyberte předmět, který chcete přidat do svého profilu:</b>",
            "en": "📚🛒 <b>Select the lessons you want to add to your profile:</b>",
            "ua": "📚🛒 <b>Виберіть предмет, який хочете додати до свого профілю:</b>"
            }

        text_profile_lessons_catalog = {
            "ru": "📚 <b>Каталог всех предметов:</b>",
            "cz": "📚 <b>Katalog všech předmětů:</b>",
            "en": "📚 <b>Catalog of all lessons:</b>",
            "ua": "📚 <b>Каталог всіх предметів:</b>"
            }
        
        text_profile_select_edit = {
            "ru": "✍️ <b>Редактировать:</b>",
            "en": "✍️ <b>Edit:</b>",
            "cz": "✍️ <b>Upravit:</b>",
            "ua": "✍️ <b>Редагувати:</b>"
            }

        ti_profile_lessons_add_delete = {
            "ru": "📚🛒 Добавить/Убрать предметы",
            "en": "📚🛒 Add/Remove lessons",
            "cz": "📚🛒 Přidat/Odstranit předměty",
            "ua": "📚🛒 Додати/Видалити предмети"
            }

        ti_profile_edit = {
            "ru": "✍ Редактировать профиль",
            "en": "✍ Edit profile",
            "cz": "✍ Upravit profil",
            "ua": "✍ Редагувати профіль"
            }
        
        @staticmethod
        def kb_profile_menu(language: str) -> InlineKeyboardBuilder:
            builder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(
                    text=TextMenu.MyTeachersProfile.ti_profile_edit.get(language, 'ru'),
                    callback_data=TeacherSettingsMenu(
                        menu_type=TypeTeacherSettingsMenu.profile_edit
                        ).pack()
                    ),
                InlineKeyboardButton(
                    text=TextMenu.MyTeachersProfile.ti_profile_lessons_add_delete.get(language, 'ru'),
                    callback_data=TeacherSettingsMenu(
                        menu_type=TypeTeacherSettingsMenu.profile_lessons_add
                        ).pack()
                    )
                )
            builder.adjust(1)
            return builder
        

        ti_profile_edit_all = {
            "ru": "👩‍🏫 Всё",
            "en": "👩‍🏫 All",
            "cz": "👩‍🏫 Vše",
            "ua": "👩‍🏫 Все"
            }
        
        ti_profile_edit_description = {
            "ru": "📝 Описание",
            "en": "📝 Description",
            "cz": "📝 Popis",
            "ua": "📝 Опис"
            }   

        text_login_error = {
            "ru": 
                "❌<b>У вас отсуствует логин (username)! </b>\n\n"
                "Пожалуйста, создайте его в настройках профиля телеграмма."
                "Ваш профиль уже создан, но не отображается в каталоге репетиторов, пока вы не поставите <b>логин(username)</b>!\n",

            "cz":
                "❌<b>Nemáte přihlašovací jméno (username)! </b>\n\n"
                "Vytvořte jej prosím v nastavení profilu telegramu."
                "Váš profil je již vytvořen, ale nebude zobrazen v katalogu lektorů, dokud nezadáte <b>přihlašovací jméno(username)</b>!\n",

            "en":
                "❌<b>You don't have a login (username)! </b>\n\n"
                "Please create it in the telegram profile settings."
                "Your profile is already created, but will not be displayed in the catalog of tutors until you enter <b>login(username)</b>!\n",

            "ua":
                "❌<b>У вас відсутнє логін (username)! </b>\n\n"
                "Будь ласка, створіть його в налаштуваннях профілю телеграму."
                "Ваш профіль вже створено, але не відображається в каталозі репетиторів, поки ви не введете <b>логін(username)</b>!\n"
            }

        text_teacher_state = {
            True:
                {
                    "ru": "✅ Профиль Активирован",
                    "en": "✅ Profile Activated",
                    "ua": "✅ Профіль активовано",
                    "cz": "✅ Profil aktivován"
                },
            False:
                {
                    "ru": "❌ Профиль Деактивирован",
                    "en": "❌ Profile Deactivated",
                    "ua": "❌ Профіль деактивовано",
                    "cz": "❌ Profil deaktivován"
                }
        }


