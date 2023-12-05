import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database  # pylint: disable=import-error
from views.view import View  # pylint: disable=import-error


class BudgetView(View):
    def __init__(self, parent, *args, account="", **kwargs):
        super().__init__(parent, *args, **kwargs,  bg="#1e453e")
        self.pack(side=tk.LEFT, fill=tk.BOTH, pady=2, expand=True)
        self.widgets()

    def widgets(self):
        # Back button
        back_button = tk.Button(self, text="LogOut",
                                command=self.logout_action)
        back_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        # First Treeview (on the left)
        columns = ("Income Amount", "Source", "Category")
        self.treeview = ttk.Treeview(
            self, columns=columns, show="headings", selectmode="browse")

        # Define column headings
        for col in columns:
            self.treeview.heading(col, text=col)

        # Set column widths
        self.treeview.column("Income Amount", width=130)
        self.treeview.column("Source", width=130)
        self.treeview.column("Category", width=130)

        # Pack the first Treeview
        self.treeview.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        # Example data (replace this with your actual data)
        data = [
            ("OP pankki", 50000, "Palkka"),
            ("mökku vuokraus", 800, "Sijoitukset"),
            # Add more data as needed
        ]

        # Insert data into the first Treeview
        for item in data:
            self.treeview.insert("", tk.END, values=item)

        # Second Treeview (on the right)
        # Replace with your desired column names
        columns2 = ("Expense Amount", "Description", "Category")
        self.treeview2 = ttk.Treeview(
            self, columns=columns2, show="headings", selectmode="browse")

        # Define column headings for the second Treeview
        for col in columns2:
            self.treeview2.heading(col, text=col)

        # Set column widths for the second Treeview
        # Replace with your desired column widths
        self.treeview2.column("Expense Amount", width=130)
        self.treeview2.column("Description", width=130)
        self.treeview2.column("Category", width=130)

        data2 = [
            ("MökkiLaina", 500, "Laina"),
            ("DNA-lasku", 80, "Laskut"),
            # Add more data as needed
        ]

        # Insert data into the first Treeview
        for item in data2:
            self.treeview2.insert("", tk.END, values=item)

        # Pack the second Treeview
        self.treeview2.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

    def logout_action(self):
        self.master.controller.load_login_view()

    def add_income_action(self):
        pass

    def add_expense_action(self):
        pass

    def remove_expense_action(self):
        # TODO:
        # message box to confirm deleting
        pass

    def remove_income_action(self):
        # TODO:
        # message box to confirm deleting
        pass

    def drop_curren_budget_action(self):
        # TODO:
        # message box to confirm deleting
        pass
