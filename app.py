from flask import Flask, make_response, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

SERVER_NAME = "localhost"
USERNAME = "root"
PASSWORD = "password"

def connectSql(database_name):
    return mysql.connector.connect(host=SERVER_NAME, user=USERNAME, password=PASSWORD, database=database_name)

def returnQueryResults(query, params=None):
    connection = connectSql("ourvle_clone")
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        retval = cursor.fetchall()
    except mysql.connector.Error as e:
        retval = make_response(f"Query Execution Error: {e}", 400)
    finally:
        cursor.close()
        connection.close()
    return retval

def executeQuery(query, params=None):
    connection = connectSql("ourvle_clone")
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        connection.commit()
        retval = {"success": "Operation successful"}
    except mysql.connector.Error as e:
        retval = {"error": f"Query Execution Error: {e}"}
    finally:
        cursor.close()
        connection.close()
    return make_response(jsonify(retval), 201 if 'success' in retval else 400)

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>OURVLE CLONE API</h1>"

# Register User
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  # 'admin', 'lecturer', or 'student'

    if not username or not password or not role:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    hashed_password = generate_password_hash(password)
    query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    params = (username, hashed_password, role)

    return executeQuery(query, params)

# User Login
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = "SELECT password FROM users WHERE username = %s"
    params = (username,)
    result = returnQueryResults(query, params)

    if not result:
        return make_response(jsonify({"error": "User not found"}), 404)

    stored_password = result[0][0]
    if check_password_hash(stored_password, password):
        return jsonify({"success": "Login successful"})
    else:
        return make_response(jsonify({"error": "Invalid credentials"}), 401)

# Create Course
@app.route('/courses', methods=['POST'])
def create_course():
    data = request.json
    course_name = data.get('course_name')
    admin_id = data.get('admin_id')  # Ensure only admins can create courses

    if not course_name or not admin_id:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = "INSERT INTO courses (course_name, admin_id) VALUES (%s, %s)"
    params = (course_name, admin_id)

    return executeQuery(query, params)

# Retrieve Courses
@app.route('/courses', methods=['GET'])
def retrieve_courses():
    query = "SELECT * FROM courses"
    courses = returnQueryResults(query)
    return jsonify(courses)

# Register for Course
@app.route('/courses/register', methods=['POST'])
def register_for_course():
    data = request.json
    course_id = data.get('course_id')
    user_id = data.get('user_id')

    if not course_id or not user_id:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = "INSERT INTO course_registrations (course_id, user_id) VALUES (%s, %s)"
    params = (course_id, user_id)

    return executeQuery(query, params)

# Retrieve Members of a Course
@app.route('/courses/<int:course_id>/members', methods=['GET'])
def get_course_members(course_id):
    try:
        query = """
        SELECT u.user_id, u.username, u.role
        FROM users u
        JOIN student_courses sc ON u.user_id = sc.student_id
        WHERE sc.course_id = %s
        """
        members = returnQueryResults(query, (course_id,))
        if not members:
            return jsonify({"message": "No members found for this course"}), 404
        return jsonify(members)
    except Exception as e:
        return make_response(f"Error: {e}", 500)

# Retrieve Calendar Events
@app.route('/courses/<int:course_id>/calendar', methods=['GET'])
def retrieve_calendar_events(course_id):
    query = "SELECT * FROM calendar_events WHERE course_id = %s"
    params = (course_id,)
    events = returnQueryResults(query, params)
    return jsonify(events)

# Create Calendar Event
@app.route('/courses/<int:course_id>/calendar', methods=['POST'])
def create_calendar_event(course_id):
    data = request.json
    event_name = data.get('event_name')
    event_date = data.get('event_date')

    if not event_name or not event_date:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = "INSERT INTO calendar_events (course_id, event_name, event_date) VALUES (%s, %s, %s)"
    params = (course_id, event_name, event_date)

    return executeQuery(query, params)

# Forums: Create and Retrieve
@app.route('/courses/<int:course_id>/forums', methods=['POST'])
def create_forum(course_id):
    data = request.json
    forum_title = data.get('forum_title')

    if not forum_title:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = "INSERT INTO forums (course_id, forum_title) VALUES (%s, %s)"
    params = (course_id, forum_title)

    return executeQuery(query, params)

@app.route('/courses/<int:course_id>/forums', methods=['GET'])
def retrieve_forums(course_id):
    query = "SELECT * FROM forums WHERE course_id = %s"
    params = (course_id,)
    forums = returnQueryResults(query, params)
    return jsonify(forums)

# Discussion Threads: Create and Retrieve
@app.route('/forums/<int:forum_id>/threads', methods=['POST'])
def create_thread(forum_id):
    data = request.json
    user_id = data.get('user_id')
    title = data.get('title')
    post = data.get('post')

    if not user_id or not title or not post:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = "INSERT INTO discussion_threads (forum_id, user_id, title, post) VALUES (%s, %s, %s, %s)"
    params = (forum_id, user_id, title, post)

    return executeQuery(query, params)

@app.route('/forums/<int:forum_id>/threads', methods=['GET'])
def retrieve_threads(forum_id):
    query = "SELECT * FROM discussion_threads WHERE forum_id = %s"
    params = (forum_id,)
    threads = returnQueryResults(query, params)
    return jsonify(threads)

# Replies to Threads
@app.route('/threads/<int:thread_id>/replies', methods=['POST'])
def reply_to_thread(thread_id):
    data = request.json
    user_id = data.get('user_id')
    post = data.get('post')

    if not user_id or not post:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = "INSERT INTO discussion_threads (forum_id, user_id, post, parent_thread_id) VALUES ((SELECT forum_id FROM discussion_threads WHERE thread_id = %s), %s, %s, %s)"
    params = (thread_id, user_id, post, thread_id)

    return executeQuery(query, params)

# Course Content: Add and Retrieve
@app.route('/courses/<int:course_id>/content', methods=['POST'])
def add_course_content(course_id):
    data = request.json
    section = data.get('section')
    content_title = data.get('content_title')
    content_link = data.get('content_link')
    content_file_path = data.get('content_file_path')

    if not content_title or not section:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = "INSERT INTO course_content (course_id, section, content_title, content_link, content_file_path) VALUES (%s, %s, %s, %s, %s)"
    params = (course_id, section, content_title, content_link, content_file_path)

    return executeQuery(query, params)

@app.route('/courses/<int:course_id>/content', methods=['GET'])
def retrieve_course_content(course_id):
    query = "SELECT * FROM course_content WHERE course_id = %s"
    params = (course_id,)
    content = returnQueryResults(query, params)
    return jsonify(content)

# Assignments: Create, Submit, and Grade
@app.route('/courses/<int:course_id>/assignments', methods=['POST'])
def create_assignment(course_id):
    data = request.json
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')

    if not title or not due_date:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = "INSERT INTO assignments (course_id, title, description, due_date) VALUES (%s, %s, %s, %s)"
    params = (course_id, title, description, due_date)

    return executeQuery(query, params)

@app.route('/assignments/<int:assignment_id>/submit', methods=['POST'])
def submit_assignment(assignment_id):
    data = request.json
    student_id = data.get('student_id')
    file_path = data.get('file_path')

    if not student_id or not file_path:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = "INSERT INTO assignment_submissions (assignment_id, student_id, file_path) VALUES (%s, %s, %s)"
    params = (assignment_id, student_id, file_path)

    return executeQuery(query, params)

@app.route('/assignments/<int:assignment_id>/grade', methods=['POST'])
def grade_assignment(assignment_id):
    data = request.json
    submission_id = data.get('submission_id')
    grade = data.get('grade')

    if not submission_id or grade is None:
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    query = "UPDATE assignment_submissions SET grade = %s WHERE submission_id = %s"
    params = (grade, submission_id)

    return executeQuery(query, params)


@app.route('/reports/courses/50plus', methods=['GET'])
def courses_with_50_plus_students():
    query = "SELECT * FROM courses_with_50_plus_students"
    results = returnQueryResults(query)
    return jsonify(results)

@app.route('/reports/students/5plus', methods=['GET'])
def students_with_5_plus_courses():
    query = "SELECT * FROM students_with_5_plus_courses"
    results = returnQueryResults(query)
    return jsonify(results)

@app.route('/reports/lecturers/3plus', methods=['GET'])
def lecturers_with_3_plus_courses():
    query = "SELECT * FROM lecturers_with_3_plus_courses"
    results = returnQueryResults(query)
    return jsonify(results)

@app.route('/reports/courses/top10', methods=['GET'])
def top_10_most_enrolled_courses():
    query = "SELECT * FROM top_10_most_enrolled_courses"
    results = returnQueryResults(query)
    return jsonify(results)

@app.route('/reports/students/top10', methods=['GET'])
def top_10_students_with_highest_averages():
    query = "SELECT * FROM top_10_students_with_highest_averages"
    results = returnQueryResults(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=8000, debug=True)