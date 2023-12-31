import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from views.view import View  # pylint: disable=import-error

class TransactionView(View):
    """
    View class for displaying and managing transactions in the Budget App.

    This class extends the base 'View' class and provides functionality for
    displaying transaction data, adding, editing, and deleting transactions.

    Attributes:
    - props (dict): A dictionary containing properties for configuring the view.
      It includes columns, categories, data, and balance information.

    Methods:
    - __init__(self, parent, props={}, *args, **kwargs): Initializes the TransactionView instance.
    - widgets(self): Creates and configures the widgets for the view.
    - update_cash_balance_view(self, bal): 
      Updates the displayed cash balance with the specified value.
    - validate_amount(self, amount): Validates the input amount for transactions.
    - add_row(self): Displays a popup window for adding a new transaction row.
    - edit_row(self): Displays a popup window for editing a selected transaction row.
    - save_edit_action(self, selected, entries, window, selected_item_id): 
      Saves changes after editing a row.
    - save_row_action(self, entries, window): Saves a new row of transaction data.
    - delete_row(self): Deletes selected transaction row(s) from the view.
    """

    def __init__(self, parent, props={}, *args, **kwargs):
        """
        Initializes the TransactionView instance.

        Args:
            parent: The parent widget.
            props (dict): A dictionary containing properties for configuring the view.
            *args, **kwargs: Additional arguments and keyword arguments.
        """
        super().__init__(parent, bg="#1C2142", *args, **kwargs)
        self.pack(side=tk.LEFT, fill=tk.BOTH, pady=2, expand=True)
        self.props = props
        self.widgets()
        self.controller = parent.master.master.controller

    def widgets(self):
        """
        Creates and configures the widgets for the view.
        """
        columns = self.props["columns"]
        categories = self.props["categories"]
        data = self.props["data"]
        balance = self.props["balance"]

        '''
        Insert Entry Rows
        '''
        insert_frame = tk.Frame(self, bg="#1C2142")
        insert_frame.pack(pady=5)

        treeview = ttk.Treeview(self, columns=columns,
                                show="headings", height=15)
        self.treeview = treeview
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=150)

        for item in data:
            treeview.insert("", tk.END, values=item)

        add_btn = tk.Button(insert_frame , text="Add Row", command=self.add_row)
        edit_btn = tk.Button(insert_frame , text="Edit Row",
                             command=self.edit_row)
        delete_btn = tk.Button(
            insert_frame , text="Delete Row", command=self.delete_row)

        add_btn.grid(row=0, column=len(columns) + 1, padx=5, pady=5)
        edit_btn.grid(row=0, column=len(columns) + 2, padx=5, pady=5)
        delete_btn.grid(row=0, column=len(columns) + 3, padx=5, pady=5)

        insert_frame .grid(row=0, column=0, sticky="ew")
        treeview.grid(row=1, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        '''
        Label to show text near the Delete button
        '''
        self.cash_bal_label = tk.Label(
            insert_frame , text="Cash Balance:", fg="white", bg="#1C2142")
        self.cash_bal_label.grid(row=0, column=len(
            columns) + 4, padx=5, pady=5, sticky="nsew")

        self.message_label = tk.Label(
            insert_frame , text=balance, fg="white", bg="#1C2142")
        self.message_label.grid(row=0, column=len(
            columns) + 5, padx=5, pady=5, sticky="nsew")

    #tämän kansssa ongelmmia näyttää väärän värisenä cash balance
    def update_cash_balance_view(self, bal):
        """
        Updates the displayed cash balance with the specified value and colour.

        Args:
            bal: The new cash balance value and text colour.
        """
        if self.message_label.winfo_exists():
            if bal < 0:
                balance_colour = "red"
            elif bal == 0:
                balance_colour = "yellow"
            else:
                balance_colour = "lightgreen"

        self.message_label.config(
            text=str(bal), fg=balance_colour)

    def validate_amount(self, amount):
        """
        Validates the input amount for transactions.
        Allow only digits and one dot in the "Amount" entry

        Args:
            amount: The input amount to be validated.

        Returns:
            bool: True if the amount is valid, False otherwise.
        """
        return amount.replace('.', '', 1).isdigit()

    def add_row(self):
        """
        Displays a popup window for adding a new transaction row.
        """
        window = tk.Toplevel(self.master)
        window.title("Create New Row")
        window.geometry("+{}+{}".format(self.winfo_rootx() +
                        10, self.winfo_rooty() + 50))

        entries = []
        for i, col in enumerate(self.props["columns"]):

            label = tk.Label(window, text=col + ":")
            label.grid(row=i, column=0, padx=10, pady=5)

            match col:
                case "Amount":
                    entry = tk.Entry(window, validate="key")
                    entry["validatecommand"] = (
                        entry.register(self.validate_amount), "%P")

                case "Category":
                    entry = ttk.Combobox(
                        window, values=self.props["categories"])
                    entry.set(self.props["categories"][0])

                case _:
                    entry = tk.Entry(window)
                    entry.insert(0, "")

            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

            save_btn = tk.Button(window,
                                 text="Save Changes",
                                 command=lambda: self.save_row_action(entries, window))

            save_btn.grid(row=len(self.props["columns"]) + 1,
                          columnspan=len(self.props["columns"]) - 1,
                          pady=10)
        self.update_cash_balance_view(self.controller.get_income_expense_diff())

    def edit_row(self):
        """
        Displays a popup window for editing a selected transaction row.
        """
        selected = self.treeview.selection()
        if selected:
            values = self.treeview.item(selected, "values")
            print(values)
            selected_item_id = values[3]
            window = tk.Toplevel(self.master)
            window.title("Edit Row")
            window.geometry(
                "+{}+{}".format(self.winfo_rootx() + 110, self.winfo_rooty() + 50))

            entries = []
            for i, col in enumerate(self.props["columns"]):
                label = tk.Label(window, text=col + ":")
                label.grid(row=i, column=0, padx=10, pady=5)
                entry = tk.Entry(window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(0, values[i])
                entries.append(entry)

            save_btn = tk.Button(window,
                    text="Save Changes",
                    command=lambda: self.save_edit_action(selected, entries,
                     window, selected_item_id))

            save_btn.grid(row=len(self.props["columns"]) + 1,
                          columnspan=len(self.props["columns"]) - 1,
                          pady=10)

        else:
            messagebox.showerror(
                "No Row Selected", "Please select a row to edit.")

        # self.update_cash_balance_view(self.controller.get_income_expense_diff())

    def save_edit_action(self, selected, entries, window, selected_item_id):
        """
        Saves changes after editing a row.

        Args:
            selected: The selected transaction row.
            entries: List of entry widgets.
            window: The popup window for editing.
            selected_item_id: The ID of the selected item in treeview.
        """
        item_id = selected_item_id
        values = [entry.get() for entry in entries if entry.get() is not None]
        values.append(item_id)
        if not values[0] or not values[1] or not values[2]:
            messagebox.showerror(
                "Wrong input", "Please add values for all columns.")
            return
        else:
            if values[2] == "Income":
                if self.controller.upd_income(*values):
                    print("DONE income update")
                    self.treeview.item(selected, values=values)
                    self.update_cash_balance_view(
                        self.controller.get_income_expense_diff())
            elif values[2] == "Expense":
                if self.controller.upd_expense(*values):
                    print("DONE expense update")
                    self.treeview.item(selected, values=values)
                    self.update_cash_balance_view(
                        self.controller.get_income_expense_diff())

        self.controller.load_budget_view()
        self.update_cash_balance_view(
            self.controller.get_income_expense_diff())
        window.destroy()

    def save_row_action(self, entries, window):
        """
        Saves a new row of transaction data.

        Args:
            entries: List of entry widgets.
            window: The popup window for adding a new row.
        """
        values = [entry.get() for entry in entries if entry.get() is not None]

        if values[2] == "Income":
            if values[0] == "":
                messagebox.showerror("Wrong input", "Please add amount.")
                return
            elif values[1] == "":
                messagebox.showerror("Wrong input", "Please add source.")
                return

            if self.controller.add_income(*values):
                print("DONE income")
                self.treeview.insert("", tk.END, values=values)
                self.controller.load_budget_view()

        if values[2] == "Expense":
            if values[0] == "":
                messagebox.showerror("Wrong input", "Please add amount.")
                return
            elif values[1] == "":
                messagebox.showerror("Wrong input", "Please add description.")
                return

            if self.controller.add_expense(*values):
                print("DONE expense")
                self.treeview.insert("", tk.END, values=values)
                self.controller.load_budget_view()

        window.destroy()
        self.update_cash_balance_view(self.controller.get_income_expense_diff())

    def delete_row(self):
        """
        Deletes selected transaction row(s) from the view.
        """
        selected = self.treeview.selection()
        if selected:
            for item_id in selected:
                item = self.treeview.item(item_id)
                values = item['values']
                # print(f"Selected values: {values}")

                if values[2] == "Expense":
                    if self.controller.del_expense(*values):
                        print("Deleted selected row(s)")
                        self.treeview.delete(item_id)
                        self.update_cash_balance_view(
                            self.controller.get_income_expense_diff())
                        self.controller.load_budget_view()

                if values[2] == "Income":
                    if self.controller.del_income(*values):
                        print("Deleted selected row(s)")
                        self.treeview.delete(item_id)
                        self.update_cash_balance_view(
                            self.controller.get_income_expense_diff())
                        self.controller.load_budget_view()
        else:
            messagebox.showerror(
                "No Row Selected", "Please select a row to delete.")
