-- COURSES WITH 50 OR MORE STUDENTS
CREATE VIEW courses_with_50_plus_students AS
SELECT c.course_id, c.course_name, COUNT(sc.student_id) AS student_count
FROM courses c
JOIN student_courses sc ON c.course_id = sc.course_id
GROUP BY c.course_id, c.course_name
HAVING COUNT(sc.student_id) >= 50;

-- STUDENTS TAKING 5 OR MORE COURSES
CREATE VIEW students_with_5_plus_courses AS
SELECT u.user_id, u.username, COUNT(sc.course_id) AS course_count
FROM users u
JOIN student_courses sc ON u.user_id = sc.student_id
WHERE u.role = 'student'
GROUP BY u.user_id, u.username
HAVING COUNT(sc.course_id) >= 5;

-- LECTURERS TEACHING 3 OR MORE COURSES
CREATE VIEW lecturers_with_3_plus_courses AS
SELECT u.user_id, u.username, COUNT(c.course_id) AS course_count
FROM users u
JOIN courses c ON u.user_id = c.lecturer_id
WHERE u.role = 'lecturer'
GROUP BY u.user_id, u.username
HAVING COUNT(c.course_id) >= 3;

-- 10 MOST ENROLLED COURSES
CREATE VIEW top_10_most_enrolled_courses AS
SELECT c.course_id, c.course_name, COUNT(sc.student_id) AS student_count
FROM courses c
JOIN student_courses sc ON c.course_id = sc.course_id
GROUP BY c.course_id, c.course_name
ORDER BY student_count DESC
LIMIT 10;

-- TOP 10 STUDENTS WITH HIGHEST OVERALL AVERAGES
CREATE VIEW top_10_students_highest_averages AS
SELECT u.user_id, u.username, AVG(a.grade) AS average_grade
FROM users u
JOIN assignment_submissions a ON u.user_id = a.student_id
WHERE u.role = 'student'
GROUP BY u.user_id, u.username
ORDER BY average_grade DESC
LIMIT 10;
