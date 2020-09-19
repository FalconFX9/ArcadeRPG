import arcade
import sys
import os
import constants as C
from arcade.gui import UIManager, UIFlatButton


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Menu(arcade.View):

    def __init__(self, state, window: arcade.Window):
        super().__init__(window)
        self.window = window
        self.state = state
        self.background_img = None
        self.ui_manager = UIManager(self.window)

    def setup(self):
        self.background_img = arcade.load_texture(resource_path(C.RESOURCES + 'Backgrounds/Menu.png'))
        self.ui_manager.purge_ui_elements()

        start = UIFlatButton('PLAY', self.window.width // 2, self.window.height // 2 - 115, 200, 125)

        start.set_style_attrs(font_color=arcade.color.WHITE,
                              font_color_hover=arcade.color.WHITE,
                              font_color_press=arcade.color.WHITE,
                              bg_color=arcade.color.GREEN,
                              bg_color_hover=(0, 150, 0),
                              bg_color_press=arcade.color.DARK_GREEN,
                              border_color_hover=arcade.color.WHITE,
                              border_color=arcade.color.GREEN,
                              border_color_press=arcade.color.WHITE)

        self.ui_manager.add_ui_element(start)

        @start.event('on_click')
        def play():
            self.state = 1
            print('GO!')

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, C.WIDTH, C.HEIGHT, self.background_img)
