from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import List, Optional, Dict
from enum import Enum
from decimal import Decimal
import re
from fastapi.testclient import TestClient

app = FastAPI()


# Enum for food category
class FoodCategory(str, Enum):
    APPETIZER = "appetizer"
    MAIN_COURSE = "main_course"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SALAD = "salad"


# FoodItem model with validations
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


# In-memory DB
menu_db: Dict[int, FoodItem] = {}
current_id = 1

# API Endpoints


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


# ========================== TESTS ==========================

client = TestClient(app)


# 1. Valid Margherita Pizza
def test_valid_margherita_pizza():
    response = client.post(
        "/menu",
        json={
            "id": 0,
            "name": "Margherita Pizza",
            "description": "Classic pizza with tomato sauce, mozzarella cheese, and fresh basil",
            "category": "main_course",
            "price": 15.99,
            "preparation_time": 20,
            "ingredients": [
                "pizza dough",
                "tomato sauce",
                "mozzarella",
                "basil",
                "olive oil",
            ],
            "calories": 650,
            "is_vegetarian": True,
            "is_spicy": False,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Margherita Pizza"


# 2. Invalid Price ($0.50)
def test_invalid_price():
    response = client.post(
        "/menu",
        json={
            "id": 0,
            "name": "Mini Soup",
            "description": "Tiny soup for tasting",
            "category": "appetizer",
            "price": 0.50,
            "preparation_time": 5,
            "ingredients": ["water", "salt"],
            "is_spicy": False,
        },
    )
    assert response.status_code == 422


# 3. Beverage marked as Spicy
def test_spicy_beverage():
    response = client.post(
        "/menu",
        json={
            "id": 0,
            "name": "Hot Coffee",
            "description": "Strong coffee with spices",
            "category": "beverage",
            "price": 5.00,
            "preparation_time": 5,
            "ingredients": ["coffee", "milk", "sugar"],
            "is_spicy": True,
        },
    )
    assert response.status_code == 422
    assert "cannot be spicy" in response.text


# 4. Empty Ingredients List
def test_empty_ingredients():
    response = client.post(
        "/menu",
        json={
            "id": 0,
            "name": "Bread",
            "description": "Plain bread",
            "category": "appetizer",
            "price": 2.00,
            "preparation_time": 2,
            "ingredients": [],
            "is_spicy": False,
        },
    )
    assert response.status_code == 422
    assert "List should have at least 1 item" in response.text


# 5. Invalid Name (contains digits/specials)
def test_invalid_name():
    response = client.post(
        "/menu",
        json={
            "id": 0,
            "name": "Pizza123!",
            "description": "Invalid pizza name",
            "category": "main_course",
            "price": 10.00,
            "preparation_time": 10,
            "ingredients": ["cheese", "sauce"],
            "is_spicy": False,
        },
    )
    assert response.status_code == 422
    assert "Name must contain only letters and spaces" in response.text


if __name__ == "__main__":
    test_valid_margherita_pizza()
    test_invalid_price()
    test_spicy_beverage()
    test_empty_ingredients()
    test_invalid_name()
    print("All tests passed successfully!")
