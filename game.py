import json
from window import DirectionWindow, GameOverWindow, WinnerWindow

"""
    Load json file for loads text, rooms, rooms descriptions, etc..
"""
def get_json_file_game():
    with open('game.json', 'r') as file_game:
        file_json = file_game.read()

    return json.loads(file_json)

score = 0 #score of the player
level = 1 #level of the player
rooms = {} #list of rooms
player = '' #name of player
attempts = 5 #number of attempts to retry
game_file = {} #file containing some game data: rooms, texts, etc
max_objects = 5 #number of objects in all rooms
max_score = 275 #score of the player
actual_room = {} #room where is the player currently
max_attempts = 5 #number of attempts in the game
inventory= ['map'] #list of inventory
error_message = '' #message to display when an error occurs into the room battle
alert_message = '' #message to be displayed when user lose
player_welcome = False #to know if show player welcome or not
directions_done = [] #save directions when user pass the level

def start_game():
    set_rooms()
    get_player_info() 


def get_player_info():
    global player, error_message

    show_errors_if_exists()

    if player == '':
        player = cinput("\nWhat is your name? : ", return_exact_value=True)
        if player == '':
            error_message = 'The player name cannot be empty'
            get_player_info()

    move_to_room('intro_scene')
    intro_scene()


def update_player_info():
    text = '{0}{1}{2}{3}{4}'.format(
        f"[Player: {player} | ",
        f"Room: {actual_room['name']} | ",
        f"Score: {score} | ",
        f"Level: {level} | ",
        f"Attempts: {attempts}]"
    )

    print(text)

def show_final_score():
    
    obtained_objecs = len(inventory) - 1 # -m because the user no select the map

    attempts_result = (100 / max_attempts) * attempts;
    objects_result = (100 / max_objects) * obtained_objecs;
    score_result = (100 / max_score) * score;

    percent  = round((attempts_result + objects_result + score_result) / 3)

    subtract_to_attempts = 5 - (5 / 100) * attempts_result
    subtract_to_objects = 35 - (35 / 100) * objects_result
    subtract_to_score = 60 - (60 / 100) * score_result
    subtract_total = (subtract_to_attempts + subtract_to_objects + subtract_to_score)
    
    percent_total = percent - (percent * subtract_total) / 100 
    percent_total = round(percent_total, 1)

    if percent_total >= 75 and percent_total < 90:
        score_message = 'Well, you can do so much better :)'
 
    elif percent_total >= 90  and percent_total < 100: 
        score_message = 'Very good, you almost got all the points :D'

    elif percent_total == 100: 
        score_message = 'Wonderful, you have finished with more than the required punctuation ;)'

    elif percent_total > 100: 
        score_message = 'Awesome, you ended up with more than the required score :()'

    else: 
        score_message = 'You got a low score, keep improving :|'

    percent_total = "100%+" if percent_total > 100 else f'{percent_total}%'
  
    text = '{0}{1}{2}{3}'.format(
        f"[Points:     {score}/{max_score}]\n",
        f"[Objects:    {obtained_objecs}/{max_objects}]\n",
        f"[Attempts:   {attempts}/{max_attempts}]\n",
        f"[Percentage: {percent_total}/100%]\n"
    )

    print(f"{player}, You've been obtained the next score:")
    print(text)
    print(score_message)
    
    
def set_rooms():
    global rooms, actual_room, game_file

    game_file = get_json_file_game()
    actual_room = game_file['rooms']['intro_scene']
    
    rooms = game_file['rooms']
    for room_key in rooms:
        rooms[room_key] = rooms[room_key]


def menu():
    print('-Menu')
    print('---Type inventory to view the objects obtained')
    print('---Type exit or die to exit the game')

def cinput(text='Enter a command: ', return_exact_value=False):
    try:
        typed_by_player = input(text)
        result = str(typed_by_player).lower()
         
        if result == 'menu':
            menu()
            desicion = cinput('Select an menu option: ')
        
            if desicion == 'exit' or desicion == 'die':
                print('See you later, you can enter whenever you want to face the challenges of the mysterious house.');
                exit()

            elif desicion == 'inventory' or desicion == 'y':
                show_inventory()

    except KeyboardInterrupt:
        return cinput(text)
    
    return typed_by_player if return_exact_value else result


def get_room_directions():
    global actual_room
    return actual_room['directions']
 
 
def drop_object(object=''):
    global inventory

    if object in inventory:
        inventory.remove(str(object))


def collect_object(object):
    global inventory

    if object != '' and not object in inventory:
        inventory.append(str(object))


def show_inventory():
    global inventory

    inventory_list = "\nGeneral inventory! \n"

    for item in inventory : 
        inventory_list += f'{item.title()}\n'

    print(inventory_list.rstrip('\n')) 


def collet_object_from_room():
    global actual_room, rooms

    objects = actual_room['objects']
    room_key = actual_room['id']
    objects_len = len(objects)

    s = "s" if objects_len != 1 else ''

    objects_list = ''
    if objects_len > 0:
        objects_list += f'There is {objects_len} object{s} in this room\n'
        for object in objects:
            objects_list += f'{object.title()}\n'
            
        print(objects_list.rstrip('\n'))

        seleccionados = ''
        total_score = 0
        for object in objects:
            decision = cinput(f"\nDo you want to add {object.title()} to inventory? (y/n): ")
            if decision == 'y':
                collect_object(object)
                add_score(5)
                total_score += 5
                seleccionados += f'{object.title()}, '

        seleccionados = seleccionados.rstrip(", ")
        if seleccionados != '':
            for object_to_remove in seleccionados.split(","):
                rooms[room_key]['objects'].remove(object_to_remove.lower().replace(" ", ''))

            print(f'You been obtained ({seleccionados}), you earned +{total_score} points.', '')
            

def set_level(l):
    global level
    level = l


def add_score(qty = 1):
    global score
    score += qty


def subtract_score(qty = 1):
    global score
    score -= qty


def add_attempts(qty = 1):
    global attempts
    attempts += qty


def subtract_attempts(qty = 1, reason = ''):
    global attempts, error_message
    attempts -= qty
    error_message = reason if reason != "" else error_message


def check_attempts():
    global attempts, error_message

    if attempts == 0:
        print(alert_message)
        game_over()


def move_to_room(room_key, return_to_room = '', is_coming_back = False):
    global actual_room

    actual_room = rooms[room_key]
    actual_room['return_to_room'] = return_to_room

    update_player_info()


def set_direction_done(direction):
    global directions_done
    directions_done.append(direction)


def is_level_required():
    global actual_room, level

    level_required = actual_room['level_required']
    return True if level_required > 0 and level <= level_required else False 


def show_errors_if_exists():
    global error_message

    if error_message != '':
        print(error_message)
        error_message=''

"""
    Here we start the game showing the intro and requesting the username
"""
def intro_scene(): 
    global player_welcome, error_message

    directions = get_room_directions()

    if player_welcome is False:
        print(f'\nWelcome {player}. Choose wisely and good luck!')
        print('--Type menu to see the menu options\n')

        player_welcome = True
    
    show_errors_if_exists()

    # print(game_file['intro_scene'], callback=collet_object_from_room)
    collet_object_from_room()

    #show the list of directions
    directions_list = "\nNow, select a direction to continue\n"
    for direction in directions:
        completed =  " is completed :)" if direction in directions_done else ''

        directions_list += '{0}{1}\n'.format(
            direction.title(),
            completed
        )

    print(directions_list) 
    
    goto = cinput("Your choices are north, east, south and west. Which will you choose?: ")
    print(f'You type {goto}')
        
    if (goto == 'north' or goto == 'n') and 'north' in directions: 
        move_to_room('great_salon_scene')
        great_salon_scene()

    elif (goto == 'east' or goto == 'e') and 'east' in directions:
        move_to_room('kitchen_scene', actual_room['id'])
        kitchen_scene()

    elif (goto == 'south' or goto =='s') and 'south' in directions:
        error_message = 'This leads to the outside of the house. You have found yourself trapped :('
        move_to_room('intro_scene')
        intro_scene()
        
    elif (goto == 'west' or goto == 'w') and 'west' in directions: 
        move_to_room('haunted_room_scene')
        haunted_room_scene()

    else:
        error_message = 'Please enter valid decision'
        intro_scene()


def great_salon_scene():
    global error_message

    show_errors_if_exists()

    # print("\nYou enter a grand salon where the windows are broken, there is a chilly atmosphere and suddenly\nyou hear a noise. It might be the wind or it might be a ghost. Which decision") 

    dw = DirectionWindow(width=400, height=400)
    option = dw.get_option()

    if option == 1: #upstairs 
        move_to_room('attic_scene')
        attic_scene()

    elif option == 2: #left 
        move_to_room('great_salon_scene')
        great_salon_scene()

    elif option == 3: #right 
        move_to_room('living_room_scene')
        living_room_scene()

    else:
        error_message = 'You were sent to Main salon'
        move_to_room('intro_scene', is_coming_back=True)
        intro_scene()


def attic_scene():
    global rooms, actual_room, level, error_message, alert_message

    if 'scene_completed' in rooms['attic_scene']:
        print("You have completed this scene")
        move_to_room('great_salon_scene',  is_coming_back=True)
        great_salon_scene()
        
    check_attempts()

    # print("""You see a tall dark figure but behind him appears to be an unknown object. What would you like to do?\nYou have to choose from your inventory an object to kill the figure with and reach the unknown object.""", '[bold yellow]', callback=show_inventory)
    
    show_errors_if_exists()
    collet_object_from_room()

    while True:
        user_decision = cinput("\nYou have chosen the right way to compelete the level. What will you like to do? Go forward or backward: ")

        if user_decision == 'forward' or user_decision == 'f':
            add_score(25)
            print(f"You've found the treasure! Congrats you have obtained +25 points.")
            
            text_action = f"You've pass the {actual_room['name']}"

            if 'scene_completed' in rooms['evil_spirit_scene']:
                set_direction_done('north')
                set_level(2)
                text_action = f"You level up to 2"

            if 'scene_completed' not in rooms['attic_scene']:
                rooms['attic_scene']['scene_completed'] = True
            
            WinnerWindow(
                prize="+25 points",
                action=text_action
            )

            move_to_room('intro_scene', is_coming_back=True)
            intro_scene()
            break

        elif user_decision == 'backward' or user_decision == 'b':
            error_message = 'You have lost the level! You have obtained 0 points and lose an attepmt.'
            alert_message = error_message
            subtract_attempts()
            move_to_room('intro_scene', is_coming_back=True)
            intro_scene()
            break

        else:
            print("Please enter valid decision")


def kitchen_scene():
    global rooms, actual_room, error_message
    
    show_errors_if_exists()
    
    if is_level_required():
        room = actual_room['name'] 
        level = actual_room['level_required'] 

        error_message = f'Ohh no! You are not allowed to pass to the {room}, you need to complete the level: {level}. Try to start north.'
        move_to_room('intro_scene', is_coming_back=True)
        intro_scene()

    else:
        def start_fight_with_zombie_cook():
            global level, error_message

            print("There's a putrid odor coming from a dark, decomposed figure, moving through the shadows. Suddenly you see him clearly: a zombie cook with a sharp knife in his hand. He looks like he's not willing to leave you alone, and he stares at you with dead eyes as he approaches you with a nasty grin on his face. You have to be very careful if you want to survive in this mysterious house.")

            show_inventory()
            get_item = cinput("\nWhat object do you want to select? ")

            if get_item == 'flamethrower' and get_item in inventory:
                
                print("Congratulations! You have managed to kill the zombie cook using a flamethrower. Your bravery and skill are impressive. Continue exploring the mysterious house and facing the dangers you encounter. Good luck!")
                    
                add_score(75)
                    
                if not 'scene_completed' in rooms['kitchen_scene']:
                    actual_room['scene_completed'] = True
                
                text_action = f"You've pass the {actual_room['name']}"
                
                set_direction_done('east')
                set_level(3)

                text_action = f"You level up to 3"
                
                WinnerWindow(
                    prize="+75 points",
                    action=text_action
                )

                move_to_room('intro_scene', is_coming_back=True)
                intro_scene()

            else:
                subtract_attempts(2)
                subtract_score(5)
                error_message = "Sorry, you've been caught and eaten by the zombie cook! Improve your strategy and try again!"
                move_to_room('intro_scene', is_coming_back=True)
                intro_scene()


        def start_scene():
            collet_object_from_room()

            dw = DirectionWindow(width=400, height=400, text_opt1='Right', text_opt2='Left', text_opt3='Backward')
            option = dw.get_option()

            if option == 1: #Right
                move_to_room('evil_spirit_scene', return_to_room='kitchen_scene')
                evil_spirit_scene()

            elif option == 2: #Left
                if 'scene_completed' in rooms['kitchen_scene']:
                    print("You have completed this scene")
                    move_to_room('intro_scene', is_coming_back=True)
                    intro_scene()

                else:
                    start_fight_with_zombie_cook()

            elif option == 3: #Backward
                move_to_room('intro_scene', is_coming_back=True)
                intro_scene()

            else:
                kitchen_scene()

        print(
            """You have found yourself in the kitchen of the haunted house. There is a mess everywhere\nas well as it being dark and burnt. While\nyou are looking around and discovering, you see an object on the floor of what appears\nto be a sword and add it to your inventory\nYou have to make a decision: right, left, backward. """ 
        )

        start_scene()
        

def evil_spirit_scene():
    global rooms, actual_room, inventory, level, error_message, alert_message

    def where_go_player():
        if actual_room['return_to_room'] == 'kitchen_scene':
            move_to_room('kitchen_scene',  is_coming_back=True)
            kitchen_scene()

        elif actual_room['return_to_room'] == 'living_room_scene':
            move_to_room('living_room_scene',  is_coming_back=True)
            living_room_scene()

    if 'scene_completed' in actual_room:
        print("You have completed this scene")
        where_go_player()
        
    check_attempts()
 
    def start_scene():
        global level
        
        show_errors_if_exists()
        show_inventory()

        get_item = cinput("\nWhat object do you want to select? ")

        if get_item == 'flashlight' and 'flashlight' in inventory:
        
            print("""Oh no, you have awakened the monster\nnow you must fight if you want to pass the level\n\nWhat do you want to do?""")
            
            dw = DirectionWindow(width=400, 
                height=400, 
                text_opt1='Fight', 
                text_opt2='Run',
                text_opt3='Backward'
            )

            option = dw.get_option()

            if option == 1: #Fight
                print("You have chosen to fight")
                
                show_inventory() 
                get_item = cinput("\nWhat object do you want to select? ")

                if get_item == 'sword' and get_item in inventory:
                    add_score(50)
                    print(f"The monster has been killed. You've found the treasure! Congrats you have obtained +50 points.")

                    if not 'scene_completed' in actual_room:
                        actual_room['scene_completed'] = True

                    text_action = f"You've pass the {actual_room['name']}"

                    if 'scene_completed' in rooms['attic_scene']:
                        set_direction_done('north')
                        set_level(2)
                        text_action = f"You level up to 2"

                    WinnerWindow(
                        prize="+50 points",
                        action=text_action
                    )
                
                    move_to_room('intro_scene', is_coming_back=True)
                    intro_scene()
                    
                else:
                    subtract_attempts()
                    error_message = 'Wrong object or object is not in inventory, you lose an attempt'
                    move_to_room('intro_scene', is_coming_back=True)
                    intro_scene()

            elif option == 2: #Run
                subtract_score(2)
                subtract_attempts(reason="You decide run, you lose an attempt and 2 score points")
                where_go_player()

            elif option == 3: #Backward
                where_go_player()

            else:
                error_message = f'Option is not valid, please write a valid option'
                start_scene()

        elif get_item != 'flashlight' and get_item in inventory:
            alert_message = 'You have been killed by the monsters because you have been selected the incorrect object for pass the level into the Evil Spirit, you lose an attempt.'
            
            subtract_attempts(reason = alert_message)
            where_go_player()
            
        else:
            error_message = f'{get_item} is not available into the inventory'
            start_scene()

    print("""\nYou are inside the room, but everything is dark because the light has been damaged """)
    start_scene()


def living_room_scene():
    global rooms, actual_room, error_message

    show_errors_if_exists()

    dw = DirectionWindow(width=400, height=400, text_opt1='Right', text_opt2='Backward', text_opt3='Left')
    option = dw.get_option()

    if option == 1: #Right
        if not 'attempt_obtained' in actual_room:
            add_attempts()
            actual_room['attempt_obtained'] = True
            print("Congratulations, you've won one more attempt.")

        else:
            error_message = "There are no more prizes in this room sadly :("

        move_to_room('living_room_scene', is_coming_back=True)
        living_room_scene()

    elif option == 2: #Backward
        move_to_room('great_salon_scene', is_coming_back=True)
        great_salon_scene()

    elif option == 3: #Left
        move_to_room('evil_spirit_scene', return_to_room='living_room_scene')
        evil_spirit_scene()

    else:
        error_message = 'You must select an option'
        living_room_scene() 
        
    
def haunted_room_scene():
    global error_message, actual_room

    if is_level_required():
        room = actual_room['name'] 
        level = actual_room['level_required'] 

        error_message = f'Ohh no! You are not allowed to pass to the {room}, you need to complete the level: {level}. Try go to north or east.'
        move_to_room('intro_scene', is_coming_back=True)
        intro_scene()
    
    check_attempts()
    show_errors_if_exists()
    collet_object_from_room()

    dw = DirectionWindow(width=400, height=400, text_opt1='Right', text_opt2='Left', text_opt3='Backward')
    option = dw.get_option()

    if option == 1: #Right
        move_to_room('trap_room_scene')
        trap_room_scene()

    elif option == 2: #Left
        move_to_room('mummy_scene')
        mummy_scene()

    elif option == 3: #Backward
        move_to_room('intro_scene', is_coming_back=True)
        intro_scene()

    else:
        error_message = 'You must select an valid option'
        move_to_room('living_room_scene', is_coming_back=True)
        living_room_scene() 


def trap_room_scene():
    global alert_message, error_message, inventory

    check_attempts()
    show_errors_if_exists()

    print('You are trapped in the room, and you must kill an unknown monster that tries to attack you, what action do you want to take?')

    print('run (r) or takeaction (t)')
    action = cinput("\nSelect a option (r/t): ")

    if action == 'takeaction' or action == 't': 
        show_inventory()

        while True:
            get_item = cinput("\nWhat object do you want to select? ")
            
            if get_item not in inventory:
                print(f'{get_item} is not available :( try again')

            else:
                error_message = "You're still trapped, you can't get out of the room this way, you lost two attempts"
                alert_message = error_message

                subtract_attempts(2)
                move_to_room('trap_room_scene')
                trap_room_scene()
                break

    elif action == 'run' or action == 'r':
        subtract_attempts()
        alert_message = 'Lograste salir de la habitacion de trampas, pero has perdido una vida'
        error_message = alert_message
        move_to_room('haunted_room_scene')
        haunted_room_scene()

    else:
        error_message = 'You must select a valid option'
        trap_room_scene()


def mummy_scene():
    global inventory, error_message, alert_message

    check_attempts()
    show_errors_if_exists()

    print('You have found the mummy that guards the treasure, what action do you want to take?')
    print('Fight (f) or run')

    action = cinput("\nSelect a option (f/r): ")

    if action == 'fight' or action == 'f': 
        show_inventory()

        get_item = cinput("\nWhat object do you want to select? ")

        if get_item in inventory and (get_item == 'amulet' or get_item ==  'amulet'):
            add_score(100)
            print(f"The mummy has been killed. You've found the treasure! Congrats you have obtained +100 points.")

            WinnerWindow(prize='+100 points', action="You've won")
            player_win()

        else:
            alert_message = 'You have been killed by the mummy!'
            error_message = alert_message
            subtract_attempts()
            mummy_scene()

    elif action == 'run' or action == 'r':
        print("""\nYou lost an attempt """)
        subtract_attempts()
        move_to_room('haunted_room_scene')
        haunted_room_scene()

    else:
        error_message = 'You must select a valid option'
        mummy_scene()
    return False
 

def ask_for_play_again():
    global player, score, attempts

    confirm = cinput("\nWant you play again? (yes/no): ")

    if confirm == 'yes' or confirm == 'y':
        confirm = cinput(f"\nWant you play like {player}?: ")
        if confirm != 'yes' or confirm != 'y':
            player = ''

        attempts = 5
        set_level(1)
        start_game()
    else:
        print("Thaks for play Tanny/'s treasure hunt!") 
        exit()


"""
    Player lose the game and all their points and downgrade the level to 1 againg
"""
def game_over():
    loser_message = "I am so sorry, you have lost the mystery house game. You failed to defeat the mummy and other monstrosities, but don't worry, you can always try again! Cheer up!"

    try:
        print(loser_message) 
        GameOverWindow()
    except :
        print(loser_message) 
    
    ask_for_play_again()


def player_win():
    print("""Congratulations! You have won the mystery house game and have shown your ability to defeat the mummy and other monstrosities. You are a true hero!""")

    show_final_score()

    ask_for_play_again()

# start_game()
show_final_score()