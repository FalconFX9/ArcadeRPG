from tiles.tile import Tile


class ChestTile(Tile):
    def __init__(self):
        super().__init__()
        self.money = None
        self.items = []
        self.open = False

    def can_enter(self, character):
        return False

    def on_interact(self, state, entity):
        pass