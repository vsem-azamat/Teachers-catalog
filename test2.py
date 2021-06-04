from db.sq_lite import cursor, conn

# text = """
#         INSERT INTO all_texts
#         (all_text)
#         VALUES ("['uk','math']")
#         """
# cursor.execute(text)
# conn.commit()

# sql = """
# SELECT all_text FROM all_texts
# """
# cursor.execute(sql)
# catalog = cursor.fetchall()
# for_split = " ".join(catalog[0][0])
# print(for_split)

text = "test1 test2"
text = text.split()

print(text)
