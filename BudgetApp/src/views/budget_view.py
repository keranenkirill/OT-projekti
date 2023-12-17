import tkinter as tk
from tkinter import ttk
from views.view import View  # pylint: disable=import-error
from views.transaction_view import TransactionView


class BudgetView(View):
    """
    View class for displaying the budget information in the Budget App.

    This class provides a user interface for viewing and managing income and expense transactions.
    It includes tabs for displaying separate views of income and expense transactions.

    Attributes:
    - None

    Methods:
    - __init__(self, parent, *args, **kwargs): Initializes the BudgetView instance.
    - widgets(self): Creates and configures the widgets for the budget view.
    - logout_action(self): Logs the user out and navigates to the login view.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initializes the BudgetView instance.

        Args:
            parent: The parent widget.
            *args, **kwargs: Additional arguments and keyword arguments.
        """
        super().__init__(parent, *args, **kwargs,  bg="#1e453e")
        self.pack(side=tk.LEFT, fill=tk.BOTH, pady=2, expand=True)
        self.widgets()

    def widgets(self):
        """
        Creates and configures the widgets for the budget view.
        """
        back_button = tk.Button(self, text="LogOut",
                                command=self.logout_action)
        back_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[10, 5], font=(
            "Helvetica", 14))  # Change font size here

        balance = self.master.controller.get_income_expense_diff()
        views = ttk.Notebook(self)

        expenses_frame = TransactionView(views, props={
            "columns": ["Amount", "Description", "Category"],
            "categories": ["Expense"],
            "data": self.master.controller.get_expenses(),
            "balance": balance
        })

        incomes_frame = TransactionView(views, props={
            "columns": ["Amount", "Source", "Category"],
            "categories": ["Income"],
            "data": self.master.controller.get_incomes(),
            "balance": balance
        })

        views.add(expenses_frame, text="Expenses")
        views.add(incomes_frame, text="Incomes")
        views.pack(expand=True, fill=tk.BOTH)

    def logout_action(self):
        """
        Logs the user out and navigates to the login view.
        """
        self.master.config.set_auth("", None)
        self.master.controller.load_login_view()
