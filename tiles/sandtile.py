from tiles.tile import Tile
from components.gridmouvement import GridMovement


class SandTile(Tile):
    def __init__(self):
        super().__init__()

    def can_enter(self, character):
        return True

    def on_walk(self, state, entity):
        movement = entity.get_component(GridMovement)
        if movement:
            movement.speed *= 0.5
