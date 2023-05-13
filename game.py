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
  
class CuteWrite:
    def __init__(self, text, color='', callback=None, time=0.005):
        # for letter in text:
        #     console.print(color+letter, end='')
        #     sleep(time)

        # print()

        if callback is not None:
            callback()

class Game:
    def __init__(self):
        
        self.player = ''                 #name of player
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
         
        hearth ='❤️  '
        attemps = hearth * self.attempts if self.attempts > 0 else "❌"

        if self.refresh_player_info:
            text = '{0}{1}{2}{3}{4}'.format(
                f"[Player: [blue]{self.player}[/] | ",
                f"Room: [blue]{self.actual_room['name']}[/] | ",
                f"Score: [blue]{self.score}[/] | ",
                f"Level: [blue]{self.level}[/] | ",
                f"Attempts: [blue]{attemps}[/]]"
            )

            console.print(text, style="bold")
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
        room_key = self.actual_room['id']
        objects_len = len(objects)

        s = "s" if objects_len != 1 else ''

        if objects_len > 0:
            tree = Tree(f'There is {objects_len} object{s} in this room')
            for object in objects:
                tree.add(f'[blue]{object.title()}')
                
            rprint(tree)

            seleccionados = ''
            total_score = 0
            for object in objects:
                decision = str(console.input(f"\n[blue]Do you want to add[/] [green]{object.title()}[/] [blue]to inventory? (y/n): ")).lower()
                if decision == 'y':
                    self.__collect_object(object)
                    self.__add_score(5)
                    total_score += 5
                    seleccionados += f'{object.title()}, '

            seleccionados = seleccionados.rstrip(", ")
            if seleccionados != '':
                for object_to_remove in seleccionados.split(","):
                    self.rooms[room_key]['objects'].remove(object_to_remove.lower().replace(" ", ''))

                CuteWrite(f'You been obtained ({seleccionados}), you earned +{total_score} points.', '[blue]', time=0.05)
                

    def __add_score(self, qty = 1):
        self.score += qty

    
    def __subtract_score(self, qty = 1):
        self.score -= qty
   
    
    def __add_attempts(self, qty = 1):
        self.attempts += qty


    def __subtract_attempts(self, qty = 1, reason = ''):
        self.attempts -= qty
        self.error_message = reason if reason != "" else self.error_message

    
    def check_attempts(self):
        if self.attempts == 0:
            CuteWrite(self.alert_message)
            sleep(1)
            self.game_over()


    def __move_to_room(self, room_key, return_to_room = '', is_coming_back = False):
        self.actual_room = self.rooms[room_key]
        self.actual_room['return_to_room'] = return_to_room

        room_name = self.actual_room['name']
        # Loading(f'{"Coming back" if is_coming_back else "Entering"} to {room_name}', time=1.5)
        self.update_header()
        getattr(self, room_key)()


    def __set_direction_done(self,room_key, direction):
        self.directions_done.append(direction)
        # del self.rooms[room_key]['directions'][direction] 

    
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

        self.__move_to_room('intro_scene')

    
    def intro_scene(self): 
        directions = self.__get_room_directions()

        if self.player_welcome is False:
            # CuteWrite(f'Welcome {self.player}. Choose wisely and good luck!', color="[bold blue]", time=0.05)
            self.player_welcome = True
        
        self.show_errors_if_exists()

        # CuteWrite(self.game_file['intro_scene'], color="[bold blue]", callback=self.collet_object_from_room)
        self.collet_object_from_room()

        #show the list of directions
        tree = Tree("\nNow, select a direction to continue")
        for direction in directions:
            completed =  " is completed ✅" if direction in self.directions_done else ''
            color =  "green" if direction in self.directions_done else 'yellow'

            tree.add('[{0}]{1}{2}'.format(
                color,
                direction.title(),
                completed
            ))

        # if len(self.directions_done) > 0:
        #     # dd = tree.add(f'[blue]You have already been in this direction')
        #     for direction_done in self.directions_done:
        #         tree.add(f'[green]{direction_done} is completed ✅')

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
            self.error_message = 'This leads to the outside of the house. You have found yourself trapped 😢!'
            self.__move_to_room('intro_scene') 
            
        elif (goto == 'west' or goto == 'w') and 'west' in directions:
            start_direction('west',  self.actual_room['id'])

        else:
            self.refresh_player_info = False
            self.error_message = 'Please enter valid decision'
            self.intro_scene()

 
    def great_salon_scene(self):
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
            self.error_message = 'You were sent to Main salon'
            self.__move_to_room('intro_scene', is_coming_back=True)
    
    
    def attic_scene(self):
        if 'scene_completed' in self.actual_room:
            CuteWrite("You have completed this scene", '[green]', time=0.05)
            self.__move_to_room('great_salon_scene',  is_coming_back=True)
            
        self.check_attempts()

        # CuteWrite("""You see a tall dark figure but behind him appears to be an unknown object. What would you like to do?\nYou have to choose from your inventory an object to kill the figure with and reach the unknown object.""", '[bold yellow]', callback=self.show_inventory)
        
        self.show_errors_if_exists()
        self.collet_object_from_room()

        while True:
            user_decision = str(console.input("\n[blue]You have chosen the right way to compelete the level. What will you like to do? Go forward or backward: ")).lower()

            if user_decision == 'forward' or user_decision == 'f':
                self.__add_score(25)
                CuteWrite(f"You've found the treasure! Congrats you have obtained +25 points.", '[bold green]', time=0.05)
              
                text_action = f"You've pass the {self.actual_room['name']}"

                if 'scene_completed' in self.rooms['evil_spirit_scene']:
                    self.__set_direction_done('intro_scene', 'north')
                    self.level = 2
                    text_action = f"You level up to 2"


                if 'scene_completed' not in self.rooms['attic_scene']:
                    self.rooms['attic_scene']['scene_completed'] = True
                
                WinnerWindow(
                    prize="+25 points",
                    action=text_action
                )

                self.__move_to_room('intro_scene', is_coming_back=True)
                break

            elif user_decision == 'backward' or user_decision == 'b':
                self.error_message = 'You have lost the level! You have obtained 0 points and lose an attepmt.'
                self.alert_message = self.error_message
                self.__subtract_attempts()
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

            self.error_message = f'Ohh no! You are not allowed to pass to the {room}, you need to complete the level: {self.level}. Try to start north.'
            self.__move_to_room(return_to_room, is_coming_back=True)
 
        else:
            def start_fight_with_zombie_cook():
                CuteWrite("There's a putrid odor coming from a dark, decomposed figure, moving through the shadows. Suddenly you see him clearly: a zombie cook with a sharp knife in his hand. He looks like he's not willing to leave you alone, and he stares at you with dead eyes as he approaches you with a nasty grin on his face. You have to be very careful if you want to survive in this mysterious house.", '[bold red]')

                self.show_inventory()
                get_item = str(console.input("\n[yellow]What object do you want to select? ")).lower()

                if get_item == 'flamethrower' and get_item in self.inventory:
                    
                    CuteWrite("Congratulations! You have managed to kill the zombie cook using a flamethrower. Your bravery and skill are impressive. Continue exploring the mysterious house and facing the dangers you encounter. Good luck!", '[bold green]', time=0.05)
                        
                    self.__add_score(75)
                        
                    if not 'scene_completed' in self.actual_room:
                        self.actual_room['scene_completed'] = True
                    
                    text_action = f"You've pass the {self.actual_room['name']}"
                    
                    self.__set_direction_done('intro_scene', 'east')
                    self.level = 3
                    text_action = f"You level up to 3"
                    
                    WinnerWindow(
                        prize="+75 points",
                        action=text_action
                    )

                    self.__move_to_room('intro_scene', is_coming_back=True)

                else:
                    self.__subtract_attempts(2)
                    self.__subtract_score(5)
                    self.error_message = "Sorry, you've been caught and eaten by the zombie cook! Improve your strategy and try again!"
                    self.__move_to_room('great_salon_scene', is_coming_back=True)


            def start_scene():
                self.collet_object_from_room()

                dw = DirectionWindow(width=400, height=400, text_opt1='Right', text_opt2='Left', text_opt3='Backward')
                option = dw.get_option()

                if option == 1: #Right
                    self.__move_to_room('evil_spirit_scene', return_to_room='kitchen_scene')

                elif option == 2: #Left
                    if 'scene_completed' in self.actual_room:
                        CuteWrite("You have completed this scene", '[green]', 0.05)
                        self.__move_to_room(self.actual_room['return_to_room'],  is_coming_back=True)

                    else:
                        start_fight_with_zombie_cook()

                elif option == 3: #Backward
                    self.__move_to_room('intro_scene', is_coming_back=True)

                else:
                    self.kitchen_scene()

            CuteWrite(
                text="""You have found yourself in the kitchen of the haunted house. There is a mess everywhere\nas well as it being dark and burnt. While\nyou are looking around and discovering, you see an object on the floor of what appears\nto be a sword and add it to your inventory\nYou have to make a decision: right, left, backward. """, 
                color='[bold yellow]', 
                callback=start_scene
            )
            

    def evil_spirit_scene(self):
        if 'scene_completed' in self.actual_room:
            CuteWrite("You have completed this scene", '[green]', time=0.05)
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
                        CuteWrite(f"The monster has been killed. You've found the treasure! Congrats you have obtained +50 points.", '[bold green]', time=0.05)

                        if not 'scene_completed' in self.actual_room:
                            self.actual_room['scene_completed'] = True

                        text_action = f"You've pass the {self.actual_room['name']}"

                        if 'scene_completed' in self.rooms['attic_scene']:
                            self.__set_direction_done('intro_scene', 'north')
                            self.level = 2
                            text_action = f"You level up to 2"

                        WinnerWindow(
                            prize="+50 points",
                            action=text_action
                        )
                    
                        self.__move_to_room('intro_scene')
                        
                    else:
                        self.__subtract_attempts()
                        self.error_message = 'Wrong object or object is not in inventory, you lose an attempt'
                        self.__move_to_room('intro_scene', is_coming_back=True)

                elif option == 2: #Run
                    self.__subtract_score(2)
                    self.__subtract_attempts(reason="You decide run, you lose an attempt and 2 score points")
                    self.__move_to_room(self.actual_room['return_to_room'],  is_coming_back=True)

                elif option == 3: #Backward
                    self.__move_to_room(self.actual_room['return_to_room'],  is_coming_back=True)

                else:
                    self.error_message = f'Option is not valid, please write a valid option'
                    start_scene()

            elif get_item != 'flashlight' and get_item in self.inventory:
                self.alert_message = 'You have been killed by the monsters because you have been selected the incorrect object for pass the level into the Evil Spirit, you lose an attempt.'
                
                self.__subtract_attempts(reason = self.alert_message)
                self.__move_to_room(self.actual_room['return_to_room'],  is_coming_back=True)
                
            else:
                self.error_message = f'{get_item} is not available into the inventory'
                start_scene()

        CuteWrite("""\nYou are inside the room, but everything is dark because the light has been damaged """, '[bold yellow]', callback=start_scene)


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
            else:
                self.error_message = "There are no more prizes in this room sadly :("

            self.__move_to_room('living_room_scene', is_coming_back=True)
        elif option == 2: #Backward
            self.__move_to_room('great_salon_scene', is_coming_back=True)

        elif option == 3: #Left
            self.__move_to_room('evil_spirit_scene', return_to_room='living_room_scene')

        else:
            self.error_message = 'You must select an option'
            self.living_room_scene() 
            
        
    def haunted_room_scene(self):
        self.check_attempts()
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
        self.check_attempts()
        self.show_errors_if_exists()

        console.print('[red]You are trapped in the room, and you must kill an unknown monster that tries to attack you, what action do you want to take?')

        console.print('[green]run (r)[/] or [blue]takeaction (t)[/]')
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
                    self.alert_message = self.error_message

                    self.__subtract_attempts(2)
                    self.__move_to_room('trap_room_scene')
                    break

        elif action == 'run' or action == 'r':
            self.__subtract_attempts()
            self.alert_message = 'Lograste salir de la habitacion de trampas, pero has perdido una vida'
            self.error_message = 'Lograste salir de la habitacion de trampas, pero has perdido una vida'
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
                CuteWrite(f"The mummy has been killed. You've found the treasure! Congrats you have obtained +100 points.", '[bold green]', time=0.05)
                
                WinnerWindow(prize='+100 points', action="You've won")
                self.player_win()

            else:
                self.alert_message = 'You have been killed by the mummy!'
                self.error_message = self.alert_message
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
    
    def ask_for_play_again(self):
        confirm = str(console.input("\n[blue]Want you play again?")).lower()

        if confirm == 'yes' or confirm == 'y':
            confirm = str(console.input(f"\n[blue]Want you play like [green]{self.player}[/]?:")).lower()
            if confirm != 'yes' or confirm != 'y':
                self.player = ''

            self.intro()
            self.score = 0
            self.level = 1
            self.attempts = 5
        else:
            CuteWrite("Thaks for play Tanny/'s treasure hunt!", '[bold red]', time=0.07) 
            exit()

    """
        Player lose the game and all their points and downgrade the level to 1 againg
    """
    def game_over(self):
        loser_message = "I am so sorry, you have lost the mystery house game. You failed to defeat the mummy and other monstrosities, but don't worry, you can always try again! Cheer up!"

        try:
            CuteWrite(loser_message, '[bold red]', time=0.05) 
            GameOverWindow()
        except :
            CuteWrite(loser_message, '[bold red]', time=0.05) 
        
        self.ask_for_play_again()

    
    def player_win(self):
        CuteWrite(
            text="""Congratulations! You have won the mystery house game and have shown your ability to defeat the mummy and other monstrosities. You are a true hero!""",
            time=0.05,
            color='[bold green]'
        )

        self.ask_for_play_again()

 
Game()