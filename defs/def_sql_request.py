from db.sq_lite import cursor
import math

dict_for_th_start = {'list_cvut': 'ČVUT', 'list_uk': 'Karlov', 'list_vse': 'VŠE',
                     'list_czu': 'ČZU', 'list_vut': 'VUT', 'list_masaryk': 'Masaryk',
                     'list_math': 'Математика', 'list_nostr': 'Нострификация', 'list_boil': 'Биология',
                     'list_chem': 'Химия', 'list_czech': 'Чешский', 'list_engl': 'Английский'
                     }


def list_teachers(pages, now_page, list_login, list_about, callback_for_dict):
    from_dict = dict_for_th_start.get(callback_for_dict)  # example date: uk, vse
    now_page = int(now_page)
    number_page = now_page

    if now_page == 1:
        for_pages = 0
    elif now_page > 1:
        now_page -= 1
        for_pages = now_page * 5
    now_page -= 1

    th_all = f"""<b>Список репетиторов: {from_dict}</b>
    """
    for i in range(5):
        try:
            th = (f"""
{for_pages + 1 + i}) <b>Логин:</b> {list_login[for_pages + i]}
   <b>Описание:</b> {list_about[for_pages + i]}
                """)
        except:
            th = ""
        th_all += th
    th_pages = (f"""
Страница: {number_page} из {pages}
    """)
    th_all += th_pages
    return th_all


def sql_request(univ_less, for_request):
    list_login = []
    list_about = []
    quest = '=? '
    sql = "SELECT login, about FROM list_teachers WHERE " + univ_less + quest
    cursor.execute(sql, [for_request])
    catalog = cursor.fetchall()
    for i in catalog:
        login = i[0]
        about = i[1]
        list_login.append(login)
        list_about.append(about)
    pages = int(math.ceil((len(list_login)) / 5))
    return list_login, list_about, pages
