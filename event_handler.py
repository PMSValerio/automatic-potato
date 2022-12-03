

class EventHandler:
    __instance = None

    def get():
        if EventHandler.__instance is None:
            EventHandler()
        return EventHandler.__instance

    def __init__(self):
        if EventHandler.__instance is not None:
            raise Exception("Singleton class already initialised")
        else:
            EventHandler.__instance = self

        self.listeners = {}
    
    def subscribe(self, listener, event):
        if event not in self.listeners:
            self.listeners[event] = []    
        self.listeners[event].append(listener)
    
    def unsubscribe(self, listener, event):
        if event in self.listeners:
            if listener in self.listeners[event]:
                self.listeners[event].remove(listener)
    
    def publish(self, event, args = None):
        for listener in self.listeners[event]:
            listener.on_notify(event, args)
