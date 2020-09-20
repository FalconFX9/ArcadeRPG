import constantes as C
from composants.controlable import Controllable
from composants.mouvementgrille import GridMovement
from composants.orientable import Orientable
from composants.position import Position
from composants.collisionneur import Collider
from composants.joueur import Player
from composants.zombie import Zombie
from composants.boitealignee import AlignedBox
from composants.autonomiebouclee import LoopedAI
from composants.autonomieciblee import RandomAI
from composants.inventaire import Inventory
from composants.stats import Stats
from time import time
import random
import pickle


class GState:

    def __init__(self, state):
        self.combat_mechanic = None
        try:
            pickle_in = open('ressources\\save.chonker', 'rb')
            save_data = pickle.load(pickle_in)
        except FileNotFoundError:
            save_data = None
        self.state = state
        self.state.player = self.state.usine_entity.crée('player')
        if save_data:
            inventory = self.state.player.get_component(Inventory)
            inventory.inventory = save_data[0]
            cx, cy = save_data[1]
            cx, cy = int(cx), int(cy)
            level_init = state.levels[save_data[2]]
        else:
            cx, cy = None, None
            level_init = None
            self.state.player.get_component(Position).levels = state.levels[(3, 3)]
        self.state.entities.append(self.state.player)
        self.state.player.get_component(Inventory).stats = self.state.player.get_component(Stats)
        for level in self.state.levels.values():
            self.state.prepare_entities(level, True)
        if save_data:
            self.state.destroyed_entities = save_data[4]
            for entity in self.state.entitys:
                if entity.id in self.state.destroyed_entities:
                    self.state.entities_to_destroy.add(entity)
            stats = self.state.player.get_component(Stats)
            saved_states = save_data[5]
            stats.lvl_up(saved_states.level)
            inventory.vérifie_stats()
            stats.XP = saved_states.XP
            stats.HP = saved_states.HP

        self.state.move_entity(self.state.player, level_init, cx, cy)
        self.temps = time()

    def __clean_up(self):
        while self.state.entities_to_destroy:
            entity = self.state.entities_to_destroy.pop()

            if entity.contient_composant(Player):
                self.state.state = C.ÉTAT_ÉCHEC

            else:
                if entity in self.state.entities:
                    self.state.entitys.remove(entity)

    def __update_grid_movement(self, entity):
        level = self.state.player.get_component(Position).level
        position = entity.get_component(Position)
        movement = entity.get_component(GridMovement)

        if not position or not movement or position.level != level:
            return

        orientable = entity.get_component(Orientable)
        controllable = entity.get_component(Controllable)

        if movement.reload is not None:
            movement.reload = movement.reload - movement.speed
            if movement.reload <= 0:
                self.state.move_entity(
                    entity, None, movement.cx, movement.cy)
            else:
                position.x, position.y = self.state.calculate_position(entity)
        elif orientable.reload is not None:
            orientable.reload = orientable.reload - 1
            if orientable.reload > 0:
                orientable.stop()

        movement.vitesse = 1
        if movement.reload is None:
            self.__update_ai_movement(entity)

        if controllable and controllable.force and not self.state.in_movement(entity):

            if orientable and orientable.cost == 0 and controllable.force != orientable.orientation:
                orientable.orientation = controllable.force

            if orientable and controllable.force != orientable.orientation:
                orientable.orientation = controllable.force
                orientable.reload = orientable.cost

            else:
                tuile = self.calculate_target_tile(entity, controllable.force)
                if tuile and self.__can_enter(position.level, tuile, entity):
                    movement.sx = position.x
                    movement.sy = position.y
                    movement.cx = tuile.x
                    movement.cy = tuile.y

                    movement.reload = movement.cost

    def calculate_target_tile(self, entity, direction):
        position = entity.get_component(Position)
        movement = entity.get_component(GridMovement)

        if not position or not movement:
            return None

        x = position.x
        y = position.y
        if direction == C.DIRECTION_N:
            y -= 1
        elif direction == C.DIRECTION_O:
            x -= 1
        elif direction == C.DIRECTION_S:
            y += 1
        elif direction == C.DIRECTION_E:
            x += 1

        level = position.level
        if 0 <= x < level.l and 0 <= y < level.h:
            return level.map[int(x)][int(y)]

        return None

    def __update_looped_auto_movement(self, entity):
        ab = entity.get_component(LoopedAI)
        ctrl = entity.get_component(Controllable)
        pos = entity.get_component(Position)

        if not (ab and ctrl and pos):
            return

        cycle = ab.cycle
        x, y = cycle[0]

        if pos.x == x and pos.y == y:
            cycle.append(cycle.pop(0))
            x, y = cycle[0]

        if y < pos.y:
            ctrl.force = C.DIRECTION_N
        elif x < pos.x:
            ctrl.force = C.DIRECTION_O
        elif y > pos.y:
            ctrl.force = C.DIRECTION_S
        elif x > pos.x:
            ctrl.force = C.DIRECTION_E
        else:
            ctrl.force = None

    def __update_targeted_ai_movement(self, entity):
        ac = entity.get_component(RandomAI)
        ctrl = entity.get_component(Controllable)
        pos = entity.get_component(Position)
        ori = entity.get_component(Orientable)

        if not (ac and ctrl and pos):
            return

        pos_player = self.state.player.get_component(Position)
        dir_player_x = C.DIRECTION_O if pos_player.x < pos.x else C.DIRECTION_E
        dir_player_y = C.DIRECTION_N if pos_player.y < pos.y else C.DIRECTION_S

        if pos_player.x == pos.x \
                and (not ori or ori.orientation == dir_player_y) \
                or pos_player.y == pos.y \
                and (not ori or ori.orientation == dir_player_x):

            if pos_player.x == pos.x and pos_player.y == pos.y:
                ctrl.force = None
            else:
                ctrl.force = ori.orientation

        else:
            dirs = [C.DIRECTION_N, C.DIRECTION_O, C.DIRECTION_S, C.DIRECTION_E]
            mode = random.random()

            if mode < 0.1:
                dirs.remove(ori.orientation)
                ctrl.force = random.choice(dirs)
            elif mode < 0.3:
                ctrl.force = ori.orientation if ori else random.choice(ori)
            else:
                ctrl.force = None

    def __update_ai_movement(self, entity):
        if entity.get_component(Position).level == self.state.player.get_component(Position).level:
            self.__update_looped_auto_movement(entity)
            self.__update_targeted_ai_movement(entity)

    def __update_map(self):
        for column in self.state.player.level.map:
            for tile in column:
                tile.update(self.state)

    def __update_tiles(self):
        position = self.state.player.get_component(Position)
        if not position:
            return

        for column in position.level.map:
            for tile in column:
                tile.actualise(self.state)

    def __apply_tile_effects(self):
        for entity in list(self.state.entities):
            position = entity.get_component(Position)
            if position:
                x, y = self.state.calculate_position(entity)
                tile = position.niveau.carte[int(x)][int(y)]
                tile.on_walk(self.state, entity)

    def __can_enter(self, level, tile, entity):
        if not tile.can_enter(entity):
            return False

        for e in self.state.entities:
            if e == entity:
                continue

            pn = e.get_component(Position)
            if not pn or pn.level != level:
                continue

            mvt = e.get_component(GridMovement)
            if mvt:
                if mvt.reload is not None:
                    if (mvt.sx == tile.x and mvt.sy == tile.y
                        or mvt.cx == tile.x and mvt.cy == tile.y):
                        return False
                elif pn and pn.x == tile.x and pn.y == tile.y:
                    return False

        return True

    def __update_physics(self):
        for entity in self.state.entities:
            self.__update_grid_movement(entity)

    def __apply_entity_interactions(self):
        entities = list(self.state.entities)
        no_entities = len(entities)
        for i in range(no_entities):
            e1 = entities[i]
            collider1 = e1.get_component(Collider)

            for j in range(i + 1, no_entities):
                e2 = entities[j]
                collider2 = e2.obtient_composant(Collider)

                if not collider1 and not collider2:
                    continue

                if self.__in_collision(e1, e2):
                    if collider1:
                        collider1.apply(self.state, e1, e2)

                    if collider2:
                        collider2.apply(self.state, e2, e1)

    def __in_collision(self, e1, e2):
        p1 = e1.get_component(Position)
        p2 = e2.get_component(Position)

        if p1.level.id == p2.level.id:

            aabb1 = e1.get_component(AlignedBox)
            if aabb1:
                minx1 = aabb1.minx
                miny1 = aabb1.miny
                maxx1 = aabb1.maxx
                maxy1 = aabb1.maxy
            else:
                minx1 = miny1 = maxx1 = maxy1 = 0

            aabb2 = e2.get_component(AlignedBox)
            if aabb2:
                minx2 = aabb2.minx
                miny2 = aabb2.miny
                maxx2 = aabb2.maxx
                maxy2 = aabb2.maxy
            else:
                minx2 = miny2 = maxx2 = maxy2 = 0

            return p1.x + minx1 < p2.x + maxx2 \
                and p2.x + minx2 < p1.x + maxx1 \
                and p1.y + miny1 < p2.y + maxy2 \
                and p2.y + miny2 < p1.y + maxy1
        else:
            return False

    def __slow_regen(self):
        if self.time + 1 <= time():
            stats = self.state.player.get_component(Stats)
            if stats.HP < stats.HP_MAX:
                stats.HP += stats.HP_MAX * 0.01
                if stats.HP > stats.HP_MAX:
                    stats.HP = stats.HP_MAX
            self.time = time()

    def update(self):
        if self.state.state == C.LEVEL_STATE:
            self.__slow_regen()
            self.__update_tiles()
            self.__update_physics()
            self.__apply_tile_effects()
            self.__apply_entity_interactions()
            self.__clean_up()
        elif self.state.state == C.COMBAT_STATE or self.state.state == C.VICTORY_STATE:
            self.combat_mechanic.turn_manager()
            self.combat_mechanic.combat_check()