from tiles.tile import Tile
from components.inventory import Inventory
from components.position import Position

class ChestTile(Tile):
    def __init__(self):
        super().__init__()
        self.money = None
        self.items = []
        self.open = False

    def can_enter(self, character):
        return False

    def on_interact(self, state, entity):
        inventory = entity.obtain_component(Inventory)
        if not self.open:
            if self.money:
                inventory.ajoute_argent(self.money)
            for id in self.items:
                inventory.add_item(entity.ensemble_items[int(id)])
            if state.levels[entity.obtain_component(Position).level.id].map1[self.x][self.y].variant == '1060':
                state.levels[entity.obtain_component(Position).level.id].map1[self.x][self.y].variant = '1062'
            else:
                state.levels[entity.obtain_component(Position).level.id].map2[self.x][self.y].variant = '1062'
            self.open = True