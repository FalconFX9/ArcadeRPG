from components.inventory import Inventory


class Merchant:
    def __init__(self):
        self.required_item = {}
        self.given_item = {}
        self.missing_item = []
        self.dialogue = None
        self.exchange = False
        self.counter = None

    def on_exchange(self, player):
        if not self.exchange:
            inventory = player.obtient_composant(Inventory)
            for item in self.required_item.values():
                if item.id in inventory.inventory:
                    if item in self.missing_item:
                        self.missing_item.remove(item)
                elif item.id not in self.missing_item:
                    self.dialogue = "The item " + item.nom + " is not in your inventory"
                    if item not in self.missing_item:
                        self.missing_item.append(item)
                    break
            if len(self.missing_item) == 0:
                for item in self.required_item.values():
                    inventory.inventory.pop(item.id)
                self.exchange = True
                for item in self.given_item.values():
                    inventory.add_item(item)
                self.missing_item.append(None)
                self.dialogue = "Here is your reward: " + item.nom
