# Arkkitehtuurikuvaus

## Pakkausrakenne
![Pakkausrakenne](./kuvat/pakkausrakenne.png)

**wrappers** sisältää pygame riippuvuuksien injektointia varten liittyvät luokat. (ennen, "di": "dependency injection"). Ei kovin merkityksellinen osa projektia.

Esimerkki sisältö: `clock.py`, `renderer.py`

**game** sisältää pelilogiikkaan liittyvät luokat, kuten fysiikat, animaatiot, tasojen tietorakenteet ja niiden käsittelyyn käytettävät osat. Näitä käytetään aktiivisesti pelin aikana.

Esimerkki sisältö: `map.py`, `body.py`, `sprite_animation.py`

**sprites** sisältää kaikki pelin sprite luokat. Kaikki oliot joilla on sijainti pelimaailmassa ja näkyvä komponentti kuuluvat tänne.

Esimerkki sisältö: `player.py`, `enemy.py`, `block.py`

**ui** kaikki käyttöliittymään liittyvät luokat, kuten LevelUI, EditorUI ja yksittäiset komponentit.

Esimerkki sisältö: `button.py`, `confirm_box.py`, `level_ui.py`

**scenes** sisältää kaikki sovelluksen eri tilat. Yksi scene yhdistää kaikki tilassa tarvittavan logiikan ja käyttöliittymän.

Esimerkki sisältö: `main_menu.py`, `level.py`, `end_screen.py`

**tools** hyödyllisiä yksittäisiä funktioita, pieniä luokkia ja esim. tietokannan käsittely.

Esimerkki sisältö: `asset_helpers.py`, `db.py`, `font_manager.py`

## Yleistä tietoa

Sovellus rakentuu itsenäisistä scene-luokista, joista kukin vastaa yhden sovelluksen tilan (esim. päävalikko, editori) hallinnasta.
GameLoop-luokka hallinnoi aktiivista sceneä ja vaihtaa scenejä, kun scene ilmoittaa olevansa valmis.
Scene-luokat käyttävät tarvittaessa apuluokkia oman tilansa piirtämiseen, pelaajan syötteiden käsittelyyn ja logiikan toteuttamiseen omassa tilassaan.
Tietokantaan tallennetaan esimerkiksi kenttien ja aikojen tiedot.
Pelissä näkyvät oliot (kuten pelaaja, vihollinen ja palikat) ovat kaikki sprites-kansion Sprite-olioita ja tarvittaessa käyttävät Body-luokkaa liikkumista ja muita fysiikoita varten.

### Esimerkki tiedon kulkemisesta

- Käyttäjän syötteet (näppäimistö, hiiri) välitetään GameLoopin kautta aktiiviselle Scene-oliolle.
- Scene käsittelee syötteet ja päivittää logiikkaa, esim. liikuttaa pelaajaa, lisää palikoita kenttään.
- Renderer piirtää ruudulle aktiivisen Scene-olion tarjoaman näkymän sen draw-metodin avulla.
- Kun Scene haluaa siirtyä seuraavaan tilaan, esim. päävalikosta tasolistaan, GameLoop vaihtaa aktiivisen Scene-olion.
- Tietokantaa käytetään tasojen ja aikojen hakemiseen.

## Luokkakaavio

Alla oleva luokkakaavio kuvaa sovelluksen keskeisten luokkien suhteet toisiinsa.
Scene-luokat perivät yhteisen Scene-pohjaluokan ja hallitsevat oman tilansa logiikkaa ja näkymää.
Lisäksi näkyvät tärkeimmät pelioliot ja niiden suhteet, kuten esim: Player ja Enemy, joilla molemmilla on Body liikkumista varten.

```mermaid
classDiagram
    GameLoop "1" --> "1" Scene

    Scene <|-- Level
    Scene <|-- LevelEditor
    Scene <|-- MainMenu
    Scene <|-- EndScreen
    Scene <|-- LevelList

    Level "1" --> "1" Map
    Level "1" --> "1" Timer
    Level "1" --> "1" Sprites
    Level "1" --> "1" LevelUI

    Sprites "1" --> "1" Player
    Sprites "1" --> "*" Enemy
    Sprites "1" --> "*" Blocks
    Sprites "1" --> "1" End
    Sprites "1" --> "1" Cursor

    Player "1" --> "1" Body
    Enemy "1" --> "1" Body

    LevelEditor "1" --> "1" Map
    LevelEditor "1" --> "1" EditorUI
    LevelEditor <..> db

    Timer <..> db

    LevelList <.. db
```

## Käyttöliittymä

Tämä kuvaa sovelluksen tilojen eli Scenejen välistä siirtymistä käyttäjän toiminnan perusteella.
Käyttäjä voi liikkua päävalikosta editoriin, tasolistaan, yksittäiseen tasoon ja tason suoritettua lopetustilaan.
Tilojen välillä liikkuminen tapahtuu aina aktiivisen Scene-olion kautta.

```mermaid
flowchart TD
    MainMenu <--> LevelListEditor["LevelList (Editor)"]
    MainMenu <--> LevelListPlay["LevelList (Play)"]
    MainMenu --> Exit

    LevelListEditor["LevelList (Editor)"] <--> LevelEditor
    LevelListPlay["LevelList (Play)"] <--> Level

    Level <--> EndScreen
    Level --> |retry|Level

    EndScreen --> LevelListPlay["LevelList (Play)"]
  
```

## Sekvenssikaaviot
Alla oleva kaavio kuvaa tyypillisen pelin aloitusprosessin tapahtumaketjun.
Se näyttää kuinka pelaajan syöte välittyy aktiiviselle Scene-oliolle, ja kuinka Scene vaihtuu taustalla GameLoopin ohjaamana.
Lisäksi kuvataan kuinka tietokantaa hyödynnetään tason tietojen hakemisessa ja kuinka Renderer vastaa piirtämisestä.

```mermaid
sequenceDiagram
    actor Pelaaja
    participant MainMenu
    participant GameLoop
    participant LevelList
    participant Level
    participant database
    participant Renderer

    Note over GameLoop: active scene: MainMenu
    Pelaaja->>GameLoop: click screen (at "Play")
    GameLoop->>MainMenu: input_mouse("left", pos)
    MainMenu->>MainMenu: set_next_scene("level_list", "level")
    GameLoop->>MainMenu: is_done()
    MainMenu-->>GameLoop: True
    GameLoop->>MainMenu: get_next_scene()
    MainMenu-->>GameLoop: ("level_list", "level")
    GameLoop->>LevelList: LevelList("level")
    Note over GameLoop: active scene: LevelList
    LevelList->>database: get_all_levels()
    database-->>LevelList: ([id, name, data])
    LevelList->>database: get_all_best_times()
    database-->>LevelList: ([id, time])
    GameLoop->>Renderer: render()
    Renderer->>LevelList: draw()
    Pelaaja->>GameLoop: click screen (at "Level 1")
    GameLoop->>LevelList: input_mouse("left", pos)
    LevelList->>LevelList: set_next_scene("level", level_data(id,name,[...]))
    GameLoop->>LevelList: is_done()
    LevelList-->>GameLoop: True
    GameLoop->>LevelList: get_next_scene()
    LevelList-->>GameLoop: ("level", {1, "Level 1", [...]})
    GameLoop->>Level: Level(level_data(1, "Level 1", [...])
    Note over GameLoop: active scene: Level
```
