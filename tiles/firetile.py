import constants as C
from tiles.tile import Tile
from components.player import Player


class FireTile(Tile):
    def __init__(self):
        super().__init__()

    def can_enter(self, entity):
        return True

    def on_entrance(self, state, entity):
        if entity.contains_component(Player):
            state.state = C.FAILURE_STATE
