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
