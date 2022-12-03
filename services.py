import event_handler
import entity_manager
import group_space

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
    
        self.event_handler : event_handler.EventHandler = event_handler.EventHandler.get()
        self.entity_manager : entity_manager.EntityManager = entity_manager.EntityManager.get()
        self.physics_engine : group_space.GroupSpace = group_space.GroupSpace.get()
    
    def setup(self):
        self.entity_manager.init()
        self.physics_engine.init()
    
service_locator : Services = None
