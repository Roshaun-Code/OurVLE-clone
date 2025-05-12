-- Insert 50 lecturers
INSERT INTO users (username, password, role)
SELECT 
    CONCAT('lecturer_', seq) AS username,
    CONCAT('password', seq) AS password,
    'lecturer' AS role
FROM (
    SELECT @row := @row + 1 AS seq
    FROM (SELECT 0 UNION ALL SELECT 0) t1, (SELECT 0 UNION ALL SELECT 0) t2,
         (SELECT @row := 0) t3
    LIMIT 50
) seq_table;

-- Insert 200 courses, each assigned to a random lecturer
INSERT INTO courses (course_name, lecturer_id)
SELECT 
    CONCAT('Course ', seq) AS course_name,
    FLOOR(1 + (RAND() * 50)) AS lecturer_id  -- Random lecturer ID between 1 and 50
FROM (
    SELECT @row := @row + 1 AS seq
    FROM (SELECT 0 UNION ALL SELECT 0) t1, (SELECT 0 UNION ALL SELECT 0) t2,
         (SELECT @row := 0) t3
    LIMIT 200
) seq_table;

-- Enroll each student in 3 random courses
INSERT INTO student_courses (student_id, course_id)
SELECT 
    student_id,
    FLOOR(1 + (RAND() * 200)) AS course_id  -- Random course ID between 1 and 200
FROM (
    SELECT user_id AS student_id
    FROM users
    WHERE role = 'student'
) students
CROSS JOIN (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) AS three_courses;

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
INSERT INTO discussion_threads (forum_id, user_id, title, post)
SELECT 
    forum_id,
    FLOOR(1 + (RAND() * 100000)) AS user_id,  -- Random student ID
    CONCAT('Thread Title ', seq) AS title,
    CONCAT('This is the content of thread ', seq) AS post
FROM forums
CROSS JOIN (
    SELECT @row := @row + 1 AS seq
    FROM (SELECT 0 UNION ALL SELECT 0) t1, (SELECT 0 UNION ALL SELECT 0) t2,
         (SELECT @row := 0) t3
    LIMIT 10  -- 10 threads per forum
) seq_table;

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
    FLOOR(1 + (RAND() * 100000)) AS student_id,  -- Random student ID
    CONCAT('/path/to/submission_', assignment_id, '_', student_id, '.pdf') AS file_path,
    FLOOR(50 + (RAND() * 50)) AS grade  -- Random grade between 50 and 100
FROM assignments
CROSS JOIN (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) submissions;