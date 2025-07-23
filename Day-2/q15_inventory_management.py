inventory={
    "apples":{"price":1.05,"quantity":100},
    "bananas":{"price":0.75,"quantity":150},
    "oranges":{"price":2.00,"quantity":80},
}

# Add a New Product
inventory["grapes"] = {"price": 2.50, "quantity": 50}
print("Added Grapes:", inventory["grapes"])

# Update Product Price
inventory["bananas"]["price"] = 0.80  
print("Updated Banana Price:", inventory["bananas"]["price"])

# Sell 25 Apples and update quantity
inventory["apples"]["quantity"] -= 25  
print("Updated Apple Quantity:", inventory["apples"]["quantity"])

# Calculate Total Inventory Value
def calculate_total_value(inventory):
    total_value = 0
    for product, details in inventory.items():
        total_value += details["price"] * details["quantity"]
    print("Total Inventory Value: ", total_value) 

# Find Low Stock Products
def find_low_stock_products(inventory, threshold=50):
    low_stock = []
    for product, details in inventory.items():
        if details["quantity"] < threshold:
            low_stock.append(product)
    print("Low stock products with quantity < 50: ",low_stock)

