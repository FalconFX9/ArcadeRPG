from tiles.tile import Tile


class ChestTile(Tile):
    def __init__(self):
        super().__init__()
        self.money = None
        self.items = []
        self.open = False

    def peut_entrer(self, entity):
        return False

    def sur_interaction(self, state, entity):
        pass