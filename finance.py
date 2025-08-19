import json
from datetime import datetime
from collections import defaultdict

class Expense:
    def __init__(self, description, category, amount, date_str):
        self.description = description
        self.category = category
        self.amount = float(amount)
        self.date = datetime.strptime(date_str, "%Y-%m-%d")

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} | {self.category} | ₹{self.amount:.2f} | {self.description}"

    def to_dict(self):
        return {
            "description": self.description,
            "category": self.category,
            "amount": self.amount,
            "date": self.date.strftime("%Y-%m-%d")
        }

    @staticmethod
    def from_dict(data):
        return Expense(data["description"], data["category"], data["amount"], data["date"])

class FinanceTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.load_from_file()

    def add_expense(self, description, category, amount, date_str):
        expense = Expense(description, category, amount, date_str)
        self.expenses.append(expense)

    def view_expense(self):
        return sorted(self.expenses, key=lambda x: x.date)

    def get_category_totals(self):
        totals = defaultdict(float)
        for expense in self.expenses:
            totals[expense.category] += expense.amount
        return dict(totals)

    def get_monthly_totals(self):
        monthly = defaultdict(float)
        for expense in self.expenses:
            key = expense.date.strftime("%Y-%m")
            monthly[key] += expense.amount
        return dict(sorted(monthly.items()))

    def save_to_file(self):
        with open(self.filename, "w") as f:
            json.dump([e.to_dict() for e in self.expenses], f, indent=4)

    def load_from_file(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.expenses = [Expense.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.expenses = []

    def delete_expenses_by_description(self, desc):
        original_count = len(self.expenses)
        self.expenses = [e for e in self.expenses if e.description != desc]
        return original_count - len(self.expenses)

    def delete_expenses_by_category(self, category):
        original_count = len(self.expenses)
        self.expenses = [e for e in self.expenses if e.category != category]
        return original_count - len(self.expenses)

    def delete_expenses_by_date(self, date_str):
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            original_count = len(self.expenses)
            self.expenses = [e for e in self.expenses if e.date != target_date]
            return original_count - len(self.expenses)
        except ValueError:
            return -1

    def delete_all_expenses(self):
        count = len(self.expenses)
        self.expenses.clear()
        return count
