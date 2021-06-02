from aiogram.utils.exceptions import BadRequest

from db.sq_lite import cursor, conn


# RETURN "WELCOME" TEXT FROM SQL IF EXISTS
def welcome_from_sql(chat_id: str):
    sql = "SELECT * FROM welcome WHERE chat_id =(?)"
    cursor.execute(sql, [chat_id])
    welcome_dates = cursor.fetchone()

    if welcome_dates[2] == 0:   # RETURN NONE, BECAUSE STATE OF ON/OFF = "OFF"
        return None
    elif welcome_dates[2] == 1:
        return welcome_dates     # RETURN TEXT
    else:
        for i in range(len(welcome_dates)):
            error_dates = f"{welcome_dates[i]}, "
            error_text = "Error in def welcome_from_sql. Dates: " + error_dates
        return error_text


# SETTINGS WELCOME MESSAGE
def welcome_setting(chat_id: str, welcome_message):
    if welcome_message == "":  # START "IF" WITHOUT TEXT
        sql = """
                SELECT * 
                FROM welcome 
                WHERE chat_id = (?)
                """
        cursor.execute(sql, [chat_id])
        welcome_dates = cursor.fetchone()
        if welcome_dates is None:  # SET NEW SETTINGS IF NOT EXISTS IN DB FOR NEW CHAT
            sql = """
                    INSERT INTO welcome 
                    VALUES (?,?,?,?)
                    """
            values = [chat_id, "Добро пожаловать в чат!", str(1), str(0)]
            cursor.execute(sql, values)
            conn.commit()
            return "Приветствие активировано"
        else:  # CHANGING ON/OFF STATUS
            on_off_status = int(welcome_dates[2])
            if on_off_status == 1:
                on_off_status = "0"
                hello_text = "Выключено"
            else:
                on_off_status = "1"
                hello_text = "Включено"
            sql = f"""
                    UPDATE welcome 
                    SET on_off = ? 
                    WHERE chat_id = ?
                    """
            values = (on_off_status, chat_id)
            cursor.execute(sql, values)
            conn.commit()
            return f"Приветствие {hello_text}."
    else:  # CHANGING TEXT OF CHAT
        sql = """
                SELECT *
                FROM welcome
                WHERE chat_id = ?
                """
        cursor.execute(sql, [chat_id])
        sql_dates = cursor.fetchone()
        if sql_dates is None:  # INSERT AND ACTIVATE
            sql = """
                    INSERT INTO welcome
                    VALUES (?,?,?,?)
                    """
            values = (chat_id, welcome_message, "1", "0")
            cursor.execute(sql, values)
            conn.commit()
            return f"Приветствие активировано: \n\n{welcome_message}"
        else:  # ONLY SETTING WELCOME
            sql = f"""
                    UPDATE welcome 
                    SET text = ? 
                    WHERE chat_id = ?
                    """
            values = (welcome_message, chat_id)
            cursor.execute(sql, values)
            conn.commit()
        return f"Приветствие отредактировано: \n\n{welcome_message}"


# def w_button(chat_id: str):
#     sql = """
#             SELECT button
#             FROM welcome
#             WHERE chat_id = ?
#             """
#     cursor.execute(sql, [chat_id])
#     button_state_from_sql = cursor.fetchone()
#     if button_state_from_sql is not None:
#         if button_state_from_sql[0] == 0:
#             button_state = "1"
#             text_activate = "активирована"
#         else:
#             button_state = "0"
#             text_activate = "деактивирована"
#
#         sql = f"""
#                 UPDATE welcome
#                 SET button = ?
#                 WHERE chat_id = ?
#                 """
#         value = (button_state, chat_id)
#         cursor.execute(sql, value)
#         conn.commit()
#         return f"Кнопка FaceControl {text_activate}.", int(button_state)
#     else:
#         return 'Активируйте сначала "welcome"', None


# def face_state(chat_id: str, user_id: str):
#     sql = """
#         SELECT *
#         FROM face_control
#         WHERE user_id = ?
#         """
#     cursor.execute(sql, [user_id])
#     sql_dates = cursor.fetchone()
#     try:
#         return sql_dates[2]
#     except:
#         return None


