from tiles.tile import Tile
from components.position import Position
from components.gridmouvement import GridMovement
from components.inventory import Inventory


class WaterTile(Tile):
    def __init__(self):
        super().__init__()

    def can_enter(self, entity):
        inventory = entity.get_component(Inventory)
        if 132 in inventory.inventory.keys():
            return True
        else:
            return True

    def on_entrance(self, state, entity):
        movement = entity.get_component(GridMovement)
        if movement:
            movement.speed *= 0.8
        """
        position = entité.obtient_composant(Position)
        mouvement = entité.obtient_composant(MouvementGrille)
        if position and mouvement:
            mouvement.recharge = mouvement.coût
            mouvement.sx = mouvement.cx = position.x
            mouvement.sy = mouvement.cy = position.y
        """
