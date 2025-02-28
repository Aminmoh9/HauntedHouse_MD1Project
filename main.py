rooms = {
    'Foyer': {
        'description': 'A dimly lit entrance hall with a grand staircase.',
        'connections': ['Library','Outside', 'Diner'],
        'hidden connections': [],
        'items': {
            'mirrors': {'name': 'mirrors', 'description': "You stand before the tall, dusty mirrors lining the walls",
                        "collect": False, "hidden": False},
            'rug': {'name': 'rug', 'description': "A soft rug, blending into the room's atmosphere.", "collect": False, "hidden": False},
            'chandelier': {'name': 'chandelier', 'description': "A grand chandelier, casting light with elegance", "collect": False, "hidden": False},
    },
        'image':'foyer.jpeg'
    },
    'Library': {
        'description': 'Walls lined with ancient books. A cold draft chills you.',
        'connections': ['Bedroom', 'Basement'],
        'hidden connections' : [],
        'items': {
            'bookshelf': {'name': 'bookshelf', 'description': "An old bookshelf, filled with forgotten books.", "collect": False, "hidden": False},
            'painting': {'name': 'painting', 'description': "A beautiful painting, but nothing extraordinary.", "collect": False, "hidden": False},
            'chest': {'name': 'chest', 'description': "A heavy chest, tucked away in the corner.", "collect": False, "hidden": False},
    },
        'image':'library.jpeg'
    },
    'Bedroom': {
        'description': 'A cozy bedroom with a large bed and a wardrobe.',
        'connections': ['Library'],
        'hidden connections' : [],
        'items': {
            'pistol': {'name': 'pistol', 'description': "A compact sidearm for self-defense or hunting. This item is collectable", "collect": True, "hidden": False},
            'flashlight': {'name': 'flashlight', 'description': "A portable light source for dark areas. This item is collectable", "collect": True, "hidden": False},
            'garlic bulb': {'name': 'garlic bulb', 'description': "A potent ingredient, often used to ward off unwanted pests. This item is collectable", "collect": True, "hidden": False},
    },
        'image':'bedroom.jpeg'
    },
    'Basement': {
        'description': 'A dark and damp basement with a musty smell.',
        'connections': ['Library', 'Kitchen'],
        'hidden connections' : [],
        'items': {
            'bonus': {'name': 'bonus', 'description': "You better check it out!", "collect": False, "hidden": False},
            'rusty chain': {'name': 'rusty chain', 'description': "An old, rusted chain, its purpose lost to time.", "collect": False, "hidden": False},
            'broken mirror': {'name': 'broken mirror', 'description': "A shattered mirror, its cracks reflecting a fractured image", "collect": False, "hidden": False},
    },
        'image':'basement.jpeg'
    },
    'Kitchen': {
        'description': 'A dark kitchen filled with strange smells.',
        'connections': ['Diner', 'Basement'],
        'hidden connections' : [],
        'items': {
            'potion': {'name': 'potion', 'description': "A mysterious potion, known for its healing properties.", "collect": False, "hidden": False},
            'cabinet': {'name': 'cabinet', 'description': "An old kitchen cabinet, worn with age, offering little of interest.", "collect": False, "hidden": False},
    },
        'image':'kitchen.jpeg'
    },
    'Diner': {
        'description': 'An elegant dining room with an old chandelier.',
        'connections': ['Kitchen','Foyer'],
        'hidden connections' : [],
        'items': {
            'table': {'name': 'table', 'description': "A large dining table, adorned with candles that flicker in the dim light.", "collect": False, "hidden": False},
            'mural': {'name': 'mural', 'description': "A beautifully painted mural, depicting a scene frozen in time", "collect": False, "hidden": False},
    },
        'image':'diner.jpeg'
    },
    'Outside':{
        'description': 'You step into the cold night. Freedom at last!',
        'connections': ['Foyer'],
        'hidden connections': [],
        'items': {},
        'image':'outside.jpeg'
        }
    }

import random
import time
import threading
from IPython.display import Image, display


class Room:
    def __init__(self, name, description,image_url):
        self.name = name
        self.description = description
        self.connections = {}     #Visible connection (rooms you can move to)
        self.items = []   # List of items in the room
        self.hidden_connections = {} # Hidden connections to be unlocked through solving puzzles
        self.locked = False
        self.image_url = image_url

    def connect(self, room, locked=False):
        self.connections[room.name.lower()] = room
        room.connections[self.name.lower()] = self
        if locked:
            room.locked = True 
    
    def show_image(self):
        # Use IPython display to show the image
        display(Image(self.image_url,width=300, height=300))
        

class Item:
    def __init__(self, name, description, collect=False, hidden=False):
        self.name = name
        self.description = description
        self.collect = collect
        self.hidden = hidden
 
class Player:
    def __init__(self, start_room, total_time=600 ):
        self.current_room = start_room
        
        self.inventory = None
        self.key_inventory = []
        self.total_time = total_time  # Total time for the game in seconds
        self.time_left = total_time  # Time remaining in seconds
        self.game_over = False  # Flag to track game state
        self.timer_thread = threading.Thread(target=self.start_timer)  # Create a separate thread for the timer
        self.timer_thread.start()  # Start the timer in the background
    
    #Starting the timer
    def start_timer(self):
        while self.time_left > 0 and not self.game_over:
            time.sleep(1)  # Wait for 1 second
            self.time_left -= 1  # Decrease time by 1 second
            self.print_remaining_time()  # Print remaining time every second

        if self.time_left == 0:
            self.game_over = True
            self.end_game()

    def print_remaining_time(self):
        minutes, seconds = divmod(self.time_left, 60)
        print(f"Time remaining: {minutes:02}:{seconds:02}", end="\r")

    def end_game(self):
        print("Game Over! You failed to escape in time.")
        self.game_over = True  # Stop the game
        exit()
    def stop_timer(self):
        """Stop the timer thread if the game ends."""
        self.game_over = True
        if self.timer_thread.is_alive():
            self.timer_thread.join()  # Wait for the timer thread to finish gracefully

    def move(self, room_name):
        if self.game_over:
            print("The game is over. You cannot move anymore.")
            return
        
        room_name = room_name.strip() 

        if room_name in self.current_room.connections:
            next_room = self.current_room.connections[room_name]

            if next_room.locked:
                print(f"The door to {next_room.name} is locked. You need to solve a puzzle to open the door.")
                return
            
            else:
                self.current_room = next_room
                print(f"You move to {next_room.name}. {self.current_room.description}")

                # Display the image of the new room
                self.current_room.show_image()

                if next_room.name != "Outside":
                    print(f"You see exits to:", ', '.join([r for r in self.current_room.connections.keys()]))
        else:
            print(f"You can't go that way. Available exits: {', '.join([r for r in self.current_room.connections.keys()])}")

    # Explore function
    def explore_room(self):
        if self.game_over:
            print("The game is over. You cannot explore anymore.")
            return
        if self.current_room.items:
            print("\nYou see in this room:")
            for item in self.current_room.items:
                print(f" - {item.name} ")
        else:
            print("\nThere are no items in this room.")

    # Examine function
    def examine_item(self, examine_item):
        if self.game_over:
            print("The game is over. You cannot examine items anymore.")
            return 
        for item in self.current_room.items:
            if examine_item.lower() == item.name.lower():
                print(f"\nExamining {item.name}:")
                print(item.description)

                # Special cases with functions
                if item.name.lower() == "mirrors":
                    return self.mirror_challenge(item)
                if item.name.lower() == "chest":
                    return self.solve_riddle_for_key_a(item)
                if item.name.lower() == "bonus":
                    return self.vampire_challenge(item)
                if item.name.lower() == "cabinet":
                    return self.solve_riddle_for_key(item)
                if item.name.lower() == "table":
                    return self.candle_challenge(item)

                # If the item has no special function, simply print and exit the function
                return  

        print(f"There is no item named '{examine_item}' in this room.")


    # Pick up function
    def pick_up_items(self, picked_item):
        if self.game_over:
            print("The game is over. You cannot pick up items anymore.")
            return
       # First, check if the desired item is present in the current room
        for item in self.current_room.items:
          if picked_item.lower() == item.name.lower():
            # Check if the item is collectible
             if item.collect:
                #If there is an item in the inventory, place it back in the room
                 if self.inventory is not None:
                    self.current_room.items.append(self.inventory)
                    print(f"{self.inventory.name} has been placed back in the room.")
                # Add the item to the inventory and remove it from the room
                 self.inventory = item
                 self.current_room.items.remove(item)
                 print(f"You picked up {item.name}")
                 return
             else:
                print(f"{item.name} is not collectable.")
                return
        # If the item is not in the environment
        print(f"There is no item named '{picked_item}' in this room.")
       

    # The Foyer challenge
    def mirror_challenge(self,mirrors):
        correct_sequence = "ACB"
        print("As you gaze into your reflection, a voice whispers: 'Solve the riddle to proceed!\n"
                "The mirrors display a series of strange symbols: [A, B, C].")

        while True: 
            answer = input("Enter the correct order (e.g., A B C): ").replace(" ", "").upper()

            if answer == correct_sequence:
                print("\nThe riddle is solved! The door to the library is now unlocked.\n")
                Library.locked = False
                break
            print("\nThe mirrors flicker. The order is incorrect. Try again.\n")

    # The library riddle
    def solve_riddle_for_key_a(self,chest):
        print("Solve the riddle to proceed.")
        print("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. Who am I")

        
        correct_password = "echo"

        while True:
            answer = input("Enter your answer: ").strip().lower()

            if  answer == correct_password:
                print("\nYou solved the riddle! The bedroom is now unlocked.\n")
                Bedroom.locked=False
                break
            else:
                print("\nIncorrect answer. The riddle remains unsolved. Try again.\n")

    # The Basement challenge
    def vampire_challenge(self, bonus):
        print(f"A vampire has appeared in the Basement! Do you want to fight or flee?")

        player_input = input("Do you want to fight or flee? (fight/flee): ").lower()

        if player_input == "flee":
            print("You decided to flee!")
            return self.flee()  

        elif player_input == "fight":

            has_garlic = self.inventory is not None and self.inventory.name.lower() == "garlic bulb"
            has_flashlight = self.inventory is not None and self.inventory.name.lower() == "flashlight"
            has_pistol = self.inventory is not None and self.inventory.name.lower() == "pistol"

            if has_garlic:
                print("Lucky you have picked up the garlic. The vampire is defeated!")
                return self.win_vampire_challenge()
            
            elif has_flashlight:
                print("You only have a flashlight with you. Even though it is no sun light, it might help to defate the vampire. There is a 50% chance of winning...")
                chance = random.random()
                if chance < 0.5:
                    print("The flashlight stuns the vampire! You win!")
                    return self.win_vampire_challenge()
                else:
                    print("The flashlight failed! The vampire attacks!")
                    return self.lose_vampire_challenge()
            
            elif has_pistol:
                print("You have a pistol with you. That does not defeat the vampire. He attacks you...")
                return self.lose_vampire_challenge()
            
            else:
                print("Invalid answer. Enter fight or flee.")
                return self.vampire_challenge(bonus)            

    def win_vampire_challenge(self):
        result = "You defeated the vampire! The door to the kitchen is now open." 
        Kitchen.locked = False 
        print(result)
        return result
    
    def lose_vampire_challenge(self):
        result = "You lost against the vampire! You wake up in the foyer ..."  
        print(result)

        self.current_room = room_objects["Foyer"]
        
        return result

    def flee(self):
        print("You fled from the vampire.")
        return "You successfully fled. However, you won't moving forward by this ...!"

    # The kitchen riddle
    def solve_riddle_for_key(self,cabinet):
        print("Solve this riddle to get the key to the main door to the outside:")
        print("The more you take, the more you leave behind. What am I?")

        right_answer = "footsteps"

        while True:
            answer = input("Enter your answer: ").strip().lower()

            if answer == right_answer:
                print("Correct! You have received the key to the main door.")
                Outside.locked=False
                break
            
            else:
                print("Incorrect answer. Try again later.")

            

    # The diner puzzle
    def candle_challenge(self,table):
        print("In front of you is a long dining table. You can barely see anything except the faint outlines of candle holders on the table.")
        print("The room is dark. You grope for some matches that you feel on the table.")
        print("A whisper echoes: 'You better light up the candles in the correct order!'")

        correct_answer = "123"

        while True:
            answer = input("Enter the correct order (e.g. 321): ")
            if answer == correct_answer:
                self.win_candle_challenge()
                break
            else:
                self.loose_candle_challenge()
    
    def win_candle_challenge(self):
        Foyer.locked = False
        result = "You lighted up the candles in the correct order. See! The mural shifts and opens up a passage to the foyer and the main door to exit the building!"
        print(result)
    
    def loose_candle_challenge(self):
        result = "Wrong order. Try again"
        print(result)

# new dictionary that contains objects (because original dictionary conatins strings) including instances of the rooms
room_objects = {}

# Create Room instances and store them in room_objects
for room_name, room_data in rooms.items():
    room_objects[room_name] = Room(room_name, room_data['description'],room_data['image'])    

# Connect rooms
for room_name, room_data in rooms.items():
    for connection in room_data['connections']:
        room_objects[room_name].connect(room_objects[connection])

# Add items to rooms
for room_name, room_data in rooms.items():
    if isinstance(room_data['items'], dict):
        for item_name, item_data in room_data['items'].items():
            item_obj = Item(item_data['name'], item_data['description'], item_data['collect'])
            room_objects[room_name].items.append(item_obj)
    
#Assign room objects to variables
Foyer = room_objects['Foyer']
Library = room_objects['Library']
Diner = room_objects['Diner']
Kitchen = room_objects['Kitchen']
Basement = room_objects['Basement']
Bedroom = room_objects['Bedroom']
Outside=room_objects['Outside']

#Connect rooms
Foyer.connect(Library, locked = False)
Foyer.connect(Outside, locked=True)
Library.connect(Bedroom, locked = True)
Library.connect(Basement, locked = False)
Basement.connect(Library, locked = False)
Basement.connect(Kitchen, locked = True)
Kitchen.connect(Diner, locked = False)
Diner.connect(Foyer, locked = True)

player = Player(Foyer)
mansion_image_url="mansion.jpeg"

def show_mansion_image():
    display(Image(mansion_image_url,width=400, height=400))

show_mansion_image()
print("     __________| |____")
print("    /                 \\")
print("   /      Welcome      \\")
print("  /       to  the       \\")
print("  |    Haunted Mansion  |")
print("  |     ____     ___    |")
print("  |    |    |   |___|   |")
print("__|____|____|___________|__")
print("")
print("You just entered the house. You look around and see a grand foyer. Cobwebs hang from the ceiling, and an eerie silence fills the air.")
print("Suddenly, a loud bang! The door has slammed shut behind you.")
print("You try to open it, but without success. You realize that you are trapped. Will you be able to find the key?")
print("")
print("You have 10 minutes to escape the room. Good luck!")
print("")
print(f"You are currently in {player.current_room.name}. {player.current_room.description}")
print(f"You see exits to:", ', '.join([r for r in player.current_room.connections.keys()]))
print("")
player.current_room.show_image()  # Show image for foyer on game start
print(
    "Use the following functions:\n"
    "- Explore (to see all items in a room)\n"
    "- Examine (to see the item name and description)\n"
    "- Pick (to pick up an item. You will see in the description if an item is pickable. You can only carry one item at a time.)\n"
    "- Quit (to quit the game.)\n"
    "- Move (to move to another room)\n")


while True:
    if player.game_over:  # Check if the game is over
        print("The game is over. You cannot take any more actions.")
        break  # Exit the loop if the game is over

    

    options = input("What do you want to do?: Explore/ Examine/ Move/ Pick/ Quit").lower().strip()

    if options == "explore":
        player.explore_room()

    elif options == "examine":
        examine_item = input("What item do you want to examine? Type the name of the item").strip()
        player.examine_item(examine_item)

    elif options == "pick":
        examine_item = input("What item do you want to pick? Choose wisely!").strip()
        player.pick_up_items(examine_item)

    elif options == "move":
        move_room = input("In what room do you want to move?").strip()
        if move_room:
            player.move(move_room)
            if player.current_room.name == "Outside":
                print("Congratulations! You have escaped the haunted mansion!")
                break
                
    elif options == "quit":
        if player.current_room.name == "Outside":
            print("Goodbye! Good Job!")
        else:
            print("Goodbye! Wishing you better luck next time!")
        player.game_over = True  
        break
        
    