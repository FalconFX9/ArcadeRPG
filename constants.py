import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


TITLE = 'Mon jeu'
WIDTH = 640 #704
HEIGHT = 480#544
DRAW_BACKGROUND = (255, 255, 255)
DT = 1/60
RESOURCES = resource_path('resources/')
LAYERS = 2
TILE_SIZE = 32

DIRECTION_N, DIRECTION_E, DIRECTION_S, DIRECTION_O = 1, 2, 3, 4

INITIAL_PLAYER_TILE = 0
INITIAL_PLAYER_RECTANGLE = 1
PLAYER_BOARDER = (255, 0, 0, 100)
PLAYER_WALK_RELOAD = 36

LEVEL_STATE = 0
FAILURE_STATE = 1
PAUSE_STATE = 2
COMBAT_STATE = 3
VICTORY_STATE = 4
MENU_STATE = 5
GAME_END = 6

WOLRD_SOURCE = RESOURCES + 'monde.megachonk'
ITEM_SOURCE = RESOURCES + 'items.megachonk'
DÉF_SEP_B = ' '
DÉF_SEP_C = ';'
LEVEL_TAG = 'level'
LEVEL_END_TAG = '/level'
MAP_TAG = 'map'
MAP_END_TAG = '/map'
MAP_TAG_2 = 'map2'
MAP_TAG_3 = 'map3'
PLAYER_TAG = 'player'
PLAYER_RECTANGLE_TAG = 'rectangle'
ENTITY_TILE_POSITION = 'tiles'
ENTITY_TAG = 'entity'
ENTITY_END_TAG = '/entity'
POSITION_TAG = 'position'
DÉF_BALISE_AUTONOMIE_BOUCLÉE = 'looped_ai'
DÉF_BALISE_AUTONOMIE_CIBLÉE = 'random_ai'
DIALOGUE_TAG = 'dialogue'
ITEM_TAG = 'item'
ITEM_ID_TAG = 'id'
ITEM_ATTACK_TAG = 'attack'
ITEM_DEFENCE_TAG = 'armor'
ITEM_QUANTITY_TAG = 'quantity'
ITEM_TYPE_TAG = 'type'
ITEM_PRICE_TAG = 'price'
ITEM_END_TAG = '/item'
EPHEMERAL_TAG = 'ephemeral'
MERCHANT_TAG = 'merchant'
COMBAT_TAG = 'combat'
RELOAD_ANIM = 150

STATS_PER_LEVEL = {
    1: (500, 0, 20, 200),
    2: (600, 1, 25, 300),
    3: (700, 2, 30, 500),
    4: (700, 3, 40, 800),
    5: (900, 4, 50, 1100),
    6: (1000, 5, 60, 1400),
    7: (1100, 6, 80, 1700),
    8: (1200, 7, 100, 2000),
    9: (1300, 8, 120, 2400),
    10: (1400, 9, 140, 2800),
}
XP_GAIN = {
    'Bat': 50,
    'BlackGhost': 100,
    'SkelSoldier': 120,
    'BlueOrb': 50,
    'DarkSoldier': 400,
    'Wolf': 150,
    'Skeleton': 90,
    'Devil': 150,
    'Boss': 1000,
}