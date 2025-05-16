-- Insert 100,000 students
SET @row = 0;
INSERT INTO users (username, password, role)
SELECT 
    CONCAT('student_', @row := @row + 1) AS username,
    CONCAT('password', @row) AS password,
    'student' AS role
FROM (
    SELECT 0 UNION ALL SELECT 0 UNION ALL SELECT 0 UNION ALL SELECT 0 UNION ALL SELECT 0
) t1, (SELECT 0 UNION ALL SELECT 0 UNION ALL SELECT 0 UNION ALL SELECT 0 UNION ALL SELECT 0) t2;

-- Insert 50 lecturers
SET @row = 0;
INSERT INTO users (username, password, role)
SELECT 
    CONCAT('lecturer_', @row := @row + 1) AS username,
    CONCAT('password', @row) AS password,
    'lecturer' AS role
FROM (
    SELECT 0 UNION ALL SELECT 0 UNION ALL SELECT 0 UNION ALL SELECT 0 UNION ALL SELECT 0
) t1;

-- Insert 200 courses, each assigned to a random lecturer
SET @row = 0;
INSERT INTO courses (course_name, lecturer_id)
SELECT 
    CONCAT('Course ', @row := @row + 1) AS course_name,
    lecturer_id
FROM (
    SELECT 
        user_id AS lecturer_id,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY RAND()) AS course_count
    FROM users
    WHERE role = 'lecturer'
) lecturers
WHERE course_count <= 5;

-- Ensure each lecturer teaches at least 1 course
INSERT INTO courses (course_name, lecturer_id)
SELECT 
    CONCAT('Mandatory Course for Lecturer ', lecturer_id) AS course_name,
    lecturer_id
FROM (
    SELECT user_id AS lecturer_id
    FROM users
    WHERE role = 'lecturer'
) lecturers
WHERE lecturer_id NOT IN (
    SELECT DISTINCT lecturer_id
    FROM courses
);

-- Enroll each student in 3 to 6 random courses
SET @row = 0;
INSERT INTO student_courses (student_id, course_id)
SELECT 
    student_id,
    course_id
FROM (
    SELECT 
        student_id,
        course_id,
        ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY RAND()) AS course_count
    FROM (
        SELECT 
            user_id AS student_id,
            FLOOR(1 + (RAND() * 200)) AS course_id
        FROM users
        WHERE role = 'student'
    ) random_courses
) limited_courses
WHERE course_count BETWEEN 3 AND 6;

-- Ensure each course has at least 10 members
INSERT INTO student_courses (student_id, course_id)
SELECT 
    student_id,
    course_id
FROM (
    SELECT 
        user_id AS student_id,
        course_id
    FROM users
    CROSS JOIN (
        SELECT course_id
        FROM courses
    ) all_courses
    WHERE role = 'student'
    LIMIT 10
) course_members;

-- Insert 4 events per course
INSERT INTO calendar_events (course_id, event_title, event_description, event_date)
SELECT 
    course_id,
    CONCAT('Week ', week, ' Event') AS event_title,
    CONCAT('Description for Week ', week, ' Event in Course ', course_id) AS event_description,
    DATE_ADD('2025-05-01', INTERVAL FLOOR(RAND() * 28) DAY) AS event_date
FROM (
    SELECT course_id, week
    FROM courses
    CROSS JOIN (SELECT 1 AS week UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4) weeks
) course_weeks;

-- Insert forums for each course
INSERT INTO forums (course_id, forum_title)
SELECT 
    course_id,
    CONCAT('Forum for Course ', course_id) AS forum_title
FROM courses;

-- Insert threads for each forum
SET @row = 0;
INSERT INTO discussion_threads (forum_id, user_id, title, post)
SELECT 
    forum_id,
    user_id,  -- Select valid user_id from the users table
    CONCAT('Thread Title ', @row := @row + 1) AS title,
    CONCAT('This is the content of thread ', @row) AS post
FROM forums
CROSS JOIN (
    SELECT user_id
    FROM users
    WHERE role = 'student'
    ORDER BY RAND()
    LIMIT 1
) valid_users;

-- Insert course content for each course
INSERT INTO course_content (course_id, section, content_title, content_link, content_file_path)
SELECT 
    course_id,
    CONCAT('Section ', section) AS section,
    CONCAT('Content Title ', section) AS content_title,
    CONCAT('http://example.com/content_', section) AS content_link,
    NULL AS content_file_path
FROM courses
CROSS JOIN (SELECT 1 AS section UNION ALL SELECT 2 UNION ALL SELECT 3) sections;

-- Insert assignments for each course
INSERT INTO assignments (course_id, title, description, due_date)
SELECT 
    course_id,
    CONCAT('Assignment for Course ', course_id) AS title,
    CONCAT('Description for Assignment in Course ', course_id) AS description,
    DATE_ADD('2025-05-01', INTERVAL FLOOR(RAND() * 28) DAY) AS due_date
FROM courses;

-- Insert assignment submissions for each assignment
INSERT INTO assignment_submissions (assignment_id, student_id, file_path, grade)
SELECT 
    assignment_id,
    user_id AS student_id,
    CONCAT('/path/to/submission_', assignment_id, '_', user_id, '.pdf') AS file_path,
    FLOOR(50 + (RAND() * 50)) AS grade
FROM assignments
CROSS JOIN users
WHERE users.role = 'student';