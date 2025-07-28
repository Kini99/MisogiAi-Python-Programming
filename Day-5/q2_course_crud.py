from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

app = FastAPI()

db_students = {}
db_courses = {}
db_professors = {}
db_enrollments = []

# ======= MODELS =======
class Student(BaseModel):
    id: int
    name: str
    email: str
    major: str
    year: int
    gpa: float = 0.0

class Course(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    professor_id: int
    max_capacity: int

class Professor(BaseModel):
    id: int
    name: str
    email: str
    department: str
    hire_date: date

class Enrollment(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date
    grade: Optional[float] = None

# ======= UTILITY FUNCTIONS =======
def calculate_gpa(student_id: int):
    grades = [e.grade for e in db_enrollments if e.student_id == student_id and e.grade is not None]
    if grades:
        db_students[student_id].gpa = round(sum(grades) / len(grades), 2)

# ======= STUDENTS =======
@app.get("/students", response_model=List[Student])
def get_students():
    return list(db_students.values())

@app.post("/students", response_model=Student)
def create_student(student: Student):
    if student.id in db_students:
        raise HTTPException(status_code=400, detail="Student already exists")
    db_students[student.id] = student
    return student

@app.get("/students/{id}", response_model=Student)
def get_student(id: int):
    if id not in db_students:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_students[id]

@app.put("/students/{id}", response_model=Student)
def update_student(id: int, student: Student):
    if id not in db_students:
        raise HTTPException(status_code=404, detail="Student not found")
    db_students[id] = student
    return student

@app.delete("/students/{id}")
def delete_student(id: int):
    db_students.pop(id, None)
    global db_enrollments
    db_enrollments = [e for e in db_enrollments if e.student_id != id]
    return {"message": "Student deleted"}

@app.get("/students/{id}/courses")
def get_student_courses(id: int):
    if id not in db_students:
        raise HTTPException(status_code=404, detail="Student not found")
    enrolled_course_ids = [e.course_id for e in db_enrollments if e.student_id == id]
    return [db_courses[cid] for cid in enrolled_course_ids if cid in db_courses]

# ======= COURSES =======
@app.get("/courses", response_model=List[Course])
def get_courses():
    return list(db_courses.values())

@app.post("/courses", response_model=Course)
def create_course(course: Course):
    if course.id in db_courses:
        raise HTTPException(status_code=400, detail="Course already exists")
    if course.professor_id not in db_professors:
        raise HTTPException(status_code=400, detail="Professor does not exist")
    db_courses[course.id] = course
    return course

@app.get("/courses/{id}", response_model=Course)
def get_course(id: int):
    if id not in db_courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_courses[id]

@app.put("/courses/{id}", response_model=Course)
def update_course(id: int, course: Course):
    if id not in db_courses:
        raise HTTPException(status_code=404, detail="Course not found")
    db_courses[id] = course
    return course

@app.delete("/courses/{id}")
def delete_course(id: int):
    db_courses.pop(id, None)
    global db_enrollments
    db_enrollments = [e for e in db_enrollments if e.course_id != id]
    return {"message": "Course deleted"}

@app.get("/courses/{id}/students")
def get_course_students(id: int):
    if id not in db_courses:
        raise HTTPException(status_code=404, detail="Course not found")
    student_ids = [e.student_id for e in db_enrollments if e.course_id == id]
    return [db_students[sid] for sid in student_ids if sid in db_students]

# ======= PROFESSORS =======
@app.get("/professors", response_model=List[Professor])
def get_professors():
    return list(db_professors.values())

@app.post("/professors", response_model=Professor)
def create_professor(professor: Professor):
    if professor.id in db_professors:
        raise HTTPException(status_code=400, detail="Professor already exists")
    db_professors[professor.id] = professor
    return professor

@app.get("/professors/{id}", response_model=Professor)
def get_professor(id: int):
    if id not in db_professors:
        raise HTTPException(status_code=404, detail="Professor not found")
    return db_professors[id]

@app.put("/professors/{id}", response_model=Professor)
def update_professor(id: int, professor: Professor):
    if id not in db_professors:
        raise HTTPException(status_code=404, detail="Professor not found")
    db_professors[id] = professor
    return professor

@app.delete("/professors/{id}")
def delete_professor(id: int):
    db_professors.pop(id, None)
    for cid in list(db_courses):
        if db_courses[cid].professor_id == id:
            del db_courses[cid]
            global db_enrollments
            db_enrollments = [e for e in db_enrollments if e.course_id != cid]
    return {"message": "Professor and related courses deleted"}

@app.get("/professors/{id}/courses")
def get_professor_courses(id: int):
    if id not in db_professors:
        raise HTTPException(status_code=404, detail="Professor not found")
    return [c for c in db_courses.values() if c.professor_id == id]

# ======= ENROLLMENTS =======
@app.get("/enrollments", response_model=List[Enrollment])
def get_enrollments():
    return db_enrollments

@app.post("/enrollments")
def enroll_student(enrollment: Enrollment):
    if enrollment.student_id not in db_students or enrollment.course_id not in db_courses:
        raise HTTPException(status_code=404, detail="Student or Course not found")

    if any(e.student_id == enrollment.student_id and e.course_id == enrollment.course_id for e in db_enrollments):
        raise HTTPException(status_code=400, detail="Already enrolled")

    current_enrollment = sum(1 for e in db_enrollments if e.course_id == enrollment.course_id)
    if current_enrollment >= db_courses[enrollment.course_id].max_capacity:
        raise HTTPException(status_code=400, detail="Course at full capacity")

    db_enrollments.append(enrollment)
    return {"message": "Student enrolled"}

@app.put("/enrollments/{student_id}/{course_id}")
def update_grade(student_id: int, course_id: int, grade: float):
    for e in db_enrollments:
        if e.student_id == student_id and e.course_id == course_id:
            e.grade = grade
            calculate_gpa(student_id)
            return {"message": "Grade updated"}
    raise HTTPException(status_code=404, detail="Enrollment not found")

@app.delete("/enrollments/{student_id}/{course_id}")
def delete_enrollment(student_id: int, course_id: int):
    global db_enrollments
    db_enrollments = [e for e in db_enrollments if not (e.student_id == student_id and e.course_id == course_id)]
    calculate_gpa(student_id)
    return {"message": "Enrollment removed"}



# ============================== TESTS ==============================
from fastapi.testclient import TestClient
client=TestClient(app)


def test_all():
    assert client.post("/professors", json={"id": 1, "name": "Dr. Smith", "email": "smith@example.com", "department": "CS", "hire_date": "2020-01-01"}).status_code == 200
    assert client.post("/students", json={"id": 1, "name": "Alice", "email": "alice@example.com", "major": "CS", "year": 2, "gpa": 0.0}).status_code == 200
    assert client.post("/courses", json={"id": 1, "name": "Python", "code": "CS101", "credits": 4, "professor_id": 1, "max_capacity": 2}).status_code == 200
    assert client.post("/enrollments", json={"student_id": 1, "course_id": 1, "enrollment_date": "2023-01-01", "gpa": 0.0}).status_code == 200
    assert client.put("/enrollments/1/1?grade=4.0").status_code == 200
    student = client.get("/students/1").json()
    assert student["gpa"] == 4.0

test_all()

print("All tests passed successfully!")