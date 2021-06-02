from aiogram import types

from loader import dp, bot
from keyboards.inline.db_list import next_back, next, back
# next_back_callback = CallbackData("next", "page", "univ_less")
from keyboards.inline.button_school import school_teacher1, school_teacher2
from defs.def_sql_request import list_teachers, sql_request
from filters import NextBackUL
from defs.def_sql_request import dict_for_th_start

dict_univ = {'list_cvut': 'cvut', 'list_uk': 'uk', 'list_vse': 'vse',
             'list_czu': 'czu', 'list_vut': 'vut', 'list_masaryk': 'masaryk'}

dict_less = {'list_math': 'math', 'list_nostr': 'nostr', 'list_biol': 'biol', 'list_chem': 'chem',
             'list_czech': 'czech', 'list_engl': 'engl', 'list_fyz': 'fz', 'list_prog': 'prog',
             'list_eco': 'eco', 'list_prav': 'prav'}


@dp.callback_query_handler(regexp=r"^list_")
async def th_list(callback_query: types.CallbackQuery):
    splitted = callback_query.data.split(
        "_")
    # example "callback_data": list_cvit_2
    # example "splitted": [list], [cvut], [2]
    for_request = splitted[1]
    now_page = 1
    call_back = f"list_" + for_request

    if call_back in dict_univ.keys():
        univ_less = "univ"
    elif call_back in dict_less.keys():
        univ_less = "lesson"
    else:
        print('Error in start if/elif')

    await bot.answer_callback_query(callback_query.id)
    list_login, list_about, pages = sql_request(univ_less, for_request)

    if pages > 1:
        await bot.send_message(callback_query.from_user.id,
                               list_teachers(pages, now_page, list_login, list_about, call_back),
                               reply_markup=next)
    elif pages > 0:
        await bot.send_message(callback_query.from_user.id,
                               list_teachers(pages,now_page, list_login, list_about, call_back))
    elif pages == 0:
        await bot.send_message(callback_query.from_user.id, text="Вы можете стать первым! \nОтпишите @vsem_azamat")


@dp.callback_query_handler(regexp=r"^page_")  # next_page
async def list_paging(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = callback_query.message.text
    text_split = text.split()
    now_page = int(text_split[-3])  # 1
    for_request_for_dict_big = text_split[2]  # Karlov
    for_request_for_dict = list(dict_for_th_start)[list(dict_for_th_start.values()).index(for_request_for_dict_big)]

    if callback_query.data == "page_next":
        now_page += 1
    elif callback_query.data == "page_back":
        if now_page == 1:
            pass
        elif now_page > 1:
            now_page -= 1

    if for_request_for_dict in dict_univ:
        univ_less = "univ"
        for_request = dict_univ.get(for_request_for_dict)
    elif for_request_for_dict in dict_less:
        univ_less = "lesson"
        for_request = dict_less.get(for_request_for_dict)
    else:
        print('Error in start if/elif (next/back page)')

    list_login, list_about, pages = sql_request(univ_less, for_request)

    if pages > 0:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=list_teachers(pages, now_page, list_login, list_about, for_request_for_dict))

        if now_page == 1:
            await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                                reply_markup=next)
        elif pages == now_page:
            await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                                reply_markup=back)
        elif pages > now_page:
            await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                                reply_markup=next_back)
    elif pages == 0:
        pass
    elif pages < now_page:
        pass


@dp.callback_query_handler(NextBackUL())  # for changing univ/less tables
async def th_list(callback_query: types.CallbackQuery):
    if callback_query.data == 'sort_less':
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                            reply_markup=school_teacher2)
    elif callback_query.data == 'sort_univ':
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                            reply_markup=school_teacher1)






