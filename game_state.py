from common import *
import services

class GameState:
    def enter(self):
        pass

    def update(self, delta):
        raise NotImplementedError

    def exit(self):
        pass

    def draw(self, surface):
        raise NotImplementedError


class LevelState(GameState):
    def enter(self):
        from pygame import Vector2
        import test_entities
        services.service_locator.entity_manager.clear()
        test_entities.Test1(Vector2(WIDTH / 2 * SCALE, HEIGHT / 2 * SCALE))
        test_entities.Test2(Vector2(WIDTH / 2 * SCALE + SCALE * 3, HEIGHT / 2 * SCALE + SCALE * 3))
        test_entities.Test2(Vector2(WIDTH / 2 * SCALE - SCALE * 3, HEIGHT / 2 * SCALE - SCALE * 3))
    
    def update(self, delta):
        import random
        from pygame import Vector2
        import test_entities

        if random.random() < 0.01:
            xx = random.randrange(0, WIDTH * SCALE)
            yy = random.randrange(0, HEIGHT * SCALE)
            test_entities.Test2(Vector2(xx, yy))

        services.service_locator.entity_manager.update_all(delta)

    def exit(self):
        services.service_locator.entity_manager.clear()
    
    def draw(self, surface):
        surface.fill((220, 220, 220))
        services.service_locator.entity_manager.draw_all(surface)


class GameStateMachine:
    def __init__(self, states : dict, init_state : GameState):
        self.current_state : GameState = init_state
        self.current_state.enter()

        self.states = states

        services.service_locator.event_handler.subscribe(self, "new_game_state")
    
    def on_notify(self, event, arg):
        if event == "new_game_state":
            if arg in self.states:
                self.current_state.exit()
                self.current_state = self.states[arg]
                self.current_state.enter()
