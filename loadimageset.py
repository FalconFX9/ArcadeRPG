import arcade
import constants as C


class LoadImageSet:

    def __init__(self):
        self.tiles = []
        self.items = []
        self.entity_images = {}
        self.animations = {}

    @staticmethod
    def __load(image_set, width, height):
        image = arcade.load_texture(C.RESOURCES + image_set)
        img_x = image.width
        img_y = image.height
        locations = []
        for image_y in range(0, int(img_y / height)):
            for image_x in range(0, int(img_x / width)):
                locations.append((image_x * width, image_y * height, width, height))
        images = arcade.load_textures(C.RESOURCES + image_set, locations)
        return images, locations

    @staticmethod
    def __load_2d(spritesheet, sp_width, sp_height, columns, count, margin=0):
        images = arcade.load_spritesheet(C.RESOURCES + spritesheet, sp_width, sp_height, columns, count, margin)
        x_axis = []
        for x in range(count//columns):
            rows = []
            x_axis.append(rows)
            for y in range(x * columns, x * columns + columns):
                rows.append(images[y])

        return x_axis

    def load_tiles(self, tileset, width, height):
        self.tiles = self.__load(tileset, width, height)

    def load_items(self, itemset, width, height):
        self.items = self.__load(itemset, width, height)

    def load_animations(self, id, imageset, width, height):
        self.animations[id] = self.__load(imageset, width, height)

    def load_entities(self, id, spritesheet, sp_width, sp_height, columns, count):
        self.entity_images[id] = self.__load_2d(spritesheet, sp_width, sp_height, columns, count)

    def obtain_tile(self, id):
        return self.tiles[id]

    def obtain_item(self, id):
        return self.items[id]

    def obtain_animation(self, id):
        return self.animations[id]

    def obtain_entity(self, id, orientation):
        return self.entity_images[id][orientation]
