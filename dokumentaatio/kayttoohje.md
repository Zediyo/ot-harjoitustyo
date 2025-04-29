# Käyttöohje

Lataa uusin release tästä linkistä

## Ohjelman käynnistys

Varmista että koneellasi on python 3.10 tai uudempi ja poetry asennettuna.

Ensimmäisellä kerralla suoritä seuraava komento juurikansiossa.

```bash
poetry install
```

Nyt voit käynnistää pelin suorittamalla komennon

```bash
poetry run invoke start
```
## Pelin aloittaminen, pelitila ja lopetus

Käynnistämisen jälkeen olet aloitusruudussa. Valitse "Play".

![peli1](./kuvat/peli1.png)

Nyt olet pelitilan tasovalikossa. Valitse taso jota haluat pelata tai "Back" jos haluat siirtyä takaisin edelliseen näkymään.
Tasojen nimi näkyy napissa josta siirryt pelitilaan. Nimen yläpuolella näkyy joko vihreällä nopein suoritusaika tasossa tai punaisella "--:--" jos tasossa ei ole suoritusta vielä.

![peli2](./kuvat/peli2.png)

Pelissä on punaisia palikoita joiden läpi ei voi kulkea, sinisiä palkoita joita voit kerätä ja asettaa kentälle.
Viholliseen osuessa taso alkaa alusta ja maaliin päästyä peli päättyy.
Ylhäällä näet myös tason nimen, kuinka monta palikkaa sinulla on käytettävissä ja suorituksen ajan.
Back nappulasta pääset takaisin tasolistaan.

![peli3](./kuvat/peli3.png)

Maaliin päästyä olet lopetusruudussa jossa voit palata takaisin tasolistaan tai pelata saman tason uudestaan.
Keskellä näet myös tason suorituksen ajan ja parhaan ajan.

![peli4](./kuvat/peli4.png)