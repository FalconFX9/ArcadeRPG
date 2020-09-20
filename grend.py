import arcade
import constants as C
from arcade.gui import UIManager, UIFlatButton
from loadimageset import LoadImageSet


class Menu(arcade.View):

    def __init__(self, state, window: arcade.Window):
        super().__init__(window)
        self.window = window
        self.state = state
        self.background_img = None
        self.ui_manager = UIManager(self.window)

    def setup(self):
        self.background_img = arcade.load_texture(C.RESOURCES + 'Backgrounds/Menu.png')
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


class Map(arcade.View):

    def __init__(self, state, window: arcade.Window):
        super().__init__(window)
        self.state = state
        self.prev_coords = {}
        self.tiles = None
        self.entities = None

        self.image_loader = LoadImageSet()
        self.image_loader.load_tiles('tileset.png', 32, 32)

    def setup(self):
        self.tiles = arcade.SpriteList()
        self.entities = arcade.SpriteList()

    def on_level_change(self):
        position = self.state.player.get_component(Position)
        if not position:
            return
        for y in range(position.level.h - 1):
            for x in range(position.level.l):
                tile = position.level.map1[x][y]
                tile.x *= C.TILE_SIZE
                tile.y *= C.TILE_SIZE
                tile.texture = self.image_loader.obtain_tile(int(tile.variant))
                self.tiles.append(tile)
                tile = position.level.map2[x][y]
                if tile:
                    tile.x *= C.TILE_SIZE
                    tile.y *= C.TILE_SIZE
                    tile.texture = self.image_loader.obtain_tile(int(tile.variant))
                    self.tiles.append(tile)

    def on_update(self, delta_time: float):
        interpolation = delta_time / C.DT
        level = self.state.player.obtient_composant(Position).level

        for entity in self.state.entités:
            position = entity.obtient_composant(Position)
            sprite = entity.obtient_composant(Sprite)
            mouvement = entity.obtient_composant(GridMovement)

            # Seulement dessiner les entités avec un position et un sprite.
            if not position or not sprite or position.level != level:
                continue

            # Obtiens l'image appropriée.
            for image, condition in sprite.images.items():
                if condition(entity):
                    if mouvement.reload:
                        if 36 >= mouvement.reload >= 24:
                            id = 2
                        elif 24 > mouvement.reload >= 16:
                            id = 1
                        elif 16 > mouvement.reload >= 8:
                            id = 0
                        elif 8 > mouvement.reload >= 0:
                            id = 1
                    else:
                        id = 1
                    if type(image) is tuple:
                        img = image[id]
                    else:
                        img = image
                    break

            else:
                continue

            # Détermine la position en pixels.
            if self.state.state != C.PAUSE_STATE:
                x, y = self.state.calcule_position(entity, interpolation)
            else:
                x, y = self.prev_coords[entity]
            box = entity.obtient_composant(AlignedBox)
            if box:
                pos = (
                    int((x + box.minx + 0.5) * C.TILE_SIZE),
                    int((y + box.miny + 0.5) * C.TILE_SIZE)
                )
            else:
                l, h = img.get_size()
                pos = (
                    int((x + 0.5) * C.TILE_SIZE - 0.5 * l),
                    int((y + 0.5) * C.TILE_SIZE - 0.5 * h)
                )

            # Dessine l'image.
            entity = arcade.Sprite()
            entity.x = pos[0]
            entity.y = pos[1]
            entity.texture = img
            self.entities.append(entity)

            self.prev_coords[entity] = x, y

    def on_draw(self):
        arcade.start_render()
        self.tiles.draw()
        self.entities.draw()

