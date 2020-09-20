import constants as C


class Level:
    def __init__(self):
        self.id = None
        self.map = None
        self.map1 = None
        self.map2 = None
        self.map3 = None
        self.l = 0
        self.h = 0

        self.player_init = None
        self.player_init_coords = None
        self.entités_init = None
