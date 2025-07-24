from typing import List, Dict, ClassVar

class Course:
    def __init__(self, course_id, name, instructor, max_students):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.max_students = max_students
        self.enrollments = []
        self.grades = {}
        self.waitlist = []

    def __str__(self):
        return f"{self.course_id} - {self.name} by {self.instructor}"

    def get_available_spots(self):
        return self.max_students - len(self.enrollments)

    def get_enrollment_count(self):
        return len(self.enrollments)

    def is_full(self):
        return len(self.enrollments) >= self.max_students

    def add_enrollment(self, enrollment):
        if not self.is_full():
            self.enrollments.append(enrollment)
            return True
        else:
            self.waitlist.append(enrollment.student)
            return False

    def add_grade(self, student_id, grade):
        self.grades[student_id] = grade

    def get_course_statistics(self):
        if not self.grades:
            return {"average": 0, "highest": 0, "lowest": 0}
        grades = list(self.grades.values())
        return {
            "average": sum(grades) / len(grades),
            "highest": max(grades),
            "lowest": min(grades)
        }

class Student:
    total_students = 0
    all_students = []
    all_enrollments = []

    def __init__(self, student_id, name, email, program):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.program = program
        self.enrollments = []
        self.grades = {}

        Student.total_students += 1
        Student.all_students.append(self)

    def __str__(self):
        return f"{self.student_id} - {self.name}"

    @classmethod
    def get_total_students(cls):
        return cls.total_students

    def enroll_in_course(self, course):
        enrollment = Enrollment(self, course)
        added = course.add_enrollment(enrollment)
        self.enrollments.append(enrollment)
        Student.all_enrollments.append(enrollment)
        return enrollment

    def add_grade(self, course_id, grade):
        self.grades[course_id] = grade

    def get_transcript(self):
        return self.grades

    def calculate_gpa(self):
        if not self.grades:
            return 0.0
        return round(sum(self.grades.values()) / len(self.grades), 2)

    @classmethod
    def get_total_enrollments(cls):
        return len(cls.all_enrollments)

    @classmethod
    def get_average_gpa(cls):
        gpas = [student.calculate_gpa() for student in cls.all_students if student.grades]
        return round(sum(gpas) / len(gpas), 2) if gpas else 0.0

    @classmethod
    def get_top_students(cls, n=2):
        sorted_students = sorted(cls.all_students, key=lambda s: s.calculate_gpa(), reverse=True)
        return sorted_students[:n]


class Enrollment:
    def __init__(self, student, course):
        self.student = student
        self.course = course


# Test Case 1: Creating courses with enrollment limits
math_course = Course("MATH101", "Calculus I", "Dr. Smith", 3)
physics_course = Course("PHYS101", "Physics I", "Dr. Johnson", 4)
cs_course = Course("CS101", "Programming Basics", "Prof. Wong", 2)

print(f"Course: {math_course}")
print(f"Available spots in Math: {math_course.get_available_spots()}")

#  Test Case 2: Creating students with different programs
student1 = Student("S001", "Alice Wilson", "alice@university.edu", "Computer Science")
student2 = Student("S002", "Bob Davis", "bob@university.edu", "Mathematics")
student3 = Student("S003", "Carol Lee", "carol@university.edu", "Physics")

print(f"Student: {student1}")
print(f"Total students: {Student.get_total_students()}")

# Test Case 3: Course enrollment
enrollment1 = student1.enroll_in_course(math_course)
enrollment2 = student2.enroll_in_course(cs_course)
enrollment3 = student1.enroll_in_course(cs_course)

print(f"Math course enrollment count: {math_course.get_enrollment_count()}")

# Test Case 4: Adding grades and calculating GPA
student1.add_grade("MATH101", 85.0)
student1.add_grade("CS101", 92.8)
student2.add_grade("CS101", 78.3)

print(f"Alice's GPA: {student1.calculate_gpa()}")
print(f"Alice's transcript: {student1.get_transcript()}")

#  Test Case 5: Course statistics
math_course.add_grade("S001", 85.0)
math_course.add_grade("S002", 95.5)
math_course.add_grade("S003", 88.5)

course_stats = math_course.get_course_statistics()
print(f"Math course statistics: {course_stats}")

# Test Case 6: University-wide analytics using class methods
total_enrollments = Student.get_total_enrollments()
print(f"Total students: {Student.get_total_students()}, total enrollments: {total_enrollments}")

average_gpa = Student.get_average_gpa()
print(f"Average GPA: {average_gpa}")

top_students = Student.get_top_students()
print(f"Top students: {[str(s) for s in top_students]}")

# Test Case 7: Enrollment limits and waitlist
# Enrolling more students than course capacity
for i in range(4):
    student = Student(f"S10{i+1}", f"Student {i+1}", f"student{i}@uni.edu", "General")
    result = student.enroll_in_course(math_course)

print(f"Course full status: {math_course.is_full()}")
print(f"Waitlist size: {len(math_course.waitlist) if hasattr(math_course, 'waitlist') else 0}")
