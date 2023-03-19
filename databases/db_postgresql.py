from typing import Optional

from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker, exc


from .db_declaration import *

class SqlAlchemy:
    def __init__(self):
        self.url_object = URL.create(
            "postgresql+pg8000",
            username="postgres",
            password="065Ababa",
            host="localhost",
            database="teachers_bot",
        )
        self.engine = create_engine(self.url_object, client_encoding='utf8')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)
        self.s = self.session()
        self.conn = self.engine.connect()


    def conv_dict(self, query) -> dict:
        """
        Converts the query result to a dict
        """
        return [dict(i) for i in query][0]


    async def check_exists(self, id_tg: int, login: str) -> bool:
        user = self.s.query(Users).filter(Users.id_tg == id_tg).first()
        if user:
            user.login = login
            self.s.commit()
        else:
            user = Users(
                id_tg=id_tg,
                login=login,
                )
            self.s.add(user)
            self.conn.commit()
        return user

            
    async def execute(self, sql):
        return self.conn.execute(sql)

 
    async def get_user_language(self, id_tg):
        try:
            return self.s.query(Users.language).filter(Users.id_tg == id_tg).first()[0]
        except TypeError:
            return False


    async def update_user_lang(self, id_tg, user_language) -> None:
        self.s.query(Users).filter(Users.id_tg==id_tg).update({'language': user_language})
        self.s.commit()


    async def get_all_lessons(self, current_page: int = 0, rows_per_page: int = 0, exclude_null_teachers: bool = False):
        data = {'current_page': 0+rows_per_page*(current_page-1), 'rows': rows_per_page, 'exclude_null_teachers': exclude_null_teachers}
        interval = ""
        if current_page and rows_per_page:
            interval = "OFFSET :current_page LIMIT :rows"
        sql = text('SELECT * FROM get_all_lessons(:exclude_null_teachers) ' + interval)
        return self.conn.execute(sql, data)
    

    async def get_count_all_lessons(self, exclude_null_teachers: Optional[bool] = False):
        data = {'exclude_null_teachers': exclude_null_teachers}
        sql = text("SELECT get_count_all_lessons(:exclude_null_teachers);")
        return self.conn.execute(sql, data).fetchone()[0]


    # LESSONS: UNIVERSITY
    async def get_universities(self) -> list:
        return self.s.query(Universities).all()


    async def get_lessons_of_university(self, university_id):
        return self.s.query(LessonsUniversity).filter(LessonsUniversity.id_university==university_id).all()


    async def get_lesson_of_university(self, lesson_id):
        return self.s.query(LessonsUniversity).filter(LessonsUniversity.id==lesson_id).first()


    async def get_count_teachers_of_university_lesson(self, lesson_id):
        data = {'lesson_id': lesson_id}
        sql = text('SELECT get_count_teachers_of_university_lesson(:lesson_id)')
        return self.conn.execute(sql, data).fetchone()[0]
 

    async def get_teachers_of_university_lesson(self, lesson_id: int, current_page: int = 0, rows_per_page: int = 0):
        data = {'lesson_id': lesson_id, 'current_page': 0+rows_per_page*(current_page-1), 'rows': rows_per_page}
        interval = ""
        if current_page and rows_per_page:
            interval = "OFFSET :current_page LIMIT :rows"
        sql = text("SELECT * FROM get_teachers_of_university_lesson(:lesson_id) " + interval)
        return self.conn.execute(sql, data)

    
    # LESSONS: LANGUAGES
    async def get_lessons_languages(self):
        return self.s.query(LessonsLaguage).all()


    async def get_count_teachers_of_language_lesson(self, lesson_id):
        data = {'lesson_id': lesson_id}
        sql = text('SELECT get_count_teachers_of_language_lesson(:lesson_id)')
        return self.conn.execute(sql, data).fetchone()[0]


    async def get_teachers_of_language_lesson(self, lesson_id: int, current_page: int, rows_per_page: int):
        data = {'lesson_id': lesson_id, 'current_page': 0+rows_per_page*(current_page-1), 'rows': rows_per_page}
        sql = text("SELECT * FROM get_teachers_of_language_lesson(:lesson_id) OFFSET :current_page LIMIT :rows")
        return self.conn.execute(sql, data)

    
    async def get_lesson_of_language(self, lesson_id: int):
        return self.s.query(LessonsLaguage).filter(LessonsLaguage.id==lesson_id).first()


    async def get_teacher_profile(self, teacher_id: int = 0, user_id_tg: int = 0):
        if teacher_id:
            data = {'teacher_id': teacher_id}
            sql = text('SELECT * FROM get_teacher_profile(:teacher_id)')
        elif user_id_tg:
            try:
                teacher = await self.get_teacher(user_id_tg=user_id_tg)
                data = {'teacher_id': teacher.id}
                sql = text('SELECT * FROM get_teacher_profile(:teacher_id)')
            except AttributeError:
                return False
        teacher = self.conn.execute(sql, data).fetchone()
        if teacher:
            return teacher
        return False
    
    
    # TEACHER SETTINGS
    async def get_teacher(self, user_id_tg: int):
        return self.s.query(Teachers).join(Users, Users.id==Teachers.id_user).filter(Users.id_tg==user_id_tg).first()

    
    async def add_teacher_profile(self, id_tg: int, **update_fields):
        user = self.s.query(Users).filter(Users.id_tg==id_tg).first()
        teacher = await db.get_teacher(user_id_tg=id_tg)
        # Update old teacher
        if teacher:
            setattr(teacher, 'id_user', user.id)
            for field, value in update_fields.items():
                setattr(teacher, field, value)
        # Add new teacher
        else:
            teacher = Teachers(
                id_user=user.id,
                **update_fields
            )
        self.s.merge(teacher)
        self.s.commit()
        return teacher


    async def get_lessons_id_of_teacher(self, table_name: str, teacher_id: int = 0, user_id_tg: int = 0):
        
        if table_name == "TeachersLessonsLanguage":
            table = TeachersLessonsLanguage
        elif table_name == "TeachersLessonsUniversity":
            table = TeachersLessonsUniversity

        if table is None:
            raise ValueError(f"Invalid table name: {table_name}")


        if not teacher_id:
            try:
                teacher = await self.get_teacher(user_id_tg=user_id_tg)
                teacher_id = teacher.id
            except AttributeError:
                return False
        else:
            return self.s.query(table).filter(table.id_teacher==teacher_id).all()
        return False

              
    async def add_lessons_to_teacher(self, table_name: str, teacher_id: int, lesson_id: int, add: bool = True):
        """
        add: bool
            True  - add row
            False - delete row
        """
        table = None
        if table_name == "TeachersLessonsLanguage":
            table = TeachersLessonsLanguage
        elif table_name == "TeachersLessonsUniversity":
            table = TeachersLessonsUniversity

        if table is None:
            raise ValueError(f"Invalid table name: {table_name}")

        lesson = self.s.query(table).filter(table.id_teacher == teacher_id, table.id_lesson == lesson_id).first()    

        # Add lesson from teacher profile
        if lesson is None and add:
            lesson = table(
                id_teacher = teacher_id,
                id_lesson = lesson_id,
            )
            self.s.merge(lesson)
        # Delete lesson from teacher profile
        else:
            try:
                self.s.delete(lesson)
            except exc.UnmappedInstanceError:
                return
        self.s.commit()

    async def teacher_state_update(self, teacher_id: int, state: bool):
        self.s.query(Teachers).filter(Teachers.id==teacher_id).update({'state': state})
        self.s.commit()


    async def get_chats(self):
        return self.s.query(Chats).all()
    



db = SqlAlchemy()

