# Arkkitehtuurikuvaus

## Pakkausrakenne
![Pakkausrakenne](./kuvat/pakkausrakenne.png)

**wrappers** sisältää pygame riippuvuuksien injektointia varten liittyvät luokat. (ennen, "di": "dependency injection")

**game** sisältää aktiivisen pelin aikana käytettäviä luokkia joille ei ole omaa kategoriaa.

**sprites** kaikki pelin objectit jotka voivat näkyä ruudulla.

**ui** käyttöliittymään liittyvät luokat.

**scenes** sisältää kaikki sovelluksen eri tilat. Yksi scene yhdistää kaikki tilassa tarvittavan logiikan ja käyttöliittymän

**tools** hyödyllisiä yksittäisiä funktioita ja tietokannan käsittely.

## Luokkakaavio

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
Kulku sovelluksen tiloissa:
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
Pelin aloitus

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
    GameLoop->>MainMenu: get_next_scene()
    GameLoop->>MainMenu: cleanup()
    GameLoop->>LevelList: LevelList("level")
    Note over GameLoop: active scene: LevelList
    LevelList->>database: get_all_levels()
    LevelList->>database: get_all_best_times()
    GameLoop->>Renderer: render()
    Renderer->>LevelList: draw()
    Pelaaja->>GameLoop: click screen (at "Level 1")
    GameLoop->>LevelList: input_mouse("left", pos)
    LevelList->>LevelList: set_next_scene("level", level_data(id,name,[...]))
    GameLoop->>LevelList: is_done()
    GameLoop->>LevelList: get_next_scene()
    GameLoop->>LevelList: cleanup()
    GameLoop->>Level: Level(level_data(1, "Level 1", [...])
    Note over GameLoop: active scene: Level
```
