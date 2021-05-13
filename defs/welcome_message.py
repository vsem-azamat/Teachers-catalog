from db.sq_lite import cursor


def welcome_from_sql(chat_id: str):
    sql = "SELECT * FROM welcome WHERE chat_id =(?)"
    cursor.execute(sql, [chat_id])
    welcome_text = cursor.fetchone()

    if welcome_text[2] == 0:
        return None
    elif welcome_text[2] == 1:
        return welcome_text[1]
    else:
        try:
            return f"Error: sql request. Dates: {chat_id}, {welcome_text[1], welcome_text[2]}"
        except:
            return f"Error: sql request. Dates: ERROR"


def welcome_change(chat_id, welcome_message):

    sql = """
    INSERT INTO
    """

    pass
