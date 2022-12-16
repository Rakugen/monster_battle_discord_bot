# A move class that will be used for pokemon moves
# a Move has a name, type, atk, acc, PP, effect, description

class Move:
    def __init__(self, name, move_type, atk, acc, pp, effect, desc):
        self.name = name
        self.type = move_type
        self.atk = atk
        self.acc = acc
        self.pp = pp
        self.effect = effect
        self.desc = desc
