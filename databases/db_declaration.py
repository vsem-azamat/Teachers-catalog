from sqlalchemy import Table, Boolean, DateTime, \
    Column, ForeignKey,\
    Integer, BigInteger,\
    Text, VARCHAR 
    
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()


class Logs(Base):
    __tablename__ = 'Logs'
    id = Column(Integer, primary_key=True)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    
class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    id_tg = Column(BigInteger, nullable=False, unique=True)
    login = Column(Text)
    language = Column(VARCHAR(4))
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    black_list = Column(Boolean, default=False)


# Association Tables
Teachers_LessonsLanguage = Table(
    "Teachers_LessonsLanguage",
    Base.metadata,
    Column('id_teacher', BigInteger, ForeignKey('Teachers.id_tg'), nullable=False),
    Column('id_lesson', Integer, ForeignKey('LessonsLanguage.id')),
)


Teachers_LessonsUniversity = Table(
    "Teachers_LessonsUniversity",
    Base.metadata,
    Column('id_teacher', BigInteger, ForeignKey('Teachers.id_tg'), nullable=False),
    Column('id_lesson', Integer, ForeignKey('LessonsUniversity.id')),
)


LessonsUniversity_Universities = Table(
    "LessonsUniversity_Universities",
    Base.metadata,
    Column('id_lesson_university', Integer, ForeignKey('LessonsUniversity.id')),
    Column('id_university', Integer, ForeignKey('Universities.id')),
)


class Teachers(Base):
    __tablename__ = 'Teachers'

    id = Column(Integer, primary_key=True)
    id_tg = Column(BigInteger, ForeignKey('Users.id_tg'), nullable=False, unique=True)
    name = Column(Text)
    location = Column(Text)
    description = Column(Text)
    price = Column(Text)
    state = Column(Boolean, default=False)
    state_admin = Column(Boolean, default=True)
    
    lesson_university = relationship('LessonsUniversity', secondary=Teachers_LessonsUniversity, back_populates="teacher")
    lesson_language = relationship('LessonsLanguage', secondary=Teachers_LessonsLanguage, back_populates="teacher")


# University Lessons Tables
class LessonsUniversity(Base):
    __tablename__ = 'LessonsUniversity'

    id = Column(Integer, primary_key=True)
    code = Column(Text)
    name = Column(Text, nullable=False)

    teacher = relationship('Teachers', secondary=Teachers_LessonsUniversity, back_populates='lesson_university')
    university = relationship('Universities', secondary=LessonsUniversity_Universities, back_populates='lesson_university')


class Universities(Base):
    __tablename__ = 'Universities'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    link_image = Column(Text)

    lesson_university = relationship('LessonsUniversity', secondary=LessonsUniversity_Universities, back_populates='university')


# Language Lessons Tables
class LessonsLanguage(Base):
    __tablename__ = 'LessonsLanguage'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)

    teacher = relationship('Teachers', secondary=Teachers_LessonsLanguage, back_populates='lesson_language')


# Admin Table
class Admins(Base):
    __tablename__ = 'Admins'

    id = Column(Integer, primary_key=True)
    id_tg = Column(BigInteger, nullable=False)
    state = Column(Boolean, default=True)


class Chats(Base):
    __tablename__ = 'Chats'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    link = Column(Text)
