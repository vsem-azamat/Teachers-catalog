-- USERS
INSERT INTO "Users"(id, id_tg, login, start_time, language)
VALUES
    (10, 11111, 11111, current_timestamp, 'ru'),
    (20, 22222, 22222, current_timestamp, 'en'),
    (30, 33333, 33333, current_timestamp, 'cz'),
    (40, 44444, 44444, current_timestamp, 'ru'),
    (50, 55555, 55555, current_timestamp, 'en'),
    (60, 66666, 66666, current_timestamp, 'ru'),
    (70, 77777, NULL, current_timestamp, 'ru'),
    (80, 88888, NULL, current_timestamp, 'ru'),
    (90, 99999, NULL, current_timestamp, 'ru');

SELECT * FROM "Users";

-- TEACHERS
INSERT INTO "Teachers"(id, id_tg, name, description, location, price, state)
VALUES
    (10, 11111, 'Azamat', 'Занимаюсь подготовкой учеников к сдаче экзаменов, в том числе и международных. У меня много материалов и тестов для подготовки, а также различные интересные методы обучения.',
     'Praha, Skype', '100', TRUE),
    (20, 22222, 'Vanya', 'Я занимаюсь репетиторством уже более 5 лет и за это время помог многим ученикам достичь успеха в учебе. Я предлагаю индивидуальный подход и гибкий график занятий.',
     'Discord', '200', TRUE),
    (30, 33333, 'Sasha', 'Я выпускник лучшего ВУЗа страны и знаю, как достичь успеха в учебе. Мой подход основан на понимании материала и его применении на практике, что позволяет быстро и эффективно улучшить знания.',
     'Brno', '300', TRUE),
    (40, 44444, 'Anya', 'Я люблю свою работу и стараюсь подходить к каждому ученику индивидуально. У меня много интересных методик и материалов для обучения, которые помогут достичь успеха в учебе и жизни.',
     'OLOMOUC', '400', TRUE),
    (50, 55555, 'Katya', 'Я профессиональный репетитор с большим опытом работы. Владею различными методиками и стратегиями обучения, помогу с улучшением знаний и успехами в учебе.',
     'Praha', '500', False),
    (60, 66666, 'Azamat', 'Занимаюсь подготовкой учеников к сдаче экзаменов, в том числе и международных. У меня много материалов и тестов для подготовки, а также различные интересные методы обучения.',
     'Praha, Skype', '100', TRUE);


SELECT * FROM "Teachers";

-- LESSONS OF UNIVERSITY AND TEACHERS INSERTS
-- Universities
INSERT INTO "Universities"(name)
VALUES
    ('ČVUT'),
    ('UK'),
    ('VŠE'),
    ('ČZU'),
    ('VUT');

SELECT * FROM "Universities";

-- Lessons of University
INSERT INTO "LessonsUniversity"(id, code, name)
VALUES
    (10, '221023', 'Механика'),
    (20, NULL, 'DZO'),
    (30, '2A54D4', 'HUI'),
    (40, 'CODE', 'PPO'),
    (50, NULL, 'DML'),
    (60, '221025', 'Динамика'),
    (70, '221026', 'МатАнализ'),
    (80, '221027', 'Физика'),
    (90, '221028', 'Термомеханика'),
    (100, '221029', 'Математика'),
    (110, 'FY1', 'FY1');

SELECT * FROM "LessonsUniversity";

-- Connections of Lessons and Universities
INSERT INTO "Teachers_LessonsUniversity"(id_teacher, id_lesson)
VALUES
    (11111, 10),
    (11111, 60),
    (11111, 70),
    (11111, 90),
    (22222, 10),
    (33333, 10),
    (22222 ,20),
    (22222, 50),
    (44444, 10),
    (55555, 30);

SELECT * FROM "Teachers_LessonsUniversity";

-- Connections of Lessons and Universities
INSERT INTO "LessonsUniversity_Universities"(id_lesson_university, id_university)
VALUES
    (10, 1),
    (20, 2),
    (30, 1),
    (40, 3),
    (50, 1);

SELECT * FROM "LessonsUniversity_Universities";

-------------------------------------------

-- LESSONS OF LANGUAGE AND TEACHERS INSERTS
-- Lessons of Language
INSERT INTO "LessonsLanguage"
VALUES
    (10, 'English'),
    (20, 'Spain'),
    (30, 'German'),
    (40, 'Czech'),
    (50, 'Russian'),
    (60, 'Slovak'),
    (70, 'Test');

-- Connections of Lessons and Languages
INSERT INTO "Teachers_LessonsLanguage"(id_teacher, id_lesson)
VALUES
    (11111, 10),
    (11111, 60),
    (11111, 20),
    (11111, 30),
    (22222, 10),
    (33333, 10),
    (22222 ,20),
    (22222, 50),
    (44444, 10),
    (44444, 30);


-- CHATS
INSERT INTO "Chats"(name, link)
VALUES
    ('ČVUT',    't.me/cvut_chat'),
    ('VŠE',     't.me/vse_chat'),
    ('Karlov',  't.me/karlov_chat'),
    ('VŠCHT',   't.me/vscht_chat'),
    ('MUNI',    't.me/masaryk_chat'),
    ('VUT',     't.me/vut_chat'),
    ('ZČU',     't.me/zcu_chat')
;