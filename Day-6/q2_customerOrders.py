from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import List, Optional, Dict
from enum import Enum
from decimal import Decimal
import re
from fastapi.testclient import TestClient

app = FastAPI()

# ENUM
class FoodCategory(str, Enum):
    APPETIZER = "appetizer"
    MAIN_COURSE = "main_course"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SALAD = "salad"


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    READY = "ready"
    DELIVERED = "delivered"

# MENU MODEL
class FoodItem(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    category: FoodCategory
    price: Decimal = Field(..., gt=0, decimal_places=2)
    is_available: bool = True
    preparation_time: int = Field(..., ge=1, le=120)
    ingredients: List[str] = Field(..., min_items=1)
    calories: Optional[int] = Field(None, gt=0)
    is_vegetarian: bool = False
    is_spicy: bool = False

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not re.fullmatch(r"[A-Za-z\s]+", v):
            raise ValueError("Name must contain only letters and spaces")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v < 1 or v > 100:
            raise ValueError("Price must be between $1.00 and $100.00")
        return v

    @field_validator("is_spicy")
    @classmethod
    def validate_spicy(cls, v, info: ValidationInfo):
        if info.data.get("category") in {FoodCategory.DESSERT, FoodCategory.BEVERAGE} and v:
            raise ValueError("Desserts and beverages cannot be spicy")
        return v

    @field_validator("calories")
    @classmethod
    def validate_calories(cls, v, info: ValidationInfo):
        if v and info.data.get("is_vegetarian") and v >= 800:
            raise ValueError("Vegetarian items must have less than 800 calories")
        return v

    @field_validator("preparation_time")
    @classmethod
    def validate_prep_time(cls, v, info: ValidationInfo):
        if info.data.get("category") == FoodCategory.BEVERAGE and v > 10:
            raise ValueError("Preparation time for beverages should be ≤ 10 minutes")
        return v

    @property
    def price_category(self) -> str:
        if self.price < 10:
            return "Budget"
        elif self.price <= 25:
            return "Mid-range"
        return "Premium"

    @property
    def dietary_info(self) -> List[str]:
        info = []
        if self.is_vegetarian:
            info.append("Vegetarian")
        if self.is_spicy:
            info.append("Spicy")
        return info

# ORDER MODELS
class OrderItem(BaseModel):
    menu_item_id: int
    menu_item_name: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., gt=0, le=10)
    unit_price: Decimal = Field(..., gt=0, max_digits=6, decimal_places=2)

    @property
    def item_total(self) -> Decimal:
        return self.quantity * self.unit_price

class Customer(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., pattern=r'^\d{10}$')
    address: str

class Order(BaseModel):
    id: Optional[int] = None
    customer: Customer
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.PENDING

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def total_price(self) -> Decimal:
        return sum(item.item_total for item in self.items) + Decimal("2.99")

# IN-MEMORY DATABASES
menu_db: Dict[int, FoodItem] = {}
current_id = 1

orders_db: Dict[int, Order] = {}
next_order_id = 1

# MENU ENDPOINTS
@app.get("/menu")
def get_all_menu_items():
    return list(menu_db.values())

@app.get("/menu/{item_id}")
def get_menu_item(item_id: int):
    item = menu_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/menu", status_code=201)
def add_menu_item(item: FoodItem):
    global current_id
    item.id = current_id
    menu_db[current_id] = item
    current_id += 1
    return item

@app.put("/menu/{item_id}")
def update_menu_item(item_id: int, updated_item: FoodItem):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item.id = item_id
    menu_db[item_id] = updated_item
    return updated_item

@app.delete("/menu/{item_id}", status_code=204)
def delete_menu_item(item_id: int):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del menu_db[item_id]

@app.get("/menu/category/{category}")
def get_items_by_category(category: FoodCategory):
    return [item for item in menu_db.values() if item.category == category]

# ORDER ENDPOINTS
@app.post("/orders", status_code=201)
def create_order(order: Order):
    global next_order_id
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item.")
    order.id = next_order_id
    orders_db[next_order_id] = order
    next_order_id += 1
    return order

@app.get("/orders")
def get_all_orders():
    return list(orders_db.values())

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, status: OrderStatus):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    return order

# TESTING
client = TestClient(app)

def test_valid_order():
    response = client.post("/orders", json={
        "customer": {
            "name": "Alice Smith",
            "phone": "5551234567",
            "address": "123 Oak Street, Springfield"
        },
        "items": [
            {
                "menu_item_id": 1,
                "menu_item_name": "Margherita Pizza",
                "quantity": 1,
                "unit_price": 15.99
            },
            {
                "menu_item_id": 2,
                "menu_item_name": "Spicy Chicken Wings",
                "quantity": 2,
                "unit_price": 12.50
            }
        ]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["customer"]["name"] == "Alice Smith"
    assert data["items"][0]["menu_item_name"] == "Margherita Pizza"

if __name__ == "__main__":
    test_valid_order()
    print("Order test passed successfully!")
