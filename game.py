import arcade
import constants as C
from grend import Menu, Map
from gamestate import GameState
from gstate import GState
from gworldfile import Gworldfile
from gitemfiles import Gitemfiles
import copy


class Game(arcade.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = GameState()
        self.state.init_levels = Gworldfile.load(C.WOLRD_SOURCE)
        self.state.levels = copy.deepcopy(self.state.init_levels)
        self.gstate = GState(self.state)
        self.menu = Menu(self.state, self)
        self.map = Map(self.state, self.gstate, self)
        self.state.state = C.LEVEL_STATE


if __name__ == '__main__':
    game = Game(C.WIDTH, C.HEIGHT, C.TITLE, update_rate=C.DT)
    game.show_view(game.map)
    arcade.run()
