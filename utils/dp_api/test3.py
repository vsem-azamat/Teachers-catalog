from sq_lite import cursor

sql = "SELECT * FROM list_teachers WHERE univ=?"
cursor.execute(sql,[('uk')])

pr = cursor.fetchall()
b=0

for i in pr:
    b+=1
    login = i[1]
    about = i[6]
    print(f"""
    {b}) login:{login}
        описание: {about}
        """
          )