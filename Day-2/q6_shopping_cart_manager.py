# Shopping Cart Manager
cart = []

def add_item():
    item = input("Enter item to add to cart: ")
    cart.append(item)
    print("item added successfully!\n")

def remove_item():
    item = input("Enter item to remove from cart: ").lower()
    found = False
    for i in cart:
        if item == i.lower():
            cart.remove(i)
            print(f"{item} removed successfully!\n")
            found = True
    if not found:
        print("item not found.")
    print()

def remove_last_item():
    cart.pop()
    print("Last item removed successfully!\n")
    
def display_alphabetical_cart():
    if not cart:
        print("Cart is empty.\n")
    else:
        for item in sorted(cart):
            print(f"- {item}")

def display_cart_indices():
    if not cart:
        print("Cart is empty.\n")
    else:
        for index, item in enumerate(cart):
            print(f"{index}: {item}")

def main():
    while True:
        print("1. Add item")
        print("2. Remove specific item")
        print("3. Remove last added item")
        print("4. Display cart in alphabetical order")
        print("5. Display cart with indices")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_item()
        elif choice == '2':
            remove_item()
        elif choice == '3':
            remove_last_item()
        elif choice == '4':
            display_alphabetical_cart()
        elif choice == '5':
            display_cart_indices()
        else:
            print("Invalid choice. Please try again.\n")

main()
