from src.database import DBController as db  # pylint: disable=unknown-option-value


db.init_database()
db.create_tables()


print("\n\nLISÄTÄÄN KÄYTTÄJÄ:")
db.login_user("Lollapallo", "kek")


user_id = db.create_user("ErkKa", "NappiKukkaro01")
db.login_user("ErkKa", "kek")

print("\n\nLISÄTÄÄN EXPENSE:")
db.add_expense(40, "dna lasku", user_id)
db.add_expense(680, "vuokra", user_id)
db.add_expense(11, "netflix", user_id)
db.add_expense(8, "spotify", user_id)
db.add_expense(13, "kotinetti", user_id)
db.add_expense(550, "sijoitukset", user_id)
db.add_expense(300, "vapaa-ajan kulut", user_id)


print("PIZDEC")

print("\n\nLISÄTÄÄN INCOME:")
db.add_income("kela", 340, user_id)
db.add_income("palkka", 1560, user_id)


print("\n\nHAETAAN KÄYTTÄJÄN KAIKKI KULUT:")
db.get_all_expenses(user_id)


print("\n\nHAETAAN KÄYTTÄJÄN KULUJEN YHTEISSUMMA:")
db.get_summ_of_all_expenses(user_id)


print("\n\nHAETAAN KÄYTTÄJÄN KAIKKI TULOT:")
db.get_all_incomes(user_id)


print("\n\nHAETAAN KÄYTTÄJÄN TULOJEN YHTEISSUMMA:")
db.get_summ_of_all_incomes(user_id)


print("\n\nHAETAAN KÄYTTÄJÄN TULOJEN JA MENOJEN EROTUS:")
db.get_income_expense_diff(user_id)

db.close()


# db.execute_statement("")
