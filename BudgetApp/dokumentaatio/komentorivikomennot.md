## Komentorivitoiminnot
### Asennus
:warning: KAIKKI KOMENNOT TOTEUTETAAN BudgetApp -hakemistossa :warning:

1. Asenna riippuvuudet:

```bash
poetry install
```

2. Suorita vaadittavat alustustoimenpiteet tietokannalle:

```bash
poetry run invoke build
```

##
### Ohjelman käynnistäminen

Asennus ohjeiden jälkeen, ohjelma käynnistetään komennolla:

```bash
poetry run invoke start
```
##
### Testaus

Testit suoritetaan komennolla:

```bash
poetry run invoke test
```
##
### Testikattavuus

Testikattavuusraportin generoidaan komennolla:

```bash
poetry run invoke coveragehtml
```

Raportti löytyy _htmlcov_-hakemistosta.
##
### Pytest
```bash
poetry run invoke test
```

### Pylint

Tiedoston [.pylintrc](./.pylintrc) määrittelemät tarkistukset:

```bash
poetry run invoke lint
```
