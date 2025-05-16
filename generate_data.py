import random
from faker import Faker

fake = Faker()

# Function to write queries to a file
def write_query_to_file(file, query):
    file.write(query + ";\n")

# Generate and insert users
def generate_users(file):
    # Insert students
    for _ in range(1, 100001):
        username = fake.name()
        password = fake.password()
        role = "student"
        student_id = f"620{random.randint(100000, 999999)}"  # 9-digit ID starting with 620
        query = f"INSERT IGNORE INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        write_query_to_file(file, query)
    
    # Insert lecturers
    for _ in range(1, 51):
        username = fake.name()
        password = fake.password()
        role = "lecturer"
        query = f"INSERT IGNORE INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        write_query_to_file(file, query)
    
    # Insert admins
    for i in range(1, 6):
        username = f"admin_{i}"
        password = f"password{i}"
        role = "admin"
        query = f"INSERT IGNORE INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        write_query_to_file(file, query)

# Generate and insert courses
def generate_courses(file):
    # Simulate lecturer IDs
    lecturer_ids = range(1, 51)  # Assuming 50 lecturers exist
    
    for i, lecturer_id in enumerate(lecturer_ids, start=1):
        if i > 200:  # Limit to 200 courses
            break
        course_name = f"Course {i}"
        query = f"INSERT INTO courses (course_name, lecturer_id) VALUES ('{course_name}', {lecturer_id})"
        write_query_to_file(file, query)

# Generate and insert student-course enrollments
def generate_enrollments(file):
    # Simulate student and course IDs
    student_ids = list(range(1, 100001))  # Assuming 100,000 students exist
    course_ids = list(range(1, 201))  # Assuming 200 courses exist
    
    # Ensure each course has at least 10 members
    for course_id in course_ids:
        enrolled_students = random.sample(student_ids, 10)
        for student_id in enrolled_students:
            query = f"INSERT INTO student_courses (student_id, course_id) VALUES ({student_id}, {course_id})"
            write_query_to_file(file, query)
    
    # Assign additional enrollments randomly
    for student_id in student_ids:
        # Each student is enrolled in 3 to 6 random courses
        num_courses = random.randint(3, 6)
        enrolled_courses = random.sample(course_ids, num_courses)
        for course_id in enrolled_courses:
            query = f"INSERT INTO student_courses (student_id, course_id) VALUES ({student_id}, {course_id})"
            write_query_to_file(file, query)

# Generate and insert calendar events
def generate_calendar_events(file):
    # Simulate course IDs
    course_ids = range(1, 201)  # Assuming 200 courses exist
    
    for course_id in course_ids:
        for week in range(1, 5):  # 4 events per course
            event_title = f"Week {week} Event"
            event_description = f"Description for Week {week} Event in Course {course_id}"
            event_date = f"2025-05-{random.randint(1, 28)}"
            query = f"INSERT INTO calendar_events (course_id, event_title, event_description, event_date) VALUES ({course_id}, '{event_title}', '{event_description}', '{event_date}')"
            write_query_to_file(file, query)

# Generate and insert forums
def generate_forums(file):
    # Simulate course IDs
    course_ids = range(1, 201)  # Assuming 200 courses exist
    
    for course_id in course_ids:
        forum_title = f"Forum for Course {course_id}"
        query = f"INSERT INTO forums (course_id, forum_title) VALUES ({course_id}, '{forum_title}')"
        write_query_to_file(file, query)

# Generate and insert course content
def generate_course_content(file):
    # Simulate course IDs
    course_ids = range(1, 201)  # Assuming 200 courses exist
    
    for course_id in course_ids:
        for week in range(1, 5):  # 4 pieces of content per course
            section = f"Week {week}"
            content_title = f"Content for Week {week} in Course {course_id}"
            content_link = fake.url()
            content_file_path = f"/path/to/content_{course_id}_week_{week}.pdf"
            query = f"INSERT INTO course_content (course_id, section, content_title, content_link, content_file_path) VALUES ({course_id}, '{section}', '{content_title}', '{content_link}', '{content_file_path}')"
            write_query_to_file(file, query)

# Main function
def main():
    with open("generated_data.sql", "w") as file:
        generate_users(file)
        generate_courses(file)
        generate_enrollments(file)
        generate_calendar_events(file)
        generate_forums(file)
        generate_course_content(file)
    print("SQL file 'generated_data.sql' created successfully")

if __name__ == "__main__":
    main()