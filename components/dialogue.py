import constants as C
from components.orientable import Orientable


class Dialogue:
    def __init__(self, dialogue):
        self.dialogue = dialogue
        self.counter = 0
        self.active = False

    def on_interaction(self, entity, player):
        self.active = True
        orientation_player = player.get_component(Orientable).orientation
        orientation = entity.get_component(Orientable)
        if orientation_player == C.DIRECTION_N:
            orientation.orientation = C.DIRECTION_S
        elif orientation_player == C.DIRECTION_S:
            orientation.orientation = C.DIRECTION_N
        elif orientation_player == C.DIRECTION_E:
            orientation.orientation = C.DIRECTION_O
        elif orientation_player == C.DIRECTION_O:
            orientation.orientation = C.DIRECTION_E
        self.counter += 1
