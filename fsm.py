class FSM:
    def __init__(self):
        self.state_handlers = {}

        self.state = -1
        self.next = -1
    
    # adds a state and assigns it the handler to be called when changing to said state
    def add_state(self, state, handler, set_start = False):
        self.state_handlers[state] = handler
        
        if set_start:
            self.state = self.next = state
    

    def change_state(self, state):
        if state in list(self.state_handlers.keys()):
            self.next = state


    def update(self):
        transition = self.state != self.next
        if transition:
            key_list = list(self.state_handlers.keys())
            self.state = self.next if self.next in key_list else key_list[0] # sanity check

        if self.state_handlers[self.state] is not None:
            self.state_handlers[self.state](transition)
