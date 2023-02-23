-- USERS
INSERT INTO users(id, id_tg, start_time, lang)
VALUES
    (10, 11111, current_timestamp, 'ru'),
    (20, 22222, current_timestamp, 'en'),
    (30, 33333, current_timestamp, 'cz'),
    (40, 44444, current_timestamp, 'ru'),
    (50, 55555, current_timestamp, 'en');
SELECT * FROM users;

-- TEACHERS
INSERT INTO teachers(id, id_user, name, description_univ, description_nostr, link, price)
VALUES
    (10, 10, 'Azamat', 'descr univ', 'descr nostr', 'link', '100'),
    (20, 20, 'Vanya', 'descr univ', 'descr nostr', 'link', '200'),
    (30, 30, 'Sasha', 'descr univ', 'descr nostr', 'link', '300'),
    (40, 40, 'Anya', 'descr univ', 'descr nostr', 'link', '400'),
    (50, 50, 'Katya', 'descr univ', 'descr nostr', 'link', '500');

SELECT * FROM teachers;

-- Universities
INSERT INTO universities(id, name)
VALUES
    (10, 'ČVUT'),
    (20, 'UK'),
    (30, 'VŠE'),
    (40, 'ČZU'),
    (50, 'VUT');

SELECT * FROM universities;

-- Lessons of Universities
INSERT INTO lessons_univ(id, id_univ, code, name)
VALUES
    (10, 10, '221023', 'ME2'),
    (20, 20, NULL, 'DZO'),
    (30, 30, '2A54D4', 'HUI'),
    (40, 40, 'CODE', 'PPO'),
    (50, 50, NULL, 'DML'),
    (60, 10, '221025', 'ME1'),
    (70, 10, '221026', 'PP1'),
    (80, 10, '221027', 'FY1'),
    (90, 10, '221028', 'TM');

SELECT * FROM lessons_univ;

-- Lessons of Applicants
INSERT INTO lessons_school(id, name)
VALUES
    (10, 'mathematics'),
    (20, 'history'),
    (20, 'informatics'),
    (30, 'english'),
    (40, 'geography'),
    (50, 'biology');

SELECT * FROM lessons_school;

--
INSERT INTO "teachers.lessons_univ"(id, id_teachers, id_lessons)
VALUES
    (10, 10, 10),
    (20, 10, 60),
    (30, 10, 70),
    (40, 10, 90),
    (50, 20, 10),
    (60, 30, 10),
    (70, 20 ,20),
    (80, 20, 50),
    (90, 40, 10),
    (100, 50, 30);


SELECT * FROM "teachers.lessons_univ";
-- DELETE FROM "teachers.lessons_univ" WHERE id!=0;