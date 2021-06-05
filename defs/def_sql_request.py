from aiogram.utils.markdown import hlink

from db.sq_lite import cursor
import math

dict_for_th_start = {'list_cvut': 'ČVUT', 'list_vse': 'VŠE',
                     'list_uk': 'Karlov', 'list_czu': 'ČZU',
                     'list_vut': 'VUT', 'list_masaryk': 'Masaryk',
                     'list_vscht': 'vscht',

                     'list_math': 'Математика', "list_fyz": "Физика",
                     'list_prog': 'Програмирование', 'list_stat': 'Статистика',
                     'list_eco': 'Экономика', 'list_prav': 'Право',
                     'list_boil': 'Биология', 'list_chem': 'Химия',
                     'list_czech': 'Чешский', 'list_engl': 'Английский',
                     'list_nostr': 'Нострификация'
                     }


def list_teachers(pages, now_page, list_login, list_about, callback_for_dict, list_link):
    from_dict = dict_for_th_start.get(callback_for_dict)  # example date: uk, vse
    now_page = int(now_page)
    number_page = now_page

    if now_page == 1:
        for_pages = 0
    elif now_page > 1:
        now_page -= 1
        for_pages = now_page * 3
    now_page -= 1

    th_all = f"""<b>Репетиторы: {from_dict}</b>
    """
    for i in range(3):
        try:
            if list_link[for_pages + i] is not None:
                link = hlink('Подробнее о преподавателе', f'{list_link[for_pages + i]}')
            else:
                link = ''
        except:
            link = ''

        try:
            th = (f"""
{for_pages + 1 + i}) {list_login[for_pages + i]}

{list_about[for_pages + i]}
<b>{link}</b>
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
    list_link = []
    quest = '=? '
    sql = "SELECT login, about, link FROM list_teachers WHERE " + univ_less + quest
    cursor.execute(sql, [for_request])
    catalog = cursor.fetchall()
    for i in catalog:
        login = i[0]
        about = i[1]
        link = i[2]
        list_login.append(login)
        list_about.append(about)
        list_link.append(link)
    pages = int(math.ceil((len(list_login)) / 3))
    return list_login, list_about, list_link, pages
