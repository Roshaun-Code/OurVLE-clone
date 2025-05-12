-- USERS TABLE
CREATE TABLE users (
    user_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'lecturer', 'student') NOT NULL
);

-- COURSES TABLE
CREATE TABLE courses (
    course_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    lecturer_id BIGINT UNSIGNED UNIQUE,
    FOREIGN KEY (lecturer_id) REFERENCES users(user_id)
);

-- STUDENT COURSE REGISTRATION TABLE
CREATE TABLE student_courses (
    student_id BIGINT UNSIGNED,
    course_id BIGINT UNSIGNED,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- CALENDAR EVENTS TABLE
CREATE TABLE calendar_events (
    event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_id BIGINT UNSIGNED,
    event_title VARCHAR(255),
    event_description TEXT,
    event_date DATE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- FORUMS TABLE
CREATE TABLE forums (
    forum_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_id BIGINT UNSIGNED,
    forum_title VARCHAR(255) NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- DISCUSSION THREADS TABLE
CREATE TABLE discussion_threads (
    thread_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    forum_id BIGINT UNSIGNED,
    user_id BIGINT UNSIGNED,
    title VARCHAR(255),
    post TEXT,
    parent_thread_id BIGINT UNSIGNED, -- for replies
    FOREIGN KEY (forum_id) REFERENCES forums(forum_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_thread_id) REFERENCES discussion_threads(thread_id)
);

-- COURSE CONTENT TABLE
CREATE TABLE course_content (
    content_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_id BIGINT UNSIGNED,
    section VARCHAR(255),
    content_title VARCHAR(255),
    content_link TEXT,
    content_file_path TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- ASSIGNMENTS TABLE
CREATE TABLE assignments (
    assignment_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_id BIGINT UNSIGNED,
    title VARCHAR(255),
    description TEXT,
    due_date DATE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- STUDENT ASSIGNMENT SUBMISSIONS TABLE
CREATE TABLE assignment_submissions (
    submission_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    assignment_id BIGINT UNSIGNED,
    student_id BIGINT UNSIGNED,
    file_path TEXT,
    grade DECIMAL(5,2), -- decimal grade
    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id),
    FOREIGN KEY (student_id) REFERENCES users(user_id)
);