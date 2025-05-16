import random
from faker import Faker

fake = Faker()

# Function to write queries to a file
def write_query_to_file(file, query):
    file.write(query + ";\n")

# Generate and insert users
def generate_users(file):
    # Insert students
    for i in range(1, 100001):
        username = fake.unique.user_name()  # Generate a unique username
        password = fake.password()
        role = "student"
        query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        write_query_to_file(file, query)
    
    # Insert lecturers
    for i in range(1, 51):
        username = fake.unique.user_name()  # Generate a unique username
        password = fake.password()
        role = "lecturer"
        query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        write_query_to_file(file, query)
    
    # Insert admins
    for i in range(1, 6):
        username = f"admin_{i}"  # Admin usernames are predefined
        password = f"password{i}"
        role = "admin"
        query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', '{role}')"
        write_query_to_file(file, query)

# Generate and insert courses
def generate_courses(file):
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
            write_query_to_file(file, query)
            course_id += 1

# Generate and insert student-course enrollments
def generate_enrollments(file):
    student_ids = list(range(1, 100001))  
    course_ids = list(range(1, 201))  
    
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
    course_ids = range(1, 201)  
    
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
    course_ids = range(1, 201)  
    
    for course_id in course_ids:
        forum_title = f"Forum for Course {course_id}"
        query = f"INSERT INTO forums (course_id, forum_title) VALUES ({course_id}, '{forum_title}')"
        write_query_to_file(file, query)

# Generate and insert course content
def generate_course_content(file):
    course_ids = range(1, 201)  
    
    for course_id in course_ids:
        for week in range(1, 5):  
            section = f"Week {week}"
            content_title = f"Content for Week {week} in Course {course_id}"
            content_link = fake.url()
            content_file_path = f"/path/to/content_{course_id}_week_{week}.pdf"
            query = f"INSERT INTO course_content (course_id, section, content_title, content_link, content_file_path) VALUES ({course_id}, '{section}', '{content_title}', '{content_link}', '{content_file_path}')"
            write_query_to_file(file, query)

# Generate and insert assignments
def generate_assignments(file):
    # Simulate course IDs
    course_ids = range(1, 201)  
    
    for course_id in course_ids:
        for i in range(1, 4):  # 3 assignments per course
            title = f"Assignment {i} for Course {course_id}"
            description = f"Description for Assignment {i} in Course {course_id}"
            due_date = f"2025-05-{random.randint(1, 28)}"
            query = f"INSERT INTO assignments (course_id, title, description, due_date) VALUES ({course_id}, '{title}', '{description}', '{due_date}')"
            write_query_to_file(file, query)

# Generate and insert assignment submissions
def generate_assignment_submissions(file):
    assignment_ids = range(1, 601)  
    student_ids = range(1, 100001)  
    
    for assignment_id in assignment_ids:
        for _ in range(10):  
            student_id = random.choice(student_ids)
            file_path = f"/path/to/submission_{assignment_id}_{student_id}.pdf"
            grade = random.randint(50, 100)  
            query = f"INSERT INTO assignment_submissions (assignment_id, student_id, file_path, grade) VALUES ({assignment_id}, {student_id}, '{file_path}', {grade})"
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
        generate_assignments(file)
        generate_assignment_submissions(file)
    print("SQL file 'generated_data.sql' created successfully")

if __name__ == "__main__":
    main()