# **Aineopintojen harjoitustyö: ohjelmistotekniikka, syksy 2023**

# BudgetApp

## Dokumentaatio
- [_Sovelluksen käyttöohje_](./BudgetApp/dokumentaatio/kayttoohje.md)
- [_Vaatimusmäärittely_](./BudgetApp/dokumentaatio/vaativuusmaarittely.md)
- [_Arkkitehtuurikuvaus_](./BudgetApp/dokumentaatio/arkkitehtuuri.md)
- [_Testausdokumentti_](./BudgetApp/dokumentaatio/testaus.md)
- [_Työaikakirjanpito_](./BudgetApp/dokumentaatio/tuntikirjanpito.md)
- [_Changelog_](./BudgetApp/dokumentaatio/Changelog.md)

## Komentorivitoiminnot
### Asennus
Suorita tässä olevat lähdekoodin asennusohjeet: [Release](https://github.com/keranenkirill/OT-projekti/releases/tag/viikko7_upd)


⚠️ **Kaikki alla olevat komennot suoritettava BudgetApp -hakemistossa** ⚠️
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
   