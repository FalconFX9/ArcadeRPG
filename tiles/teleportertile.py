from tiles.tile import Tile


class TeleporterTile(Tile):
    def __init__(self):
        super().__init__()
        self.cx = 0
        self.cy = 0
        self.clevel = 0

    def can_enter(self, entity):
        return True

    def on_enter(self, state, entity):
        state.déplace_entité(entity, state.niveaux[self.clevel], self.cx, self.cy)
