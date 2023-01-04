from enum import Enum
import services
import pygame

from common import *

class SoundMixer:
    def __init__(self):
        self.now_playing = ""
    
    def setup(self):
        services.service_locator.event_handler.subscribe(self, Events.PAUSE_UNPAUSE)


    # play music if not already playing
    def play_music(self, music_id):
        if self.now_playing == music_id:
            return
        self.now_playing = music_id
        pygame.mixer.music.load(music_id.value)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.05)
    

    def stop_music(self):
        if self.is_playing():
            pygame.mixer.music.stop()
    

    def is_playing(self):
        return pygame.mixer.music.get_busy()


    def on_notify(self, event, arg):
        if event == Events.PAUSE_UNPAUSE:
            if arg: 
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
