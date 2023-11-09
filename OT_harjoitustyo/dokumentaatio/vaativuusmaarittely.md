# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksen avulla käyttäjien on mahdollista toteuttaa budjetointia, eli seurata tuloja ja menoja. Sovellusta on mahdollista käyttää useamman rekisteröityneen käyttäjän, joilla kaikilla on omien tapreiden mukaan luottu budjetti.

## Käyttäjät

Sovelluksella on ainoastaan yksi käyttäjärooli eli _normaali käyttäjä_. 

## Käyttöliittymäluonnos

Sovellus koostuu kuudesta eri näkymästä:

[**_kuva käyttöliittymäluonnoksesta_**](./OHTE_harjoitustyo_luonnos_budjettisovellus.pdf)

Sovellus aukeaa kirjautumisnäkymään, josta on mahdollista siirtyä uuden käyttäjän luomisnäkymään tai onnistuneen kirjautumisen yhteydessä kirjaantuneen käyttäjän budjetti-näkymään.

## Perusversion tarjoama toiminnallisuus

### Ennen kirjautumista

- Käyttäjä voi luoda järjestelmään käyttäjätunnuksen
  - Käyttäjätunnuksen täytyy olla uniikki
- Käyttäjä voi kirjautua järjestelmään
  - Kirjautuminen onnistuu syötettäessä olemassaoleva käyttäjätunnus ja salasana kirjautumislomakkeelle
  - Jos käyttäjää ei olemassa, tai salasana ei täsmää, ilmoittaa järjestelmä tästä virheviestillä

### Kirjautumisen jälkeen

- Käyttäjä näkee oman budjetti näkymän
- Käyttäjä voi luoda uuden butjetin nollaamalla nykyisen
  - Luotu budjetti näkyy ainoastaan sen luoneelle käyttäjälle
- Käyttäjä voi lisätä/poistaa tuloja ja menoja
- Käyttäjä voi kirjautua ulos järjestelmästä

## Jatkokehitysideoita

Perusversion jälkeen järjestelmää täydennetään ajan salliessa esim. seuraavilla toiminnallisuuksilla:

- Oleamassa olevien yksittäisten tulojen/menojen muokkaaminen 
- Käyttäjätiimit, jotka näkevät kaikki yhteiset todot
- Mahdollisuus useampaan erilliseen budjettinäkymään
- Käyttäjätunnuksen poisto kaikkineen tietoineen
- Graaffista sisältöä (charts)