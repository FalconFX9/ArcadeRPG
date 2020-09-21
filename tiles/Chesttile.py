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
        inventory = entity.get_component(Inventory)
        if not self.open:
            if self.money:
                inventory.add_money(self.money)
            for id in self.items:
                inventory.add_item(state.item_set[int(id)])
            if state.levels[entity.get_component(Position).level.id].map1[self.mapx][self.mapy].variant == '1060':
                state.levels[entity.get_component(Position).level.id].map1[self.mapx][self.mapy].variant = '1062'
            else:
                state.levels[entity.get_component(Position).level.id].map2[self.mapx][self.mapy].variant = '1062'
            self.open = True
            state.force_update = True
