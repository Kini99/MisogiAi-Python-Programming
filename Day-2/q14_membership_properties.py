fruits_list = ["apple", "banana", "orange", "apple", "grape"]
fruits_tuple = ("apple", "banana", "orange")
fruits_set = {"apple", "banana", "orange", "grape"}
fruits_dict = {"apple": 5, "banana": 3, "orange": 8, "grape": 2}

print("Membership Testing ('apple' in ...):")
print("In List:", "apple" in fruits_list)
print("In Tuple:", "apple" in fruits_tuple)
print("In Set:", "apple" in fruits_set)
print("In Dict (keys):", "apple" in fruits_dict)

print("\nLength of Each Structure:")
print("List:", len(fruits_list))       # Can have duplicates
print("Tuple:", len(fruits_tuple))     # Immutable sequence
print("Set:", len(fruits_set))         # Unique elements only
print("Dict:", len(fruits_dict))       # Counts keys only

print("\nIterating and Printing Elements:")

print("List Elements:")
for fruit in fruits_list:
    print(fruit)

print("\nTuple Elements:")
for fruit in fruits_tuple:
    print(fruit)

print("\nSet Elements (unordered):")
for fruit in fruits_set:
    print(fruit)

print("\nDict Keys and Values:")
for fruit, count in fruits_dict.items():
    print(f"{fruit}: {count}")

print("\nPerformance Notes (Membership Testing):")
print("""
- Set and Dict offer the fastest lookup times (O(1) on average) using hashing.
- List and Tuple are slower (O(n)) as they perform a linear scan.
- Use Set or Dict when fast membership checking is important.
""")

print("Iteration Patterns:")
print("- List: for item in list")
print("- Tuple: for item in tuple")
print("- Set: for item in set (no duplicates, unordered)")
print("- Dict: for key in dict / for key, value in dict.items()")
