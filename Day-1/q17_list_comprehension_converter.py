squares = [i * i for i in range(10)]
print("Squares:", squares)

evens = [i for i in range(10) if i % 2 == 0]
print("Evens:", evens)

pairs = [(x, y) for x in range(3) for y in range(2)]
print("Pairs:", pairs)
