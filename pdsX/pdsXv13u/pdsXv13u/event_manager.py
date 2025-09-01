class EventManager:
    def __init__(self):
        self.events = {}

    def bind(self, event_name, handler):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(handler)

    def trigger(self, event_name):
        if event_name in self.events:
            for handler in self.events[event_name]:
                handler()