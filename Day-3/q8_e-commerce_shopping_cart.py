class Product:
    products = []

    def __init__(self, product_id, name, price, category, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity
        Product.products.append(self)

    def get_product_info(self):
        return f"{self.name} (${self.price}) in {self.category}"

    def update_stock(self, quantity):
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            return True
        return False

    @classmethod
    def get_total_products(cls):
        return len(cls.products)

    @classmethod
    def get_total_revenue(cls):
        return sum(p.price * (p.initial_stock - p.stock_quantity) for p in cls.products if hasattr(p, 'initial_stock'))

    @classmethod
    def get_most_popular_category(cls):
        category_sales = {}
        for p in cls.products:
            sold = getattr(p, 'initial_stock', p.stock_quantity) - p.stock_quantity
            category_sales[p.category] = category_sales.get(p.category, 0) + sold
        if not category_sales:
            return None
        return max(category_sales, key=category_sales.get)

    def __post_init__(self):
        self.initial_stock = self.stock_quantity


class Customer:
    def __init__(self, customer_id, name, email, customer_type="regular"):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.customer_type = customer_type

    def get_discount_rate(self):
        return 10 if self.customer_type == "premium" else 0

    def __str__(self):
        return f"{self.name} ({self.customer_type})"


class ShoppingCart:
    def __init__(self, customer):
        self.customer = customer
        self.items = {}  # product_id -> (product, quantity)

    def add_item(self, product, quantity):
        if product.product_id in self.items:
            self.items[product.product_id][1] += quantity
        else:
            self.items[product.product_id] = [product, quantity]

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]

    def get_total_items(self):
        return sum(q for _, q in self.items.values())

    def get_cart_items(self):
        return [(p.name, q) for p, q in self.items.values()]

    def get_subtotal(self):
        return round(sum(p.price * q for p, q in self.items.values()), 2)

    def calculate_total(self):
        subtotal = self.get_subtotal()
        discount = self.customer.get_discount_rate()
        total = subtotal * (1 - discount / 100)
        return round(total, 2)

    def place_order(self):
        for product, quantity in self.items.values():
            if product.stock_quantity < quantity:
                return f"Insufficient stock for {product.name}"
        for product, quantity in self.items.values():
            if not hasattr(product, 'initial_stock'):
                product.initial_stock = product.stock_quantity
            product.update_stock(quantity)
        return "Order placed successfully"

    def clear_cart(self):
        self.items.clear()


# Test Case 1: Creating products with different categories
laptop = Product("P001", "Gaming Laptop", 1299.99, "Electronics", 10)
book = Product("P002", "Python Programming", 49.99, "Books", 25)
shirt = Product("P003", "Cotton T-Shirt", 19.99, "Clothing", 50)

print(f"Product info: {laptop.get_product_info()}")
print(f"Total products in system: {Product.get_total_products()}")

# Test Case 2: Creating customer and shopping cart
customer = Customer("C001", "John Doe", "john@email.com", "premium")
cart = ShoppingCart(customer)

print(f"Customer: {customer}")
print(f"Customer discount: {customer.get_discount_rate()}%")

# Test Case 3: Adding items to cart
cart.add_item(laptop, 1)
cart.add_item(book, 2)
cart.add_item(shirt, 3)

print(f"Cart total items: {cart.get_total_items()}")
print(f"Cart subtotal: ${cart.get_subtotal():.2f}")

# Test Case 4: Applying discounts and calculating final price
final_total = cart.calculate_total()
print(f"Final total (with {customer.get_discount_rate()}% discount): ${final_total:.2f}")

# Test Case 5: Inventory management
print(f"Laptop stock before order: {laptop.stock_quantity}")
order_result = cart.place_order()
print(f"Order result: {order_result}")
print(f"Laptop stock after order: {laptop.stock_quantity}")

# Test Case 6: Class methods for business analytics
popular_category = Product.get_most_popular_category()
print(f"Most popular category: {popular_category}")

total_revenue = Product.get_total_revenue()
print(f"Total revenue: ${total_revenue:.2f}")

# Test Case 7: Cart operations
cart.remove_item("P002")  # Remove book
print(f"Items after removal: {cart.get_cart_items()}")

cart.clear_cart()
print(f"Items after clearing: {cart.get_total_items()}")
