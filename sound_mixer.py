from enum import Enum
import pygame

from common import *

class SoundMixer:
    def __init__(self):
        self.now_playing = ""
    
    def play_music(self, music_id):
        if self.now_playing == music_id:
            return
        self.now_playing = music_id
        pygame.mixer.music.load(music_id)
        pygame.mixer.music.play(-1)
    
    def stop_music(self):
        if self.is_playing():
            pygame.mixer.music.stop()
    
    def is_playing(self):
        return pygame.mixer.music.get_busy()
