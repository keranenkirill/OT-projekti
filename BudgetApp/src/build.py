import os
from database import DBController as db  # pylint: disable=import-error


def initialize():
    path = "budget_app.db"
    if os.path.exists(os.path.join(os.getcwd(), path)):
        os.remove(path)

    db.init_database(path)
    db.create_tables()

    print("ok db")


if __name__ == "__main__":
    initialize()
