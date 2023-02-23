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
    id_tg = Column(BigInteger, nullable=False)
    login = Column(Text)
    lang = Column(VARCHAR(4))
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    black_list = Column(Boolean, default=False)


class Teachers(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(Text, nullable=False)
    description_univ = Column(Text)
    description_nostr = Column(Text)
    link = Column(Text)
    price = Column(Text)


class TeachersLessonsUniv(Base):
    __tablename__ = 'teachers.lessons_univ'

    id = Column(Integer, primary_key=True)
    id_teachers = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    id_lessons = Column(Integer, ForeignKey('lessons_univ.id'), nullable=False)


class TeachersLessonsNostr(Base):
    __tablename__ = 'teachers.lessons_nostr'

    id = Column(Integer, primary_key=True)
    id_teachers = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    id_lessons = Column(Integer, ForeignKey('lessons_school.id'), nullable=False)


class LessonsSchool(Base):
    __tablename__ = 'lessons_school'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


class LessonsUniv(Base):
    __tablename__ = 'lessons_univ'

    id = Column(Integer, primary_key=True)
    id_univ = Column(Integer, ForeignKey('universities.id'))
    code = Column(Text)
    name = Column(Text, nullable=False)


class Universities(Base):
    __tablename__ = 'universities'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    link_image = Column(Text)


class Admins(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    id_tg = Column(BigInteger, nullable=False)
    state = Column(Boolean, default=True)  # global state of admin
