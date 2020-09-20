class Inventory:
    def __init__(self):
        self.inventory = {}
        self.inventory['money'] = 0
        self.stats = None

    def add_money(self, argent):
        self.inventory['money'] += int(argent)

    def add_item(self, item):
        self.inventory[item.id] = item
        self.stats.attack += item.attack
        self.stats.defence += item.defence

    def check_stats(self):
        for item in self.inventory.values():
            if type(item) is not int:
                self.stats.attack += item.attack
                self.stats.defence += item.defence

    def del_item(self, item):
        self.stats.attack -= item.attack
        self.stats.defence -= item.defence
        self.inventory.pop(item.id)

    def print_items(self):
        print('\t'.join(['Name', 'Atk', 'Def', 'Val']))
        for item in self.inventory.values():
            print('\t'.join([str(x) for x in [item.name, item.attack, item.armor, item.price]]))
