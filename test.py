from db.sq_lite import cursor, conn


def welcome_change(chat_id: str, welcome_message):
    if welcome_message == "":
        sql = "SELECT * FROM welcome WHERE chat_id =(?)"
        print(sql)
        cursor.execute(sql, [chat_id])
        welcome_dates = cursor.fetchall()
        if len(welcome_dates) == 0:
            sql = "INSERT INTO welcome VALUES (?,?,?)"
            values = [chat_id,"Добро пожаловать в чат!", str(1)]
            cursor.execute(sql, values)
            conn.commit()

    else:
        pass


chat_id = -1001404474065
print(welcome_change(chat_id, ""))
