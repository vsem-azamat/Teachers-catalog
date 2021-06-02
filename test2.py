from db.sq_lite import cursor, conn

text ="""
        INSERT INTO list_teachers 
        (login, about) 
        VALUES ("test", "proslo")"""

cursor.execute(text)
conn.commit()


