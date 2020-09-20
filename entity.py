import constants as C


class Entity:

    def __init__(self, id=None):
        self.id = id
        self.components = {}

    def __str__(self):
        nom_composants = ', '.join(map(lambda type_composant: type_composant.__name__, self.components))
        return f'Entité(id={self.id}),composants=[{nom_composants}]'

    def add_component(self, *composant):
        for c in composant:
            self.components[c.__class__] = c

        return self

    def contains_component(self, type_composant):
        return type_composant in self.components

    def get_component(self, type_composant):
        if type_composant not in self.components:
            return None

        return self.components[type_composant]

    def remove_component(self, type_composant):
        if type_composant in self.components:
            del self.components[type_composant]