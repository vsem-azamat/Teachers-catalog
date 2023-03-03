from sqlalchemy import create_engine, Table,\
    Column, ForeignKey,\
    Integer, BigInteger,\
    Text, VARCHAR ,\
    Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    id_tg = Column(BigInteger, nullable=False, unique=True)
    login = Column(Text)
    language = Column(VARCHAR(4))
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    black_list = Column(Boolean, default=False)


class Teachers(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(Text)
    location = Column(Text)
    description = Column(Text)
    price = Column(Text)
    state = Column(Boolean, default=False)


# University Lessons Tables
class LessonsUniversity(Base):
    __tablename__ = 'lessons_university'

    id = Column(Integer, primary_key=True)
    id_university = Column(Integer, ForeignKey('universities.id'))
    code = Column(Text)
    name = Column(Text, nullable=False)


class TeachersLessonsUniversity(Base):
    __tablename__ = 'teachers.lessons_university'

    id = Column(Integer, primary_key=True)
    id_teacher = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    id_lesson = Column(Integer, ForeignKey('lessons_university.id'))


class Universities(Base):
    __tablename__ = 'universities'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    link_image = Column(Text)


# Language Lessons Tables
class LessonsLaguage(Base):
    __tablename__ = 'lessons_language'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)


class TeachersLessonsLanguage(Base):
    __tablename__ = 'teachers.lessons_language'

    id = Column(Integer, primary_key=True)
    id_teacher = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    id_lesson = Column(Integer, ForeignKey('lessons_language.id'))


# School Lessons Tables
class LessonsSchool(Base):
    __tablename__ = 'lessons_school'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


class TeachersLessonsSchool(Base):
    __tablename__ = 'teachers.lessons_school'

    id = Column(Integer, primary_key=True)
    id_teacher = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    id_lesson = Column(Integer, ForeignKey('lessons_school.id'))


# Admin Table
class Admins(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    id_tg = Column(BigInteger, nullable=False)
    state = Column(Boolean, default=True)