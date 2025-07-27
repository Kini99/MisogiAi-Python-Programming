import re


class Product:
    VALID_CATEGORIES = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
    
    def __init__(self, name, base_price, discount_percent=0, stock_quantity=0, category='Electronics'):
        self.name = name
        self.base_price = base_price
        self.discount_percent = discount_percent
        self.stock_quantity = stock_quantity
        self.category = category
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError("Name must be between 3 and 50 characters")
        
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', value):
            raise ValueError("Name can only contain letters, numbers, spaces, and hyphens")
        
        self._name = value
    
    @property
    def base_price(self):
        return self._base_price
    
    @base_price.setter
    def base_price(self, value):   
        if value <= 0:
            raise ValueError("Base price must be positive")
        
        if value > 50000:
            raise ValueError("Base price cannot exceed $50,000")
        
        self._base_price = float(value)
    
    @property
    def discount_percent(self):
        return self._discount_percent
    
    @discount_percent.setter
    def discount_percent(self, value):  
        if value < 0 or value > 75:
            raise ValueError("Discount percent must be between 0 and 75")
        
        self._discount_percent = round(float(value), 2)
    
    @property
    def stock_quantity(self):
        return self._stock_quantity
    
    @stock_quantity.setter
    def stock_quantity(self, value):   
        if value < 0:
            raise ValueError("Stock quantity cannot be negative")
        
        if value > 10000:
            raise ValueError("Stock quantity cannot exceed 10,000 units")
        
        self._stock_quantity = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value): 
        if value not in self.VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(self.VALID_CATEGORIES)}")
        
        self._category = value
    
    @property
    def final_price(self):
        discount_amount = (self._base_price * self._discount_percent) / 100
        return round(self._base_price - discount_amount, 2)
    
    @property
    def savings_amount(self):
        return round((self._base_price * self._discount_percent) / 100, 2)
    
    @property
    def availability_status(self):
        if self._stock_quantity == 0:
            return "Out of Stock"
        elif self._stock_quantity < 10:
            return "Low Stock"
        else:
            return "In Stock"
    
    @property
    def product_summary(self):
        return (f"{self._name} | {self._category} | "
                f"${self.final_price:.2f} (${self._base_price:.2f} - {self._discount_percent}% off) | "
                f"{self.availability_status} ({self._stock_quantity} units)")

if __name__ == "__main__":
    # Test Case 1
    product = Product("Gaming Laptop", 1299.99, 15.5, 25, "Electronics")
    assert product.name == "Gaming Laptop"
    assert product.base_price == 1299.99
    assert product.discount_percent == 15.5
    assert abs(product.final_price - 1098.49) < 0.01
    assert abs(product.savings_amount - 201.5) < 0.01
    assert product.availability_status == "In Stock"

    # Test Case 2
    product.discount_percent = 20.567
    assert product.discount_percent == 20.57
    assert abs(product.final_price - 1032.59) < 0.01  
    
    product.stock_quantity = 5
    assert product.availability_status == "Low Stock"

    # Test Case 3
    try:
        product.name = "AB"
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "between 3 and 50 characters" in str(e)

    try:
        product.base_price = -100
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    try:
        product.category = "InvalidCategory"
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    # Test Case 4
    assert "Gaming Laptop" in product.product_summary
    assert "1299.99" in product.product_summary
    assert "Low Stock" in product.product_summary

    print("✅ All tests passed!")
