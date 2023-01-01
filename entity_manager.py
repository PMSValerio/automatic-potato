from pygame.sprite import Group

from common import *
import services

class EntityManager:
    def __init__(self):
        self.entities = {}
        for layer in EntityLayers:
            self.entities[layer] = []

        self.remove_queue = [] # all entities are deleted at the end of the update at the same time
    
    # initialisations that depend on other services
    def setup(self):
        services.service_locator.event_handler.subscribe(self, Events.NEW_ENTITY)
        services.service_locator.event_handler.subscribe(self, Events.KILL_ENTITY)

    # add entity to register
    def add_entity(self, entity):
        if entity.col_layer in self.entities:
            if entity not in self.entities[entity.col_layer]: # sanity check
                self.entities[entity.col_layer].append(entity)
                services.service_locator.physics_engine.add_entity(entity)
    
    # queue entity for removal
    def remove_entity_request(self, entity):
        self.remove_queue.append(entity)
    
    # actually remove entity from register; this should never be called externally
    def _remove_entity(self, entity):
        if entity.col_layer in self.entities:
            if entity in self.entities[entity.col_layer]:
                services.service_locator.physics_engine.remove_entity(entity)
                self.entities[entity.col_layer].remove(entity)
    
    # return all entities in a list
    def get_all(self, exclude = []):
        return [entity for layer in self.entities for entity in self.entities[layer] if layer not in exclude]
    
    # call update on all entities, update physics and finally remove those on queue
    def update_all(self, delta):
        all_entities = self.get_all()
        
        # update all entities
        for entity in all_entities:
            last_pos = entity.pos.copy()
            entity._update(delta)
            services.service_locator.physics_engine.update_entity(entity, last_pos)
        
        # update physics
        services.service_locator.physics_engine.update_collisions()
        
        # remove all entities queued for removal
        for to_remove in self.remove_queue:
            self._remove_entity(to_remove)
    
    # call draw on all entities
    def draw_all(self, surface):
        all_entities = self.get_all([EntityLayers.VFX])
        all_entities.sort(key = lambda e : e.pos.y) # sort according to y coordinate, so that entities located above on the screen will be drawn first
        for entity in all_entities:
            entity.draw(surface)
        # visual effects are to be drawn above all other entities regardless of their y coordinate
        for entity in self.entities[EntityLayers.VFX]:
            entity.draw(surface)
    
    # remove all entities
    def clear(self):
        self.remove_queue.clear()
        for e in self.get_all():
            self._remove_entity(e)
    
    # event callback
    def on_notify(self, event, arg):
        if event == Events.NEW_ENTITY:
            self.add_entity(arg)
        elif event == Events.KILL_ENTITY:
            self.remove_entity_request(arg)
