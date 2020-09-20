import constants as C
from tiles.tiles import *
from level import Level

class Gworldfile:

    TILES = {'0': TerrainTile,
              '2': WallTile,
              '3': WaterTile,
              '5': SandTile,
              '6': TeleporterTile,
              '8': LeverTile,
              'b': SwitchingTile,
              'c': ChestTile
              }

    @staticmethod
    def __load_file(file):
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def __converter(tile_data):
        if tile_data == 't':
            return '0'
        elif tile_data == 'm':
            return '2'
        elif tile_data == 'e':
            return '3'
        elif tile_data == 'f':
            return '4'
        elif tile_data == 's':
            return '5'
        elif tile_data == 'T':
            return '6'
        elif tile_data == 'g':
            return '7'
        elif tile_data == 'l':
            return '8'
        elif tile_data == 'r':
            return '9'
        else:
            return tile_data

    @staticmethod
    def __analyse_position(lines):
        line = lines.pop(0)
        parties = line.split()

        if parties[1] == C.ENTITY_TILE_POSITION:
            type = C.INITIAL_PLAYER_TILE
        elif parties[1] == C.PLAYER_RECTANGLE_TAG:
            type = C.INITIAL_PLAYER_RECTANGLE

        coordinates = []

        for partie in parties[2:]:
            x, y = partie.split(C.DÉF_SEP_C)
            coordinates.append((int(x), int(y)))

        return type, coordinates

    @staticmethod
    def __analyse_autonomie_bouclée(lines):
        line = lines.pop(0)
        parties = line.split()

        # Reading a list of coordinates.
        coordinates = []
        for partie in parties[1:]:
            x, y = partie.split(C.DÉF_SEP_C)
            coordinates.append((int(x), int(y)))

        return coordinates

    @staticmethod
    def __analyse_marchand(lines):
        line = lines.pop(0)
        parties = line.split()

        # Lire une liste de coordinates.
        items_reception = []
        items = parties[1].split(C.DÉF_SEP_C)
        for item in items:
            items_reception.append(item)
        items_donation = []
        items = parties[2].split(C.DÉF_SEP_C)
        for item in items:
            items_donation.append(item)

        return items_reception, items_donation

    @staticmethod
    def __analyse_map(lines):
        map = []
        lines.pop(0)
        y = 0
        while True:
            line = lines.pop(0)
            if line == C.MAP_END_TAG:
                break

            row = []
            map.append(row)

            line = line.split(C.DÉF_SEP_B)

            for x, tile_data in enumerate(line):
                if '-1' not in tile_data:
                    tile = Gworldfile.__analyse_tile(
                        Gworldfile.__converter(tile_data), x, y)

                    row.append(tile)
                else:
                    row.append(None)

            y += 1

        map = list(zip(*map))
        return map

    @staticmethod
    def __analyse_tile(data, x, y):
        data = data.split(C.DÉF_SEP_C)
        tile = Gworldfile.TILES[data[0]]()
        tile.mapx = x
        tile.mapy = y
        type_tile = type(tile)

        if type_tile == TeleporterTile:
            x_niv = int(data[1])
            y_niv = int(data[2])
            tile.clevel = (x_niv, y_niv)
            tile.cx = int(data[3])
            tile.cy = int(data[4])
            tile.color = (int(data[5]), int(data[6]), int(data[7]))
        elif type_tile == LeverTile:
            tile.clevel = int(data[1])
            tile.cx = int(data[2])
            tile.cy = int(data[3])

            data_tile_alt = C.DÉF_SEP_C.join(data[4:])

            tile.tile_alt = Gworldfile.__analyse_tile(
                data_tile_alt, tile.cx, tile.cy)
        elif type_tile == SwitchingTile:
            tile.variant = 'terrain'
        elif type_tile == ChestTile:
            tile.variant = data[1]
            if len(data) >= 3:
                tile.argent = data[2]
            if len(data) > 3:
                for x in range(3, len(data)):
                    tile.items.append(data[x])
        else:
            tile.variant = data[1]

        return tile

    @staticmethod
    def __analyse_level(lines):
        level = Level()
        level.init_entities = []
        lines.pop(0)

        i = 0
        while lines:
            line = lines[0]
            tag = line.split()[0]

            if tag == C.MAP_TAG:
                level.map1 = Gworldfile.__analyse_map(lines)
                level.l = len(level.map1)
                level.h = len(level.map1[0])
            elif tag == C.MAP_TAG_2:
                level.map2 = Gworldfile.__analyse_map(lines)
            elif tag == C.PLAYER_TAG:
                level.joueur_init, level.joueur_init_coords = Gworldfile.__analyse_joueur(
                    lines)
            elif tag == C.LEVEL_END_TAG:
                lines.pop(0)
                break
            elif tag == C.ENTITY_TAG:
                entity = Gworldfile.__analyse_entities(lines)
                level.entities_init.append(entity)
            else:
                lines.pop(i - 1)
            i += 1
        level.map = list(level.map1)
        for y in range(level.h):
            for x in range(level.l):
                if level.map2[x][y]:
                    level.map[x] = list(level.map[x])
                    level.map[x][y] = level.map2[x][y]

        return level

    @staticmethod
    def __analyse_jeu(lines):
        levels = {}

        while lines:
            line = lines[0]
            parties = line.split()
            tag = parties[0]

            if tag == C.LEVEL_TAG:
                level = Gworldfile.__analyse_level(lines)
                level.id = int(parties[1]), int(parties[2])

                levels[level.id] = level

            else:
                raise ValueError(f'tag unknown: {tag}')

        return levels

    @staticmethod
    def load(file):
        data = Gworldfile.__load_file(file)
        lines = data.splitlines()
        lines = list(filter(len, lines))
        lines = list(map(str.strip, lines))
        levels = Gworldfile.__analyse_jeu(lines)
        return levels

    @staticmethod
    def __analyse_joueur(lines):
        return Gworldfile.__analyse_position(lines)

    @staticmethod
    def __analyse_combat(lines, tag):
        line = lines.pop(0)
        parties = line.split()
        parties.remove(tag)
        entities = []
        for partie in parties:
            entities.append(partie.split(C.DÉF_SEP_C))
        return entities

    @staticmethod
    def __analyse_entities(lines):
        data = {}

        line = lines.pop(0)
        parties = line.split()

        data['type'] = parties[1]

        while lines:
            line = lines[0]
            tag = line.split()[0]

            if tag == C.POSITION_TAG:
                data['position'], data['position_coords'] = Gworldfile.__analyse_position(
                    lines)
            elif tag == C.DÉF_BALISE_AUTONOMIE_BOUCLÉE:
                data['looped_ai'] = Gworldfile.__analyse_autonomie_bouclée(
                    lines)
            elif tag == C.DÉF_BALISE_AUTONOMIE_CIBLÉE:
                lines.pop(0)
                data['random_ai'] = True
            elif tag == C.EPHEMERAL_TAG:
                line = lines.pop(0)
                id = line.split()
                data['ephemeral'] = id[1]
            elif tag == C.DIALOGUE_TAG:
                line = lines.pop(0)
                dialogue = line.split(C.DÉF_SEP_C)
                dialogue.remove(tag + " ")
                data['dialogue'] = dialogue
            elif tag == C.MERCHANT_TAG:
                data['marchand'] = Gworldfile.__analyse_marchand(lines)
            elif tag == C.COMBAT_TAG:
                data['combat'] = Gworldfile.__analyse_combat(lines, tag)
            elif tag == C.ENTITY_END_TAG:
                lines.pop(0)
                break
            else:
                raise ValueError(f'tag unknown: {tag}')

        return data
