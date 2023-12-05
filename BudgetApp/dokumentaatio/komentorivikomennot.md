## Komentorivitoiminnot
### Asennus

1. Asenna riippuvuudet:

```bash
poetry install
```

2. Suorita vaadittavat alustustoimenpiteet:

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
poetry run invoke coverage
```

Raportti löytyy _htmlcov_-hakemistosta.
##
### Pylint

Tiedoston [.pylintrc](./.pylintrc) määrittelemät tarkistukset:

```bash
poetry run invoke lint
```
