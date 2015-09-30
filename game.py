"""The game engine and the function for parsing user inputs."""

import os
from sys import exit

import enemies
from player import Player
from map import rooms
from util import divider
from util import delay

def play():
    """The engine that runs the game."""
    
    # Clear the command prompt and show the game introduction.
    os.system('cls')
    print """
 ______            _        _______  _______  _______  _       
(  __  \ |\     /|( (    /|(  ____ \(  ____ \(  ___  )( (    /|
| (  \  )| )   ( ||  \  ( || (    \/| (    \/| (   ) ||  \  ( |
| |   ) || |   | ||   \ | || |      | (__    | |   | ||   \ | |
| |   | || |   | || (\ \) || | ____ |  __)   | |   | || (\ \) |
| |   ) || |   | || | \   || | \_  )| (      | |   | || | \   |
| (__/  )| (___) || )  \  || (___) || (____/\| (___) || )  \  |
(______/ (_______)|/    )_)(_______)(_______/(_______)|/    )_)
                                                               
 _______  _______    ______   _______  _______  _______ 
(  ___  )(  ____ \  (  __  \ (  ___  )(  ___  )(       )
| (   ) || (    \/  | (  \  )| (   ) || (   ) || () () |
| |   | || (__      | |   ) || |   | || |   | || || || |
| |   | ||  __)     | |   | || |   | || |   | || |(_)| |
| |   | || (        | |   ) || |   | || |   | || |   | |
| (___) || )        | (__/  )| (___) || (___) || )   ( |
(_______)|/         (______/ (_______)(_______)|/     \|
                                                        
        Type help for instructions, q to quit.
        """
    divider()
    print "Your quest is to defeat the evil spider in the Dungeon of Doom."
    divider()
    print rooms[player.room].description()
    
    # Run game engine while the player is alive.
    while player.is_alive():
        try:
            
            # Provide prompt to user.
            divider()
            prompt = raw_input("\nWhat do you want to do?\n> ")
            os.system('cls')
            
            # Determine what action to take based on user input.
            parse(prompt)
            divider()
            
            # Update the toom conditions based on the user's action.
            rooms[player.room].update_room_conditions()
            
            # End game if victory condition is met.
            if victory():
                break
                
            # Print the updated room conditions.
            print rooms[player.room].description()
            
        except KeyboardInterrupt:
            quit()
    
    # Final text printed when the game ends.
    print "The End."

def quit():
    """Quit the game and exit back to the command line."""
    os.system('cls')
    print "Quitting the game."
    exit(0)
    
def victory():
    """Victory conditions of the game."""
    
    # Victory condition: The spider in the spider room is dead.
    return not rooms['spider_room'].contents['spider'].is_alive()
    
def parse(prompt):
    """Determine what action to take based on the user input, prompt."""
    
    # List of acceptable first words in user input.
    movements = ["move", "go", "travel", "head"]
    directions = ["north", "south", "east", "west", "n", "s", "e", "w"]
    fighting = ["kill", "destroy", "fight", "slay"]
    looking = ["look", "see", "inspect", "view", "search"]
    taking = ["take", "get", "steal"]
    using = ["use", "put", "combine", "pull", "push", \
             "close", "open", "lock", "unlock"]
    using_connecters = ["on","with","in"]
    
    # Split user input into list of words.
    input = prompt.lower().split()
    
    # Parse the list of words in the user input.
    
    # No user input.
    if input == []:
        print "You didn't enter anything!"
        return
    
    # View inventory.
    elif len(input) == 1 and get_first_word(input) == "inventory":
        return player.look("inventory")
    
    # View help.
    elif len(input) == 1 and get_first_word(input) == "help":
        return help()
    
    # Quit the game.
    elif len(input) == 1 and get_first_word(input) == "quit":
        return quit()
    
    # Move to a new location (north, south, east, or west).
    elif get_first_word(input) in movements or \
         get_first_word(input) in directions:
        
        # Delete the move prompt, leaving only the direction.
        if len(input) > 1 and get_first_word(input) in movements: del input[0]
        
        # Format the direction for the player's move method.
        # For example, "north" becomes "N"
        direction = input[-1][0].upper()
        player.move(direction)
    
    # Fight an enemy.
    elif get_first_word(input) in fighting:        
        fight_prompt = input[0]
        enemy = input[-1]
        
        # User supplied a fight prompt but no enemy to fight.
        if enemy == fight_prompt:
            print "What do you want to %s?" % fight_prompt
        
        else:
            try:
                # If the specified enemy is in the room, fight it.
                enemy_to_fight = rooms[player.room].contents[enemy]
                player.fight(enemy_to_fight)
            except KeyError:
                print "You can't %s that!" % fight_prompt
    
    # Look at something.
    elif get_first_word(input) in looking:    
        look_prompt = input[0]
        thing = input[-1]
        
        # User supplied a look prompt but nothing to look at, view, see, etc.
        if thing == look_prompt:
            if look_prompt == "look":
                look_prompt += " at"
            print "What do you want to %s?" % look_prompt

        else:
            player.look(thing)
    
    # Take something.
    elif get_first_word(input) in taking:    
        take_prompt = input[0]
        item = input[-1]
        player.take(take_prompt, item)
    
    # Use something.
    elif get_first_word(input) in using:
        input = [word for word in input if word != "the"]        
        use_prompt = input[0]
        
        # Input contains only a user prompt.
        if len(input) == 1:
            print "What do you want to %s?" % use_prompt
        
        # Input is in 'use X' format.
        elif len(input) == 2:
            object = input[1]
            player.use(use_prompt, object)
        
        # Input is in 'use X on' or 'use X Y' format.
        elif len(input) == 3:
            object = input[1]
            
            # 'use X on'
            if input[2] in using_connecters:
                use_connecter = input[2]
                print "What do you want to %s the %s %s?" % (
                use_prompt, object, use_connecter)
                
            # 'use X Y'
            else:
                other_object = input[2]
                print "How do you want to %s %s and %s together?" % (
                use_prompt, object, other_object)
        
        # Input is in 'use X on Y' format.
        else:
            object = input[1]
            use_connecter = input[2]
            other_object = input[-1]
            player.use(use_prompt, object, use_connecter, other_object)
    
    # User input cannot be parsed.
    else:
        print "I don't understand."


def get_first_word(input):
    """Return the first word of the user input."""
    return input[0]

def help():
    """Print the game's documentation for the user."""

    print"""
    quit - Quit the game.
    help - Get help.
    inventory - See your inventory.
    take <item> - Add something to your inventory.
    look <thing> - Get the description of something.
    use <item> - Use an item from your inventory.
    fight <enemy> - Fight an enemy.
    move <direction> - Move north, south, east, or west.
    """

# Create the player and start the game.
player = Player("hero", 20, 8, "entrance_room")        
play()