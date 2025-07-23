while True:
    user_input = input("Enter your age (1–120): ").strip()

    if not user_input:
        print("Invalid input. Please enter a valid number.\n")
        continue

    try:
        age = int(user_input)

        if 1 <= age <= 120:
            print(f"\nYou entered a valid age: {age}")
            break
        else:
            print("Out of range. Please enter a number between 1 and 120.\n")

    except ValueError:
        print("Invalid input. Please enter a valid number.\n")
