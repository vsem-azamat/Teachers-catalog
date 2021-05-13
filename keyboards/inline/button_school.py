from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

school_teacher1 = InlineKeyboardMarkup(row_wight=2,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(
                                                   text='ČVUT',
                                                   callback_data='list_cvut_1'
                                               ),
                                               InlineKeyboardButton(
                                                   text='VŠE',
                                                   callback_data='list_vse_1'
                                               )

                                           ],
                                           [
                                               InlineKeyboardButton(
                                                   text='Karlov',
                                                   callback_data='list_uk_1'
                                               ),
                                               InlineKeyboardButton(
                                                   text='ČZU',
                                                   callback_data='list_czu_1'
                                               )
                                           ],
                                           [
                                               InlineKeyboardButton(
                                                   text='VUT',
                                                   callback_data='list_vut_1'
                                               ),
                                               InlineKeyboardButton(
                                                   text='Masaryk',
                                                   callback_data='list_masaryk_1'
                                               )
                                           ],
                                           [
                                               # InlineKeyboardButton(
                                               #     text='Стать репетитором',
                                               #     callback_data='list_add'
                                               # ),
                                               InlineKeyboardButton(
                                                   text='По предметам',
                                                   callback_data='sort_less'
                                               )
                                           ]
                                       ])

school_teacher2 = InlineKeyboardMarkup(row_width=2,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(
                                                   text='Математика',
                                                   callback_data='list_math'
                                               ),
                                               InlineKeyboardButton(
                                                   text='Нострификация',
                                                   callback_data='list_nostr'
                                               )
                                           ],
                                           [
                                               InlineKeyboardButton(
                                                   text='Биология',
                                                   callback_data='list_biol'
                                               ),
                                               InlineKeyboardButton(
                                                   text='Химия',
                                                   callback_data='list_chem'
                                               )
                                           ],
                                           [
                                               InlineKeyboardButton(
                                                   text='Чешский',
                                                   callback_data='list_czech'
                                               ),
                                               InlineKeyboardButton(
                                                   text='Английский',
                                                   callback_data='list_engl'
                                               )
                                           ],
                                           [
                                               InlineKeyboardButton(
                                                   text='По ВУЗ-ам',
                                                   callback_data='sort_univ'
                                               )
                                           ]
                                       ])
