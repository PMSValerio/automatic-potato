from common import *

class NoEventException(Exception):
    def __init__(self, event):
        super().__init__("Non-existent event: " + str(event))

# manage events by allowing listeners to subscribe/unsubscribe and/or publish to a 
class EventHandler:
    def __init__(self):
        self.listeners = {}
        for event in Events:
            self.listeners[event] = []
    

    def subscribe(self, listener, event):
        # raise exception if this event is not listed
        if event not in self.listeners:
            raise NoEventException(event)

        # add listener to list    
        self.listeners[event].append(listener)
    

    def unsubscribe(self, listener, event):
        # check if event is listed, if listener is subscribed and then unsub 
        if event in self.listeners:
            if listener in self.listeners[event]:
                self.listeners[event].remove(listener)
    

    def publish(self, event, args = None):
        # raise exception if this event is not listed
        if event not in self.listeners:
            raise NoEventException(event)
        
        # notify all listeners subscribed this event
        for listener in self.listeners[event]:
            listener.on_notify(event, args)
