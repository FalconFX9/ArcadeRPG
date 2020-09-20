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
HEIGHT = 490#544
DRAW_BACKGROUND = (255, 255, 255)
DT = 1/120
RESOURCES = resource_path('resources/')

INITIAL_PLAYER_TILE = 0
INITIAL_PLAYER_RECTANGLE = 1
PLAYER_BOARDER = (255, 0, 0, 100)

DÉF_MONDE_SOURCE = RESOURCES + 'monde.def'
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
ITEM_END_TAG = 'id'
ITEM_ATTACK_TAG = 'attack'
ITEM_DEFENCE_TAG = 'defence'
ITEM_QUANTITY_TAG = 'quantity'
ITEM_END_TAG = '/item'
EPHEMERAL_TAG = 'ephemeral'
MERCHANT_TAG = 'merchant'
COMBAT_TAG = 'combat'