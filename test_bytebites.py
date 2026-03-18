from decimal import Decimal
from models import Customer, FoodItem, Menu, Transaction


# --- Shared test data ---

BURGER = FoodItem("Spicy Burger", Decimal("9.99"), "Mains", 4.5)
SODA = FoodItem("Large Soda", Decimal("2.50"), "Drinks", 4.0)

def make_customer():
    return Customer("Alice")

def make_menu():
    return Menu()

def make_transaction(customer=None, menu=None):
    return Transaction(customer or make_customer(), menu or make_menu())


# --- Customer ---

def test_customer_name_is_stored_correctly():
    assert make_customer().get_name() == "Alice"

def test_purchase_history_starts_empty():
    assert make_customer().get_purchase_history() == []

def test_add_purchase_appends_to_history():
    customer = make_customer()
    customer.add_purchase(make_transaction(customer=customer))
    assert len(customer.get_purchase_history()) == 1

def test_multiple_purchases_accumulate_in_history():
    customer = make_customer()
    menu = make_menu()
    customer.add_purchase(make_transaction(customer=customer, menu=menu))
    customer.add_purchase(make_transaction(customer=customer, menu=menu))
    assert len(customer.get_purchase_history()) == 2


# --- FoodItem ---

def test_food_item_name_is_stored_correctly():
    assert BURGER.get_name() == "Spicy Burger"

def test_food_item_price_is_stored_correctly():
    assert BURGER.get_price() == Decimal("9.99")

def test_food_item_category_is_stored_correctly():
    assert BURGER.get_category() == "Mains"

def test_food_item_popularity_rating_is_stored_correctly():
    assert BURGER.get_popularity_rating() == 4.5

def test_set_popularity_rating_updates_correctly():
    burger = FoodItem("Spicy Burger", Decimal("9.99"), "Mains", 4.5)
    burger.set_popularity_rating(3.0)
    assert burger.get_popularity_rating() == 3.0


# --- Menu ---

def test_add_new_item_returns_true():
    assert make_menu().add_item(BURGER) == True

def test_add_duplicate_item_returns_false():
    menu = make_menu()
    menu.add_item(BURGER)
    assert menu.add_item(BURGER) == False

def test_duplicate_item_not_added_to_list():
    menu = make_menu()
    menu.add_item(BURGER)
    menu.add_item(BURGER)
    assert len(menu.get_all_items()) == 1

def test_filter_by_category_returns_matching_items():
    menu = make_menu()
    menu.add_item(BURGER)
    menu.add_item(SODA)
    assert menu.filter_by_category("Mains") == [BURGER]

def test_remove_existing_item_returns_true():
    menu = make_menu()
    menu.add_item(SODA)
    assert menu.remove_item(SODA) == True

def test_remove_item_not_on_menu_returns_false():
    assert make_menu().remove_item(SODA) == False

def test_filter_by_category_is_case_insensitive():
    menu = make_menu()
    menu.add_item(SODA)
    assert menu.filter_by_category("drinks") == [SODA]


# --- Transaction ---

def test_add_valid_menu_item_returns_true():
    menu = make_menu()
    menu.add_item(BURGER)
    txn = make_transaction(menu=menu)
    assert txn.add_item(BURGER) == True

def test_add_item_not_on_menu_returns_false():
    ghost = FoodItem("Unicorn Steak", Decimal("999.99"), "Fantasy", 5.0)
    assert make_transaction().add_item(ghost) == False

def test_adding_same_item_twice_sets_quantity_to_two():
    menu = make_menu()
    menu.add_item(BURGER)
    txn = make_transaction(menu=menu)
    txn.add_item(BURGER)
    txn.add_item(BURGER)
    assert txn.get_selected_items()[BURGER] == 2

def test_calculate_total_with_multiple_items():
    menu = make_menu()
    menu.add_item(BURGER)
    menu.add_item(SODA)
    txn = make_transaction(menu=menu)
    txn.add_item(BURGER)
    txn.add_item(BURGER)
    txn.add_item(SODA)
    assert txn.get_total_cost() == Decimal("22.48")

def test_remove_item_decrements_quantity():
    menu = make_menu()
    menu.add_item(BURGER)
    txn = make_transaction(menu=menu)
    txn.add_item(BURGER)
    txn.add_item(BURGER)
    txn.remove_item(BURGER)
    assert txn.get_selected_items()[BURGER] == 1

def test_total_updates_after_removing_item():
    menu = make_menu()
    menu.add_item(BURGER)
    menu.add_item(SODA)
    txn = make_transaction(menu=menu)
    txn.add_item(BURGER)
    txn.add_item(BURGER)
    txn.add_item(SODA)
    txn.remove_item(BURGER)
    assert txn.get_total_cost() == Decimal("12.49")

def test_remove_item_deletes_key_when_quantity_reaches_zero():
    menu = make_menu()
    menu.add_item(BURGER)
    txn = make_transaction(menu=menu)
    txn.add_item(BURGER)
    txn.remove_item(BURGER)
    assert BURGER not in txn.get_selected_items()

def test_remove_item_not_in_order_returns_false():
    menu = make_menu()
    menu.add_item(BURGER)
    txn = make_transaction(menu=menu)
    assert txn.remove_item(BURGER) == False
