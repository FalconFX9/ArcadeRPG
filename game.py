import arcade
import constants as C
from grend import Menu, Map
from gamestate import GameState
from gstate import GState
from gworldfile import Gworldfile
from gitemfiles import Gitemfiles
from combatmechanic import CombatMechanic
import copy


class Game(arcade.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = GameState()
        self.state.init_levels = Gworldfile.load(C.WOLRD_SOURCE)
        self.state.item_set = Gitemfiles.load(C.ITEM_SOURCE)
        self.state.levels = copy.deepcopy(self.state.init_levels)
        self.menu = Menu(self.state, self)
        self.map = Map(self.state, self)
        self.gstate = GState(self.state)
        self.state.state = C.LEVEL_STATE
        self.map.gstate = self.gstate
        self.gstate.combat_mechanic = CombatMechanic(self.state)
        self.state.entity_factory.combat_mechanic = self.gstate.combat_mechanic


if __name__ == '__main__':
    game = Game(C.WIDTH, C.HEIGHT, C.TITLE, update_rate=C.DT)
    game.show_view(game.map)
    arcade.run()
