
CREATE OR REPLACE FUNCTION get_teachers_of_university_lesson(IDlesson INT)
    RETURNS TABLE (
        id INT, id_tg BIGINT, login TEXT, name TEXT, location TEXT, description TEXT, price TEXT, link TEXT, lessons TEXT
        ) AS
    $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT teachers.id, users.id_tg, users.login, teachers.name, teachers.location, teachers.description, teachers.price, teachers.location,
               string_agg(lessons_university.name, ', ') AS lessons
    FROM "teachers.lessons_university"
        JOIN teachers ON "teachers.lessons_university".id_teacher = teachers.id
        JOIN users ON teachers.id_user = users.id
        INNER JOIN lessons_university ON "teachers.lessons_university".id_lesson = lessons_university.id
    WHERE teachers.id IN (
        SELECT DISTINCT "teachers.lessons_university".id_teacher
        FROM "teachers.lessons_university"
        WHERE "teachers.lessons_university".id_lesson = IDlesson
    )
    GROUP BY teachers.id, users.id_tg, users.login, teachers.name, teachers.description, teachers.price, teachers.location;
END $$
LANGUAGE plpgsql;

-- DROP FUNCTION get_teachers_of_university_lesson(id_lesson INT);
SELECT * FROM get_teachers_of_university_lesson(10) OFFSET 0;

-----------------------------
CREATE OR REPLACE FUNCTION get_count_teachers_of_university_lesson(IDlesson INT)
    RETURNS INT AS $$
DECLARE
    count_rows INT;
BEGIN
    SELECT DISTINCT count(*) INTO count_rows
    FROM "teachers.lessons_university"
    WHERE "teachers.lessons_university".id_lesson = IDlesson;
    RETURN count_rows;
END $$
LANGUAGE plpgsql;

SELECT get_count_teachers_of_university_lesson(10);

---------------------------------

-- LANGUAGES
CREATE OR REPLACE FUNCTION get_teachers_of_language_lesson(IDlesson INT)
    RETURNS TABLE (
        id INT, id_tg BIGINT, login TEXT, name TEXT, location TEXT, description TEXT, price TEXT, link TEXT, lessons TEXT
        ) AS
    $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT teachers.id, users.id_tg, users.login, teachers.name, teachers.location, teachers.description, teachers.price, teachers.location,
               string_agg(lessons_language.name, ', ') AS lessons
    FROM "teachers.lessons_language"
        JOIN teachers ON "teachers.lessons_language".id_teacher = teachers.id
        JOIN users ON teachers.id_user = users.id
        INNER JOIN lessons_language ON "teachers.lessons_language".id_lesson = lessons_language.id
    WHERE teachers.id IN (
        SELECT DISTINCT "teachers.lessons_language".id_teacher
        FROM "teachers.lessons_language"
        WHERE "teachers.lessons_language".id_lesson = IDlesson
    )
    GROUP BY teachers.id, users.id_tg, users.login, teachers.name, teachers.description, teachers.price, teachers.location;
END $$
LANGUAGE plpgsql;

-- DROP FUNCTION get_teachers_of_language_lesson;
SELECT * FROM get_teachers_of_language_lesson(10);
----



---------------------------------

CREATE OR REPLACE FUNCTION get_count_teachers_of_language_lesson(IDlesson INT)
    RETURNS INT AS $$
DECLARE
    count INT;
BEGIN
    SELECT DISTINCT count(*) INTO count
    FROM "teachers.lessons_language"
    WHERE "teachers.lessons_language".id_lesson = IDlesson;
    RETURN count;
END $$
LANGUAGE plpgsql;

SELECT get_count_teachers_of_language_lesson(10);

---------------------------------------------
CREATE OR REPLACE FUNCTION get_all_lessons()
    RETURNS TABLE(
        id INT, name TEXT, code TEXT, link_image TEXT
                 ) AS
    $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT L.id, L.name, L.code, U.link_image
    FROM lessons_university AS L
        JOIN universities AS U ON L.id_university = U.id
    UNION
    SELECT L.id, L.name, NULL AS code, NULL AS link
    FROM lessons_school AS L;
END; $$
LANGUAGE plpgsql;

SELECT * FROM get_all_lessons();

---------------------------------------------

CREATE OR REPLACE FUNCTION get_teacher_profile(id_teacher INT)
    RETURNS TABLE (
        id INT, id_tg BIGINT, login TEXT, name TEXT, location TEXT, description TEXT, price TEXT, state BOOLEAN,
        lessons_university TEXT, lessons_language TEXT, lesson_school TEXT
        ) AS
    $$
BEGIN
    RETURN QUERY
    SELECT
        teachers.id, users.id_tg, users.login, teachers.name, teachers.location, teachers.description, teachers.price, teachers.state,
        (SELECT string_agg(lessons_university.name, ', ')
         FROM "teachers.lessons_university"
        JOIN lessons_university ON "teachers.lessons_university".id_lesson = lessons_university.id
         WHERE "teachers.lessons_university".id_teacher = teachers.id) AS lessons_university,
        (SELECT string_agg(lessons_language.name, ', ')
         FROM "teachers.lessons_language"
         JOIN lessons_language ON "teachers.lessons_language".id_lesson = lessons_language.id
         WHERE "teachers.lessons_language".id_teacher = teachers.id) AS lessons_language,
        (SELECT string_agg(lessons_school.name, ', ')
         FROM "teachers.lessons_school"
         JOIN lessons_school ON "teachers.lessons_school".id_lesson = lessons_school.id
         WHERE "teachers.lessons_school".id_teacher = teachers.id) AS lesson_school
    FROM teachers
    JOIN users ON teachers.id_user = users.id
    WHERE teachers.id = 10;
END $$
LANGUAGE plpgsql;

SELECT * FROM get_teacher_profile(10)