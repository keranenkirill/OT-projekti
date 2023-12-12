import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database  # pylint: disable=import-error
from views.view import View  # pylint: disable=import-error
from views.transaction_view import TransactionView


class BudgetView(View):
    def __init__(self, parent, *args, account="", **kwargs):
        super().__init__(parent, *args, **kwargs,  bg="#1e453e")
        self.pack(side=tk.LEFT, fill=tk.BOTH, pady=2, expand=True)
        self.widgets()



    def widgets(self):
        # Back button
        back_button = tk.Button(self, text="LogOut", command=self.logout_action)
        back_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[10,5], font=("Helvetica", 14))  # Change font size here

        
        columns = ["Amount", "Category", "Description"]
        categories = ("Income", "Expenses")
        data = []


        views = ttk.Notebook(self)

        expenses_frame = TransactionView(views, props={
            "columns": ["Amount", "Description", "Category"],
            "categories": ["Expense"],
            "data": self.master.controller.get_expenses()
        })


        incomes_frame = TransactionView(views, props={
            "columns": ["Amount", "Source", "Category"],
            "categories": ["Income"],
            "data": self.master.controller.get_incomes()
        })


        all_frame = TransactionView(views, props={
            "columns": columns,
            "categories": ["Income", "Expenses"],
            "data": data
        })

        #wallet_frame = ttk.Frame(views)

        views.add(expenses_frame, text="Expenses")
        views.add(incomes_frame, text="Incomes")
        views.add(all_frame, text="All")
        #views.add(wallet_frame, text="My Wallet")


        views.pack(expand=True, fill=tk.BOTH)





      

    def logout_action(self):
        self.master.config.setAuth("", None)
        self.master.controller.load_login_view()

    def add_income_action(self):
        self.master.controller.add_income(src, amnt, self.master.config.id)
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
