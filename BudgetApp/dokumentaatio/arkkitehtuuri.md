# Arkkitehtuurikuvaus

## Käyttöliittymä
Käyttöliittymä koostuu näkymistä:
- Kirjautuminen
- Kunnuksenluonti
- BudgetView
   -  avautuvat ikkunat:
      - tulon/menon lisääminen ja tietojen syöttäminen
      - tulon/menon muokkaaminen ja tietojen syöttäminen

## Sovelluslogiikka


```mermaid
 classDiagram
      Expenses "*" --> "1" User
      Incomes "*" --> "1" User
      class User{
          username
          password
      }
      class Expenses{
          id
          amount
          description
          user_id
      }
      class Incomes{
          id
          amount
          source
          user_id
      }
```

## Tietojen tallennus
Ohjelmassa käytetään SQLite -tietokantaa, johon tallennetaan käyttäjän tiedot, sekä tuloihin/menoihin liittyvät tiedot

Tietokanta alustetaan build.py -tiedostossa

## Päätoiminallisuudet

### Käyttäjän kirjaantuminen
```mermaid
sequenceDiagram
  actor User
  participant UI
  participant login_view
  participant view_controller
  participant database

  User->>UI: click "Login" button
  UI->>login_view: login_action("kalle", "kalle123")
  login_view ->> view_controller: login("kalle", "kalle123")
  view_controller->>database: login_user("kalle", "kalle123")
  database-->>login_view: user_id
  database-->>UI: user
  UI->UI: set_auth("kalle", "kalle123")
  UI->UI: load_budget_view()
```

### Uuden käyttäjän luominen
```mermaid
sequenceDiagram
  actor User
  participant UI
  participant register_view
  participant view_controller
  participant login_view
  participant database
  
  User->>UI: click "No account? Register here" button
  UI->UI: load_register_view()
  UI->>register_view: register_action()
  register_view ->> view_controller: register("paavo", "paavo123", "paavo123")
  view_controller ->> database: create_user("paavo", "paavo123", "paavo123")
  database ->> register_view: user_id
  register_view ->> UI: 
  UI->UI: load_login_view()
```

### Tulon/kulun lisääminen
Tulon ja kulun lisääminen ovat lähes identtiset toiminallisuuksiltaan, siksi käsittelemme tässä vain tulon lisäämistä
```mermaid
sequenceDiagram
  actor User
  participant UI
  participant budget_view
  participant view_controller
  participant transaction_view
  participant database
  
  User-> User: assume we user just logged in and clicked Expenses tab...
  User->> UI: click "Add row" button
  UI->> budget_view: load_budget_view()
  budget_view->> transaction_view: add_row()
  transaction_view->transaction_view: popup window for adding a new expense row
  User->> UI: Inserts needed inputs
  UI->> transaction_view: inputs
  User->> UI: click "Save Changes" button
  UI->> transaction_view: save_row_action()
  transaction_view->> view_controller: add_expense(*values)
  transaction_view->> database: add_expense(*values)
  database->> UI: Returns data, refreshes the window, and displays new data.
```


## Ohjelman rakenteeseen ja toiminallisuuteen jääneet heikkoudet
   - Tulojen kokonaismäärän intuitiivinen näyttäminen puuttuu
   - Kulujen kokonaismäärän intuitiivinen näyttäminen puuttuu
   - Tulojen ja kulujen erotuksena olevan käteisvaran buginen näkymä
   - Käyttäjän kirjaantumista ei ole tuettu hashing -toteutuksella, eikä tarkisteta syötettyjen merkkien määrää. Käyttäjänimi ei ole uniikki 



