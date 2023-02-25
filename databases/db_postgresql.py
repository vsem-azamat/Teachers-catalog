from sqlalchemy import URL, create_engine, text, func
from sqlalchemy.orm import sessionmaker

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


    async def check_exists(self, id_tg) -> bool:
        return True if self.s.query(Users).filter(Users.id_tg == id_tg).first() else False


    async def execute(self, sql):
        return self.conn.execute(sql)

 
    async def get_user_lang(self, id_tg):
        try:
            return self.s.query(Users.language).filter(Users.id_tg == id_tg).first()[0]
        except TypeError:
            return False


    async def new_user(self, id_tg: int, login: str):
        """
        Add the user to the DB if it doesn't exist
        """
        if not await self.check_exists(id_tg):
            user = Users(id_tg=id_tg, login=login)
            self.s.add(user)
            self.s.commit()


    async def update_user_lang(self, id_tg, language) -> None:
        self.s.query(Users).filter(Users.id_tg==id_tg).update({'language': language})
        self.s.commit()


    async def get_all_lessons(self):
        sql = text('SELECT * FROM get_all_lessons()')
        return self.conn.execute(sql)


    # LESSONS: UNIVERSITY
    async def get_universities(self) -> list:
        return self.s.query(Universities).all()


    async def get_lessons_of_university(self, univ_id):
        return self.s.query(LessonsUniversity).filter(LessonsUniversity.id==univ_id).all()


    async def get_lesson_of_university(self, lesson_id):
        return self.s.query(LessonsUniversity).filter(LessonsUniversity.id==lesson_id).first()


    async def get_count_teachers_of_university_lesson(self, lesson_id):
        data = {'lesson_id': lesson_id}
        sql = text('SELECT get_count_teachers_of_university_lesson(:lesson_id)')
        return self.conn.execute(sql, data).fetchone()[0]


    async def get_teachers_of_university_lesson(self, lesson_id: int, current_page: int, rows_per_page: int):
        data = {'lesson_id': lesson_id, 'current_page': 0+rows_per_page*(current_page-1), 'rows': rows_per_page}
        sql = text("SELECT * FROM get_teachers_of_university_lesson(:lesson_id) OFFSET :current_page LIMIT :rows")
        return self.conn.execute(sql, data)


    # LESSONS: LANGUAGES
    async def get_languages(self):
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


    async def get_teacher_profile(self, id_teacher):
        data = {'id_teacher': id_teacher}
        sql = text('SELECT * FROM get_teacher_profile(:id_teacher)')
        return self.conn.execute(sql, data).first()
    

db = SqlAlchemy()

