import constants as C
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
from entityfactory import EntityFactory
import random
import copy


class GameState:

    def __init__(self):
        self.dt = C.DT
        self.state = C.LEVEL_STATE
        self.entity_factory = None

        self.levels = None
        self.player = None
        self.item_set = None
        self.entities = []
        self.entities_to_destroy = set()
        self.destroyed_entities = []
        self.combat_launch_entities = None
        self.buttons = {}
        self.target_buttons = []
        self.inventory_buttons = []

        self.image_loader = None

        self.init_levels = None

    def create_buttons(self):
        self.bouttons['Attaque'] = Boutton(34, 242, 106, 30, 'Attaque', (255, 255, 255, 0), (255, 255, 255, 128))
        self.bouttons['Guérir'] = Boutton(34, 272, 106, 30, 'Guérir', (255, 255, 255, 0), (255, 255, 255, 128))
        self.bouttons['Fuir'] = Boutton(34, 302, 106, 30, 'Fuir', (255, 255, 255, 0), (255, 255, 255, 128))
        self.bouttons['Jouer'] = Boutton(261, 394, 182, 126, 'Jouer', (255, 255, 255, 0), (255, 255, 255, 128))
        self.bouttons_cible.append(Boutton(486, 86, 48, 48, None, None, None))
        self.bouttons_cible.append(Boutton(496, 206, 48, 48, None, None, None))
        self.bouttons_cible.append(Boutton(506, 326, 48, 48, None, None, None))
        self.bouttons_cible.append(Boutton(516, 446, 48, 48, None, None, None))
        for x in range(10):
            self.inventory_buttons.append(Boutton((x * 20) + 32, 552, 16, 16, None, (255, 255, 255, 0), (255, 255, 255, 128)))

    def calculate_start_position(self, mode, coords):
        # Définir la position.
        print(mode, coords)
        if mode == C.INITIAL_PLAYER_RECTANGLE:
            x1, y1 = coords[0]
            x2, y2 = coords[1]
            x = random.randint(x1, x2)
            y = random.randint(y1, y2)
        elif mode == C.INITIAL_PLAYER_TILE:
            x, y = random.choice(coords)
        else:
            x, y = 10, 13

        return x, y

    def destroy_entity(self, entity):
        self.entities_to_destroy.add(entity)
        if entity.id is not None and entity.id not in self.destroyed_entities:
            self.destroyed_entities.append(entity.id)

    def calculate_position(self, entity, interpolation=0):
        position = entity.get_component(Position)
        if not position:
            return None, None

        movement = entity.get_component(GridMovement)
        if movement and movement.reload is not None:
            interp_mvt = min(1 - (movement.reload - movement.speed * interpolation) / movement.cost, 1)

            return (movement.sx * (1 - interp_mvt) + movement.cx * interp_mvt), \
                (movement.sy * (1 - interp_mvt) + movement.cy * interp_mvt)

        return position.x, position.y

    def in_movement(self, entity):
        movement = entity.get_component(GridMovement)
        if movement and movement.reload is not None:
            return True

        orientable = entity.get_component(Orientable)
        if orientable and orientable.reload is not None:
            return True

        return False

    def prepare_entities(self, level, init=False):
        def positioned_enj(entity):
            position = entity.get_component(Position)

            return not position or not position.level or entity.contains_component(Player) or entity.contains_component(Ephemeral)

        self.entities = list(filter(positioned_enj, self.entities))
        for data in level.entities_init:
            if 'ephemeral' not in data.keys() or ('ephemeral' in data.keys() and init):
                entity_type = data['type']
                entity = self.entity_factory.create(entity_type)
                self.entities.append(entity)
                x, y = None, None
                if 'position' in data:
                    x, y = self.calculate_start_position(data['position'], data['position_coords'])

                if 'ephemeral' in data:
                    entity.add_component(Ephemeral())
                    if entity.id:
                        entity.id = (entity.id, data['ephemeral'])
                    else:
                        entity.id = data['ephemeral']

                if 'dialogue' in data:
                    entity.add_component(Dialogue(data['dialogue']))

                if 'merchant' in data:
                    entity.add_component(Merchant())
                    merchant = entity.get_component(Merchant)
                    for id in data['merchant'][0]:
                        item = self.item_set[int(id)]
                        merchant.requested_item[item.id] = item
                    for id in data['merchant'][1]:
                        item = self.item_set[int(id)]
                        merchant.given_item[item.id] = item

                if 'combat' in data:
                    entity.add_component(InitiateCombat())
                    combat = entity.get_component(InitiateCombat)
                    counter = 0
                    for enemy_data in data['combat']:
                        enemy = self.entity_factory.create(enemy_data[0])
                        combat.combat_entities[counter] = enemy
                        stats = enemy.get_component(Stats)
                        stats.lvl_up(int(enemy_data[1]))
                        counter += 1

                if 'looped_ai' in data:
                    cycle = data['looped_ai']
                    x, y = cycle[0]
                    cycle.append(cycle.pop(0))
                    entity.add_component(
                        Controllable(),
                        LoopedAi(cycle)
                    )

                elif 'random_ai' in data:
                    entity.add_component(
                        Controllable(),
                        RandomAi()
                    )

                entity.get_component(Position).level = level
                self.move_entity(entity, None, x, y)

    def move_entity(self, entity, level=None, cx=None, cy=None):
        position = entity.get_component(Position)
        if not position:
            return

        if level is None:
            level = position.level

        if cx is None or cy is None:
            if entity != self.player:
                return

            position.level = None

            orientable = entity.get_component(Orientable)
            if orientable:
                orientable.orientation = C.DIRECTION_E

            controllable = entity.get_component(Controllable)
            if controllable:
                controllable.force = None

            cx, cy = self.calculate_start_position(level.player_init, level.player_init_coords)

        movement = entity.get_component(GridMovement)
        if movement:
            movement.stop()

        orientable = entity.get_component(Orientable)
        if orientable:
            orientable.stop()

        if entity == self.player and level != position.level:
            self.prepare_entities(level)

        move = level != position.level or position.x != cx or position.y != cy

        if entity.get_component(Player) and position.level is not None:
            if position.level.id != level.id:
                pass

        position.level = level
        position.x = cx
        position.y = cy
        if move:
            tile = level.map[cx][cy]
            tile.on_entrance(self, entity)
            x_niv, y_niv = level.id
            if cx == 0:
                self.move_entity(entity, self.levels[(x_niv - 1, y_niv)], 20, cy)
            elif cx == 21:
                self.move_entity(entity, self.levels[(x_niv + 1, y_niv)], 1, cy)
            elif cy == 0:
                self.move_entity(entity, self.levels[(x_niv, y_niv - 1)], cx, 15)
            elif cy == 16:
                self.move_entity(entity, self.levels[(x_niv, y_niv + 1)], cx, 1)

    def reset_level(self, level_id):
        self.levels[level_id] = copy.deepcopy(self.init_levels[level_id])
