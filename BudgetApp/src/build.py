import os
from database import DBController as db  # pylint: disable=import-error


def initialize():
    """
    Initializes the budget app database by removing the existing database file,
    creating a new database, and creating necessary tables.

    This function checks if the database file already exists, and if so, removes it.
    Then, it initializes a new database using the DBController class from the 'database' module,
    and creates the required tables ('Users', 'Expenses', 'Incomes').

    The database file 'budget_app.db' is created in the current working directory.

    Usage:
    - Call this function to set up the initial state of the budget app database.
    """
    path = "budget_app.db"
    if os.path.exists(os.path.join(os.getcwd(), path)):
        os.remove(path)

    db.init_database(path)
    db.create_tables()

    print("ok db")


if __name__ == "__main__":
    initialize()
