from typing import Optional, Union, List

from sqlalchemy import URL, create_engine, and_
from sqlalchemy.orm import sessionmaker, configure_mappers, Query


# Local imports
from bot.config import settingsDB
from bot.databases.db_declaration import *


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
    
    
    def _update_db(self):
        """Update the database schema in case of changes."""
        configure_mappers()


    def _drop_all(self):
        """Drop all tables in the database."""
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

 
    async def check_exists(self, id_tg: int, login: Optional[str] = None) -> Users:
        """
        Checks if a user exists in the database.

        Args:
            id_tg (int): The Telegram ID of the user.
            login (str): The username of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        user = self.s.query(Users).filter(Users.id_tg == id_tg).first()
        if user:
            user.login = login # type: ignore
            self.s.commit()
        else:
            user = Users(
                id_tg=id_tg,
                login=login,
            )
            self.s.add(user)
            self.s.commit()
        return user
    
 
    async def get_user_language(self, id_tg: int) -> str:
        """
        Gets the language of a user.

        Args:
            id_tg (int): The Telegram ID of the user.

        Returns:
            str: The language of the user.
        """
        user = self.s.query(Users).filter(Users.id_tg == id_tg).first()
        if user:
            return str(user.language)
        return ''


    async def update_user_language(self, id_tg: int, user_language: str) -> None:
        """
        Updates the language of a user.

        Args:
            id_tg (int): The Telegram ID of the user.
            user_language (str): The language of the user.

        Returns:
            None
        """
        self.s.query(Users).filter(Users.id_tg==id_tg).update({'language': user_language})
        self.s.commit()

    # TODO: Rewrite this method: must return a Query
    async def get_all_lessons(self, current_page: Optional[int] = 1, rows_per_page: Optional[int] = False, exclude_null_teachers: bool = False) -> List[Union[LessonsLanguage, LessonsUniversity]]:
        """
        Get all lessons from database.

        Args:
            current_page (int): The current page.
            rows_per_page (int): The number of rows per page.
            exclude_null_teachers (bool): Exclude lessons without teachers.

        Returns:
            List[Union[LessonsLanguage, LessonsUniversity]]: List of lessons.
        """        
        lessons_languages = self.s.query(LessonsLanguage)
        lessons_universities = self.s.query(LessonsUniversity)

        if exclude_null_teachers:
            lessons_languages = lessons_languages\
                .join(Teachers_LessonsLanguage)\
                .join(Teachers)\
                .filter(
                    and_(
                        Teachers.state.is_(True),
                        Teachers.state_admin.is_not(False)
                    )
                ).join(Users).filter(Users.login.isnot(None))
            lessons_universities = lessons_universities\
                .join(Teachers_LessonsUniversity)\
                .join(Teachers)\
                .filter(
                    and_(
                        Teachers.state.is_(True),
                        Teachers.state_admin.is_not(False)
                    )
                ).join(Users).filter(Users.login.is_not(None))

        lessons = lessons_languages.all() + lessons_universities.all()
        
        if current_page and rows_per_page:
            lessons = lessons[(current_page-1)*rows_per_page:current_page*rows_per_page]
        return lessons

    # TODO: Rewrite method which use this method. Should return a Query for better performance
    async def get_count_all_lessons(self, exclude_null_teachers: bool = False) -> int:
        """
        Get count all lessons from database.

        Args:
            exclude_null_teachers (bool): Exclude lessons without teachers.

        Returns:
            int: Count lessons.
        """
        lessons = await self.get_all_lessons(exclude_null_teachers=exclude_null_teachers)
        return len(lessons)

    
    # UNIVERSITY
    async def get_universities(self, exclude_null_teachers: Optional[bool] = False) -> Query[Universities]:
        """
        Get all universities from database.

        Args:
            exclude_null_teachers (bool): Exclude universities without teachers.

        Returns:
            Query[Universities]: Query of universities.
        """
        universities = self.s.query(Universities)
        if exclude_null_teachers:
            universities = universities\
                .join(LessonsUniversity.university)\
                .join(Teachers_LessonsUniversity)\
                .join(Teachers)\
                    .filter(
                        and_(
                            Teachers.state.is_(True),
                            Teachers.state_admin.is_not(False)
                        )
                    ).join(Users).filter(Users.login.isnot(None))
        return universities
            

    # LESSONS: UNIVERSITY
    async def get_lessons_of_university(self, university_id: int, exclude_null_teachers: Optional[bool] = False) -> Query[LessonsUniversity]:
        """
        Get all lessons of university from database.

        Args:
            university_id (int): The id of university.
            exclude_null_teachers (bool): Exclude lessons without teachers.

        Returns:
            Query[LessonsUniversity]: Query of lessons.
        """
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
                        Teachers.state_admin.is_not(False)
                    )
                ).join(Users).filter(Users.login.isnot(None))
        return lessons


    async def get_lesson_of_university(self, lesson_id) -> LessonsUniversity:
        """
        Get lesson of university from database.

        Args:
            lesson_id (int): The id of lesson.

        Returns:
            LessonsUniversity: Lesson.
        """
        return self.s.query(LessonsUniversity).filter(LessonsUniversity.id==lesson_id).first()


    # TEACHERS: UNIVERSITY
    async def get_teachers_of_university_lesson(self, lesson_id: int, current_page: Optional[int] = False, rows_per_page: Optional[int] = 0, 
        exclude_null_teachers: Optional[bool] = False) -> Query[Teachers]:
        """
        Get all teachers of university lesson from database.

        Args:
            lesson_id (int): The id of lesson.
            current_page (int): The current page.
            rows_per_page (int): The number of rows per page.
            exclude_null_teachers (bool): Exclude teachers without teachers.

        Returns:
            Query[Teachers]: Query of teachers.
        """
        
        teachers = self.s.query(Teachers)\
            .join(Teachers_LessonsUniversity)\
            .join(LessonsUniversity)\
            .filter(LessonsUniversity.id==lesson_id)
            
        if exclude_null_teachers:
            teachers = teachers.filter(
                and_(
                    Teachers.state.is_(True),
                    Teachers.state_admin.is_not(False),
                ),
            ).join(Users).filter(Users.login.isnot(None))
        
        if current_page and rows_per_page:
            teachers = teachers.limit(rows_per_page).offset(rows_per_page*(current_page-1))
        
        return teachers

    
    # LESSONS: LANGUAGES
    async def get_lessons_of_languages(self, exclude_null_teachers: Optional[bool] = False) -> Query[LessonsLanguage]:
        """
        Get all lessons of languages from database.

        Args:
            exclude_null_teachers (bool): Exclude lessons without teachers.

        Returns:
            Query[LessonsLanguage]: Query of lessons.
        """
        lessons = self.s.query(LessonsLanguage)
        if exclude_null_teachers:
            lessons = lessons\
                .join(Teachers_LessonsLanguage)\
                .join(Teachers)\
                .filter(
                    and_(
                        Teachers.state.is_(True),
                        Teachers.state_admin.is_not(False)
                    )
                ).join(Users).filter(Users.login.isnot(None))
        return lessons
    

    # TEACHERS: LANGUAGES
    async def get_teachers_of_language_lesson(self, lesson_id: int, current_page: Optional[int] = False, rows_per_page: Optional[int] = 0, 
        exclude_null_teachers: Optional[bool] = False) -> Query[Teachers]:
        """
        Get all teachers of language lesson from database.

        Args:
            lesson_id (int): The id of lesson.
            current_page (int): The current page.
            rows_per_page (int): The number of rows per page.
            exclude_null_teachers (bool): Exclude teachers without teachers.

        Returns:
            Query[Teachers]: Query of teachers.
        """
        teachers = self.s.query(Teachers)\
            .join(Teachers_LessonsLanguage)\
            .join(LessonsLanguage)\
            .filter(LessonsLanguage.id==lesson_id)
        
        if exclude_null_teachers:
            teachers = teachers.filter(
                and_(
                    Teachers.state.is_(True),
                    Teachers.state_admin.is_not(False),
                )
            ).join(Users).filter(Users.login.isnot(None))
        
        if current_page and rows_per_page:
            teachers = teachers.limit(rows_per_page).offset(rows_per_page*(current_page-1))
        
        return teachers

    
    async def get_lesson_of_language(self, lesson_id: int) -> Optional[LessonsLanguage]:
        """
        Get lesson of language from database.

        Args:
            lesson_id (int): The id of lesson.

        Returns:
            LessonsLanguage: Lesson.
        """
        return self.s.query(LessonsLanguage).filter(LessonsLanguage.id==lesson_id).first()


    # TEACHER
    async def get_teacher(self, teacher_id_tg: int) -> Optional[Teachers]:
        """
        Get teacher from database.

        Args:
            teacher_id_tg (int): The id of teacher.

        Returns:
            Teachers: Teacher.
        """
        return self.s.query(Teachers).filter(Teachers.id_tg==teacher_id_tg).first()


    # TEACHER SETTINGS
    async def upset_teacher_profile(self, new_teacher: Teachers) -> Teachers:
        """
        Add or update teacher profile in database.

        Args:
            new_teacher (Teachers): The teacher object.

        Returns:
            Teachers: Teacher.
        """
        teacher = await self.get_teacher(teacher_id_tg=new_teacher.id_tg) # type: ignore

        # If teacher exists -> Update
        if teacher:
            for key, value in new_teacher.__dict__.items():
                if key != "_sa_instance_state" or value is not None:
                    setattr(teacher, key, value)

        # If teacher does not exist -> Add
        else:
            teacher = new_teacher
            self.s.add(teacher)

        self.s.commit()
        return teacher

              
    async def add_lessons_to_teacher(self, teacher_id_tg: int, lesson: Union[LessonsUniversity, LessonsLanguage], add: bool = True) -> Teachers:
        """
        Add or remove lessons to teacher.

        Args:
            teacher_id_tg (int): The id of teacher.
            lesson (Union[LessonsUniversity, LessonsLanguage]): The lesson object.
            add (bool): Add or remove lesson.

        Returns:
            Teachers: Teacher.
        """
        teacher = await self.get_teacher(teacher_id_tg=teacher_id_tg)

        # Check if lesson exists
        if isinstance(lesson, LessonsUniversity):
            lesson = self.s.query(LessonsUniversity).filter(LessonsUniversity.id==lesson.id).first()
        elif isinstance(lesson, LessonsLanguage):
            lesson = self.s.query(LessonsLanguage).filter(LessonsLanguage.id==lesson.id).first()
        else:
            raise ValueError("lesson must be LessonsUniversity or LessonsLanguage")
        
        # Add lesson to teacher
        if add:
            if isinstance(lesson, LessonsUniversity) and lesson not in teacher.lesson_university:
                teacher.lesson_university.append(lesson)
            elif isinstance(lesson, LessonsLanguage) and lesson not in teacher.lesson_language:
                teacher.lesson_language.append(lesson)
            
        # Remove lesson from teacher
        else:
            if isinstance(lesson, LessonsUniversity) and lesson in teacher.lesson_university:
                teacher.lesson_university.remove(lesson)
            elif isinstance(lesson, LessonsLanguage) and lesson in teacher.lesson_language:
                teacher.lesson_language.remove(lesson)
        
        self.s.commit()
        return teacher



    async def teacher_state_update(self, teacher_id_tg: int, state: bool) -> Teachers:
        """
        Update teacher state.

        Args:
            teacher_id_tg (int): The id of teacher.
            state (bool): The state of teacher.

        Returns:
            Teachers: Teacher.
        """
        teacher = await self.get_teacher(teacher_id_tg=teacher_id_tg)
        teacher.state = state # type: ignore

        self.s.commit()
        return teacher


    async def get_chats(self) -> Query[Chats]:
        """
        Get all chats from database.

        Returns:
            Query[Chats]: Query of chats.
        """
        return self.s.query(Chats)


db = SqlAlchemy()

