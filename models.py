"""
ByteBites Backend Models

Four core domain classes for the ByteBites system:
- Customer: Represents a user with purchase history
- FoodItem: Represents a menu item with pricing and metadata
- Menu: Manages the collection of all available food items
- Transaction: Represents a customer purchase containing selected items
"""

from decimal import Decimal


class Customer:
    """Represents a customer with their name and purchase history tracking."""

    def __init__(self, name: str):
        self.name = name
        self.purchase_history = []

    def get_name(self) -> str:
        return self.name

    def get_purchase_history(self) -> list:
        return self.purchase_history

    def add_purchase(self, transaction) -> None:
        self.purchase_history.append(transaction)


class FoodItem:
    """Represents a food item with name, price, category, and popularity rating."""

    def __init__(self, name: str, price: Decimal, category: str, popularity_rating: float):
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> Decimal:
        return self.price

    def get_category(self) -> str:
        return self.category

    def get_popularity_rating(self) -> float:
        return self.popularity_rating

    def set_popularity_rating(self, rating: float) -> None:
        self.popularity_rating = rating


class Menu:
    """Manages the collection of all food items and provides filtering by category."""

    def __init__(self):
        self.items = []

    def add_item(self, item: FoodItem) -> bool:
        if any(existing.get_name() == item.get_name() for existing in self.items):
            return False
        self.items.append(item)
        return True

    def remove_item(self, item: FoodItem) -> bool:
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def get_all_items(self) -> list:
        return self.items

    def filter_by_category(self, category: str) -> list:
        return [item for item in self.items if item.get_category() == category]


class Transaction:
    """Represents a customer purchase transaction containing selected items and total cost."""

    def __init__(self, customer: Customer, menu: Menu):
        self.customer = customer
        # Ties the transaction to a specific menu so only valid, approved items can be added.
        self.menu = menu
        self.selected_items = {}  # {FoodItem: quantity}
        self.total_cost = Decimal("0")

    def get_customer(self) -> Customer:
        return self.customer

    def get_selected_items(self) -> dict:
        return self.selected_items

    def get_total_cost(self) -> Decimal:
        return self.total_cost

    def add_item(self, item: FoodItem) -> bool:
        if item not in self.menu.get_all_items():
            return False
        self.selected_items[item] = self.selected_items.get(item, 0) + 1
        self.calculate_total_cost()
        return True

    def remove_item(self, item: FoodItem) -> bool:
        if item not in self.selected_items:
            return False
        if self.selected_items[item] > 1:
            self.selected_items[item] -= 1
        else:
            del self.selected_items[item]
        self.calculate_total_cost()
        return True

    def calculate_total_cost(self) -> Decimal:
        self.total_cost = sum(item.get_price() * qty for item, qty in self.selected_items.items())
        return self.total_cost
