import constants as C


class Stats:
    def __init__(self, agility, modifier=(1, 1, 1, 1)):
        self.HP_MAX = None
        self.HP = None
        self.defence = None
        self.attack = None
        self.XP = 0
        self.XP_MAX = None
        self.agility = agility
        self.level = 1
        self.stats_per_level = {}
        for level in range(1, len(C.STATS_PER_LEVEL) + 1):
            stats = []
            self.stats_per_level[level] = stats
            for x in range(4):
                stats.append(C.STATS_PER_LEVEL[level][x] * modifier[x])
        self.lvl_up(self.level)
        self.HP = self.HP_MAX

    def check_level(self):
        if self.XP >= self.XP_MAX:
            self.XP -= self.XP_MAX
            self.lvl_up(self.level + 1)
            return True
        else:
            return False

    def lvl_up(self, level):
        self.HP_MAX, self.defence, self.attack, self.XP_MAX = self.stats_per_level[level]
        self.level = level

    def reinit_hp(self):
        self.HP = self.HP_MAX
