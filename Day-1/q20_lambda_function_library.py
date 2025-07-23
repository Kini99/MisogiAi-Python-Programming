# Lambda function for square calculation
square = lambda x: x * x

# Lambda function for string manipulation
reverse = lambda s: s[::-1]

# Lambda function for filtering even numbers
filter_evens = lambda lst: list(filter(lambda x: x % 2 == 0, lst))

print("Square of 5:", square(5))                   
print("Reverse of 'hello':", reverse("hello"))      
print("Even numbers in [1, 2, 3, 4, 5, 6]:", filter_evens([1, 2, 3, 4, 5, 6])) 
