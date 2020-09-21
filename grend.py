import arcade
import copy
import constants as C
from arcade.gui import UIManager, UIFlatButton
from loadimageset import LoadImageSet
from loadimages import LoadImages
from components.controllable import Controllable
from components.gridmouvement import GridMovement
from components.orientable import Orientable
from components.position import Position
from components.player import Player
from components.loopedai import LoopedAi
from components.randomai import RandomAi
from components.ephemeral import Ephemeral
from components.dialogue import Dialogue
from components.merchant import Merchant
from components.initiatecombat import InitiateCombat
from components.stats import Stats
from components.inventory import Inventory
from components.sprite import Sprite
from components.alignedbox import AlignedBox
from entityfactory import EntityFactory


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
        self.tiles2 = None
        self.entities = None
        self.gstate = None
        self.current_level = None

        self.state.image_loader = LoadImages()
        self.state.image_loader.load('Target', 'GraphicalInterface/Crosshair.png')
        self.state.image_loader.load('TargetTr', 'GraphicalInterface/CrosshairTransparency.png')
        self.state.image_loader.load('Menu1', 'GraphicalInterface/AttackMenu.png')
        self.state.image_loader.load('Dialogue', 'GraphicalInterface/DialogueEtendu.png')
        self.state.image_loader.load('Combat_player', 'Entities/BigSoldier.png')
        self.state.image_loader.load('Attacked_player', 'Entities/BigSoldierDmg.png')
        self.state.image_loader.load('Bat', 'Entities/pipo-enemy001.png')
        self.state.image_loader.load('BlackGhost', 'Entities/pipo-enemy010b.png')
        self.state.image_loader.load('SkelSoldier', 'Entities/pipo-enemy026.png')
        self.state.image_loader.load('BlueOrb', 'Entities/pipo-enemy012a.png')
        self.state.image_loader.load('DarkSoldier', 'Entities/pipo-enemy018b.png')
        self.state.image_loader.load('Skeleton', 'Entities/pipo-enemy039.png')
        self.state.image_loader.load('Devil', 'Entities/pipo-enemy040.png')
        self.state.image_loader.load('Wolf', 'Entities/pipo-enemy002a.png')
        self.state.image_loader.load('Boss', 'Entities/pipo-boss002.png')

        self.state.image_loader.resize('Target', 48, 48)
        self.state.image_loader.resize('TargetTr', 48, 48)
        self.state.image_loader.resize('Combat_player', 92, 128)
        self.state.image_loader.resize('Attacked_player', 92, 128)
        self.state.image_loader.resize('Bat', 320, 320)
        self.state.image_loader.resize('BlackGhost', 260, 260)
        self.state.image_loader.resize('SkelSoldier', 160, 160)
        self.state.image_loader.resize('BlueOrb', 280, 280)
        self.state.image_loader.resize('DarkSoldier', 160, 160)
        self.state.image_loader.resize('Skeleton', 160, 160)
        self.state.image_loader.resize('Devil', 200, 200)
        self.state.image_loader.resize('Wolf', 180, 180)
        self.state.image_loader.resize('Boss', 426, 200)

        image_loader = LoadImageSet()
        image_loader.load_entities('Player', 'Entities/Soldier 01-1.png', 32, 32, 3, 12)
        image_loader.load_entities('Mr Chad', 'Entities/Male 01-1.png', 32, 32, 3, 12)
        image_loader.load_entities('NPC Intro', 'Entities/Male 04-1.png', 32, 32, 3, 12)
        image_loader.load_entities('BlackGhost', 'Entities/Enemy 15-1.png', 32, 32, 3, 12)
        image_loader.load_entities('SkelSoldier', 'Entities/Enemy 04-1.png', 32, 32, 3, 12)
        image_loader.load_entities('BlueOrb', 'Entities/Enemy 16-5.png', 32, 32, 3, 12)
        image_loader.load_entities('DarkSoldier', 'Entities/Enemy 05-1.png', 32, 32, 3, 12)
        image_loader.load_entities('Skeleton', 'Entities/Enemy 06-1.png', 32, 32, 3, 12)
        image_loader.load_entities('Wolf', 'Entities/Dog 01-3.png', 32, 32, 3, 12)
        image_loader.load_entities('Boss', 'Entities/Boss 01.png', 288, 288, 3, 12)
        self.state.entity_factory = EntityFactory(self.state, image_loader, self.state.image_loader)

        self.image_loader = LoadImageSet()
        self.image_loader.load_tiles('tileset.png', 32, 32)
        self.image_loader.load_items('roguelikeitems.png', 16, 16)
        self.image_loader.load_animations('Guérir', 'heal_003.png', 192, 192)

    def on_show_view(self):
        self.setup()

    def setup(self):
        self.tiles = arcade.SpriteList()
        self.tiles2 = arcade.SpriteList()
        self.entities = arcade.SpriteList()
        self.on_level_change()

    def __interaction(self):
        orientable = self.state.player.get_component(Orientable)
        tuile = self.gstate.calculate_target_tile(self.state.player, orientable.orientation)
        for entity in self.state.entities:
            position = entity.get_component(Position)
            dialogue = entity.get_component(Dialogue)
            combat = entity.get_component(InitiateCombat)
            if position.x == tuile.mapx and position.y == tuile.mapy and position.level == self.state.player.get_component(
                    Position).level:
                if dialogue:
                    dialogue.sur_interaction(entity, self.state.player)
                    merchant = entity.get_component(Merchant)
                    if dialogue.conteur >= len(dialogue.dialogue) + 1:
                        if merchant:
                            merchant.on_exchange(self.state.player)
                            if dialogue.conteur >= len(dialogue.dialogue) + len(merchant.missing_item) + 1:
                                if None in merchant.missing_item:
                                    merchant.items_manquants.remove(None)
                                dialogue.active = False
                                dialogue.counter = 0
                                merchant.dialogue = None
                            else:
                                dialogue.counter += 1
                        else:
                            dialogue.counter = 0
                            dialogue.active = False
                elif combat:
                    self.state.combat_launch_entity = entity
                    combat.on_interact(self.state)
                    for entity in combat.combat_entities.values():
                        entity.get_component(Stats).reinit_HP()
                    self.gstate.combat_mechanic.enemies = copy.copy(combat.combat_entities)
                    if self.gstate.combat_mechanic.enemies[0].id == 'Boss':
                        self.gstate.combat_mechanic.enemies[1] = self.gstate.mécanique_combat.ennemis.pop(0)

        tuile.sur_interaction(self.state, self.state.player)

    def on_level_change(self):
        level = self.state.player.get_component(Position).level
        self.current_level = level
        for entity_2 in self.state.entities:
            if level == entity_2.get_component(Position).level:
                self.entities.append(arcade.Sprite())
        position = self.state.player.get_component(Position)
        if not position:
            return
        for y in range(position.level.h - 1):
            for x in range(position.level.l):
                tile = position.level.map1[x][y]
                tile.texture = self.image_loader.obtain_tile(int(tile.variant))
                tile.center_x = (tile.mapx * C.TILE_SIZE - (C.TILE_SIZE // 2))
                tile.center_y = (C.HEIGHT + C.TILE_SIZE // 2) - tile.mapy * C.TILE_SIZE
                self.tiles.append(tile)
                tile = position.level.map2[x][y]
                if tile:
                    tile.texture = self.image_loader.obtain_tile(int(tile.variant))
                    tile.center_x = tile.mapx * C.TILE_SIZE - C.TILE_SIZE + 16
                    tile.center_y = C.HEIGHT - (tile.mapy * C.TILE_SIZE) + 16
                    self.tiles2.append(tile)

    def on_key_press(self, symbol: int, modifiers: int):
        controllable = self.state.player.get_component(Controllable)
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            controllable.force = C.DIRECTION_N
        elif symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            controllable.force = C.DIRECTION_E
        elif symbol == arcade.key.S or symbol == arcade.key.DOWN:
            controllable.force = C.DIRECTION_S
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            controllable.force = C.DIRECTION_O
        elif symbol == arcade.key.SPACE:
            self.__interaction()

    def on_key_release(self, symbol: int, modifiers: int):
        controllable = self.state.player.get_component(Controllable)
        if controllable:
            force = controllable.force
            if ((symbol == arcade.key.W or symbol == arcade.key.UP) and force == C.DIRECTION_N) or \
                    ((symbol == arcade.key.S or symbol == arcade.key.DOWN) and force == C.DIRECTION_S) or \
                    ((symbol == arcade.key.A or symbol == arcade.key.LEFT) and force == C.DIRECTION_O) or \
                    ((symbol == arcade.key.D or symbol == arcade.key.RIGHT) and force == C.DIRECTION_E):
                controllable.force = 0

    def on_update(self, delta_time: float):
        interpolation = delta_time / C.DT
        level = self.state.player.get_component(Position).level
        if self.current_level != level:
            self.setup()
        counter = 0
        for num, entity in enumerate(self.state.entities):
            position = entity.get_component(Position)
            sprite = entity.get_component(Sprite)
            mouvement = entity.get_component(GridMovement)

            if not position or not sprite or position.level != level:
                continue

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

            if self.state.state != C.PAUSE_STATE:
                x, y = self.state.calculate_position(entity, interpolation)
            else:
                x, y = self.prev_coords[entity]
            box = entity.get_component(AlignedBox)
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

            if len(self.entities) > len(self.state.entities):
                self.entities = arcade.SpriteList()
                for entity_2 in self.state.entities:
                    if level == entity_2.get_component(Position).level:
                        self.entities.append(arcade.Sprite())
            self.entities[counter].center_x = pos[0] - 16
            self.entities[counter].center_y = C.HEIGHT - pos[1] + 16
            self.entities[counter].texture = img

            self.prev_coords[entity] = x, y

            self.gstate.update()
            counter += 1

    def on_draw(self):
        arcade.start_render()
        self.tiles.draw()
        self.tiles2.draw()
        self.entities.draw()
