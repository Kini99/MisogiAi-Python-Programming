school={
    "Math":{
        "teacher":"Mr. Smith",
        "students": [("Alice", 85),("Bob", 92),("Carol", 78)],
    },
    "Science":{
        "teacher":"Ms. Johnson",
        "students": [("David", 88),("Eve", 94),("Frank", 82)],
    }
}

# Print Teacher Names
for subject, info in school.items():
    print(f"{subject} Teacher: {info['teacher']}")

# Calculate Class Average Grades
for subject, info in school.items():
    students = info["students"]
    total = sum(score for _, score in students)
    avg = total / len(students)
    print(f"{subject} Average: {avg:.2f}")

# Find Top Student Across All Classes
top_student = ("", 0)  # (name, score)

for subject, info in school.items():
    for name, score in info["students"]:
        if score > top_student[1]:
            top_student = (name, score)

print(f"Top Student: {top_student[0]} with {top_student[1]} marks")

# Use Unpacking
for subject, info in school.items():
    print(f"{subject} Students:")
    for name, score in info["students"]:
        print(f" - {name}: {score}")

