import random
import mysql.connector
from mysql.connector import Error

# Database connection
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ourvle_clone"
        )
        if connection.is_connected():
            print("Connected to the database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Generate and insert users
def generate_users(connection):
    cursor = connection.cursor()
    # Insert students
    for i in range(1, 100001):
        username = f"student_{i}"
        password = f"password{i}"
        role = "student"
        cursor.execute("INSERT IGNORE INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    
    # Insert lecturers
    for i in range(1, 51):
        username = f"lecturer_{i}"
        password = f"password{i}"
        role = "lecturer"
        cursor.execute("INSERT IGNORE INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    
    # Insert admins
    for i in range(1, 6):
        username = f"admin_{i}"
        password = f"password{i}"
        role = "admin"
        cursor.execute("INSERT IGNORE INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    
    connection.commit()
    print("Users inserted successfully")

# Generate and insert courses
def generate_courses(connection):
    cursor = connection.cursor()
    # Ensure lecturers exist before assigning them to courses
    cursor.execute("SELECT user_id FROM users WHERE role = 'lecturer'")
    lecturer_ids = [row[0] for row in cursor.fetchall()]
    
    # Ensure each lecturer is assigned to only one course
    for i, lecturer_id in enumerate(lecturer_ids, start=1):
        if i > 200:  # Limit to 200 courses
            break
        course_name = f"Course {i}"
        cursor.execute("INSERT INTO courses (course_name, lecturer_id) VALUES (%s, %s)", (course_name, lecturer_id))
    
    connection.commit()
    print("Courses inserted successfully")

# Generate and insert student-course enrollments
def generate_enrollments(connection):
    cursor = connection.cursor()
    # Ensure students and courses exist before enrolling them
    cursor.execute("SELECT user_id FROM users WHERE role = 'student'")
    student_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT course_id FROM courses")
    course_ids = [row[0] for row in cursor.fetchall()]
    
    for student_id in student_ids:
        # Each student is enrolled in 3 random courses
        enrolled_courses = random.sample(course_ids, 3)
        for course_id in enrolled_courses:
            cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
    
    connection.commit()
    print("Enrollments inserted successfully")

# Generate and insert calendar events
def generate_calendar_events(connection):
    cursor = connection.cursor()
    # Ensure courses exist before creating events
    cursor.execute("SELECT course_id FROM courses")
    course_ids = [row[0] for row in cursor.fetchall()]
    
    for course_id in course_ids:
        for week in range(1, 5):  # 4 events per course
            event_title = f"Week {week} Event"
            event_description = f"Description for Week {week} Event in Course {course_id}"
            event_date = f"2025-05-{random.randint(1, 28)}"
            cursor.execute("INSERT INTO calendar_events (course_id, event_title, event_description, event_date) VALUES (%s, %s, %s, %s)", (course_id, event_title, event_description, event_date))
    
    connection.commit()
    print("Calendar events inserted successfully")

# Main function
def main():
    connection = connect_to_database()
    if connection:
        try:
            generate_users(connection)
            generate_courses(connection)
            generate_enrollments(connection)
            generate_calendar_events(connection)
        except Error as e:
            print(f"Error during data generation: {e}")
        finally:
            connection.close()
            print("Database connection closed")

if __name__ == "__main__":
    main()