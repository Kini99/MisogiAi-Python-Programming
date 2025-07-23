grades = [85, 92, 78, 90, 88, 76, 94, 89, 87, 91]

# Slice grades from index 2 to 7
sliced_grades = grades[2:8]
print("Sliced Grades (index 2 to 7):", sliced_grades)

# Use list comprehension to find grades above 85
above_85 = [grade for grade in grades if grade > 85]
print("Grades above 85:", above_85)

# Replace the grade at index 3 with 95
grades[3] = 95
print("Updated Grades after replacing index 3 with 95:", grades)

# Append three new grades
grades.append(93)
grades.append(90)
grades.append(88)
print("Grades after appending 93, 90, and 88:", grades)

# Sort in descending order and display the top 5 grades
grades.sort(reverse=True)
top_5_grades = grades[:5]
print("Top 5 Grades in Descending Order:", top_5_grades)
