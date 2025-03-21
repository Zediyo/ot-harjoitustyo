# Sovelluksen tarkoitus
2d tasohyppely peli jossa voidaan luoda omia tasoja.

# Suunnitellut toiminnallisuudet

## Perusversio

- Aloitusruutu josta voi valita pelattavan tason tai tehdä/muokata oman.
		
- Pelissä on perus vasen/oikea liikkuminen ja hyppiminen.
	- A/D/space input
	- gravity + collision detection
	
- Pelissä voi asetella omia paloja kenttään.
	- mouse1 add, mouse2 remove
	- max range 3 block length (add + remove)
	- max active limit (level specific + item pickups)
	
- Pelissä on liikkuvia "vihollisia"

- Peli ottaa aikaa tasojen suorituksesta ja tallentaa ne.
	- SQL db
	
- Pelissä voi tehdä omia tasoja (editor)
	- mouse1 add object, mouse2 remove object
	- custom level config (gravity, start values, ...)
	- save as files

## Jatkokehitysideoita

- -