from tiles.tile import Tile


class LeverTile(Tile):

    def __init__(self):
        super().__init__()
        self.clevel = None
        self.cx = None
        self.cy = None
        self.tile_alt = None

    def can_enter(self, entity):
        return True

    def on_enter(self, state, entity):
        map = state.levels[self.clevel].map

        actuel_tile = map[self.cx][self.cy]

        map[self.cx] = list(map[self.cx])

        map[self.cx][self.cy] = self.tile_alt

        self.tile_alt = actuel_tile
