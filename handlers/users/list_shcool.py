from aiogram import types

from loader import dp, bot
from sq_lite import cursor
from keyboards.inline.db_list import next, back, next_back

import math

@dp.callback_query_handler()
async def th_list(callback_query: types.CallbackQuery):
    dict_univ = {'list_cvut':'cvut', 'list_uk':'uk', 'list_vse':'vse',
                 'list_czu':'czu', 'list_vut':'vut', 'list_masaryk':'masaryk'}
    dict_less = {'list_math':'math','list_nostr':'nostr','list_boil':'biol','list_chem':'chem',
                 'list_czech':'czech','list_engl':'engl'}


    if callback_query.data in dict_univ:
        try:
            await bot.answer_callback_query(callback_query.id)
            univ = dict_univ.pop(callback_query.data)
            list_login = []
            list_about = []
            sql = "SELECT * FROM list_teachers WHERE univ = ?"
            cursor.execute(sql, [(univ)])
            catalog = cursor.fetchall()
            d = 0  # порядковый номер для спика учителей
            now_page = 1  # текущая страница
            pages = 0  # количество страниц
            for i in catalog:
                login = i[1]
                about = i[6]
                list_login.append(login)
                list_about.append(about)
                pages = int(round((len(list_login)) / 5,0))
                count_th = len(list_login)
        except:
            print('Error dp script')

        try:
            


            th_all = ''
            for i in range(5):
                try:
                    th = (f'''
    Логин: {list_login[i]}
    Описание: {list_about[i]}
                    ''')
                except:
                    print('Error th list')
                    th = ''
                th_all += th

            th_low = (f'''
    Страница: {now_page} из {pages}
                ''')

            ##########################################
            markup_for_list = None
            if now_page == 1:
                markup_for_list = next

            elif now_page > 1 and now_page > pages:
                markup_for_list = next_back

            elif now_page < 1 and now_page == pages:
                markup_for_list = back
            ##########################################
                # ЕСЛИ ДЕЛАЮ ХУЙНЮ, МАЯЧТЕ

            th_all += th_low
            await bot.send_message(callback_query.from_user.id, text=th_all, reply_markup=markup_for_list)

        except:
            print('Error handler')












    # elif callback_query.data in dict_less:
    #     await bot.answer_callback_query(callback_query.id)
    #     less = dict_less.pop(callback_query.data)
    #     pass



    # elif callback_query.data == 'list_next':
    #     await bot.answer_callback_query(callback_query.id)
    #     await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=school_teacher2)
    #
    #
    # if callback_query.data == 'list_back':
    #     await bot.answer_callback_query(callback_query.id)
    #     await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=school_teacher1)


































# @dp.callback_query_handler()
# async def list1_univerity(callback_query: types.CallbackQuery):

    # if callback_query.data == 'list_cvut':
    #     await bot.answer_callback_query(callback_query.id)
    #     b = 1
    #     univers = 'cvut'
    #
    # if callback_query.data == 'list_vse':
    #     await bot.answer_callback_query(callback_query.id)
    #     b = 1
    #     univers = 'vse'
    #
    # if callback_query.data == 'list_uk':
    #     await bot.answer_callback_query(callback_query.id)
    #     b = 1
    #     univers = 'uk'
    #
    # if callback_query.data == 'list_czu':
    #     await bot.answer_callback_query(callback_query.id)
    #     b = 1
    #     univers = 'czu'
    #
    # if callback_query.data == 'list_vut':
    #     await bot.answer_callback_query(callback_query.id)
    #     b = 1
    #     univers = 'vut'
    #
    # if callback_query.data == 'list_masaryk':
    #     await bot.answer_callback_query(callback_query.id)
    #     b = 1
    #     univers = 'masaryk'

    # if callback_query.data == 'list_add':
    #     await bot.answer_callback_query(callback_query.id)
    #     await bot.send_message(callback_query.from_user.id,'Напишите нам на бота и мы вас добавим!')

#     if callback_query.data == 'list_next':
#         await bot.answer_callback_query(callback_query.id)
#         await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=school_teacher2)
#
# #####################################################
#
#     if callback_query.data == 'list_back':
#         await bot.answer_callback_query(callback_query.id)
#         await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=school_teacher1)

    # if b == 1:
    #     list_login = []
    #     list_about = []
    #     sql = "SELECT * FROM list_teachers WHERE univ = ?"
    #     cursor.execute(sql,[(univers)])
    #     catalog = cursor.fetchall()
    #     d = 0 #порядковый номер для спика учителей
    #     now_page = 1 #текущая страница
    #     pages = 0 #количество страниц
    #
    #     for i in catalog:
    #         login = i[1]
    #         about = i[6]
    #         list_login.append(login)
    #         list_about.append(about)
    #         pages = math.ceil((len(list_login))/5)
    #         count_th = len(list_login)
    #
    #
    #
    #         # print(now_page)
    #
    #
    #
    #         await bot.send_message(callback_query.from_user.id, text=list_login, reply_markup=next)
    #
    #
    #     if now_page > 1 and now_page > pages:
    #         await bot.send_message(callback_query.from_user.id, text=list_login, reply_markup=next_back)
    #
    #
    #     if now_page > 1 and now_page == pages:
    #         await bot.send_message(callback_query.from_user.id, text=list_login, reply_markup=back)
    #
    #
    # ########################################
    #
    #     if callback_query.data == 'next':
    #         now_page +=1
    #         return now_page
    #     if callback_query.data == 'back':
    #         now_page -= 1
    #



