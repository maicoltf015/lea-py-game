import os
import json
from rich.console import Console  
from rich.tree import Tree
from rich import print as rprint
from time import sleep
from helpers.window import DirectionWindow, GameOverWindow, WinnerWindow

# global console
console = Console()

class Loading():
    def __init__(self, l, f='', time=0.5):
        data = [1]
        with console.status(f"[bold blue]{l}") as status:
            while data:
                num = data.pop(0)
                sleep(time)
                # console.log(f"[green]Finish fetching data[/green] {num}")

            if f!= '':
                console.log(f'[bold][red]{f}!')
 
class CustomPrint():
    def __init__(self, text):
        # borde = Box(width=len(text) + 4, height=3)
        console.rule(text.center(len(text) + 2), style="bold green")
 
class CuteWrite:
    def __init__(self, text, color='', callback=None, time=0.005):
        for letter in text:
            console.print(color+letter, end='')
            sleep(time)
        print()
        if callback is not None:
            callback()

class Game:
    def __init__(self):
        
        self.player = 'Lea'                    #name of player
        self.score = 0                      #score of the player
        self.level = 1                      #level of the player
        self.is_level_completed = 0         #check if is the level completed
        self.rooms = {}                     #list of rooms
        self.inventory= []                  #list of inventory
        self.attempts = 5

        self.game_file = self.get_json_file_game()
        self.actual_room = self.game_file['rooms']['intro_scene']

        self.error_message = ''
        self.alert_message = ''
        self.player_welcome = False
        self.refresh_player_info = True
        self.directions_done = []

        # set the rooms of the game
        # Loading("Starting game")
        # Loading("Setting Rooms")
        self.__set_rooms()

        # Loading("Setting Inventory")
        self.__set_inventory()
 
        # game intro
        self.intro()
     
    
    def update_header(self, cls=True):  
        
        if cls:
            os.system('cls')
        
        if self.refresh_player_info:
            CustomPrint(f"Player: {self.player} | Room: {self.actual_room['name']} | Score: {self.score} | Level: {self.level}")
        else:
            self.refresh_player_info = True

     
    def __set_rooms(self):
        rooms = self.game_file['rooms']
        for room_key in rooms:
            self.rooms[room_key] = rooms[room_key]

    
    def __get_room_directions(self):
        return self.actual_room['directions']

    
    def __set_inventory(self, object=''):
        self.inventory = ['map']
 
    
    def __drop_object(self, object=''):
        if object in self.inventory:
            self.inventory.remove(str(object))

    
    def __collect_object(self, object):
        if object != '' and not object in self.inventory:
            self.inventory.append(str(object))
    
    
    def show_inventory(self):
        tree = Tree("\n\nGeneral inventory!")
        # gi = tree.add("[blue]My objects")
        
        for item in self.inventory : 
            tree.add(item.title())

        # ro = tree.add(f"[green]{self.actual_room['name']} objects")
        # objects = self.actual_room['objects']
        # if len(objects) > 0: 
        #     for object in self.actual_room['objects']:
        #         ro.add(object.title())
        # else:
        #     ro.add('[red]No objects in this room')

        rprint(tree) 


    def collet_object_from_room(self):
        objects = self.actual_room['objects']
         
        if len(objects) > 0:
            tree = Tree("Room objects")
            for object in objects:
                tree.add(f'[blue]{object.title()}')
                
            rprint(tree)

            for object in objects:
                decision = str(console.input(f"\n[blue]Do you want to add[/] [green]{object.title()}[/] [blue]to inventory? (y/n): ")).lower()
                if decision == 'y':
                    self.actual_room['objects'].remove(object)
                    self.__collect_object(object)
                    CuteWrite(f'{object.title()} has been obtained', '[blue]')
                    sleep(1)


    def __add_score(self, qty = 1):
        self.score += qty

    
    def __subtract_score(self, qty = 1):
        self.score -= qty
   
    
    def __add_attempts(self, qty = 1):
        self.attempts += qty


    def __subtract_attempts(self, qty = 1):
        self.attempts += qty

    
    def check_attempts(self):
        if self.attempts == 0:
            CuteWrite(self.alert_message)
            sleep(1)
            self.game_over()


    def __move_to_room(self, room_key, return_to_room = '', is_coming_back = False):
        self.actual_room = self.rooms[room_key]
        self.actual_room['return_to_room'] = return_to_room

        room_name = self.actual_room['name']
        Loading(f'{"Coming back" if is_coming_back else "Entering"} to {room_name}', time=1.5)
        getattr(self, room_key)()


    def __set_direction_done(self,room_key, direction):
        self.directions_done.append(direction)
        del self.rooms[room_key]['directions'][direction] 

    
    def is_level_required(self):
        level_required = self.actual_room['level_required']
        return True if level_required > 0 and self.level <= level_required else False 

    
    def show_errors_if_exists(self):
        if self.error_message != '':
            CuteWrite(self.error_message, '[bold red]')
            self.error_message=''
            sleep(1)
    
    """
        Here we start the game showing the intro and requesting the username
    """
    def intro(self):
        # CuteWrite(self.game_file['intro'], color="[bold blue]")
        self.get_player_info()


    def get_player_info(self):
        self.show_errors_if_exists()

        if self.player == '':
            self.player = str(console.input("\n\n[green]What is your name?: "))
            if self.player == '':
                self.error_message = 'The player name cannot be empty'
                self.get_player_info()

        self.intro_scene()

    
    def intro_scene(self): 
        self.update_header(cls=False)
        directions = self.__get_room_directions()

        if self.player_welcome is False:
            CuteWrite(f'Welcome {self.player}. Choose wisely and good luck!', color="[bold blue]")
            self.player_welcome = True
        
        self.show_errors_if_exists()

        # CuteWrite(self.game_file['intro_scene'], color="[bold blue]", callback=self.collet_object_from_room)
        self.collet_object_from_room()

        #show the list of directions
        tree = Tree("\nNow, select a direction to continue")
        for direction in directions:
            tree.add(f'[blue]{direction.title()}')


        if len(self.directions_done) > 0:
            # dd = tree.add(f'[blue]You have already been in this direction')
            for direction_done in self.directions_done:
                tree.add(f'[green]{direction_done} is completed ✅')
                 

        rprint(tree) 
        
        goto = str(console.input("\n[blue]Your choices are north, east, south and west. Which will you choose?: ")).lower()

        def start_direction(d, return_to_room=''): 
            room_key = directions[d]
            self.__move_to_room(room_key, return_to_room) 
            
        if (goto == 'north' or goto == 'n') and 'north' in directions: 
            start_direction('north')
 
        elif (goto == 'east' or goto == 'e') and 'east' in directions:
           start_direction('east', self.actual_room['id'])
        
        elif (goto == 'south' or goto =='s') and 'south' in directions:
            self.__subtract_score()
            self.actual_room = self.game_file['rooms']['intro_scene']
            console.print(f'[red]This leads to the outside of the house. You have found yourself trapped 😢!')
            self.intro_scene()
            
        elif (goto == 'west' or goto == 'w') and 'west' in directions:
            start_direction('west',  self.actual_room['id'])

        else:
            self.refresh_player_info = False
            self.error_message = 'Please enter valid decision'
            self.intro_scene()

 
    def great_salon_scene(self):
        self.update_header() 
        self.show_errors_if_exists()

        # CuteWrite("\nYou enter a grand salon where the windows are broken, there is a chilly atmosphere and suddenly\nyou hear a noise. It might be the wind or it might be a ghost. Which decision", color="[bold blue]") 

        dw = DirectionWindow(width=400, height=400)
        option = dw.get_option()

        if option == 1: #upstairs 
            self.__move_to_room('attic_scene')

        elif option == 2: #left 
            self.__move_to_room('great_salon_scene')

        elif option == 3: #right 
            self.__move_to_room('living_room_scene')

        else:
            self.error_message = 'Select a valid option'
            self.great_salon_scene()
    
    def attic_scene(self):
        self.update_header()
        self.check_attempts()
        

        # CuteWrite("""You see a tall dark figure but behind him appears to be an unknown object. What would you like to do?\nYou have to choose from your inventory an object to kill the figure with and reach the unknown object.""", '[bold yellow]', callback=self.show_inventory)
        
        self.show_errors_if_exists()
        self.collet_object_from_room()

        while True:
            user_decision = str(console.input("\n[blue]You have chosen the right way to compelete the level. What will you like to do? Go forward or backward: ")).lower()

            if user_decision == 'forward' or user_decision == 'f':
                self.__add_score(25)
                CuteWrite(f"You've found the treasure! Congrats you have obtained 25 points.", '[bold green]')
                self.__set_direction_done('intro_scene', 'north')
                WinnerWindow()
                self.level = 2
                self.__move_to_room('intro_scene', is_coming_back=True)
                break
            elif user_decision == 'backward' or user_decision == 'b':
                self.__subtract_attempts()
                CuteWrite(f"you have lost the level! You have obtained 0 points.", '[bold red]')
                sleep(0.5)
                self.__move_to_room('intro_scene', is_coming_back=True)
                break
            else:
                CuteWrite("Please enter valid decision", '[bold red]')

    
    def kitchen_scene(self):
        self.show_errors_if_exists()
        
        if self.is_level_required():
            self.refresh_player_info = True
            room = self.actual_room['name']
            return_to_room = self.actual_room['return_to_room']

            self.error_message = f'Ohh no! You are not allowed to pass to the {room}, you need to complete the level: {self.level}'
            self.__move_to_room(return_to_room, is_coming_back=True)
 
        else:
            def start_scene():
                dw = DirectionWindow(width=400, height=400, text_opt1='Right', text_opt2='Left', text_opt3='Backward')
                option = dw.get_option()

                if option == 1: #Right
                    self.__move_to_room('evil_spirit_scene', return_to_room='kitchen_scene')

                elif option == 2: #Left
                    self.kitchen_scene()

                elif option == 3: #Backward
                    self.__move_to_room('intro_scene', is_coming_back=True)

                else:
                    self.kitchen_scene()

            CuteWrite(
                text="""
                    You have found yourself in the kitchen of the haunted house. There is a mess everywhere
                    as well as it being dark and burnt. While you are looking around and discovering, you see an object on the floor of what appears
                    to be a sword and add it to your inventory. You have to make a decision: right, left, backward. """, 
                color='[bold yellow]', 
                callback=start_scene
            )
            

    def evil_spirit_scene(self):
        if 'scene_completed' in self.actual_room:
            CuteWrite("You have completed this scene", '[green]')
            sleep(0.5)
            self.__move_to_room(self.actual_room['return_to_room'],  is_coming_back=True)
            
        self.check_attempts()

        def start_scene():
            self.show_errors_if_exists()
            self.show_inventory()

            get_item = str(console.input("\n[yellow]What object do you want to select? ")).lower()

            if get_item == 'flashlight' and 'flashlight' in self.inventory:

                CuteWrite("""Oh no, you have awakened the monster\nnow you must fight if you want to pass the level\n\nWhat do you want to do?""", color='[bold red]')
                sleep(2) 
                
                dw = DirectionWindow(width=400, 
                    height=400, 
                    text_opt1='Fight', 
                    text_opt2='Run',
                    text_opt3='Backward'
                )

                option = dw.get_option()

                if option == 1: #Fight
                    CuteWrite("You have chosen to fight", '[bold green]', time=0.05)
                    
                    self.show_inventory() 
                    get_item = str(console.input("\n[blue]What object do you want to select? ")).lower()

                    if get_item == 'sword' and get_item in self.inventory:
                        self.__add_score(50)
                        CuteWrite(f"The monster has been killed. You've found the treasure! Congrats you have obtained +50 points.", '[bold green]')
                        WinnerWindow()
                        self.__set_direction_done('intro_scene', 'east')

                        if not 'scene_completed' in self.actual_room:
                            self.actual_room['scene_completed'] = True

                        self.intro_scene()
                        
                    else:
                        CuteWrite("Wrong object or object is not in inventory", '[bold green]', time=0.05)
                        self.__subtract_attempts()
                        self.evil_spirit_scene()

                elif option == 2: #Run
                    self.__subtract_attempts()
                    self.evil_spirit_scene()

                elif option == 3: #Backward
                    self.__move_to_room(self.actual_room['return_to_room'],  is_coming_back=True)

                else:
                    self.error_message = f'Option is not valid, please write a valid option'
                    start_scene()
            else:
                self.error_message = f'{get_item} is not available into the inventory'
                start_scene()

        CuteWrite("""\nYou are inside the room, but everything is dark because the light has been damaged """, '[bold blue]', callback=start_scene)


    def living_room_scene(self):
        self.show_errors_if_exists()

        dw = DirectionWindow(width=400, height=400, text_opt1='Right', text_opt2='Backward', text_opt3='Left')
        option = dw.get_option()

        if option == 1: #Right
            if not 'attempt_obtained' in self.actual_room:
                self.__add_attempts()
                self.actual_room['attempt_obtained'] = True
                CuteWrite("Congratulations, you've won one more attempt.")
                sleep(0.5)

            self.living_room_scene()
        elif option == 2: #Backward
            self.__move_to_room('great_salon_scene', is_coming_back=True)

        elif option == 3: #Left
            self.__move_to_room('evil_spirit_scene', return_to_room='living_room_scene')

        else:
            self.error_message = 'You must select an option'
            self.living_room_scene() 
            
        
    def haunted_room_scene(self):
        self.show_errors_if_exists()
        self.collet_object_from_room()

        dw = DirectionWindow(width=400, height=400, text_opt1='Right', text_opt2='Left', text_opt3='Backward')
        option = dw.get_option()

        if option == 1: #Right
            self.__move_to_room('trap_room_scene')

        elif option == 2: #Left
            self.__move_to_room('mummy_scene')

        elif option == 3: #Backward
            self.__move_to_room('intro_scene', is_coming_back=True)

        else:
            self.error_message = 'You must select an option'
            self.living_room_scene() 

    
    def trap_room_scene(self):
        self.show_errors_if_exists()

        console.print('[red]You are trapped in the room, and you must kill an unknown monster that tries to attack you, what action do you want to take?')

        console.print('[green]run (r)[/] or [blue]takeaction[/]')
        action = str(console.input("\n[red]Select a option (r/t): ")).lower()

        if action == 'takeaction' or action == 't': 
            self.show_inventory()

            while True:
                get_item = str(console.input("\n[blue]What object do you want to select? ")).lower()
                
                if get_item not in self.inventory:
                    CuteWrite(f'{get_item} is not available :( try again')
                    sleep(0.5)
                else:
                    self.error_message = "You're still trapped, you can't get out of the room this way, you lost two attempts"
                    self.__subtract_attempts(2)
                    self.trap_room_scene()
                    break

        elif action == 'run' or action == 'r':
            self.__subtract_attempts()
            self.__move_to_room('haunted_room_scene')

        else:
            self.error_message = 'You must select a valid option'
            self.trap_room_scene()

    
    def mummy_scene(self):
        self.check_attempts()
        self.show_errors_if_exists()

        console.print('[red]You have found the mummy that guards the treasure, what action do you want to take?')

        console.print('[red]Fight (f)[/] or [green]run[/]')
        action = str(console.input("\n[red]Select a option (f/r): ")).lower()

        if action == 'fight' or action == 'f': 
            self.show_inventory()

            get_item = str(console.input("\n[blue]What object do you want to select? ")).lower()

            if get_item in self.inventory and (get_item == 'amulet' or get_item ==  'amulet'):
                self.__add_score(100)
                CuteWrite(f"The mummy has been killed. You've found the treasure! Congrats you have obtained +100 points.", '[bold green]')
                WinnerWindow()
                self.player_win()

            else:
                self.alert_message = 'You have been killed by the mummy!'
                self.error_message = 'You have been killed by the mummy!'
                self.__subtract_attempts()
                self.mummy_scene()

        elif action == 'run' or action == 'r':
            CuteWrite("""\nYou lost an attempt """, '[bold red]')
            self.__subtract_attempts()
            self.__move_to_room('haunted_room_scene')

        else:
            self.error_message = 'You must select a valid option'
            self.mummy_scene()
        return False


    def get_json_file_game(self):
        with open('game.json', 'r') as file_game:
            file_json = file_game.read()

        return json.loads(file_json)
    

    """
        Player lose the game and all their points and downgrade the level to 1 againg
    """
    def game_over(self):
        try:
            GameOverWindow()
        except :
            CuteWrite("You lose!", '[bold red]') 
            
        confirm = str(console.input("\n[blue]Want you play again?")).lower()

        if confirm == 'yes' or confirm == 'y':
            confirm = str(console.input(f"\n[blue]Want you play like {self.player}?")).lower()
            if confirm != 'yes' or confirm != 'y':
                self.player = ''
            self.intro()
            self.score = 0
            self.level = 1
            self.attempts = 5
        else:
            exit()
    
    def player_win(self):
        CuteWrite(
            text="""Congratulations, you have finished the game""",
            time=0.008
        )
 
Game()