```mermaid
 classDiagram
    Monopolipeli "1" -- "2" Noppa
    Monopolipeli "1" -- "1" Pelilauta
    Pelilauta "1" -- "40" Ruutu
    Ruutu "1" -- "1" Ruutu : seuraava
    Ruutu "1" -- "0..8" Pelinappula
    Pelinappula "1" -- "1" Pelaaja
    Pelaaja "2..8" -- "1" Monopolipeli

	Ruutu  <|-- Aloitusruutu
	Ruutu  <|-- Vankila
	Ruutu  <|-- SattumaJaYhteismaa
	Ruutu  <|-- AsematJaLaitokset
	Ruutu  <|-- NormaalitKadut

	NormaalitKadut "1" -- "1" Nimi
	NormaalitKadut "1" -- "0..4" Talo
	NormaalitKadut "1" -- "0..1" Hotelli

	Monopolipeli "1" -- "1" Aloitusruutu
	Monopolipeli "1" -- "1" Vankila

	Ruutu "1" --> "1" Toiminto
	SattumaJaYhteismaa "1" --> "*" Kortti
	Kortti "1" --> "1" Toiminto

	Toiminto "1" --> "*" Toiminnot

	NormaalitKadut "*" -- "1" Pelaaja

	Pelaaja "1" --> "*" Raha
```