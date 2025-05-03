# Ohjelmistotekniikka, harjoitustyö
**pygame** 2d platformer game + *level editor*

## Release
- [Viikko 5](https://github.com/Zediyo/ot-harjoitustyo/releases/tag/viikko5)
- [Viikko 6](https://github.com/Zediyo/ot-harjoitustyo/releases/tag/viikko6)
- [Loppupalautus](https://github.com/Zediyo/ot-harjoitustyo/releases/tag/loppupalautus)

## Dokumentaatio
- [käyttöohje](dokumentaatio/kayttoohje.md)
- [vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)
- [changelog](dokumentaatio/changelog.md)
- [arkkitehtuurikuvaus](dokumentaatio/arkkitehtuuri.md)
- [testausdokumentti](dokumentaatio/testaus.md)
- [lähdeviite](dokumentaatio/lahdeviite.md)

## Käyttö
Komennot ajetaan ohjelman juuri kansiossa.

#### Asennus
```bash
poetry install
```
#### Käynnistys
```bash
poetry run invoke start
```
#### Testaus
```bash
poetry run invoke test
```
#### Testikattavuus
```bash
poetry run invoke coverage-report
```
#### Lint
```bash
poetry run invoke lint
```
#### Format
```bash
poetry run invoke format
```
