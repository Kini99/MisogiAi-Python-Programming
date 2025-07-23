from functools import reduce

# Convert list of integers to strings
str_nums = list(map(str, [1, 2, 3, 4]))
print("String Numbers: ", str_nums)

# Find the product of all elements in a list
product = reduce(lambda x, y: x * y, [1, 2, 3, 4])
print("Product: ", product)

# Filter words longer than 3 characters
long_words = list(filter(lambda w: len(w) > 3, ['hi', 'hello', 'sun', 'world']))
print("Long Words: ", long_words)

# Create a list of even squares from 1 to 10
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print("Even Squares: ", even_squares)

# Filter prime numbers from 1 to 20
primes = [x for x in range(2, 21) if all(x % d != 0 for d in range(2, int(x**0.5)+1))]
print("Primes: ", primes)

