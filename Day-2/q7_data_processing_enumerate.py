students=["Alice", "Bob","Carol","David","Eve"]
scores=[85,92,78,88,95]

# Numberated list of students
for index, student in enumerate(students):
    print(f"{index+1}. {student}")

# Students with their scores
for index, (student, score) in enumerate(zip(students, scores)):
    print(f"{index+1}. {student} - {score} points")

# Positions of high scores
for index, score in enumerate(scores):
    if score >= 90:
        print(index)

# Positions of students in dict
students_scores = {index: student for index, student in enumerate(students)}
print(students_scores)