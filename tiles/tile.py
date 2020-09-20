from abc import ABC, abstractmethod


class Tile(ABC):

    def __init__(self):
        self.x = None
        self.y = None
        self.color = None
        self.variant = None

    def actualise(self, state):
        pass

    @abstractmethod
    def can_enter(self, character):
        pass

    def on_entrance(self, state, entity):
        pass

    def on_walk(self, state, entity):
        pass

    def on_interact(self, state, entity):
        pass
