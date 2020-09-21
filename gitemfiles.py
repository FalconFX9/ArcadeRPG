import constants as C
from components.item import Item


class Gitemfiles:

    @staticmethod
    def __charge_fichier(file):
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def __analyse_item(lines):
        data = {}

        line = lines.pop(0)
        parties = line.split()

        data['name'] = parties[1]

        while lines:
            line = lines.pop(0)
            parties = line.split()
            tag = parties[0]

            if tag == C.ITEM_ID_TAG:
                data['id'] = int(parties[1])
            elif tag == C.ITEM_ATTACK_TAG:
                data['attack'] = int(parties[1])
            elif tag == C.ITEM_DEFENCE_TAG:
                data['defence'] = int(parties[1])
            elif tag == C.ITEM_PRICE_TAG:
                data['price'] = int(parties[1])
            elif tag == C.ITEM_TYPE_TAG:
                pass
                # données['type'] = int(parties[1])
            elif tag == C.ITEM_END_TAG:
                break
            else:
                raise ValueError(f'tag unknown: {tag}')

        return data

    @staticmethod
    def __trouve_items(lines):
        items = {}

        while lines:
            ligne = lines[0]
            tag = ligne.split()[0]

            if tag == C.ITEM_TAG:
                item = Gitemfiles.__analyse_item(lines)
                items[item['id']] = item
            else:
                raise ValueError(f'tag unknown: {tag}')

        return items

    @staticmethod
    def load(file):
        data = Gitemfiles.__charge_fichier(file)
        lines = data.splitlines()
        lines = list(filter(len, lines))
        lines = list(map(str.strip, lines))
        items_texte = Gitemfiles.__trouve_items(lines)
        items = {}
        for data in items_texte.values():
            item = Item()
            item.name = data['name']
            item.id = data['id']
            item.attack = data['attack']
            item.defence = data['defence']
            item.price = data['price']
            #item.type = données['type']
            items[item.id] = item
        return items
