# A player has a name, a list of pokemons, badges, items

class Player:
    def __init__(self, name):
        self.name = name
        self.badges = 0
        self.pokemons = []
        self.items = []

    def add_mon(self, mon):
        self.pokemons.append(mon)

    def add_item(self, item):
        self.items.append(item)

