from tiles.tile import Tile


class TerrainTile(Tile):
    def __init__(self):
        super().__init__()
    def can_enter(self, entity):
        return True