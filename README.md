tiny witch against big potato


### Game States

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

### Services

The game makes use of several different systems for managing and handling the different components of the engine.
These systems, or services, are globally accessed, initialised and managed via a service locator class which implements the Singleton Pattern, located in services.py.

## EventHandler

Located in event_handler.py. The game's implementation of the Observer pattern. It allows objects to subscribe to events defined in common.py. They can also publish said events along with an optional argument. Once this happens, the service calls a special on_notify() method on all subscribers, passing the event id and the argument.

## EntityHandler

Located in entity_handler.py. All entities in the game (player, enemies, projectiles, ...) are stored and managed in this service, which is responsible for updating and drawing all registered entities. Once a new entity is created or its die() method is called, it publishes an appopriate event, which the service handles by either adding or removing the entity to its registry.

## GroupSpace

Located in group_space.py. Responsible for detecting collisions between all entities. It is managed by the EntityManager, which calls its collisions update routine every frame and adds or removes entities from its registry. Using an entity's collision layer property, it stores it in the appropriate group (one for each layer). It defines pairs of colliding layers on startup and when updating collisions, checks every entitity against all others in a colliding layer, using pygame's sprite Groups. If a collision is detected, the service calls a collide() method on both entities, passing the other as an argument.

## GameInput

Located in game_input.py. A helper service to better handle input. By storing both the result from get_pressed() from pygame in the current frame and the one in the previous frame, it is possible to poll pressed, hold, and release key actions.

## GraphicsLoader

Located in graphics_loader.py. This service is responsible for handling loading of texture images and handling spritesheets. It ensures each image and animation strip is only loaded once, using the Flyweight pattern.

## SoundMixer

Located in sound_mixer.py. A helper service for playing and stopping music, using pygame's mixer functionality.

## AchievementsTracker

Located in achievements_tracker.py. Making heavy use of events, this services listens to any updates to one of its achievements conditions and stores them and notifies the player when necessary. By using events, it is decoupled from actual game logic.

## EnemyHandler

<!-- TODO -->

## EnemyData

<!-- TODO -->

## PlayerData

Located in player_data.py. Although not managed by the services singleton, this object, itself a singleton, is globally accessed and is meant to manage player specific data which persists through different game states, such as score, controls and selected skin.

### Entities

Each actor in the game extends a generic Entity class (located in entity.py), which extends pygame's Sprite class.

This class sets up basic data and methods to be used by other services and objects, such as spatial orientation (position, rotation, ...). It also automatically sends events when created and destroyed. The most important methods are update() and draw(), which are to be called every frame, responsible, respectively, for updating game logic, receiving the time elapsed since the last call, via the delta argument and for drawing the entity on the passed surface argument, which must be a pygame Surface.

## Player and Enemies

Both the player and enemies make use of a State Machine to handle their complex logic.

# Player Stats

The game allows for one of two skins to be selected for the player character. This skins also differ in their stats (movement speed, health, ...). In order to achieve this, the Player object (player.py) must retrieve its stats from PlayerData, making use of a TypeObject for each of the available skins.

To handle player input, the class uses Commands for each of the available actions (move in four directions and shoot). The actual key used for each action is defined in PlayerData.

# Enemy Stats ?

<!-- TODO? -->

## Remaining Entities

For other entities not as complex as the player or entities, 

### GUI

A few GUI elements have been created to simplify drawing of text and panels in UI, located in gui_utils.py. These include the TextLabel which is a uniform object capable of drawing text in different font sizes, colours, and alignments in different positions and the Achievement notification which disappears a short while after being made visible.
