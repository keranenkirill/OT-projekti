import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from views.view import View  # pylint: disable=import-error


class TransactionView(View):

    def __init__(self, parent, props={}, *args, **kwargs):
        super().__init__(parent, bg="#1C2142", *args, **kwargs)
        self.pack(side=tk.LEFT, fill=tk.BOTH, pady=2, expand=True)
        self.props = props
        self.widgets()

        # dont ask
        self.controller = parent.master.master.controller;

    def widgets(self):
        # propsi kamaa
        columns = self.props["columns"]
        categories = self.props["categories"]
        data = self.props["data"]

        ''' TODO:
                if not self.props["data"] or len(self.props["data"]) == 0:
                    self.empty_dataset_view()
                else:
                    if hasattr(self,"empty_view"):
                        self.empty_view.destroy()
        '''             

        # Insert Entry Rows
        insertFrame = tk.Frame(self, bg="#1C2142")
        insertFrame.pack(pady=5)
        



        # treeview
        treeview = ttk.Treeview(self, columns=columns, show="headings", height=15)
        self.treeview = treeview
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=150)

        for item in data:
            treeview.insert("", tk.END, values=item)


        # buttons
        add_btn = tk.Button(insertFrame, text="Add Row", command=self.add_row)
        edit_btn = tk.Button(insertFrame, text="Edit Row", command=self.edit_row)
        delete_btn = tk.Button(insertFrame, text="Delete Row", command=self.delete_row)


        add_btn.grid(row=0, column=len(columns) + 1, padx=5, pady=5)
        edit_btn.grid(row=0, column=len(columns)+ 2, padx=5, pady=5)
        delete_btn.grid(row=0, column=len(columns)+ 3, padx=5, pady=5)


        insertFrame.grid(row=0, column=0, sticky="ew")
        treeview.grid(row=1, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def validate_amount(self, amount):
        # Allow only digits and one dot in the "Amount" entry
        return amount.replace('.', '', 1).isdigit()


    def empty_dataset_view(self):
        empty_view = ttk.Frame(self, name="empty_view")
        empty_view.pack(expand=True, fill=tk.BOTH)

        update_btn = ttk.Button(empty_view, text="Refresh Data")
        update_btn.pack(pady=10)

        self.empty_view = empty_view



    def search_in_rows(self):
        # fuzzy search
        pass

    def drop_budget(self):
        pass


    def add_row(self):
        window = tk.Toplevel(self.master)
        window.title("Create New Row")

        entries = []
        for i, col in enumerate(self.props["columns"]):
            
            label = tk.Label(window, text=col + ":")
            label.grid(row=i, column=0, padx=10, pady=5)

            match col:
                case "Amount":
                    entry = tk.Entry(window, validate="key")
                    entry["validatecommand"] = (entry.register(self.validate_amount), "%P")

                case "Category":
                    entry = ttk.Combobox(window, values=self.props["categories"])
                    entry.set(self.props["categories"][0])

                case _:
                    entry = tk.Entry(window)
                    entry.insert(0, "")
                    pass
                
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)


            save_btn = tk.Button(window,
                        text="Save Changes",
                        command=lambda : self.save_row_action(entries, window))
            
            save_btn.grid(row=len(self.props["columns"]) + 1, 
                            columnspan=len(self.props["columns"]) - 1, 
                            pady=10)




    def edit_row(self):
        selected = self.treeview.selection()
        if selected:
            values = self.treeview.item(selected, "values")

            window = tk.Toplevel(self.master)
            window.title("Edit Row")

            entries = []
            for i, col in enumerate(self.props["columns"]):
                label = tk.Label(window, text=col + ":")
                label.grid(row=i, column=0, padx=10, pady=5)
                entry = tk.Entry(window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(0, values[i])
                #TODO: korjattava toiminallisuus
                entries.append(entry)


            save_btn = tk.Button(window,
                        text="Save Changes",
                        command=lambda : self.save_edit_action(selected, entries, window))
            
            save_btn.grid(row=len(self.props["columns"]) + 1, 
                            columnspan=len(self.props["columns"]) - 1, 
                            pady=10)
            
    


    def save_edit_action(self, selected, entries, window):
        values = [entry.get() for entry in entries if entry.get() is not None]
        if not values[0] or not values[1] or not values[2] :
            messagebox.showerror("Wrong input", "Please add values for all columns.")
            return
        else:
            if values[2]=="Income":
                if self.controller.upd_income(*values):
                    print("DONE income update")
                    self.treeview.item(selected, values=values)
            elif values[2]=="Expense":
                if self.controller.upd_expense(*values):
                    print("DONE expense update")
                    self.treeview.item(selected, values=values)

        window.destroy()




    def save_row_action(self, entries, window):
        values = [entry.get() for entry in entries if entry.get() is not None]


        if values[2]=="Income":
            if values[0]=="":
                messagebox.showerror("Wrong input", "Please add amount.")
                return
            elif values[1]=="":
                messagebox.showerror("Wrong input", "Please add source.")
                return
            
            if self.controller.add_income(*values):
                print("DONE income")
                self.treeview.insert("", tk.END, values=values)

        if values[2]=="Expense":
            if values[0]=="":
                messagebox.showerror("Wrong input", "Please add amount.")
                return
            elif values[1]=="":
                messagebox.showerror("Wrong input", "Please add description.")
                return

            if self.controller.add_expense(*values):
                print("DONE expense")
                self.treeview.insert("", tk.END, values=values)

        window.destroy()


    def delete_row(self):
        selected = self.treeview.selection()
        if selected:
            for item_id in selected:
                item = self.treeview.item(item_id)
                values = item['values']
                print(f"Selected values: {values}")
                if values[2] == "Expense":
                    if self.controller.del_expense(*values):
                        print("Deleted selected row(s)")
                        self.treeview.delete(item_id)

                if values[2] == "Income":
                    if self.controller.del_income(*values):
                        print("Deleted selected row(s)")
                        self.treeview.delete(item_id)
            





        
