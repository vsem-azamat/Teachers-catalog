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
            return self.s.query(Users.lang).filter(Users.id_tg == id_tg).first()[0]
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


    async def update_user_lang(self, id_tg, lang) -> None:
        self.s.query(Users).filter(Users.id_tg==id_tg).update({'lang': lang})
        self.s.commit()


    async def get_universities(self) -> list:
        return self.s.query(Universities).all()


    async def get_university_lessons(self, univ_id):
        return self.s.query(LessonsUniv).filter(LessonsUniv.id_univ==univ_id).all()
        
    
    async def get_lesson_univ_teachers(self, lessons_id):
        """
        pl/pgSQL fuction:
        
        RETURNS TABLE(
            id_tg BIGINT, 
            login TEXT, 
            name TEXT, 
            description_univ TEXT, 
            price TEXT, 
            link TEXT)
        """
        data = {'lesson_id': lessons_id}
        sql = text("SELECT * FROM get_lesson_univ_teachers(:lesson_id)")
        return self.conn.execute(sql, data).all()


    async def get_teachers_univ_profiles(self, lesson_id: int, page: int, rows: int):
        data = {'lesson_id': lesson_id, 'page': 0+rows*(page-1), 'rows': rows}
        sql = text("SELECT * FROM get_teachers_univ_profiles(:lesson_id) OFFSET :page LIMIT :rows")
        return self.conn.execute(sql, data)

    async def get_teachers_univ_profiles_count(self, lesson_id):
        data = {'lesson_id': lesson_id}
        sql = text('SELECT get_teachers_univ_profiles_count(:lesson_id)')
        return self.conn.execute(sql, data).fetchone()[0]

    async def get_teacher_lessons(self, teacher_id: int):
        return self.s.query(LessonsUniv).\
            join(TeachersLessonsUniv, LessonsUniv.id_univ==TeachersLessonsUniv.id_lessons).\
            filter(TeachersLessonsUniv.id_teachers==teacher_id).all()

    async def get_lesson_info(self, lesson_id: int):
        return self.s.query(LessonsUniv).filter(LessonsUniv.id==lesson_id).first()



    async def test(self, lesson_id: int):
        q = self.s.query(
                    Users.id_tg,
                    Users.login, 
                    Teachers.name,
                    Teachers.description_univ,
                    Teachers.price,
                    Teachers.link, 
                    
                    func.string_agg(LessonsUniv.name, ',')
                .over(partition_by=LessonsUniv.name)
                .label('lessons')).\
            join(Users, Teachers.id_user==Users.id).\
            join(TeachersLessonsUniv, Teachers.id==TeachersLessonsUniv.id_teachers).\
            join(LessonsUniv, TeachersLessonsUniv.id_lessons==LessonsUniv.id).\
            filter(LessonsUniv.id==lesson_id).distinct().all()
            
        return q
db = SqlAlchemy()

