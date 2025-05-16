import random
from faker import Faker
import mysql.connector

fake = Faker()

# Connect to the database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",     
        password="password",
        database="ourvle_clone" 
    )

# Execute a query directly in the database
def execute_query(cursor, query):
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print(f"Query: {query}")

# Generate and insert users
def generate_users(cursor):
    # Insert students
    for i in range(1, 100001):
        username = f"student_{i}"
        password = fake.password()
        role = "student"
        query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        execute_query(cursor, query)
    
    # Insert lecturers
    for i in range(1, 51):
        username = f"lecturer_{i}"
        password = fake.password()
        role = "lecturer"
        query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        execute_query(cursor, query)
    
    # Insert admins
    for i in range(1, 6):
        username = f"admin_{i}"
        password = f"password{i}"
        role = "admin"
        query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        execute_query(cursor, query)

# Generate and insert courses
def generate_courses(cursor):
    # Simulate lecturer IDs
    lecturer_ids = list(range(1, 51))  # Assuming 50 lecturers exist
    
    # Assign up to 5 courses per lecturer
    course_id = 1
    for lecturer_id in lecturer_ids:
        num_courses = random.randint(1, 5)  # Each lecturer teaches 1 to 5 courses
        for _ in range(num_courses):
            if course_id > 200:  # Limit to 200 courses
                break
            course_name = f"Course {course_id}"
            query = f"INSERT INTO courses (course_name, lecturer_id) VALUES ('{course_name}', {lecturer_id})"
            execute_query(cursor, query)
            course_id += 1

# Generate and insert student-course enrollments
def generate_enrollments(cursor):
    student_ids = list(range(1, 100001))  
    course_ids = list(range(1, 201))  
    
    # Ensure each course has at least 10 members
    for course_id in course_ids:
        enrolled_students = random.sample(student_ids, 10)
        for student_id in enrolled_students:
            query = f"INSERT INTO student_courses (student_id, course_id) VALUES ({student_id}, {course_id})"
            execute_query(cursor, query)
    
    # Assign additional enrollments randomly
    for student_id in student_ids:
        # Each student is enrolled in 3 to 6 random courses
        num_courses = random.randint(3, 6)
        enrolled_courses = random.sample(course_ids, num_courses)
        for course_id in enrolled_courses:
            query = f"INSERT INTO student_courses (student_id, course_id) VALUES ({student_id}, {course_id})"
            execute_query(cursor, query)

# Generate and insert calendar events
def generate_calendar_events(cursor):
    # Simulate course IDs
    course_ids = range(1, 201)  # Assuming 200 courses exist
    
    for course_id in course_ids:
        for week in range(1, 5):  # 4 events per course
            event_title = f"Week {week} Event"
            event_description = f"Description for Week {week} Event in Course {course_id}"
            event_date = f"2025-05-{random.randint(1, 28)}"
            query = f"INSERT INTO calendar_events (course_id, event_title, event_description, event_date) VALUES ({course_id}, '{event_title}', '{event_description}', '{event_date}')"
            execute_query(cursor, query)

# Generate and insert forums
def generate_forums(cursor):
    # Simulate course IDs
    course_ids = range(1, 201)  # Assuming 200 courses exist
    
    for course_id in course_ids:
        forum_title = f"Forum for Course {course_id}"
        query = f"INSERT INTO forums (course_id, forum_title) VALUES ({course_id}, '{forum_title}')"
        execute_query(cursor, query)

# Generate and insert course content
def generate_course_content(cursor):
    # Simulate course IDs
    course_ids = range(1, 201)  # Assuming 200 courses exist
    
    for course_id in course_ids:
        for week in range(1, 5):  # 4 pieces of content per course
            section = f"Week {week}"
            content_title = f"Content for Week {week} in Course {course_id}"
            content_link = fake.url()
            content_file_path = f"/path/to/content_{course_id}_week_{week}.pdf"
            query = f"INSERT INTO course_content (course_id, section, content_title, content_link, content_file_path) VALUES ({course_id}, '{section}', '{content_title}', '{content_link}', '{content_file_path}')"
            execute_query(cursor, query)

# Generate and insert assignments
def generate_assignments(cursor):
    # Simulate course IDs
    course_ids = range(1, 201)  # Assuming 200 courses exist
    
    for course_id in course_ids:
        for i in range(1, 4):  # 3 assignments per course
            title = f"Assignment {i} for Course {course_id}"
            description = f"Description for Assignment {i} in Course {course_id}"
            due_date = f"2025-05-{random.randint(1, 28)}"
            query = f"INSERT INTO assignments (course_id, title, description, due_date) VALUES ({course_id}, '{title}', '{description}', '{due_date}')"
            execute_query(cursor, query)

# Generate and insert assignment submissions
def generate_assignment_submissions(cursor):
    # Simulate assignment IDs and student IDs
    assignment_ids = range(1, 601)  # Assuming 3 assignments per 200 courses
    student_ids = range(1, 100001)  # Assuming 100,000 students exist
    
    for assignment_id in assignment_ids:
        for _ in range(10):  # 10 submissions per assignment
            student_id = random.choice(student_ids)
            file_path = f"/path/to/submission_{assignment_id}_{student_id}.pdf"
            grade = random.randint(50, 100)  # Random grade between 50 and 100
            query = f"INSERT INTO assignment_submissions (assignment_id, student_id, file_path, grade) VALUES ({assignment_id}, {student_id}, '{file_path}', {grade})"
            execute_query(cursor, query)

# Main function
def main():
    connection = connect_to_database()
    cursor = connection.cursor()
    
    try:
        generate_users(cursor)
        generate_courses(cursor)
        generate_enrollments(cursor)
        generate_calendar_events(cursor)
        generate_forums(cursor)
        generate_course_content(cursor)
        generate_assignments(cursor)
        generate_assignment_submissions(cursor)
        
        connection.commit()
        print("Data generated and inserted into the database successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()