import random

#game variables
game_vars = {
    'turn': 1,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    }

defender_list = ['ARCHR', 'WALL']
monster_list = ['ZOMBI', 'WWOLF']

defenders = {'ARCHR': {'name': 'Archer',
                       'maxHP': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                       },
             
             'WALL': {'name': 'Wall',
                      'maxHP': 20,
                      'min_damage': 0,
                      'max_damage': 0,
                      'price': 3,
                      }
             }

monsters = {'ZOMBI': {'name': 'Zombie',
                      'maxHP': 15,
                      'min_damage': 3,
                      'max_damage': 6,
                      'moves' : 1,
                      'reward': 2
                      },

            'WWOLF': {'name': 'Werewolf',
                      'maxHP': 10,
                      'min_damage': 1,
                      'max_damage': 4,
                      'moves' : 2,
                      'reward': 3
                      }
            }

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]

#global boolean to end game
end_game = False

#global boolean to not end turn for :don't buy or invalid inputs
dont_end_turn = False
#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field():
    letters = ["A", "B", "C", "D", "E"]
    print("     1     2     3")

    connectline= "  +"
    for row in range (len(field[0])):
        connectline += "-----+"
    print(connectline)
    for row in range (len(field)):
        first_line = "|"
        second_line = "|"
        for space in field[row]:
            if space == None:
                first_line += "     |"
                second_line += "     |"
                
            elif space[0] in monsters:
                first_line += "{:^5}|".format(space[0])
                second_line += "{:>2}/{:<2}|".format(space[1],monsters[space[0]]['maxHP'])
                
            elif space[0] in defenders:
                first_line += "{:^5}|".format(space[0])
                second_line += "{:>2}/{:<2}|".format(space[1],defenders[space[0]]['maxHP'])
                
        print(letters[row], first_line)
        print(" ", second_line)
        print(connectline)

#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):

    print("Turn {}".format(game_vars["turn"]), end = '   ')

    print("Threat = [", end="")
    
    for j in range(game_vars["threat"]): #prints "-" on same line when threat adds 1
        print("-",end="")
    for j in range(10 - game_vars["threat"]):
        print(" ",end="")
        
    print("]", end="   ")
          
    print("Danger Level: {}".format(game_vars["danger_level"]))
    print("Gold = {}    Monsters killed = {}/{}".format(game_vars["gold"], game_vars["monsters_killed"], game_vars["monster_kill_target"]))
    print("+------------{Combat Menu}------------+")
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")
    print("+-------------------------------------+")

#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")

#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_name):
    row = ord(position[0].upper()) - ord("A") 
    column = int(position[1]) -1 
    if len(position) != 2 or position[0].capitalize() not in ("A","B","C","D","E") or int(position[1]) > 3 or field[row][column] != None:
        print("Invalid Position")
        return False #unable to place unit because invalid position
    
    if unit_name in defenders:  
        field[row][column] = [unit_name, defenders[unit_name]["maxHP"]]

        return True

#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(field, game_vars):
    global dont_end_turn
    print("What unit do you wish to buy?")

    for index in range(len(defender_list)):
        print("{}. {} ({} gold)".format(index+1, defenders[defender_list[index]]["name"], defenders[defender_list[index]]["price"]))
    print("3. Don't buy")
    choice = input("Your choice? ")

    if choice == '1':
        if defenders[defender_list[0]]["price"] <= int(game_vars["gold"]): #Check if you have enough gold
            position = input("Place where? ")  #If yes, buy the unit and place the unit
            if (place_unit(field, position, defender_list[0]) == False): #check if there square is unoccupied
                dont_end_turn = True
            else:
                #since place_unit function already called, no need to call again
                game_vars["gold"] = int(game_vars["gold"]) - defenders[defender_list[0]]["price"]
                dont_end_turn = False
                
        else:
            print("You do not have enough gold to buy this unit.")
            dont_end_turn = True
            #does not end turn, brings player back to combat menu

    elif choice == '2':
        if defenders[defender_list[1]]["price"] <= int(game_vars["gold"]): #check if you have enough gold
            position = input("Place where? ")  #if yes, buy the unit and place the unit
            if (place_unit(field, position, defender_list[1]) == False): #check if there square is unoccupied
                dont_end_turn = True
            else:
                #since place_unit function already called, no need to call again
                game_vars["gold"] = int(game_vars["gold"]) - defenders[defender_list[1]]["price"]
                dont_end_turn = False
        else:
            print("You do not have enough gold to buy this unit.")
            dont_end_turn = True
            #does not end turn, brings player back to combat menu
            
    elif choice == '3':
        print("No unit bought.")
        dont_end_turn = True
        #if dont buy, nothing changes just brings player back to choosing combat menu, does not end turn

    else:
        print("Invalid action.")
        dont_end_turn = True
        #if player enters invalid nothing changes just brings player back to choosing combat menu, does not end turn


#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(defender_name, field, row, column):
    row_letter = chr(row + 65) #which lane
    defender_dmg = random.randint(defenders[defender_name]["min_damage"],defenders[defender_name]["max_damage"])                
    column_num = 0
    for item in field[row]:
        if item != None and item[0] in monsters: #if monster is on the same row
            item[1] -= defender_dmg
            if defender_dmg > 0:
                print("Archer hits {} in lane {} for {} damage!".format(monsters[field[row][column_num][0]]["name"], row_letter, defender_dmg))
    
            #item[1] = health
            #monster dies
            if item[1] <= 0:
                #field[row][column_num] = monster location
                game_vars["threat"] += monsters[field[row][column_num][0]]["reward"] #threat increases by amount of monster reward
                game_vars["gold"] += monsters[field[row][column_num][0]]["reward"]
                print("You gained {} gold as a reward!".format(monsters[field[row][column_num][0]]['reward']))
                game_vars["monsters_killed"] += 1
                print("{} in lane {} dies!".format(monsters[field[row][column_num][0]]["name"], row_letter))
                field[row][column_num] = None
                game_vars["num_monsters"] -= 1 #if num_monster = 0, spawn monster
            break
        
        column_num += 1

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(monster_details, field, row, column):
    monster_name = monster_details[0]
    global end_game #call global variable
    row_letter = chr(row + 65) 
    #column is where monster is at
    
    for i in range(column - 1,column - monsters[monster_name]["moves"] - 1, -1):
        #i is where the monster is going
        #i + 1 is where the monster is at
        if field[row][i] != None and field[row][i][0] in defenders and column - i == 1: 
            monster_dmg = random.randint(monsters[monster_name]["min_damage"],monsters[monster_name]["max_damage"])
            field[row][i][1] -= monster_dmg
            print("{} hits {} in lane {} for {} damage!".format(monsters[monster_name]["name"], defenders[field[row][i][0]]["name"], row_letter, monster_dmg))
            
            if field[row][i][1] <= 0: #defender dies
                print("{} in lane {} dies!".format(defenders[field[row][i][0]]["name"], row_letter))
                field[row][i] = monster_details
                field[row][i + 1] = None

            else:
                field[row][i + 1] = monster_details
                
            break
        
        elif field[row][i] != None and field[row][i][0] in defenders or field[row][i] != None and field[row][i][0] in monsters: #monster can't advance, defender in the way
            print("{} in lane {} is blocked from advancing!".format(monsters[monster_name]["name"], row_letter))
            field[row][i + 1] = monster_details
            break
        
        elif i < 0: #monster reached end of field
            print("{} in lane {} advances!".format(monsters[monster_name]["name"], row_letter))
            print("+---------------------------------------+")
            print("A {} has reached the city! All is lost!".format(monsters[monster_name]["name"]))
            print("You have lost the game. :(")
            end_game = True
            break

        else:
            print("{} in lane {} advances!".format(monsters[monster_name]["name"], row_letter))
            field[row][i] = monster_details
            field[row][i + 1] = None
                    
    return

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field, monster_list):
    spawn_row = random.randint(0,4) 
    random_monster = random.randint(0,1)
    monster_code = monster_list[random_monster]
    game_vars["num_monsters"] += 1

    field[spawn_row][-1] = [monster_code, monsters[monster_code]["maxHP"]]
    if end_game == False: #only prints if game is still running, if game over and threat spawns monster, this will not print
        print("***A monster has spawned!***")
    return

#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game(game_vars): #saves everything as string
    data = open("save.txt", "w")
    data.write(str(field) + "\n" + str(game_vars))
    data.close()
    print("Game saved!")
    

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game(game_vars):
    data = open("save.txt", "r")
    line_count = 1
    for i in data:
        i = i.strip("\n")
        if line_count == 1:
            field = eval(i)
            line_count += 1
        elif line_count > 1:
            game_vars = eval(i)
    return game_vars, field


#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    game_vars['turn'] = 1
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars['threat'] = 0
    game_vars['danger_level'] = 1
    
#-----------------------------------------------------
# end_turn()
#
#    when turn ends -after buying and placing unit
#    or when player chooses to end turn
#-----------------------------------------------------
def end_turn():

    if dont_end_turn == True: #for don't buy and any other invalid options (turn will not end)
        show_combat_menu(game_vars)
    else:
        game_vars["turn"] += 1
        game_vars["threat"] += random.randint(1,game_vars["danger_level"])
        game_vars["gold"] += 1
        
        row_num = 0
        for row in field:
            column_num = 0
            for space in row:
                if space != None and space[0] in defenders:
                    defender_name = space[0]
                    defender_attack(defender_name, field, row_num, column_num)
                elif space != None and space[0] in monsters:
                    monster_details = space
                    monster_advance(monster_details, field, row_num, column_num)
                column_num += 1                       
            row_num += 1
        while game_vars["threat"] >= 10: #when threat is 10, monster spawns and threat is reset
            game_vars["threat"] -= 10
            spawn_monster(field, monster_list)
        if game_vars["num_monsters"] == 0: #spawns monster if no monster on field
                spawn_monster(field, monster_list)

#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("+---------------------------------------+")
print("|          Desperate Defenders          |")
print("| Defend the city from undead monsters! |")
print("+---------------------------------------+")
print()

# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!

while True:
    print("+-------------{Main Menu}-------------+")
    show_main_menu()
    print("+-------------------------------------+")

    menu_choice = input("Your choice? ")
    
    if menu_choice == '1':
        initialize_game()
        spawn_monster(field, monster_list)
        break
    elif menu_choice == '2':
        game_vars, field = load_game(game_vars)
        break
    elif menu_choice == '3':
        print("See you next time!")
        break
    else:
        print("Please choose a valid option.")
        print()


while menu_choice != '3':
    #game ends if monster is off field or if monsters killed is 20
    if end_game == True:
        break
    if game_vars["monsters_killed"] >= game_vars['monster_kill_target']:
        print("+---------------------------------------+")
        print("You have protected the city! You win!")
        break
    
    if game_vars["turn"] % 12 == 0:
        game_vars["danger_level"] += 1
        print("***Danger level increased to {}***".format(game_vars["danger_level"]))
        print("The evil grows stronger!")
        for i in monsters:
            monsters[i]["maxHP"] += 1
            monsters[i]["reward"] += 1
            monsters[i]["min_damage"] += 1
            monsters[i]["max_damage"] += 1
        
    #draw field
    draw_field()

    #display combat menu
    show_combat_menu(game_vars)
    #choice (1. Buy Unit, 2. End Turn, 3. Save Game, 4. Quit)
    play_choice = input("Your choice? ")
    if play_choice == '1':
        buy_unit(field, game_vars)
        end_turn()
    elif play_choice == '2':
        dont_end_turn = False
        end_turn()
    elif play_choice == '3':
        save_game(game_vars)
        break
    elif play_choice == '4':
        print("See you next time!")
        break
    else:
        print("Please choose a valid option.")
        show_combat_menu(game_vars)