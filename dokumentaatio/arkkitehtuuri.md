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
    MainMenu <--> LevelListPlay["LevelList (Play)"]
    MainMenu <--> LevelListEditor["LevelList (Editor)"]
    MainMenu --> Exit

    LevelListPlay["LevelList (Play)"] --> Level
    LevelListEditor["LevelList (Editor)"] --> LevelEditor

    LevelEditor --> MainMenu

    Level --> MainMenu
    Level <--> EndScreen
    Level --> |retry|Level

    EndScreen --> MainMenu
  
```



