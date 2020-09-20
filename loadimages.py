import arcade
import constants as C


class LoadImages:
    def __init__(self):
        self.images = {}

    def load(self, id, name_of_file):
        img = arcade.load_texture(C.RESOURCES + name_of_file)
        self.images[id] = arcade.Sprite()
        self.images[id].texture = img

    def resize(self, id, x, y):
        self.images[id].width = x
        self.images[id].height = y

    def obtain(self, id):
        return self.images[id]