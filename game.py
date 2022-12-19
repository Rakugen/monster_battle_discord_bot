from player import Player
from pokemon import Pokemon
from move import Move
import random
import pandas
import pickle


# READ CSV FILES
POKEMONS_DF = pandas.read_csv("static/data/pokemon.csv")
MOVESET_DF = pandas.read_csv("static/data/movesets.csv")
MOVES_DF = pandas.read_csv("static/data/moves.csv")

# CATEGORIES FOR CSV LOOKUP
# POKEMON_CATEGORIES = ['species', 'type1', 'type2', 'hp', 'attack', 'defense', 'spattack', 'spdefense', 'speed']
# MOVE_CATEGORIES = ['move', 'description', 'type', 'category', 'power', 'accuracy', 'pp', 'z-effect']

game_on = True
STARTERS = ["Bulbasaur", "Charmander", "Squirtle", "Pikachu", "Spinda", "Vulpix", "Clefairy"]
ENEMY_STARTERS = ["Pidgey","Ekans","Paras","Meowth","Abra","Growlithe","Tentacool","Voltorb","Onix","Tangela","Machop"]
NAMES = ["Bob", "Jill", "Joe", "Cynthia", "Spike", "Lance", "Ash", "Misty", "Brock", "Dawn"]
MON_POOL1 = ["Pidgey", "Caterpie","Metapod","Rattata","Weedle","NidoranF","NidoranM","Spearow","Jigglypuff","Sandshrew",
             "Mankey","Oddish","Bellsprout","Meowth"]
MON_POOL2 = ["Exeggcute","Seel","Goldeen","Koffing","Pidgeotto","Kabuto","Beedrill","Butterfree","Lickitung","Nidorino",
             "Nidorina","Rhyhorn","Gloom","Ponyta","Poliwhirl","Onix","Hitmonlee","Arbok","Raichu"]

# Load players into ALL_PLAYERS from pickle file
with open('static/data/player_list.pkl', 'rb') as inp:
    all_players = pickle.load(inp)

def make_mon(name, level):
    # Find all moves in first x that are not null value
    moveset2 = MOVESET_DF.loc[MOVESET_DF['species'] == name].to_dict(orient="list")
    move_list = []
    for i in range(1, 11):
        new_move = moveset2['move' + str(i)][0]
        # pandas.isna() checks for NAN float type. type2 in moveset csv file sometimes is NAN.
        if not pandas.isna(new_move):
            # string manip to remove everything but the move name
            move_name = ' '.join(new_move.split(' ')[2:])
            move_list.append(move_name)

    # Create first 2 starting moves
    start_moves = []
    for i in range(0,2):
        move_loc = MOVES_DF.loc[MOVES_DF['move'] == move_list.pop(0)].to_dict(orient="list")
        new_move = Move(
            name=move_loc['move'][0],
            move_type= move_loc['type'][0],
            atk= move_loc['power'][0],
            acc= move_loc['accuracy'][0],
            pp= move_loc['pp'][0],
            effect= move_loc['z-effect'][0],
            desc= move_loc['description'][0]
        )
        start_moves.append(new_move)

    # Find a specific mon by name
    # orient="list" formats the output dict into a more friendly layout
    mon_df = POKEMONS_DF.loc[POKEMONS_DF['species'] == name].to_dict(orient="list")
    new_pokemon = Pokemon(
        name= mon_df['species'][0],
        level= level,
        type1= mon_df['type1'][0],
        type2= mon_df['type2'][0],
        hp= mon_df['hp'][0],
        atk= mon_df['attack'][0],
        defense= mon_df['defense'][0],
        spatk= mon_df['spattack'][0],
        spdef= mon_df['spdefense'][0],
        spd= mon_df['speed'][0],
        curr_moves= start_moves,
        move_list= move_list
    )
    return new_pokemon

# Function that will make a new player
def make_player(name):
    new_player = Player(name)
    for x in range(2):
        new_pokemon = make_mon(random.choice(STARTERS), 1)
        new_player.add_mon(new_pokemon)

    all_players.append(new_player)
    save_players()
    return new_player

def make_enemy(count, level):
    new_enemy = Player(random.choice(NAMES))
    for x in range(count):
        new_pokemon = make_mon(random.choice(ENEMY_STARTERS), level)
        new_enemy.add_mon(new_pokemon)

    return new_enemy

# Shows all players
def display_players():
    for player in all_players:
        item_str = ''
        for item in player.items:
            item_str += f'{item} '
        output_str = f'Player: {player.name} | Badges: {player.badges} | Items: {item_str}\n'
        pokemon_count = 1
        for mon in player.pokemons:
            output_str += f'Pokemon #{pokemon_count}: {mon.name} - ' \
                          f'Lv: {mon.level}\n' \
                          f'Type: {mon.type1}/{mon.type2}\n' \
                          f'Stats: |{mon.hp} hp|{mon.atk} atk|{mon.defense} def|{mon.spatk} spatk|{mon.spdef} spdef|{mon.spd} spd|' \
                          f'\n\t'
            pokemon_count += 1

            for move in mon.curr_moves:
                output_str += f'{move.name} - '
            # Remove trailing ' - '
            output_str = output_str[:-3] + '\n\n'

        print(output_str)

# Saves ALL_PLAYERS into pickle file
def save_players():
    with open('static/data/player_list.pkl', 'wb') as outp:
        pickle.dump(all_players, outp, -1)

# Delete a player
def delete_player(player):
    all_players.remove(player)
    save_players()



# make_player("Simon")
# make_player("Linda")

# save_players()
# delete_player()

# display_players()



# Step 1: Game starts
while game_on:
    current_player = ''
    # Step 2: Choose player, make new player, delete player
    command = input("(1) Choose a player, (2) make a new player or (3) delete a player?")
    match command:
        case '1':
            if len(all_players) == 0:
                print("No Players Available.")
            else:
                print('Choose a player: ')
                player_list_str = ''
                for i in range(len(all_players)):
                    print(f'({i+1}) {all_players[i].name}')

                player_select = input('')
                if int(player_select) not in range(len(all_players) + 1):
                    print("Invalid player choice.")
                else:
                    battle_on = True
                    active_player = all_players[int(player_select) - 1]
                    # Step 3: Player Battle Loop
                    while battle_on:
                        print(f'Player {active_player.name} is battling. ')
                        # Roll random enemy player:
                        enemy_trainer = make_enemy(2, 1)

                        # TODO: Display the enemy trainers mons:

                        # item_str = ''
                        # for item in enemy_trainer.items:
                        #     item_str += f'{item} '
                        # output_str = f'Player: {enemy_trainer.name} | Badges: {enemy_trainer.badges} | Items: {item_str}\n'
                        # pokemon_count = 1
                        # for mon in enemy_trainer.pokemons:
                        #     output_str += f'Pokemon #{pokemon_count}: {mon.name} - ' \
                        #                   f'Lv: {mon.level}\n' \
                        #                   f'Type: {mon.type1}/{mon.type2}\n' \
                        #                   f'Stats: |{mon.hp} hp|{mon.atk} atk|{mon.defense} def|{mon.spatk} spatk|{mon.spdef} spdef|{mon.spd} spd|' \
                        #                   f'\n\t'
                        #     pokemon_count += 1
                        #
                        #     for move in mon.curr_moves:
                        #         output_str += f'{move.name} - '
                        #     # Remove trailing ' - '
                        #     output_str = output_str[:-3] + '\n\n'
                        # print(output_str)




                        # Loop through enemy players pokemons:

                            # Loop player battle choice:



                        # Quit:
                        battle_on = False

        case '2':
            print('Make a new player: ')



        case '3':
            print('Delete a player: ')
            player_list_str = ''

            for i in range(len(all_players)):
                print(f'({i+1}) {all_players[i].name}')

            if len(all_players) == 0:
                print("No Players to Delete.")
            else:
                player_select = input('')

                if int(player_select) not in range(len(all_players) + 1):
                    print("Invalid player choice.")
                else:
                    print(f'Deleting: {player_select} | {all_players[int(player_select)-1].name}')
                    delete_player(all_players[int(player_select)-1])

        # Catch everything else
        case other:
            print(f'Invalid Command: {command}')

