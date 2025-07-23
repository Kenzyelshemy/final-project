# auto_colored_expense_tracker.py

import os  # For file handling
from typing import Generator  # For generator return type

# ANSI Colors for terminal text formatting
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

# Decorator for colored output

def deco(color: str):
    color_codes = {
        "red": Colors.RED,
        "green": Colors.GREEN,
        "yellow": Colors.YELLOW,
        "blue": Colors.BLUE,
    }
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(color_codes.get(color, Colors.RESET), end="")
            result = func(*args, **kwargs)
            print(Colors.RESET, end="")
            return result
        return wrapper
    return decorator

# Expense class to hold data
class Expense:
    def __init__(self, category: str, amount: float, description: str):
        self.category = category.strip().capitalize()
        self.amount = float(amount)
        self.description = description.strip()

    def __str__(self):
        return f"{self.category},{self.amount:.2f},{self.description}"

    @classmethod
    def from_line(cls, line: str):
        parts = line.strip().split(",")
        if len(parts) != 3:
            raise ValueError("Invalid expense format.")
        return cls(parts[0], float(parts[1]), parts[2])

    @staticmethod
    def is_valid_amount(amount: str):
        try:
            return float(amount) >= 0
        except ValueError:
            return False

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not value:
            raise ValueError("Description cannot be empty.")
        self._description = value

    def colored_str(self):
        return f"{Colors.BLUE}{self.category}{Colors.RESET}, {Colors.RED}${self.amount:.2f}{Colors.RESET}, {Colors.YELLOW}{self.description}{Colors.RESET}"

# Generator to yield expenses from file

def expense_generator(filename: str) -> Generator[Expense, None, None]:
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                yield Expense.from_line(line)

# Base tracker class
class ExpenseTracker:
    def __init__(self, filename="expenses.txt"):
        self.filename = filename
        self.expenses = self.load_expenses()

    def load_expenses(self):
        try:
            return list(expense_generator(self.filename))
        except FileNotFoundError:
            return []

    def save_expenses(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for expense in self.expenses:
                f.write(str(expense) + "\n")

    def add_expense(self, expense: Expense):
        self.expenses.append(expense)
        self.save_expenses()

    def delete_expense(self, desc: str):
        original_count = len(self.expenses)
        self.expenses = [e for e in self.expenses if e.description.lower() != desc.lower()]
        if len(self.expenses) < original_count:
            self.save_expenses()
            return True
        return False

    def total_spent(self):
        return sum(exp.amount for exp in self.expenses)

    def list_expenses(self):
        return self.expenses

    def __add__(self, other):
        combined = ExpenseTracker()
        combined.expenses = self.expenses + other.expenses
        return combined

    @deco("green")
    def show_welcome(self):
        print("📊 Welcome to the Auto-Colored Expense Tracker")

# Extended class for more features
class AdvancedExpenseTracker(ExpenseTracker):
    def list_expenses(self):
        print("🧾 Listing All Expenses:")
        return super().list_expenses()

    def concat_multiple_files(self, *filenames):
        for fname in filenames:
            for expense in expense_generator(fname):
                self.expenses.append(expense)
        self.save_expenses()

# CLI
if __name__ == "__main__":
    tracker = AdvancedExpenseTracker()
    tracker.show_welcome()

    while True:
        print("\n1. Add Expense")
        print("2. List Expenses")
        print("3. Delete Expense by Description")
        print("4. Show Total Spent")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            category = input("Enter category: ")
            while True:
                amount = input("Enter amount: ")
                if Expense.is_valid_amount(amount):
                    break
                else:
                    print(f"{Colors.RED}Invalid amount. Try again.{Colors.RESET}")
            description = input("Enter description: ")
            try:
                expense = Expense(category, amount, description)
                tracker.add_expense(expense)
                print(f"{Colors.GREEN}Expense added successfully!{Colors.RESET}")
            except ValueError as ve:
                print(f"{Colors.RED}{ve}{Colors.RESET}")

        elif choice == "2":
            for exp in tracker.list_expenses():
                print(exp.colored_str())

        elif choice == "3":
            desc = input("Enter description to delete: ")
            deleted = tracker.delete_expense(desc)
            print(f"{Colors.GREEN}Deleted!{Colors.RESET}" if deleted else f"{Colors.RED}Not found.{Colors.RESET}")

        elif choice == "4":
            total = tracker.total_spent()
            print(f"{Colors.BOLD}Total Spent: {Colors.GREEN}${total:.2f}{Colors.RESET}")

        elif choice == "5":
            print("👋 Goodbye!")
            break

        else:
            print(f"{Colors.RED}Invalid option. Choose between 1-5.{Colors.RESET}")
