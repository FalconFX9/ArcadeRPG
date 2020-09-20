import constants as C
from entity import Entity
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
from components.combat import Combat
from components.stats import Stats
from components.inventory import Inventory
from components.alignedbox import AlignedBox
from components.sprite import Sprite
from components.collider import Collider
import copy


class EntityFactory:

    def __init__(self, state, load_images, load_combat_images):
        self.load_images = load_images
        self.load_combat_images = load_combat_images
        self.state = state
        self.combat_mechanic = None

    def create_player(self):
        return Entity().add_component(
            Stats(5),
            Inventory(),
            Controllable(),
            GridMovement(
                C.PLAYER_WALK_RELOAD),
            Orientable(
                C.DIRECTION_O, C.PLAYER_WALK_RELOAD),
            Position(None, None, None),
            AlignedBox(-0.5, -0.5, 0.5, 0.5),
            Sprite({
                tuple(self.load_images.obtain_entity('Player', 3)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.load_images.obtain_entity('Player', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.load_images.obtain_entity('Player', 0)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.load_images.obtain_entity('Player', 2)):
                lambda e: True}),
            Player()
        )

    def create_dialogue_npc_2(self):
        return Entity().add_component(
            Position(None, None, None),
            AlignedBox(-0.5, -0.5, 0.5, 0.5),
            GridMovement(C.PLAYER_WALK_RELOAD),
            Orientable(C.DIRECTION_O, C.PLAYER_WALK_RELOAD),
            Sprite({
                tuple(self.load_images.obtain_entity('Mr Chad', 3)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.load_images.obtain_entity('Mr Chad', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.load_images.obtain_entity('Mr Chad', 0)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.load_images.obtain_entity('Mr Chad', 2)):
                lambda e: True})
        )

    def create_npc_dialogue(self):
        return Entity().add_component(
            Position(None, None, None),
            AlignedBox(-0.5, -0.5, 0.5, 0.5),
            GridMovement(C.PLAYER_WALK_RELOAD),
            Orientable(C.DIRECTION_O, C.PLAYER_WALK_RELOAD),
            Sprite({
                tuple(self.load_images.obtain_entity('NPC Intro', 3)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.load_images.obtain_entity('NPC Intro', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.load_images.obtain_entity('NPC Intro', 0)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.load_images.obtain_entity('NPC Intro', 2)):
                lambda e: True})
        )

    def create_bat(self):
        return Entity('Bat').add_component(
            Combat(self.load_combat_images.obtain('Bat')),
            Stats(15, (0.1, 0, 1, 1)),
        )

    def create_black_ghost(self):
        return Entity('BlackGhost').add_component(
            Combat(self.load_combat_images.obtiens('BlackGhost')),
            Stats(20, (0.05, 7, 3, 1)),
            Position(None, None, None),
            AlignedBox(-0.5, -0.5, 0.5, 0.5),
            GridMovement(C.PLAYER_WALK_RELOAD),
            Orientable(C.DIRECTION_O, C.PLAYER_WALK_RELOAD),
            Sprite({
                tuple(self.load_images.obtain_entity('BlackGhost', 3)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.load_images.obtain_entity('BlackGhost', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.load_images.obtain_entity('BlackGhost', 0)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.load_images.obtain_entity('BlackGhost', 2)):
                lambda e: True})
        )

    def create_skeletal_soldier(self):
        return Entity('SkelSoldier').add_component(
            Combat(self.load_combat_images.obtain('SkelSoldier')),
            Stats(5, (0.8, 4, 0.2, 1)),
            Position(None, None, None),
            AlignedBox(-0.5, -0.5, 0.5, 0.5),
            GridMovement(C.PLAYER_WALK_RELOAD),
            Orientable(C.DIRECTION_E, C.PLAYER_WALK_RELOAD),
            Sprite({
                tuple(self.load_images.obtain_entity('SkelSoldier', 3)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.load_images.obtain_entity('SkelSoldier', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.load_images.obtain_entity('SkelSoldier', 0)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.load_images.obtain_entity('SkelSoldier', 2)):
                lambda e: True})
        )

    def create_dark_soldier(self):
        return Entity('DarkSoldier').add_component(
            Combat(self.load_combat_images.obtain('DarkSoldier')),
            Stats(0, (0.4, 8, 5, 1)),
            Position(None, None, None),
            AlignedBox(-0.5, -0.5, 0.5, 0.5),
            GridMovement(C.PLAYER_WALK_RELOAD),
            Orientable(C.DIRECTION_E, C.PLAYER_WALK_RELOAD),
            Sprite({
                tuple(self.load_images.obtain_entity('DarkSoldier', 3)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.load_images.obtain_entity('DarkSoldier', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.load_images.obtain_entity('DarkSoldier', 0)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.load_images.obtain_entity('DarkSoldier', 2)):
                lambda e: True})
        )

    def create_blue_orb(self):
        return Entity('BlueOrb').add_component(
            Combat(self.load_combat_images.obtain('BlueOrb')),
            Stats(50, (0.2, 0, 0.5, 1)),
            Position(None, None, None),
            AlignedBox(-0.5, -0.5, 0.5, 0.5),
            GridMovement(C.PLAYER_WALK_RELOAD),
            Orientable(C.DIRECTION_E, C.PLAYER_WALK_RELOAD),
            Sprite({
                tuple(self.load_images.obtain_entity('BlueOrb', 3)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.load_images.obtain_entity('BlueOrb', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.load_images.obtain_entity('BlueOrb', 0)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.load_images.obtain_entity('BlueOrb', 2)):
                lambda e: True})
        )

    def create_skeleton(self):
        return Entity('Skeleton').add_component(
            Combat(self.load_combat_images.obtain('Skeleton')),
            Stats(8, (0.5, 5, 0.8, 1)),
            Position(None, None, None),
            AlignedBox(-0.5, -0.5, 0.5, 0.5),
            GridMovement(C.PLAYER_WALK_RELOAD),
            Orientable(C.DIRECTION_E, C.PLAYER_WALK_RELOAD),
            Sprite({
                tuple(self.load_images.obtain_entity('Skeleton', 3)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.load_images.obtain_entity('Skeleton', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.load_images.obtain_entity('Skeleton', 0)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.load_images.obtain_entity('Skeleton', 2)):
                lambda e: True})
        )

    def create_wolf(self):
        return Entity('Wolf').add_component(
            Combat(self.load_combat_images.obtain('Wolf')),
            Stats(30, (0.2, 0, 3, 1)),
            Position(None, None, None),
            AlignedBox(-0.5, -0.5, 0.5, 0.5),
            GridMovement(C.PLAYER_WALK_RELOAD),
            Orientable(C.DIRECTION_E, C.PLAYER_WALK_RELOAD),
            Sprite({
                tuple(self.load_images.obtain_entity('Wolf', 3)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.load_images.obtain_entity('Wolf', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.load_images.obtain_entity('Wolf', 0)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.load_images.obtain_entity('Wolf', 2)):
                lambda e: True})
        )

    def crée_diable(self):
        return Entity('Diable').add_component(
            Combat(self.load_combat_images.obtiens('Diable')),
            Stats(20, (0.2, 0, 2, 1)),
            Position(None, None, None),
            AlignedBox(-0.5, -0.5, 0.5, 0.5),
            GridMovement(C.PLAYER_WALK_RELOAD),
            Orientable(C.DIRECTION_E, C.PLAYER_WALK_RELOAD),
            Sprite({
                pygame.transform.scale(self.load_combat_images.obtiens('Diable'), (32, 32)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_N,
                pygame.transform.scale(self.load_combat_images.obtiens('Diable'), (32, 32)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_O,
                pygame.transform.scale(self.load_combat_images.obtiens('Diable'), (32, 32)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_S,
                pygame.transform.scale(self.load_combat_images.obtiens('Diable'), (32, 32)):
                lambda e: True})
        )

    def crée_boss(self):
        def en_collision(état, e1, e2):
            if e2.contient_composant(Player):
                combat = e1.get_component(InitiateCombat)
                self.state.Entity_lance_combat = e1
                combat.sur_interaction(self.state)
                self.combat_mechanic.ennemis[1] = copy.copy(e1.get_component(InitiateCombat).Entitys_combat[0])
                self.combat_mechanic.ennemis[1].get_component(Stats).réinit_HP()
                pygame.mixer.music.stop()
                musique_choisie = 'demens.mp3'
                pygame.mixer.music.load('ressources\\Musique\\' + musique_choisie)
                pygame.mixer.music.play(-1)

        return Entity('Boss').add_component(
            Combat(self.load_combat_images.obtiens('Boss')),
            Stats(10, (4, 8, 3, 1)),
            Position(None, None, None),
            AlignedBox(-4.5, -4.5, 4.5, 4.5),
            Collider(en_collision),
            GridMovement(C.PLAYER_WALK_RELOAD),
            Orientable(C.DIRECTION_E, C.PLAYER_WALK_RELOAD),
            Sprite({
                tuple(self.load_images.obtain_entity('Boss', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.load_images.obtain_entity('Boss', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.load_images.obtain_entity('Boss', 1)):
                lambda e: e.get_component(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.load_images.obtain_entity('Boss', 1)):
                lambda e: True})
        )

    def create(self, nom):
        return getattr(self, 'create_' + nom)()
