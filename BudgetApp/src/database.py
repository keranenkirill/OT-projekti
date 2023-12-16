import os
import sqlite3

class DBController:
    db = None

    @staticmethod
    def execute_statement(query, params):
        try:
            return DBController.db.execute(query, params)
        except Exception as ex:  # pylint: disable=broad-exception-caught
            print(ex)
            return False

    def close():  # pylint: disable=no-method-argument
        DBController.db.close()
        DBController.db = None

    @staticmethod
    def init_database(dbpath="budget_app.db"):
        try:
            DBController.db = sqlite3.connect(
                os.path.join(os.getcwd(), dbpath))
            DBController.db.isolation_level = None
        except Exception as ex:  # pylint: disable=broad-exception-caught
            print(ex)
            return False
        return True

    @staticmethod
    def tables_exist():
        query = (
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name IN ('Users', 'Expenses', 'Incomes');"
        )
        result = DBController.execute_statement(query, [])
        return bool(result.fetchone())

    @staticmethod
    def create_tables():
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
    def create_user(uname, psswd):
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
        query = "SELECT username, password, user_id FROM Users WHERE username = ?"
        result = DBController.execute_statement(query, [username]).fetchone()
        print(result)
        if result is not None:
            if result[1] == password:
                return result[2]
        return None

    @staticmethod
    def add_expense(amnt, descrptn, category, usr_id):
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
        query = (
            "SELECT SUM(Expenses.amount) "
            "FROM Expenses, Users "
            "WHERE Users.user_id = Expenses.user_id AND Users.user_id = ?;"
        )
        parameters = [user_id]
        kulujen_yhteissumma = DBController.execute_statement(query, parameters).fetchone()
        print("     HAETTU KÄYTTÄJÄN", user_id, "KULUJEN YHTEISSUMMA:")
        print("     ", kulujen_yhteissumma[0])
        if kulujen_yhteissumma is not None and kulujen_yhteissumma[0] is not None:
            return kulujen_yhteissumma[0]
        return 0

    @staticmethod
    def add_income(amnt, src, category, usr_id):
        query = (
            "INSERT INTO Incomes (source, amount, category, user_id) "
            "VALUES (?, ?, ?, ?)"
        )
        parameters = [src, amnt, category, usr_id]
        return DBController.execute_statement(query, parameters)

    @staticmethod
    def update_income(amnt, source, category, income_id, usr_id):
        query = (
            "UPDATE Incomes SET "
            "amount=?, source=?, category=? "
            "WHERE user_id=? AND income_id=?"
        )
        parameters = [amnt, source, category, usr_id, income_id]
        return DBController.execute_statement(query, parameters)

    @staticmethod
    def update_expense(amnt, description, category, expense_id, usr_id):
        query = (
            "UPDATE Expenses SET "
            "amount=?, description=?, category=? "
            "WHERE user_id=? AND expense_id=?"
        )
        parameters = [amnt, description, category, usr_id, expense_id]
        return DBController.execute_statement(query, parameters)

    @staticmethod
    def get_incomes(user_id):
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
        tul_yhtsym = DBController.get_summ_of_all_incomes(user_id)
        men_yhtsum = DBController.get_summ_of_all_expenses(user_id)
        print("     HAETTU KÄYTTÄJÄN", user_id, "TULOJEN JA MENOJEN EROTUS:")
        print("     ", tul_yhtsym - men_yhtsum)
        return tul_yhtsym - men_yhtsum

    @staticmethod
    def clear_expenses_by_user_id(user_id):
        query = "DELETE FROM Expenses WHERE user_id = ?;"
        parameters = [user_id]
        DBController.execute_statement(query, parameters)
        print(f"Cleared expenses for user with id {user_id}.")

    @staticmethod
    def clear_incomes_by_user_id(user_id):
        query = "DELETE FROM Incomes WHERE user_id = ?;"
        parameters = [user_id]
        DBController.execute_statement(query, parameters)
        print(f"Cleared incomes for user with id {user_id}.")

    @staticmethod
    def clear_user_and_data_by_id(user_id):
        query = "DELETE FROM Users WHERE user_id = ?;"
        parameters = [user_id]
        DBController.execute_statement(query, parameters)
        print(f"Deleted user with id {
              user_id} and associated data (expenses and incomes).")
