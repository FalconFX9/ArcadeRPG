import arcade
import constants as C


class Load_images(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self.images = {}

    def load(self, id, name_of_file):
        img = arcade.load_texture(C.RESSOURCES + name_of_file)
        self.images[id] = img.convert_alpha()

    def obtains(self, id):
        return self.images[id]