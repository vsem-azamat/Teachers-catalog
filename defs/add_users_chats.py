from db.sq_lite import cursor, conn


def add_users_of_chats(id_user):
    id_user = str(id_user)
    sql = """
    INSERT INTO chat_users
    (user_id)
    VALUES (?)
    """
    print(sql)
    cursor.execute(sql, (id_user))
    conn.commit()
