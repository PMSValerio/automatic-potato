import pygame

from common import *

class GroupSpace:
    __instance = None

    def get():
        if GroupSpace.__instance is None:
            GroupSpace()
        return GroupSpace.__instance

    def __init__(self):
        if GroupSpace.__instance is not None:
            raise Exception("Singleton class already initialised")
        else:
            GroupSpace.__instance = self
        
    def init(self):
        self.layers = {}
        for layer in EntityLayers:
            self.layers[layer] = pygame.sprite.Group()
        
        self.collisions = [] # list of pairs of layers that should be scanned for collisions
        self.add_collision(EntityLayers.PLAYER, EntityLayers.OBSTACLE)
    
    # add entity to space
    def add_entity(self, entity):
        if entity.col_layer in self.layers:
            self.layers[entity.col_layer].add(entity)
    
    # update entity in space
    def update_entity(self, entity, last_pos):
        pass # not needed with groups
    
    # remove entity from space
    def remove_entity(self, entity):
        self.layers[entity.col_layer].remove(entity)

    # add collision event between layer1 and layer2
    def add_collision(self, layer1, layer2):
        self.collisions.append((layer1, layer2))
    
    # check for collisions
    def update_collisions(self):
        for pair in self.collisions:
            col_dict = pygame.sprite.groupcollide(self.layers[pair[0]], self.layers[pair[1]], False, False)
            for e1 in col_dict.keys():
                for e2 in col_dict[e1]:
                    e1.collide(e2)
                    e2.collide(e1)
    
    # clear all entities
    def clear(self):
        for group in self.layers.values():
            group.clear()

    # test collisions for a specific sprite
    def sprite_is_collision(self, spr, layer_mask : list):
        for group in [self.layers[l] for l in self.layers.keys() if l in layer_mask]:
            return pygame.sprite.spritecollideany(spr, group)
