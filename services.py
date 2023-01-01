import event_handler
import entity_manager
import group_space
import game_input
import graphics_loader
import enemy_handler
import enemy_data

# holds and manages all relevant services/systems
class Services:
    __instance = None

    def get():
        if Services.__instance is None:
            Services()
        return Services.__instance

    def __init__(self):
        if Services.__instance is not None:
            raise Exception("Singleton class already initialised")
        else:
            Services.__instance = self
    
        self.event_handler : event_handler.EventHandler = event_handler.EventHandler()
        self.entity_manager : entity_manager.EntityManager = entity_manager.EntityManager()
        self.physics_engine : group_space.GroupSpace = group_space.GroupSpace()
        self.game_input : game_input.GameInput = game_input.GameInput()
        self.graphics_loader : graphics_loader.GraphicsLoader = graphics_loader.GraphicsLoader()
        self.enemy_handler : enemy_handler.EnemyHandler = enemy_handler.EnemyHandler()
        self.enemy_data : enemy_data.EnemyData = enemy_data.EnemyData()

    def setup(self):
        self.entity_manager.setup()
        self.enemy_handler.setup()
    
service_locator : Services = None
