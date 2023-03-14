
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
CREATE OR REPLACE FUNCTION get_all_lessons(exclude_null_teachers BOOLEAN DEFAULT FALSE)
RETURNS TABLE(
    id INT, name TEXT, code TEXT, link_image TEXT, id_university INT, name_university TEXT, source TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT L.id, L.name, L.code, U.link_image, L.id_university, U.name AS name_university, 'university' AS source
    FROM lessons_university AS L
        LEFT JOIN universities AS U ON L.id_university = U.id
        LEFT JOIN "teachers.lessons_university" AS tlu ON L.id = tlu.id_lesson
    WHERE NOT exclude_null_teachers OR tlu.id_teacher IS NOT NULL

    UNION

    SELECT L.id, L.name, NULL AS code, NULL AS link_image, NULL AS id_university, NULL AS name_university, 'language' AS source
    FROM lessons_language AS L
        LEFT JOIN "teachers.lessons_language" AS tlu ON L.id = tlu.id_lesson
    WHERE NOT exclude_null_teachers OR tlu.id_teacher IS NOT NULL

    ORDER BY source DESC, id_university DESC;
END $$
LANGUAGE plpgsql;

-- DROP FUNCTION get_all_lessons();
SELECT * FROM get_all_lessons(TRUE);

---------------------------------------------

---------------------------------------------
CREATE OR REPLACE FUNCTION get_count_all_lessons(exclude_null_teachers BOOLEAN DEFAULT FALSE)
    RETURNS INTEGER AS
$$
DECLARE
    count INTEGER = 0;
    result INTEGER = 0;
BEGIN
    SELECT COUNT(DISTINCT lessons_university.name) INTO count FROM lessons_university
        LEFT JOIN "teachers.lessons_university" ON "teachers.lessons_university".id_lesson = lessons_university.id
    WHERE not exclude_null_teachers or "teachers.lessons_university".id_teacher IS NOT NULL;

    result = result + count;

    SELECT count(DISTINCT lessons_language.name) INTO count FROM lessons_language
        LEFT JOIN "teachers.lessons_language" on "teachers.lessons_language".id_lesson = lessons_language.id
    WHERE not exclude_null_teachers or "teachers.lessons_language".id_teacher IS NOT NULL;

    result = result + count;
    RETURN result;
END;
$$
LANGUAGE plpgsql;

SELECT get_count_all_lessons(True);
---------------------------------------------



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
    WHERE teachers.id = id_teacher;
END $$
LANGUAGE plpgsql;

--------------------

