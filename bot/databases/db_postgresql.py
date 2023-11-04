from typing import Optional, Union, List

from sqlalchemy import URL, create_engine, text, and_, union_all, func, select
from sqlalchemy.orm import sessionmaker, exc, configure_mappers, joinedload, Query


from config import settingsDB
from databases.db_declaration import *


class SqlAlchemy:
    def __init__(self) -> None:
        self.url_object = URL.create(
            drivername="postgresql+pg8000",
            username=settingsDB.USERNAME,
            password=settingsDB.PASSWORD,
            host=settingsDB.HOST,
            database=settingsDB.DATABASE,
        )
        self.engine = create_engine(self.url_object, client_encoding='utf8')
        self.conn = self.engine.connect()
        Base.metadata.create_all(self.engine, checkfirst=True)
        self.session = sessionmaker(bind=self.engine)
        self.s = self.session()
    
    
    def update_db(self):
        configure_mappers()


    def drop_all(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

 
    async def check_exists(self, id_tg: int, login: Optional[str] = None) -> bool:
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
            self.s.commit()
        return user
    
 
    async def get_user_language(self, id_tg: int) -> Optional[Union[str, bool]]:
        try:
            return self.s.query(Users).filter(Users.id_tg == id_tg).first().language
        except AttributeError:
            return False


    # rewrite!
    async def update_user_lang(self, id_tg, user_language: str) -> None:
        self.s.query(Users).filter(Users.id_tg==id_tg).update({'language': user_language})
        self.s.commit()


    # rewrite which use this method
    async def get_all_lessons(self, current_page: Optional[int] = False, rows_per_page: Optional[int] = False, exclude_null_teachers: bool = False):
        """
        Retrieves all lessons based on the provided parameters.

        Parameters:
        - current_page (int): The current page number of the results. Defaults to 0.
        - rows_per_page (int): The number of rows per page. Defaults to 0.
        - exclude_null_teachers (bool): Flag indicating whether to exclude lessons with null teachers. Defaults to False.

        Returns:
        - data (dict): A dictionary containing the retrieved lesson data.
            - 'id' (int): The ID of the lesson.
            - 'name' (str): The name of the lesson.
            - 'code' (str): The code of the lesson.
            - 'link_image' (str): The link to the image associated with the lesson/university/type.
            - 'id_university' (int): The ID of the university offering the lesson.
            - 'name_university' (str): The name of the university offering the lesson.
            - 'source' (str): The source of the lesson (e.g., 'university' or 'languages, etc.').
        """
        all_lessons = []
        
        lessons_university  = self.s.query(LessonsUniversity)
        all_lessons.extend(lessons_university)
        
        lessons_language = self.s.query(LessonsLanguage)
        all_lessons.extend(lessons_language)
        
        if exclude_null_teachers:
            all_lessons = [
                lesson for lesson in all_lessons 
                    if lesson.teacher and lesson.teacher[0].state and lesson.teacher[0].state_admin
                ]

        if current_page and rows_per_page:
            current_page = rows_per_page*(current_page-1)
            all_lessons = all_lessons[current_page:current_page+rows_per_page]
        
        return all_lessons


    async def get_count_all_lessons(self, exclude_null_teachers: Optional[bool] = False) -> int:
        lessons_university = self.s.query(func.count(LessonsUniversity.id))
        lessons_language = self.s.query(func.count(LessonsUniversity.id))
                
        if exclude_null_teachers:
            lessons_university = lessons_university.join(LessonsUniversity.teacher).filter(
                and_(
                    Teachers.state.is_(True),
                    Teachers.state_admin.is_(True)
                )
            )
            lessons_language = lessons_language.join(LessonsUniversity.teacher).filter(
                and_(
                    Teachers.state.is_(True),
                    Teachers.state_admin.is_(True)
                )
            )
        count_lessons_university = lessons_university.scalar()
        count_lessons_language = lessons_language.scalar()

        return count_lessons_university + count_lessons_language


    # LESSONS: UNIVERSITY
    async def get_universities(self, exclude_null_teachers: Optional[bool] = False) -> Query[Universities]:
        universities = self.s.query(Universities)
        if exclude_null_teachers:
            universities = universities\
                .join(LessonsUniversity.university)\
                .join(Teachers_LessonsUniversity)\
                .join(Teachers)\
                    .filter(
                        and_(
                            Teachers.state.is_(True),
                            Teachers.state_admin.is_(True)
                        )
                    )
        return universities
            

    async def get_lessons_of_university(self, university_id: int, exclude_null_teachers: Optional[bool] = False) -> Query[LessonsUniversity]:
        lessons = self.s.query(LessonsUniversity)\
            .join(LessonsUniversity_Universities)\
            .join(Universities)\
            .filter(Universities.id==university_id)
        if exclude_null_teachers:
            lessons = lessons\
                .join(Teachers_LessonsUniversity)\
                .join(Teachers)\
                .filter(
                    and_(
                        Teachers.state.is_(True),
                        Teachers.state_admin.is_(True)
                    )
                )
        return lessons


    async def get_lesson_of_university(self, lesson_id):
        return self.s.query(LessonsUniversity).filter(LessonsUniversity.id==lesson_id).first()


    async def get_teachers_of_university_lesson(self, lesson_id: int, current_page: Optional[int] = False, rows_per_page: Optional[int] = 0, 
        exclude_null_teachers: Optional[bool] = False) -> Query[Teachers]:
        teachers = self.s.query(Teachers)\
            .join(Teachers_LessonsUniversity)\
            .join(LessonsUniversity)\
            .filter(LessonsUniversity.id==lesson_id)
            
        if exclude_null_teachers:
            teachers.filter(
                and_(
                    Teachers.state,
                    Teachers.state_admin
                )
            )
        
        if current_page and rows_per_page:
            current_page = rows_per_page*(current_page-1)
            teachers = teachers[current_page:current_page+rows_per_page]
        
        return teachers

    
    # LESSONS: LANGUAGES
    async def get_lessons_of_languages(self, exclude_null_teachers: Optional[bool] = False) -> Query[LessonsLanguage]:
        lessons = self.s.query(LessonsLanguage)
        if exclude_null_teachers:
            lessons = lessons\
                .join(Teachers_LessonsLanguage)\
                .join(Teachers)\
                .filter(
                    and_(
                        Teachers.state.is_(True),
                        Teachers.state_admin.is_(True)
                    )
                )
        return lessons
    

    async def get_teachers_of_language_lesson(self, lesson_id: int, current_page: Optional[int] = False, rows_per_page: Optional[int] = 0, 
        exclude_null_teachers: Optional[bool] = False) -> Query[Teachers]:
        teachers = self.s.query(Teachers)\
            .join(Teachers_LessonsLanguage)\
            .join(LessonsLanguage)\
            .filter(LessonsLanguage.id==lesson_id)
        
        if exclude_null_teachers:
            teachers.filter(
                and_(
                    Teachers.state,
                    Teachers.state_admin
                )
            )
        
        if current_page and rows_per_page:
            current_page = rows_per_page*(current_page-1)
            teachers = teachers[current_page:current_page+rows_per_page]
        
        return teachers

    
    async def get_lesson_of_language(self, lesson_id: int) -> LessonsLanguage:
        return self.s.query(LessonsLanguage).filter(LessonsLanguage.id==lesson_id).first()


    # TEACHER
    async def get_teacher(self, teacher_id_tg: int = 0) -> Teachers:
        return self.s.query(Teachers).filter(Teachers.id_tg==teacher_id_tg).first()
    

    # TEACHER SETTINGS
    # async def add_teacher_profile(self, id_tg: int, **update_fields):
        # user: Users = self.s.query(Users).filter(Users.id_tg==id_tg).first()
        # teacher = await db.get_teacher(teacher_id_tg=id_tg)
        # # Update old teacher
        # if teacher:
        #     setattr(teacher, 'id_user', user.id)
        #     for field, value in update_fields.items():
        #         setattr(teacher, field, value)
        # # Add new teacher
        # else:
        #     teacher = Teachers(
        #         id_user=user.id,
        #         **update_fields
        #     )
        # self.s.merge(teacher)
        # self.s.commit()
        # return teacher
        
    async def update_teacher_profile(self, id_tg: int, teacher_object: Teachers) -> Teachers:
        teacher = await self.get_teacher(teacher_id_tg=id_tg)
        self.s.merge(teacher_object)
        self.s.commit()
        return teacher

    
    # I THINK IT CAN BE REPLACED WITH ANOTHER METHOD: get_teacher
    # async def get_lessons_id_of_teacher(self, teacher_id_tg: int, table_name: Optional[str] = None):  
    #     if table_name == "TeachersLessonsLanguage":
    #         table = Teachers_LessonsLanguage
    #     elif table_name == "TeachersLessonsUniversity":
    #         table = Teachers_LessonsUniversity
    #     else:
    #         raise ValueError(f"Invalid table name: {table_name}")

    #     return self.s.query(table).filter(table.id_teacher==teacher_id).all()

              
    async def add_lessons_to_teacher(self, teacher_id_tg: int, table_name: str, lesson_id: int, add: bool = True) -> None:
        """
        add: bool
            True  - add row
            False - delete row
        """
        teacher = await self.get_teacher(teacher_id_tg=teacher_id_tg)

        if table_name == "TeachersLessonsLanguage":
            lesson = self.s.query(LessonsLanguage).filter(LessonsLanguage.id==lesson_id).first()
            if add:
                teacher.lesson_language.append(lesson)
            else:  
                teacher.lesson_language.remove(lesson)
        elif table_name == "TeachersLessonsUniversity":
            lesson = self.s.query(LessonsUniversity).filter(LessonsUniversity.id==lesson_id).first()
            if add:
                teacher.lesson_university.append(lesson)
            else:
                teacher.lesson_university.remove(lesson)
                
        else: 
            raise ValueError(f"Invalid table name: {table_name}")

        self.s.merge(teacher)
        self.s.commit()


    async def teacher_state_update(self, teacher_id_tg: int, state: bool) -> None:
        teacher = Teachers(id_tg=teacher_id_tg, state=state)
        self.s.merge(teacher)
        self.s.commit()


    async def get_chats(self) -> List[Chats]:
        return self.s.query(Chats).all()


db = SqlAlchemy()

