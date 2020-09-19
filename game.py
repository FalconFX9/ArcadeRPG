import arcade
import constants as C
from grend import Menu


class Game(arcade.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = None
        self.menu = Menu(self.state, self)


if __name__ == '__main__':
    game = Game(C.WIDTH, C.HEIGHT, C.TITLE, update_rate=C.DT)
    game.show_view(game.menu)
    arcade.run()
