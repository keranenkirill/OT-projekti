import os
import sqlite3
import math

try:
   print("ALUSTETAAN TIETOKANTA...")
   # poistaa tietokannan alussa (kätevä moduulin testailussa)
   os.remove("OT-projekti/OT_harjoitustyo/BudjettiSovellus/budget_app_db.db")
   print("  TIETOKANTA POISTETTU ONNISTUNEESTI")
except:
   # mikäli tietokantaa ei ollut vielä olemassa, niin exceptionilla virheviesti
   print("  TIETOKANTAA EI VOITU POISTAA, SILLÄ SE EI OLE OLEMASSA")
try:
   db = sqlite3.connect("OT-projekti/OT_harjoitustyo/BudjettiSovellus/budget_app_db.db")
   db.isolation_level = None  
   print("  TIETOKANTA LUOTU ONNISTUNEESTI")
except:
   print("  TIETOKANNAN UUDELLEENLUOMISESSA ONGELMIA")



def create_tables():
   db.execute("CREATE TABLE Users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(50) NOT NULL, password TEXT NOT NULL);")

   db.execute("CREATE TABLE Expenses (expence_id INTEGER PRIMARY KEY AUTOINCREMENT, amount INTEGER NOT NULL, description TEXT, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE);")

   db.execute("CREATE TABLE Incomes (income_id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT NOT NULL, amount INTEGER NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE);")



def create_user(uname, psswd):
   try:
      print("   ",uname, psswd)
      db.execute("INSERT INTO Users (username, password) VALUES (?,?)", [uname, psswd])
      user_id = db.execute("SELECT Users.user_id FROM Users WHERE Users.username =?", [uname]).fetchone()
      #print(user_id)
      print("     LISÄTTY ONNISTUNEESTI KAYTTÄJÄ:", uname, " id:", user_id[0])
      return user_id[0]
   except:
      print("     KÄYTTÄJÄN LISÄÄMISESSÄ TAULUUN ILMENNYT ONGELMA")



def add_expence(amnt, descrptn, usr_id):
   try:
      print("  ",amnt, descrptn, usr_id)
      db.execute("INSERT INTO Expenses (amount, description, user_id) VALUES (?, ?, ?)", [amnt, descrptn, usr_id])
      print("     LISÄTTY EXPENCE KÄYTTÄJÄLLE ",user_id,":", " MÄÄRÄ:", amnt, " KUVAUS:", descrptn)
   except:
      print("     EXPENCEN LISÄÄMISESSÄ ILMENNYT ONGELMA")



def get_all_expenses(user_id):
   try:
      #print("   ", user_id)
      kaikki_kulut = db.execute("SELECT Expenses.amount,  Expenses.description FROM Expenses, Users WHERE Users.user_id = Expenses.user_id AND Users.user_id =?;", [user_id]).fetchall()
      print("     HAETTU KÄYTTÄJÄN",user_id,"KAIKKI KULUT:")
      for kulu in kaikki_kulut:
         print("     ", kulu[1],":",kulu[0] )
   except:
      print("     KAIKKIEN KULUJEN HAKEMISESSA ILMENNYT ONGELMA")

def get_summ_of_all_expenses(user_id):
   try:
      #print("   ", user_id)
      kulujen_yhteissumma = db.execute("SELECT SUM(Expenses.amount) FROM Expenses, Users WHERE Users.user_id = Expenses.user_id AND Users.user_id =?;", [user_id]).fetchone()
      print("     HAETTU KÄYTTÄJÄN",user_id,"KULUJEN YHTEISSUMMA:")
      print("     ", kulujen_yhteissumma[0])
      return kulujen_yhteissumma[0]
   except:
      print("     KULUJEN YHTEISSUMMAN HAKEMISESSA ILMENNYT ONGELMA")



def add_income(src, amnt, usr_id):
   try:
      print("   ",src, amnt, usr_id)
      db.execute("INSERT INTO Incomes (source, amount, user_id) VALUES (?, ?, ?)", [src, amnt, usr_id])
      print("     LISÄTTY INCOME KÄYTTÄJÄLLE ",user_id,":"," LÄHDE:", src, " MÄÄRÄ:", amnt)
   except:
      print("     INCOMEN LISÄÄMISESSÄ ILMENNYT ONGELMA")



def get_all_incomes(user_id):
   try:
      #print("   ", user_id)
      kaikki_tulot = db.execute("SELECT Incomes.amount,  Incomes.source FROM Incomes, Users WHERE Users.user_id = Incomes.user_id AND Users.user_id =?;", [user_id]).fetchall()
      print("     HAETTU KÄYTTÄJÄN",user_id,"KAIKKI TULOT:")
      for tulo in kaikki_tulot:
         print("     ", tulo[1],":",tulo[0] )
   except:
      print("     KAIKKIEN TULOJEN HAKEMISESSA ILMENNYT ONGELMA")



def get_summ_of_all_incomes(user_id):
   try:
      #print("   ", user_id)
      tulojen_yhteissumma = db.execute("SELECT SUM(Incomes.amount) FROM INcomes, Users WHERE Users.user_id = Incomes.user_id AND Users.user_id =?;", [user_id]).fetchone()
      print("     HAETTU KÄYTTÄJÄN",user_id,"TULOJEN YHTEISSUMMA:")
      print("     ", tulojen_yhteissumma[0])
      return tulojen_yhteissumma[0]
   except:
      print("     TULOJEN YHTEISSUMMAN HAKEMISESSA ILMENNYT ONGELMA")



def get_income_expense_diff(user_id):
   try:
      tul_yhtsym = get_summ_of_all_incomes(user_id)
      men_yhtsum = get_summ_of_all_expenses(user_id)
      print("     HAETTU KÄYTTÄJÄN",user_id,"TULOJEN JA MENOJEN EROTUS:" )
      print("     ",tul_yhtsym-men_yhtsum)
      return tul_yhtsym-men_yhtsum
   except:
      print("TULOJEN JA MENOJEN EROTUKSEN LASKEMISESSA ONGELMIA")
