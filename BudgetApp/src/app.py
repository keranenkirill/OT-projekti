from budget_app_db import DataBaseApp

budget_app = DataBaseApp()
print(budget_app.init_database())
budget_app.create_tables()

print("\n\nLISÄTÄÄN KÄYTTÄJÄ:")
user_id = budget_app.create_user("ErkKa", "NappiKukkaro01")
print("\n\nLISÄTÄÄN EXPENSE:")
budget_app.add_expense(40, "dna lasku", user_id)
budget_app.add_expense(680, "vuokra", user_id)
budget_app.add_expense(11, "netflix", user_id)
budget_app.add_expense(8, "spotify", user_id)
budget_app.add_expense(13, "kotinetti", user_id)
budget_app.add_expense(550, "sijoitukset", user_id)
budget_app.add_expense(300, "vapaa-ajan kulut", user_id)

print("\n\nLISÄTÄÄN INCOME:")
budget_app.add_income("kela", 340, user_id)
budget_app.add_income("palkka", 1560, user_id)

print("\n\nHAETAAN KÄYTTÄJÄN KAIKKI KULUT:")
budget_app.get_all_expenses(user_id)

print("\n\nHAETAAN KÄYTTÄJÄN KULUJEN YHTEISSUMMA:")
budget_app.get_summ_of_all_expenses(user_id)

print("\n\nHAETAAN KÄYTTÄJÄN KAIKKI TULOT:")
budget_app.get_all_incomes(user_id)

print("\n\nHAETAAN KÄYTTÄJÄN TULOJEN YHTEISSUMMA:")
budget_app.get_summ_of_all_incomes(user_id)

print("\n\nHAETAAN KÄYTTÄJÄN TULOJEN JA MENOJEN EROTUS:")
budget_app.get_income_expense_diff(user_id)