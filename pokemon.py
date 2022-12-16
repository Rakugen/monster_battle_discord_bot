# Pokemon class: a pokemon has a #, name, hp/atk/def/spatk/spd, move list,

class Pokemon:
    def __init__(self, name, level, type1, type2, hp, atk, defense, spatk, spdef, spd, curr_moves, move_list):
        self.name = name
        self.level = level
        self.type1 = type1
        self.type2 = type2
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.spatk = spatk
        self.spdef = spdef
        self.spd = spd
        self.curr_moves = curr_moves
        self.move_list = move_list

    def change_move(self, move):

        pass

