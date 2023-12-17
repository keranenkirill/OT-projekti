import os
import sqlite3


class DBController:
    db = None

    @staticmethod
    def execute_statement(query, params):
        """
        Executes an SQL statement with parameters.

        Args:
            query (str): The SQL query.
            params (list): List of parameters to be substituted into the query.

        Returns:
            ResultProxy or False: The result of the execution, or False if an exception occurs.
        """
        try:
            return DBController.db.execute(query, params)
        except Exception as ex:
            print(ex)
            return False

    def close():  # pylint: disable=no-method-argument
        """
        Closes the database connection.
        """
        DBController.db.close()
        DBController.db = None

    @staticmethod
    def init_database(dbpath="budget_app.db"):
        """
        Initializes the database connection.

        Args:
            dbpath (str): Path to the SQLite database file.

        Returns:
            bool: True if the initialization is successful, False otherwise.
        """
        try:
            DBController.db = sqlite3.connect(
                os.path.join(os.getcwd(), dbpath))
            DBController.db.isolation_level = None
        except Exception as ex:
            print(ex)
            return False
        return True

    @staticmethod
    def create_tables():
        """
        Creates database tables for Users, Expenses, and Incomes if they do not exist.
        """
        DBController.db.execute(
            "CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "username VARCHAR(50) NOT NULL, password TEXT NOT NULL);")
        DBController.db.execute(
            "CREATE TABLE IF NOT EXISTS  Expenses (expense_id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "amount INTEGER NOT NULL, description TEXT, category TEXT DEFAULT 'Expense' NOT NULL, "
            "user_id INTEGER NOT NULL, "
            "FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE);")
        DBController.db.execute(
            "CREATE TABLE IF NOT EXISTS  Incomes (income_id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "amount INTEGER NOT NULL, source TEXT NOT NULL, "
            "category TEXT DEFAULT 'Income' NOT NULL, user_id INTEGER NOT NULL, "
            "FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE);")

    @staticmethod
    def get_table_names():
        """
        Retrieves the names of all tables in the database.

        Returns:
            list: List of table names.
        """
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        result = DBController.execute_statement(query, [])
        return [table[0] for table in result.fetchall()]

    @staticmethod
    def tables_exist():
        """
        Checks if the required tables ('Users', 'Expenses', 'Incomes') exist in the database.

        Returns:
            bool: True if all tables exist, False otherwise.
        """
        query = (
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name IN ('Users', 'Expenses', 'Incomes');"
        )
        result = DBController.execute_statement(query, [])
        return bool(result.fetchone())

    @staticmethod
    def create_user(uname, psswd):
        """
        Creates a new user in the Users table.

        Args:
            uname (str): User's username.
            psswd (str): User's password.

        Returns:
            int: User ID of the newly created user.
        """
        DBController.execute_statement(
            "INSERT INTO Users (username, password) VALUES (?, ?)",
            [uname, psswd])
        user_id = DBController.db.execute(
            "SELECT Users.user_id FROM Users WHERE Users.username =?",
            [uname]).fetchone()
        print("     LISÄTTY ONNISTUNEESTI KAYTTÄJÄ:",
              uname, " id:", user_id[0])
        return user_id[0]

    @staticmethod
    def login_user(username, password):
        """
        Logs in a user by checking the username and password.

        Args:
            username (str): User's username.
            password (str): User's password.

        Returns:
            int or None: User ID if login is successful, None otherwise.
        """
        query = "SELECT username, password, user_id FROM Users WHERE username = ?"
        result = DBController.execute_statement(query, [username]).fetchone()
        print(result)
        if result is not None:
            if result[1] == password:
                return result[2]
        return None

    @staticmethod
    def add_expense(amnt, descrptn, category, usr_id):
        """
        Adds an expense entry for a user in the Expenses table.

        Args:
            amnt (int): Expense amount.
            descrptn (str): Expense description.
            category (str): Expense category.
            usr_id (int): User ID.

        Returns:
            ResultProxy or False: The result of the execution, or False if an exception occurs.
        """
        query = (
            "INSERT INTO Expenses (amount, description, category, user_id) "
            "VALUES (?, ?, ?, ?)"
        )
        parameters = [amnt, descrptn, category, usr_id]
        print("     LISÄTTY EXPENSE KÄYTTÄJÄLLE ", usr_id,
              ": MÄÄRÄ:", amnt, " KUVAUS:", descrptn)
        return DBController.execute_statement(query, parameters)

    @staticmethod
    def delete_expense(amnt, descrptn, category, expense_id, usr_id):
        """
        Deletes an expense for a user in the Expenses table.

        Args:
            amnt (int): Expense amount.
            descrptn (str): Expense description.
            category (str): Expense category.
            expense_id (int): Expense ID.
            usr_id (int): User ID.

        Returns:
            ResultProxy or False: The result of the execution, or False if an exception occurs.
        """
        query = (
            "DELETE FROM Expenses WHERE "
            "amount = ? AND description = ? AND category = ? AND expense_id = ? AND user_id = ?"
        )
        parameters = [amnt, descrptn, category, expense_id, usr_id]
        print("DELETED EXPENSE FOR USER", usr_id,
              "WITH AMOUNT:", amnt, "DESCRIPTION:", descrptn)
        return DBController.execute_statement(query, parameters)

    @staticmethod
    def delete_income(amnt, source, category, income_id, usr_id):
        """
        Deletes an income for a user in the Incomes table.

        Args:
            amnt (int): Income amount.
            source (str): Income source.
            category (str): Income category.
            income_id (int): Income ID.
            usr_id (int): User ID.

        Returns:
            ResultProxy or False: The result of the execution, or False if an exception occurs.
        """
        query = (
            "DELETE FROM Incomes WHERE "
            "amount = ? AND source = ? AND category = ? AND income_id = ? AND user_id = ?"
        )
        parameters = [amnt, source, category, income_id, usr_id]
        print("DELETED EXPENSE FOR USER", usr_id,
              "WITH AMOUNT:", amnt, "DESCRIPTION:", source)
        return DBController.execute_statement(query, parameters)

    @staticmethod
    def get_expenses(user_id):
        """
        Retrieves all expenses for a specific user from the Expenses table.

        Args:
            user_id (int): User ID.

        Returns:
            list: List of tuples representing expenses (amount, description, category, expense_id).
        """
        query = (
            "SELECT Expenses.amount, Expenses.description, Expenses.category, Expenses.expense_id "
            "FROM Expenses, Users "
            "WHERE Users.user_id = Expenses.user_id AND Users.user_id = ?;"
        )
        parameters = [user_id]
        kaikki_kulut = DBController.execute_statement(
            query, parameters).fetchall()
        print("     HAETTU KÄYTTÄJÄN", user_id, "KAIKKI KULUT:")
        for kulu in kaikki_kulut:
            print("     ", kulu[1], ":", kulu[0], "id", ":", kulu[3])
        return kaikki_kulut

    @staticmethod
    def get_summ_of_all_expenses(user_id):
        """
        Calculates the total sum of all expenses for a specific user.

        Args:
            user_id (int): User ID.

        Returns:
            int: Total sum of expenses.
        """
        query = (
            "SELECT SUM(Expenses.amount) "
            "FROM Expenses, Users "
            "WHERE Users.user_id = Expenses.user_id AND Users.user_id = ?;"
        )
        parameters = [user_id]
        kulujen_yhteissumma = DBController.execute_statement(
            query, parameters).fetchone()
        print("     HAETTU KÄYTTÄJÄN", user_id, "KULUJEN YHTEISSUMMA:")
        print("     ", kulujen_yhteissumma[0])
        if kulujen_yhteissumma is not None and kulujen_yhteissumma[0] is not None:
            return kulujen_yhteissumma[0]
        return 0

    @staticmethod
    def add_income(amnt, src, category, usr_id):
        """
        Adds an income for a user in the Incomes table.

        Args:
            amnt (int): Income amount.
            src (str): Income source.
            category (str): Income category.
            usr_id (int): User ID.

        Returns:
            ResultProxy or False: The result of the execution, or False if an exception occurs.
        """
        query = (
            "INSERT INTO Incomes (source, amount, category, user_id) "
            "VALUES (?, ?, ?, ?)"
        )
        parameters = [src, amnt, category, usr_id]
        return DBController.execute_statement(query, parameters)

    @staticmethod
    def update_income(amnt, source, category, income_id, usr_id):
        """
        Updates an income for a user in the Incomes table.

        Args:
            amnt (int): New income amount.
            source (str): New income source.
            category (str): New income category.
            income_id (int): Income ID.
            usr_id (int): User ID.

        Returns:
            ResultProxy or False: The result of the execution, or False if an exception occurs.
        """
        query = (
            "UPDATE Incomes SET "
            "amount=?, source=?, category=? "
            "WHERE user_id=? AND income_id=?"
        )
        parameters = [amnt, source, category, usr_id, income_id]
        return DBController.execute_statement(query, parameters)

    @staticmethod
    def update_expense(amnt, description, category, expense_id, usr_id):
        """
        Updates an expense for a user in the Expenses table.

        Args:
            amnt (int): New expense amount.
            description (str): New expense description.
            category (str): New expense category.
            expense_id (int): Expense ID.
            usr_id (int): User ID.

        Returns:
            ResultProxy or False: The result of the execution, or False if an exception occurs.
        """
        query = (
            "UPDATE Expenses SET "
            "amount=?, description=?, category=? "
            "WHERE user_id=? AND expense_id=?"
        )
        parameters = [amnt, description, category, usr_id, expense_id]
        return DBController.execute_statement(query, parameters)

    @staticmethod
    def get_incomes(user_id):
        """
        Retrieves all incomes for a specific user from the Incomes table.

        Args:
            user_id (int): User ID.

        Returns:
            list: List of tuples representing incomes (amount, source, category, income_id).
        """
        query = (
            "SELECT Incomes.amount, Incomes.source, Incomes.category, Incomes.income_id "
            "FROM Incomes, Users "
            "WHERE Users.user_id = Incomes.user_id AND Users.user_id = ?;"
        )
        parameters = [user_id]
        kaikki_tulot = DBController.execute_statement(
            query, parameters).fetchall()
        print("     HAETTU KÄYTTÄJÄN", user_id, "KAIKKI TULOT:")
        for tulo in kaikki_tulot:
            print("     ", tulo[1], ":", tulo[0], "id", tulo[3])
        return kaikki_tulot

    @staticmethod
    def get_all_incomes_expenses(user_id):
        """
        Retrieves all incomes and expenses for a specific user from the Incomes and Expenses tables.

        Args:
            user_id (int): User ID.

        Returns:
            list: List of tuples representing incomes and expenses.
        """
        query = (
            "SELECT Incomes.amount, Incomes.source, Expenses.amount, Expenses.description "
            "FROM Incomes, Expenses, Users "
            "WHERE Users.user_id = Incomes.user_id AND Users.user_id = ?;"
        )
        parameters = [user_id]
        kaikkit_tulot_menot = DBController.execute_statement(
            query, parameters).fetchall()
        return kaikkit_tulot_menot

    @staticmethod
    def get_summ_of_all_incomes(user_id):
        """
        Calculates the total sum of all incomes for a specific user.

        Args:
            user_id (int): User ID.

        Returns:
            int: Total sum of incomes.
        """
        query = (
            "SELECT SUM(Incomes.amount) "
            "FROM Incomes, Users "
            "WHERE Users.user_id = Incomes.user_id AND Users.user_id = ?;"
        )
        parameters = [user_id]
        tulojen_yhteissumma = DBController.execute_statement(
            query, parameters).fetchone()
        print("     HAETTU KÄYTTÄJÄN", user_id, "TULOJEN YHTEISSUMMA:")
        print("     ", tulojen_yhteissumma[0])
        if tulojen_yhteissumma is not None and tulojen_yhteissumma[0] is not None:
            return tulojen_yhteissumma[0]
        return 0

    @staticmethod
    def get_income_expense_diff(user_id):
        """
        Calculates the difference between total incomes and total expenses for a specific user.

        Args:
            user_id (int): User ID.

        Returns:
            int: Difference between total incomes and total expenses.
        """
        
        tul_yhtsym = DBController.get_summ_of_all_incomes(user_id)
        men_yhtsum = DBController.get_summ_of_all_expenses(user_id)
        print("Tulot yhteensä:", tul_yhtsym)
        print("Menot yhteensä:", men_yhtsum)
        print("     HAETTU KÄYTTÄJÄN", user_id, "TULOJEN JA MENOJEN EROTUS:")
        print("     ", tul_yhtsym - men_yhtsum)
        return tul_yhtsym - men_yhtsum

    @staticmethod
    def clear_expenses_by_user_id(user_id):
        """
        Clears all expenses for a specific user from the Expenses table.

        Args:
            user_id (int): User ID.
        """
        query = "DELETE FROM Expenses WHERE user_id = ?;"
        parameters = [user_id]
        DBController.execute_statement(query, parameters)
        print(f"Cleared expenses for user with id {user_id}.")

    @staticmethod
    def clear_incomes_by_user_id(user_id):
        """
        Clears all incomes for a specific user from the Incomes table.

        Args:
            user_id (int): User ID.
        """
        query = "DELETE FROM Incomes WHERE user_id = ?;"
        parameters = [user_id]
        DBController.execute_statement(query, parameters)
        print(f"Cleared incomes for user with id {user_id}.")

    @staticmethod
    def clear_user_and_data_by_id(user_id):
        """
        Deletes a user and associated data (expenses and incomes) by user ID.

        Args:
            user_id (int): User ID.
        """
        query = "DELETE FROM Users WHERE user_id = ?;"
        parameters = [user_id]
        DBController.execute_statement(query, parameters)
        print(f"Deleted user with id {
              user_id} and associated data (expenses and incomes).")
