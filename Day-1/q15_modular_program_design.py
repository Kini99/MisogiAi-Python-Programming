# Library inventory list
inventory = []

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    inventory.append({"title": title, "author": author})
    print("Book added successfully!\n")

def search_book():
    keyword = input("Enter book title to search: ").lower()
    found = False
    for book in inventory:
        if keyword in book["title"].lower():
            print(f"Found: Book: {book['title']} | Author: {book['author']}")
            found = True
    if not found:
        print("Book not found.")
    print()

def display_inventory():
    if not inventory:
        print("Inventory is empty.\n")
    else:
        print("\nInventory:")
        for book in inventory:
            print(f"- Book: {book['title']} | Author: {book['author']}")
        print()

def main():
    while True:
        print("1. Add Book")
        print("2. Search Book")
        print("3. Display Inventory")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            add_book()
        elif choice == '2':
            search_book()
        elif choice == '3':
            display_inventory()
        elif choice == '4':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

main()
