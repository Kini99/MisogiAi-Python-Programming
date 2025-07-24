from collections import defaultdict

class GradeManager:
    def __init__(self):
        # Structure: {student_name: {subject: grade}}
        self.grades = defaultdict(dict)

    def add_grade(self, student_name, subject, grade):
        self.grades[student_name][subject] = grade

    def get_student_average(self, student_name):
        subjects = self.grades.get(student_name, {})
        if not subjects:
            return 0
        average = sum(subjects.values()) / len(subjects)
        return round(average,2)

    def get_subject_statistics(self, subject):
        subject_grades = []
        for student in self.grades.values():
            if subject in student:
                subject_grades.append(student[subject])
        if not subject_grades:
            return {'average': 0, 'highest': 0, 'lowest': 0, 'student_count': 0}
        return {
            'average': sum(subject_grades) / len(subject_grades),
            'highest': max(subject_grades),
            'lowest': min(subject_grades),
            'student_count': len(subject_grades)
        }

    def get_top_students(self, n):
        student_averages = [(name, self.get_student_average(name)) for name in self.grades]
        student_averages.sort(key=lambda x: x[1], reverse=True)
        return student_averages[:n]

    def get_failing_students(self, passing_grade=60):
        return [
            (name, self.get_student_average(name))
            for name in self.grades
            if self.get_student_average(name) < passing_grade
        ]


manager = GradeManager()

# Add grades
grades = [
    ("Alice", "Math", 95), ("Alice", "Science", 92), ("Alice", "English", 78),
    ("Bob", "Math", 83), ("Bob", "Science", 86), ("Bob", "English", 89),
    ("Charlie", "Math", 70), ("Charlie", "Science", 60), ("Charlie", "History", 91),
    ("David", "Math", 50), ("David", "Science", 55), ("David", "English", 58),
    ("Eve", "Math", 90), ("Eve", "Science", 85), ("Eve", "English", 80), ("Eve", "History", 89)
]

for student, subject, grade in grades:
    manager.add_grade(student, subject, grade)

print("Alice's average:", manager.get_student_average("Alice"))
print("Math statistics:", manager.get_subject_statistics("Math"))
print("Top 3 students:", manager.get_top_students(3))
print("Failing students:", manager.get_failing_students(60))
