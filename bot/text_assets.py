from dataclasses import dataclass

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, \
    InlineKeyboardBuilder

from bot.utils.callback_factory import PageLevels, PageSettings, TeacherLevels, TeacherSettings

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
                "Привет Я бот КОННЕКТ! 🤖\n\n"\
                
                "Я нужен, что бы помочь тебе сориентироваться в нашем пространстве.\n\n"\
                
                "Здесь ты сможешь найти себе репетитора или предложить свои услуги."\
                "На данный момент моя база только пополняется :)\n\n"\
                
                "<b>Здесь ты можешь:</b>\n"\
                "📍 Найти репетитора и помощь\n"
                "📍 Бесплатно попасть в каталог репетиторов\n"\
                "📍 Найти студенческие чаты/каналы\n"\
                "📍 Предложить сотрудничество\n\n"
                
                "/start - Обновить меню\n"
                "/language - Поменять язык",

            "cz":
                "Ahoj, já jsem bot KONNEKT! 🤖\n\n"\
                
                "Potřebuji ti pomoci zorientovat se v našem prostoru.\n\n"\
                
                "Zde si můžeš najít doučovatele nebo nabídnout své služby."\
                "Momentálně se stále rozrůstám :)\n\n"\
                
                "<b>Zde můžeš:</b>\n"\
                "📍 Najít si doučovatele a pomoc\n"
                "📍 Zdarma se dostat do katalogu doučovatelů\n"\
                "📍 Najít studentské chaty/kanály\n"\
                "📍 Nabídnout spolupráci\n\n"
                
                "/start - Obnovit menu\n"
                "/language - Změnit jazyk",

            "en":
                "Hi! I'm CONNECT bot! 🤖\n\n"
                
                "I'm here to help you navigate our platform.\n\n"
                
                "Here, you can find a tutor or offer your services. Our database is being updated daily :)\n\n"
                
                "<b>What can I do for you:</b>\n"\
                "📍 Find a tutor or study help\n"\
                "📍 Add your profile to the tutor catalog for free\n"\
                "📍 Find student chats/channels\n"\
                "📍 Offer cooperation\n\n"
                
                "/start - Refresh the menu\n"
                "/language - Change language",
                
            "ua":
                "Привіт! Я бот CONNECT! 🤖\n\n"
                
                "Я допомагаю тобі орієнтуватися на нашій платформі.\n\n"
                
                "Тут ти можеш знайти репетитора або запропонувати свої послуги. Наша база оновлюється щоденно :)\n\n"
                
                "<b>Що я можу для тебе зробити:</b>\n"\
                "📍 Знайти репетитора або допомогу в навчанні\n"\
                "📍 Додати безкоштовно свій профіль до каталогу репетиторів\n"\
                "📍 Знайти студентські чати / канали\n"\
                "📍 Запропонувати співпрацю\n\n"
                
                "/start - Оновити меню\n"
                "/language - Змінити мову", 
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
        def kb_main_menu(language: str) -> ReplyKeyboardMarkup:
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
            'en': '📚 By lessons',
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
            'ru': '<b>📚 Репетиторы по предмету:</b>',
            'en': '<b>📚 Tutors by lessons:</b>',
            'cz': '<b>📚 Lektoři podle předmětu:</b>',
            'ua': '<b>📚 Репетитори за предметом:</b>'
            }

        text_lessons_search = {
            'ru': '📚 Выберите способ поиска репетиторов по предмету:',
            'en': '📚 Choose a way to search for tutors by lessons:',
            'cz': '📚 Vyberte způsob vyhledávání lektorů podle předmětu:',
            'ua': '📚 Виберіть спосіб пошуку репетиторів за предметом:'
            }

        ti_lessons_search_with_catalog = {
            'ru': '🗂 Каталог всех предметов',
            'en': '🗂 Catalog of all lessons',
            'cz': '🗂 Katalog všech předmětů',
            'ua': '🗂 Каталог усіх предметів'
            }
        ti_lessons_search_with_google = {
            'ru': '🔎 Поиск предмета по названию',
            'en': '🔎 Search for a lesson by name',
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
            'ua': "<b>Ваш профіль виглядатиме наступним чином!</b> ⬆️\n"
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

        text_keep = {
            "ru": "Пропустить",
            "en": "Skip",
            "ua": "Пропустити",
            "cz": "Přeskočit"
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
            "ua": 
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
                "Чтобы это сделать, еще раз нажмите на кнопку Личный Кабинет.",
            "cz":
                "<b>Váš profil je téměř hotový!</b> ⬆️\n"
                "Zbývá pouze vybrat předměty, aby váš profil byl viditelný v příslušných katalozích.\n\n"
                "Abyste to udělali, klikněte ještě jednou na tlačítko Osobní účet.",
            "en":
                "<b>Your profile is almost ready!</b> ⬆️\n"
                "You just need to select subjects to make your profile visible in the corresponding catalogs.\n\n"
                "To do this, click on the Personal Account button again.",
            "ua":
                "<b>Ваш профіль майже готовий!</b> ⬆️\n"
                "Залишилося тільки вибрати предмети, щоб ваш профіль був видимим в відповідних каталогах.\n\n"
                "Щоб це зробити, ще раз натисніть кнопку Особистий кабінет."
        }


        text_profile_edit_finish = {
            "ru": "Изменения внесены в ваш профиль⬆️",
            "en": "Changes have been made to your profile⬆️",
            "ua": "Зміни внесені до вашого профілю⬆️",
            "cz": "Změny byly provedeny ve vašem profilu⬆️"
        }


        text_profile_menu = {
            "ru":
                "Здесь вы можете самостоятельно редактировать свой профиль репетитора:",
            "cz":
                "Zde si můžete sami upravit profil učitele:",
            "en":
                "Here you can edit your tutor profile yourself:",
            "ua":
                "Тут ви можете самостійно змінити свій профіль репетитора:",
            }

        text_profile_lessons_head = {
            "ru":
                "🟰🟰🟰🟰🎓🟰🟰🟰🟰\n"
                "<b>-> Вы в меню репетитора!</b>\n\n",
            "cz":
                "🟰🟰🟰🟰🎓🟰🟰🟰🟰\n"
                "<b>-> Jste v učitelském menu!</b>\n\n",
            "en":
                "🟰🟰🟰🟰🎓🟰🟰🟰🟰\n"
                "<b>-> You are in the teacher menu!</b>\n\n",
            "ua":
                "🟰🟰🟰🟰🎓🟰🟰🟰🟰\n"
                "<b>-> Ви в меню вчителя!</b>\n\n"
            }
        
        text_profile_lessons = {
            "ru":
                "Предметы отсортированы в приведенных ниже категориях. "
                "Выберите предмет, который хотите добавить себе, чтобы ваш профиль отображался в каталоге!",
            "cz":
                "Předměty jsou řazeny do kategorií uvedených níže. "
                "Vyberte si předmět, který si chcete přidat, aby byl váš profil zobrazen v katalogu!",
            "en":
                "Lessons are sorted into categories listed below. "
                "Select the lesson you want to add to yourself to make your profile visible in the catalog!",
            "ua":
                "Предмети відсортовані в наведених нижче категоріях. "
                "Виберіть предмет, який хочете додати собі, щоб ваш профіль відображався в каталозі!"
        }

        text_profile_lessons_profile_doesnt_exists = {
            "ru":
                "У вас еще нет профиля репетитора! Чтобы создать, нажмите на <b>Личный кабинет.</b>",
            "cz":
                "Ještě nemáte vytvořený profil učitele! Abyste jej vytvořili, klepněte na <b>Osobní účet.</b>",
            "en":
                "You don't have a tutor profile yet! To create one, click on <b>Personal Account.</b>",
            "ua":
                "У вас ще немає профілю репетитора! Щоб створити профіль, натисніть <b>Особистий кабінет.</b>"
        }

        text_profile_lessons_universities = {
            "ru":
                "Сортировка предметов по ВУЗ-ам:",
            "cz":
                "Třídění předmětů podle vysokých škol:",
            "en":
                "Sorting subjects by universities:",
            "ua":
                "Сортування предметів за ВУЗ-ами:"
        }

        text_profile_lessons_select = {
            "ru":
                "Выберите предмет, который хотите добавить к себе профиль:",
            "cz":
                "Vyberte předmět, který chcete přidat do svého profilu:",
            "en":
                "Select the lessons you want to add to your profile:",
            "ua":
                "Виберіть предмет, який хочете додати до свого профілю:"
        }

        text_profile_lessons_catalog = {
            "ru":
                "Каталог всех предметов!",
            "cz":
                "Katalog všech předmětů!",
            "en":
                "Catalog of all lessons!",
            "ua":
                "Каталог всіх предметів!"
        }
        
        text_profile_select_edit = {
            "ru": "<b>Редактировать:</b>",
            "en": "<b>Edit:</b>",
            "cz": "<b>Upravit:</b>",
            "ua": "<b>Редагувати:</b>"
        }

        ti_profile_lessons_add_delete = {
            "ru": "📚 Добавить/Убрать предметы",
            "en": "📚 Add/Remove lessons",
            "cz": "📚 Přidat/Odstranit předměty",
            "ua": "📚 Додати/Видалити предмети"
        }

        ti_profile_edit = {
            "ru": "✍ Редактировать профиль",
            "en": "✍ Edit profile",
            "cz": "✍ Upravit profil",
            "ua": "✍ Редагувати профіль"
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
                "❌<b>У вас отсуствует логин/username!</b>\n"
                "Пожалуйста, создайте его в настройках профиля телеграмма."
                "Без него не получится продолжить и ваш профиль не попадет в каталог репетиторов!",
            "en":
                "❌<b>You don't have a login/username!</b>\n"
                "Please create one in your Telegram profile settings. "
                "Without it, you won't be able to proceed and your profile won't be listed in the tutor directory!",
            "ua":
                "❌<b>У вас немає логіну/username!</b>\n"
                "Будь ласка, створіть його в налаштуваннях профілю Telegram. "
                "Без нього ви не зможете продовжувати і ваш профіль не буде включено в довідник репетиторів!",
            "cz":
                "❌<b>Nemáte login/username!</b>\n"
                "Vytvořte si ho v nastavení vašeho Telegram profilu. Bez něj nebude možné pokračovat a váš profil nebude zařazen do adresáře učitelů!"
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


