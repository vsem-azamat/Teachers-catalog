CREATE OR REPLACE FUNCTION get_lesson_univ_teachers(id_lesson INT)
    RETURNS TABLE(id_tg BIGINT, login TEXT, name TEXT, description_univ TEXT, price TEXT, link TEXT) AS
    $$
BEGIN
    RETURN QUERY
    SELECT users.id_tg, users.login, teachers.name, teachers.description_univ, teachers.price, teachers.link
    FROM teachers
        INNER JOIN users ON teachers.id_user = users.id
        INNER JOIN "teachers.lessons_univ" ON "teachers.lessons_univ".id_teachers = teachers.id
    WHERE "teachers.lessons_univ".id_lessons = id_lesson;
END $$
LANGUAGE plpgsql;

SELECT * FROM get_lesson_univ_teachers(10);

-----------------------

CREATE OR REPLACE FUNCTION get_teachers_univ_profiles(id_lesson INT)
    RETURNS TABLE (
        id INT, id_tg BIGINT, login TEXT, name TEXT, description_univ TEXT, price TEXT, link TEXT, lessons TEXT
        ) AS
    $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT teachers.id, users.id_tg, users.login, teachers.name, teachers.description_univ, teachers.price, teachers.link,
               string_agg(lessons_univ.name, ', ') AS lessons
    FROM "teachers.lessons_univ"
        JOIN teachers ON "teachers.lessons_univ".id_teachers = teachers.id
        JOIN users ON teachers.id_user = users.id
        INNER JOIN lessons_univ ON "teachers.lessons_univ".id_lessons = lessons_univ.id
    WHERE teachers.id IN (
        SELECT DISTINCT "teachers.lessons_univ".id_teachers
        FROM "teachers.lessons_univ"
        WHERE "teachers.lessons_univ".id_lessons = id_lesson
    )
    GROUP BY teachers.id, users.id_tg, users.login, teachers.name, teachers.description_univ, teachers.price, teachers.link;
END $$
LANGUAGE plpgsql;

SELECT * FROM get_teachers_univ_profiles(10) OFFSET 0;

-----------------------------
CREATE OR REPLACE FUNCTION get_teachers_univ_profiles_count(id_lesson INT)
    RETURNS INT AS $$
DECLARE
    count_rows INT;
BEGIN
    SELECT DISTINCT count(*) INTO count_rows
    FROM "teachers.lessons_univ"
    WHERE "teachers.lessons_univ".id_lessons = id_lesson;
    RETURN count_rows;
END $$
LANGUAGE plpgsql;

SELECT get_teachers_univ_profiles_count(10);

SELECT * FROM lessons_univ OFFSET 0 + 3*2;

SELECT get_teachers_univ_profiles_count(10)