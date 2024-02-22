import pytest
from bot.databases.db_postgresql import db, SqlAlchemy


@pytest.fixture
def db_conn():
    db.connect()
    yield db
    db.close()


@pytest.mark.asyncio
async def test_get_teachers_of_university_lesson(db_conn: SqlAlchemy):
    lesson_id = 10
    teachers_available = await db_conn.get_teachers_of_university_lesson(lesson_id, exclude_null_teachers=True)

    teachers_avaible_ids = set()
    for teacher in teachers_available:
        teachers_avaible_ids.add(teacher.id_tg)
        assert teacher.state is True, f'Teacher {teacher.id_tg} is not available: state is False'
        assert teacher.state_admin is not False, f'Teacher {teacher.id_tg} is not available: state_admin is False'
        assert teacher.user.login is not None, f'Teacher {teacher.id_tg} is not available: user.login is None'    

        assert teacher.lesson_university, f'Teacher {teacher.id_tg} is not available: lesson_language is None'


@pytest.mark.asyncio
async def test_get_teachers_of_language_lesson(db_conn: SqlAlchemy):
    language_id = 10
    teachers_avaible = await db_conn.get_teachers_of_language_lesson(language_id, exclude_null_teachers=True)
    for teacher in teachers_avaible:
        assert teacher.state is True, f'Teacher {teacher.id_tg} is not available: state is False'
        assert teacher.state_admin is not False, f'Teacher {teacher.id_tg} is not available: state_admin is False'
        assert teacher.user.login is not None, f'Teacher {teacher.id_tg} is not available: user.login is None'
        assert teacher.lesson_language, f'Teacher {teacher.id_tg} is not available: lesson_language is None'


@pytest.mark.asyncio
async def test_get_aviable_lessons_languages(db_conn: SqlAlchemy):
    lessons = await db_conn.get_lessons_of_languages(exclude_null_teachers=True)
    for lesson in lessons:
        for teacher in lesson.teacher:
            assert \
                teacher.state is True and \
                teacher.state_admin is not False and \
                teacher.user.login is not None and \
                teacher.lesson_language, \
                f'Teacher {teacher.id_tg} is not available: state is False, state_admin is False, user.login is None, lesson_language is None'


