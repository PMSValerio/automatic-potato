from enum import Enum
import pygame

from common import *

# text align (both vertical and horizontal)
class Align(Enum):
    BEGIN = 0
    CENTER = 1
    END = 2

fonts = {}


# all font sizes used in the game
def load_fonts():
    global fonts
    fonts = {
        16: pygame.font.Font("assets/font/Pokemon Classic.ttf", 16),
        32: pygame.font.Font("assets/font/Pokemon Classic.ttf", 32),
        24: pygame.font.Font("assets/font/Pokemon Classic.ttf", 24),
        48: pygame.font.Font("assets/font/Pokemon Classic.ttf", 48)
    }


class TextLabel:
    def __init__(self, text, x, y, valign, halign, size, colour = (255, 255, 255)):
        self.text = text # text to be displayed
        self.position = pygame.Vector2(x, y)
        self.valign = valign # horizontal align
        self.halign = halign # vertical align
        self.font = fonts[size] # font at selected size
        self.colour = colour

        self.render = None # the final rendered surface
        self.rect = None # surface rect

        self.set_colour(self.colour)
    

    # set text string and update position accordingly
    def set_text(self, text, x = None, y = None, colour = None):
        self.text = text
        self.render = self.font.render(self.text, True, self.colour if colour is None else colour)
        if colour is not None:
            self.colour = colour
        self.rect = self.render.get_rect()
        
        self.set_position(self.position.x if x is None else x, self.position.y if y is None else y)
    

    # update rect according to alignments
    def set_position(self, x, y):
        self.position.xy = x, y
        # horizontal
        if self.halign == Align.BEGIN:
            self.rect.left = x
        elif self.halign == Align.CENTER:
            self.rect.centerx = x
        elif self.halign == Align.END:
            self.rect.right = x
        
        # vertical
        if self.valign == Align.BEGIN:
            self.rect.top = y
        elif self.valign == Align.CENTER:
            self.rect.centery = y
        elif self.valign == Align.END:
            self.rect.bottom = y
    

    def set_colour(self, colour):
        self.colour = colour
        self.set_text(self.text)
    

    def draw(self, surface):
        surface.blit(self.render, self.rect)


class AchievementNotification:
    def __init__(self):
        self.on_dur = 2.5 # sec; time during which panel is visible
        self.on_timer = 0

        self.label = TextLabel("ACHIEVEMENT", WIDTH * 0.55, HEIGHT - BLOCK * 2.5, Align.BEGIN, Align.BEGIN, 24) # Achievement marker
        self.name = TextLabel("", WIDTH * 0.55, HEIGHT - BLOCK * 1.5, Align.BEGIN, Align.BEGIN, 16) # achievement text
        tl = self.label.rect.left - BLOCK / 2, self.label.rect.top - BLOCK / 2 # top-left corner
        self.rect = pygame.Rect(tl[0], tl[1], WIDTH - tl[0], HEIGHT - tl[1]) # panel container
    

    # make marker visible
    def turn_on(self, name):
        self.on_timer = self.on_dur
        self.name.set_text(name)
    

    # turn invisible after a while
    def update(self, delta):
        if self.on_timer > 0:
            self.on_timer -= delta
    
    
    def draw(self, surface):
        if self.on_timer > 0:
            pygame.draw.rect(surface, (40, 40, 40), self.rect)
            self.label.draw(surface)
            self.name.draw(surface)
