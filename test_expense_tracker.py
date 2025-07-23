import os
import pytest
from expense_tracker import Expense, ExpenseTracker

TEST_FILE = "test_expenses.txt"

@pytest.fixture
def tracker():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    return ExpenseTracker(filename=TEST_FILE)

def test_add_expense(tracker):
    e = Expense("Food", 12.5, "Lunch")
    tracker.add_expense(e)
    assert len(tracker.expenses) == 1
    assert tracker.expenses[0].description == "Lunch"

def test_total_spent(tracker):
    tracker.add_expense(Expense("Food", 10, "A"))
    tracker.add_expense(Expense("Transport", 5, "B"))
    assert tracker.total_spent() == 15

def test_delete_expense(tracker):
    tracker.add_expense(Expense("Books", 20, "Python"))
    deleted = tracker.delete_expense("Python")
    assert deleted
    assert len(tracker.expenses) == 0

def test_case_insensitive_delete(tracker):
    tracker.add_expense(Expense("Books", 20, "Notebook"))
    assert tracker.delete_expense("notebook")
    assert not tracker.delete_expense("notebook")

def test_invalid_amount():
    assert Expense.is_valid_amount("10")
    assert not Expense.is_valid_amount("-5")
    assert not Expense.is_valid_amount("abc")

def test_str_and_from_line():
    e = Expense("Food", 10.50, "Dinner")
    line = str(e)
    loaded = Expense.from_line(line)
    assert loaded.category == "Food"
    assert loaded.amount == 10.50
    assert loaded.description == "Dinner"

