students=[(101,"Alice",85,20),(102,"Bob","92","19"),(103,"Carol",78,21),(104,"David",88,20)]

# Student with highest grade
highest_grade_student = max(students, key=lambda x: x[2])
print("Student with highest grade:", highest_grade_student)

# Name-grade list
name_grade_list = [(student[1], student[2]) for student in students]
print("Name-Grade List:", name_grade_list)

# Tuple immutability
try:
    students[0][2] = 90  # Attempt to change the grade of the first student
except TypeError as e:
    print("Error:", e)
    print("Tuples are immutable, so we cannot change their elements directly. They are preferred for records like student data because they ensure that the data remains constant and prevents accidental modifications.") 
