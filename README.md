tiny witch against big potato


## Game States

The game is designed with a main State Machine, in which each state corresponds to a game scene, using the State Pattern.
Every game state is stored in game_state.py and manages its own transitions to other game states.
- TitleState: simply shows the Title screen animation and can transition to either the Character Select screen or the Achievements screen, depending on player input.
- AchievementsState: displays all achievements, obscuring the names of those not yet unlocked.
- CharacterSelectState: in this state, the player chooses on of the two available skins to play with and maps controls to desired keys before advancing to the Level scene.
- LevelState: the state where the actual game takes place, spawning the different waves of enemies and giving control of the character to the player. Once the game ends, either because the player clears all waves and beats the boss, or because the player meets one of the lose conditions, the game transitions to the End Results state, in case of the former, or the Game Over screen, in case of the latter.
- GameOverState: simply displays the game over message and awaits player input before advancing to the End Results screen.
- EndResultsState: shows how the player performed according to the measures collected during the Level state, mainly score and potions remaining. Advances to Scoreboard screen
- ScoreboardState: displays the top ten saved scores. In case the player's score made it into the top ten, prompts the player to register their new entry with a 3-letter name, inputted in an arcade-like manner with the arrow keys. Once confirmed, the game ends and closes.

In the Main Loop in main.py, an update() and draw() methods are constantly called on the current game state to perform that state's tasks, ensuring the main loop does not require knowledge about each individual state's behaviour.

## Services

The game makes use of several different systems for managing and handling the different components of the engine.
These systems, or services, are globally accessed, initialised and managed via a service locator class which implements the Singleton Pattern, located in services.py.

## Entities
