from abc import ABC, abstractmethod
import arcade


class Tile(ABC, arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.mapx = None
        self.mapy = None
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
