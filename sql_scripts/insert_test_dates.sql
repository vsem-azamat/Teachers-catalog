-- USERS
INSERT INTO users(id, id_tg, start_time, language)
VALUES
    (10, 11111, current_timestamp, 'ru'),
    (20, 22222, current_timestamp, 'en'),
    (30, 33333, current_timestamp, 'cz'),
    (40, 44444, current_timestamp, 'ru'),
    (50, 55555, current_timestamp, 'en'),
    (60, 66666, current_timestamp, 'ru'),
    (70, 77777, current_timestamp, 'ru'),
    (80, 88888, current_timestamp, 'ru'),
    (90, 99999, current_timestamp, 'ru');

SELECT * FROM users;

-- TEACHERS
INSERT INTO teachers(id, id_user, name, description, location, price, state)
VALUES
    (10, 10, 'Azamat', 'Занимаюсь подготовкой учеников к сдаче экзаменов, в том числе и международных. У меня много материалов и тестов для подготовки, а также различные интересные методы обучения.',
     'Praha, Skype', '100', TRUE),
    (20, 20, 'Vanya', 'Я занимаюсь репетиторством уже более 5 лет и за это время помог многим ученикам достичь успеха в учебе. Я предлагаю индивидуальный подход и гибкий график занятий.',
     'Discord', '200', TRUE),
    (30, 30, 'Sasha', 'Я выпускник лучшего ВУЗа страны и знаю, как достичь успеха в учебе. Мой подход основан на понимании материала и его применении на практике, что позволяет быстро и эффективно улучшить знания.',
     'Brno', '300', TRUE),
    (40, 40, 'Anya', 'Я люблю свою работу и стараюсь подходить к каждому ученику индивидуально. У меня много интересных методик и материалов для обучения, которые помогут достичь успеха в учебе и жизни.',
     'OLOMOUC', '400', TRUE),
    (50, 50, 'Katya', 'Я профессиональный репетитор с большим опытом работы. Владею различными методиками и стратегиями обучения, помогу с улучшением знаний и успехами в учебе.',
     'Praha', '500', TRUE);

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
INSERT INTO lessons_university(id, id_university, code, name)
VALUES
    (10, 10, '221023', 'Механика'),
    (20, 20, NULL, 'DZO'),
    (30, 30, '2A54D4', 'HUI'),
    (40, 40, 'CODE', 'PPO'),
    (50, 50, NULL, 'DML'),
    (60, 10, '221025', 'Динамика'),
    (70, 10, '221026', 'МатАнализ'),
    (80, 10, '221027', 'Физика'),
    (90, 10, '221028', 'Термомеханика');

SELECT * FROM lessons_university;

-- Lessons of Applicants
INSERT INTO lessons_school(id, name)
VALUES
    (10, 'mathematics'),
    (20, 'history'),
    (30, 'informatics'),
    (40, 'english'),
    (50, 'geography'),
    (60, 'biology');

SELECT * FROM lessons_school;

--
INSERT INTO "teachers.lessons_university"(id, id_teacher, id_lesson)
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

SELECT * FROM "teachers.lessons_university";
-- DELETE FROM "teachers.lessons_univ" WHERE id!=0;
---------------------------

-- Lessons of Languages
INSERT INTO lessons_language
VALUES
    (10, 'English'),
    (20, 'Spain'),
    (30, 'German'),
    (40, 'Czech'),
    (50, 'Russian'),
    (60, 'Slovak');
--
INSERT INTO "teachers.lessons_language"(id, id_teacher, id_lesson)
VALUES
    (10, 10, 10),
    (20, 10, 60),
    (30, 10, 20),
    (40, 10, 30),
    (50, 20, 10),
    (60, 30, 10),
    (70, 20 ,20),
    (80, 20, 50),
    (90, 40, 10),
    (100, 50, 30);


-- Lessons of School

INSERT INTO chats(name, link)
VALUES
    ('ČVUT',    't.me/cvut_chat'),
    ('VŠE',     't.me/vse_chat'),
    ('Karlov',  't.me/karlov_chat'),
    ('VŠCHT',   't.me/vscht_chat'),
    ('MUNI',    't.me/masaryk_chat'),
    ('VUT',     't.me/vut_chat'),
    ('ZČU',     't.me/zcu_chat')
;