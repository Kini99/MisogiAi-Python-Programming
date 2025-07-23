employees=[
    ("Alice", 50000, "Engineering"),
    ("Bob", 60000, "Marketing"),
    ("Carol", 55000, "Engineering"),
    ("David", 45000, "Sales"),
]

# Sort by Salary in both ascending and descending order
print("Salary ascending:", sorted(employees, key=lambda x: x[1]))
print("Salary descending:", sorted(employees, key=lambda x: x[1], reverse=True))

# Sort by Department alphabetically, Then by Salary within each department
print("Department then salary:", sorted(employees, key=lambda x: (x[2], x[1])))

# Create a Reversed List without modifying the original list
print("Reversed list:", list(reversed(employees)))

# Sort by employees name Length
print("Sorted by name length:", sorted(employees, key=lambda x: len(x[0])))

# Use .sort() when modifying the original list and sorted() when creating a new sorted list
print("Original list remains unchanged on using sorted: ", sorted(employees))
employees.sort(key=lambda x: x[1])
print("Original list changes on using .sort(): ",employees)