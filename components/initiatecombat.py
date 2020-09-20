import constants as C


class InitiateCombat:
    def __init__(self):
        self.combat_entities = {}

    def sur_interaction(self, state):
        state.state = C.COMBAT_STATE
