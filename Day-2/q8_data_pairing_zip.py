products=["Laptop","Mouse","Keyboard","Monitor"]
prices=[999.99,25.50,75.00,29.99]
quantities=[5,20,15,8]

# Product-Price pairs
for (product, price) in zip(products, prices):
    print(f"{product}: {price}")

# Total value for each product
for (product, price, quantity) in zip(products, prices, quantities):
    total_value = price * quantity
    print(f"{product}: {total_value}")

# Product Catalog Dictionary
dictionary={
    product: {"price": price, "quantity": quantity}
    for product, price, quantity in zip(products, prices, quantities)
}
print(dictionary)

# Low stock products
for (product, quantity) in zip(products, quantities):
    if quantity < 10:
        print(product)