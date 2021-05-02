DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS quiz;
DROP TABLE IF EXISTS quiz_result;

CREATE TABLE student (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);
CREATE TABLE quiz (
    quiz_id SERIAL PRIMARY KEY,
    subject VARCHAR(50) NOT NULL,
    num_questions SMALLINT NOT NULL,
    date_given DATE NOT NULL

);
CREATE TABLE quiz_result (
    student_id INTEGER REFERENCES student(student_id),
    quiz_id INTEGER REFERENCES quiz(quiz_id),
    score SMALLINT CHECK (0 <= score <= 100)
);

INSERT INTO student (first_name, last_name) VALUES ('John', 'Smith');
INSERT INTO quiz (subject, num_questions, date_given) VALUES ('Python Basics', 5, '2015-05-05');
INSERT INTO quiz_result (student_id, quiz_id, score) VALUES (1, 1, 85);