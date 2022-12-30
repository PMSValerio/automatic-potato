from common import *

class NoEventException(Exception):
    def __init__(self, event):
        super().__init__("Non-existent event: " + str(event))


class EventHandler:

    def __init__(self):
        self.listeners = {}
        for event in Events:
            self.listeners[event] = []
    
    def subscribe(self, listener, event):
        if event not in self.listeners:
            raise NoEventException(event)
        self.listeners[event].append(listener)
    
    def unsubscribe(self, listener, event):
        if event in self.listeners:
            if listener in self.listeners[event]:
                self.listeners[event].remove(listener)
    
    def publish(self, event, args = None):
        if event not in self.listeners:
            raise NoEventException(event)
        for listener in self.listeners[event]:
            listener.on_notify(event, args)
