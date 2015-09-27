import os
from sys import exit

import enemies
from player import Player
from map import rooms
from util import divider
from util import delay

def play():
    os.system('cls')
    print "Your quest is to defeat the evil spider in the Dungeon of Doom."
    divider()
    print rooms[player.room].description()
    
    while player.is_alive():
        try:
            divider()
            prompt = raw_input("\nWhat do you want to do?\n> ")
            os.system('cls')
            parse(prompt)
            divider()
            rooms[player.room].update_room_conditions()
            if victory():
                break
            print rooms[player.room].description()
        except KeyboardInterrupt:
            quit()

    print "The End."

def quit():
    os.system('cls')
    print "Quitting the game."
    exit(0)
    
def victory():
    return  not rooms['spider_room'].contents['spider'].is_alive()
    
def parse(prompt):

    movements = ["move","go","travel","head"]
    directions = ["north","south","east","west","n","s","e","w"]
    fighting = ["kill","destroy","fight","slay"]
    looking = ["look","see","inspect","view","search"]
    taking = ["take","get","steal"]
    using = ["use","put","combine","pull","push","close","open","lock","unlock"]
    using_connecters = ["on","with","in"]

    input = prompt.split()
    
    if input == []:
        print "You didn't enter anything!"
        return

    elif len(input) == 1 and input[0].lower() == "inventory":
        return player.look("look", "inventory")
    
    elif len(input) == 1 and input[0].lower() == "help":
        return help()
        
    elif len(input) == 1 and input[0].lower() == "quit":
        return quit()
    
    elif get_first_word(input) in movements or get_first_word(input) in directions:
        if len(input) > 1 and get_first_word(input) in movements: del input[0]
        direction = input[0][0].upper()
        player.move(direction)
    
    elif get_first_word(input) in fighting:        
        fight_prompt = input[0]
        enemy = input[-1]
        
        if enemy == fight_prompt:
            print "What do you want to %s?" % fight_prompt
        
        else:
            try:
                enemy_to_fight = rooms[player.room].contents[enemy]
                player.fight(enemy_to_fight)
            except KeyError:
                print "You can't %s that!" % fight_prompt
                
    elif get_first_word(input) in looking:    
        look_prompt = input[0]
        thing = input[-1]
        player.look(look_prompt, thing)

    elif get_first_word(input) in taking:    
        take_prompt = input[0]
        item = input[-1]
        player.take(take_prompt, item)
        
    elif get_first_word(input) in using:
        input = [word for word in input if word != "the"]        
        use_prompt = input[0]
        
        if len(input) == 1:
            print "What do you want to %s?" % use_prompt
        
        elif len(input) == 2:
            object = input[1]
            player.use(use_prompt, object)
            
        elif len(input) == 3:
            object = input[1]
                
            if input[2] in using_connecters:
                use_connecter = input[2]
                print "What do you want to %s the %s %s?" % \
                (use_prompt, object, use_connecter)
            else:
                other_object = input[2]
                print "How do you want to %s %s and %s together?" % \
                (use_prompt, object, other_object)
                            
        else:
            object = input[1]
            use_connecter = input[2]
            other_object = input[-1]
            player.use(use_prompt, object, use_connecter, other_object)

    else:
        print "I don't understand."


def get_first_word(input):
    return input[0].lower()

def help():
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
    
player = Player("hero", 20, 8, "entrance_room")        
play()