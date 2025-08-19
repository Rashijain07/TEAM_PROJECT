import tkinter as tk
from tkinter import ttk, messagebox
from finance import FinanceTracker

class FinanceApp:
    def __init__(self, root):
        self.tracker = FinanceTracker()
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.description_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar()

        self.categories = ["Food", "Travel", "Bills", "Entertainment", "Shopping", "Health", "Miscellaneous"]

        self.setup_ui()

    def setup_ui(self):
        title_label = ttk.Label(self.root, text="Personal Finance Tracker", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=(20, 10))

        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Description:", font=("Helvetica", 12), width=20, anchor="w").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        ttk.Entry(input_frame, textvariable=self.description_var, width=40).grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(input_frame, text="Category:", font=("Helvetica", 12), width=20, anchor="w").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.category_dropdown = ttk.Combobox(input_frame, textvariable=self.category_var, values=self.categories, state="readonly", width=38)
        self.category_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.category_dropdown.current(len(self.categories) - 1)
        ttk.Label(input_frame, text="Amount:", font=("Helvetica", 12), width=20, anchor="w").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        ttk.Entry(input_frame, textvariable=self.amount_var, width=40).grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(input_frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 12), width=20, anchor="w").grid(row=3, column=0, padx=20, pady=10, sticky="w")
        ttk.Entry(input_frame, textvariable=self.date_var, width=40).grid(row=3, column=1, padx=10, pady=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=30)

        buttons = [
            ("Add Expense", self.add_expense),
            ("View All Expenses", self.view_expenses),
            ("Category Totals", self.show_category_totals),
            ("Monthly Report", self.show_monthly_totals),
            ("Save Data", self.save_data),
            ("Load Data", self.load_data)
        ]

        for i, (text, command) in enumerate(buttons):
            row, col = divmod(i, 3)
            ttk.Button(button_frame, text=text, command=command, width=25).grid(row=row, column=col, padx=20, pady=10)

    def add_expense(self):
        try:
            desc = self.description_var.get()
            cat = self.category_var.get()
            amt = float(self.amount_var.get())
            date = self.date_var.get()
            self.tracker.add_expense(desc, cat, amt, date)
            messagebox.showinfo("Success", "Expense added!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_expenses(self):
        expenses = self.tracker.view_expense()
        result = "\n".join(str(e) for e in expenses)
        messagebox.showinfo("All Expenses", result if result else "No expenses recorded.")

    def show_category_totals(self):
        totals = self.tracker.get_category_totals()
        result = "\n".join([f"{cat}: ₹{amt:.2f}" for cat, amt in totals.items()])
        messagebox.showinfo("Category Totals", result if result else "No data available.")

    def show_monthly_totals(self):
        monthly = self.tracker.get_monthly_totals()
        result = "\n".join([f"{month}: ₹{amt:.2f}" for month, amt in monthly.items()])
        messagebox.showinfo("Monthly Report", result if result else "No data available.")

    def save_data(self):
        self.tracker.save_to_file("expenses.json")
        messagebox.showinfo("Saved", "Data saved to expenses.json")

    def load_data(self):
        self.tracker.load_from_file("expenses.json")
        messagebox.showinfo("Loaded", "Data loaded from expenses.json")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()

