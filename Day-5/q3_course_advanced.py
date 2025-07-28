from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from datetime import date
from typing import List

app = FastAPI()

# ==== In-Memory DBs ====
db_students = []
db_courses = []
db_professors = []
db_enrollments = []

# ==== Models ====
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
    gpa: float = 0.0

# ==== Student Endpoints ====
@app.post("/students")
def create_student(student: Student):
    for s in db_students:
        if s.id == student.id:
            raise HTTPException(status_code=400, detail="Student already exists")
    db_students.append(student)
    return student

@app.get("/students")
def get_students():
    return db_students

@app.get("/students/{id}")
def get_student(id: int):
    for s in db_students:
        if s.id == id:
            return s
    raise HTTPException(status_code=404, detail="Student not found")

@app.put("/students/{id}")
def update_student(id: int, updated: Student):
    for i, s in enumerate(db_students):
        if s.id == id:
            db_students[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{id}")
def delete_student(id: int):
    for s in db_students:
        if s.id == id:
            db_students.remove(s)
            return {"message": "Student deleted"}
    raise HTTPException(status_code=404, detail="Student not found")

@app.get("/students/{id}/courses")
def get_student_courses(id: int):
    enrolled = [e.course_id for e in db_enrollments if e.student_id == id]
    return [c for c in db_courses if c.id in enrolled]

# ==== Course Endpoints ====
@app.post("/courses")
def create_course(course: Course):
    if not any(p.id == course.professor_id for p in db_professors):
        raise HTTPException(status_code=400, detail="Professor does not exist")
    db_courses.append(course)
    return course

@app.get("/courses")
def get_courses():
    return db_courses

@app.get("/courses/{id}")
def get_course(id: int):
    for c in db_courses:
        if c.id == id:
            return c
    raise HTTPException(status_code=404, detail="Course not found")

@app.put("/courses/{id}")
def update_course(id: int, updated: Course):
    for i, c in enumerate(db_courses):
        if c.id == id:
            db_courses[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Course not found")

@app.delete("/courses/{id}")
def delete_course(id: int):
    for c in db_courses:
        if c.id == id:
            db_courses.remove(c)
            return {"message": "Course deleted"}
    raise HTTPException(status_code=404, detail="Course not found")

@app.get("/courses/{id}/students")
def get_course_students(id: int):
    enrolled = [e.student_id for e in db_enrollments if e.course_id == id]
    return [s for s in db_students if s.id in enrolled]

# ==== Professor Endpoints ====
@app.post("/professors")
def create_professor(professor: Professor):
    db_professors.append(professor)
    return professor

@app.get("/professors")
def get_professors():
    return db_professors

@app.get("/professors/{id}")
def get_professor(id: int):
    for p in db_professors:
        if p.id == id:
            return p
    raise HTTPException(status_code=404, detail="Professor not found")

@app.put("/professors/{id}")
def update_professor(id: int, updated: Professor):
    for i, p in enumerate(db_professors):
        if p.id == id:
            db_professors[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Professor not found")

@app.delete("/professors/{id}")
def delete_professor(id: int):
    global db_courses
    db_professors[:] = [p for p in db_professors if p.id != id]
    db_courses[:] = [c for c in db_courses if c.professor_id != id]
    return {"message": "Professor and their courses deleted"}

# ==== Enrollment Endpoints ====
@app.post("/enrollments")
def enroll_student(enrollment: Enrollment):
    if any(e.student_id == enrollment.student_id and e.course_id == enrollment.course_id for e in db_enrollments):
        raise HTTPException(status_code=400, detail="Already enrolled")
    course = next((c for c in db_courses if c.id == enrollment.course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    enrolled_count = len([e for e in db_enrollments if e.course_id == course.id])
    if enrolled_count >= course.max_capacity:
        raise HTTPException(status_code=400, detail="Course full")
    db_enrollments.append(enrollment)
    return {"message": "Enrolled"}

@app.get("/enrollments")
def get_enrollments():
    return db_enrollments

@app.put("/enrollments/{student_id}/{course_id}")
def update_grade(student_id: int, course_id: int, gpa: float):
    for e in db_enrollments:
        if e.student_id == student_id and e.course_id == course_id:
            e.gpa = gpa
            total = sum(en.gpa for en in db_enrollments if en.student_id == student_id)
            count = len([en for en in db_enrollments if en.student_id == student_id])
            for s in db_students:
                if s.id == student_id:
                    s.gpa = total / count
            return {"message": "GPA updated"}
    raise HTTPException(status_code=404, detail="Enrollment not found")

@app.delete("/enrollments/{student_id}/{course_id}")
def drop_course(student_id: int, course_id: int):
    for e in db_enrollments:
        if e.student_id == student_id and e.course_id == course_id:
            db_enrollments.remove(e)
            return {"message": "Enrollment removed"}
    raise HTTPException(status_code=404, detail="Enrollment not found")

# ==== TESTS ====
client = TestClient(app)

def test_all():
    assert client.post("/professors", json={"id": 1, "name": "Dr. Smith", "email": "smith@example.com", "department": "CS", "hire_date": "2020-01-01"}).status_code == 200
    assert client.post("/students", json={"id": 1, "name": "Alice", "email": "alice@example.com", "major": "CS", "year": 2, "gpa": 0.0}).status_code == 200
    assert client.post("/courses", json={"id": 1, "name": "Python", "code": "CS101", "credits": 4, "professor_id": 1, "max_capacity": 2}).status_code == 200
    assert client.post("/enrollments", json={"student_id": 1, "course_id": 1, "enrollment_date": "2023-01-01", "gpa": 0.0}).status_code == 200
    assert client.put("/enrollments/1/1?gpa=4.0").status_code == 200
    student = client.get("/students/1").json()
    assert student["gpa"] == 4.0

test_all()

print("All tests passed successfully!")
