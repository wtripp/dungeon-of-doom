import os
from sys import exit
from map import rooms
import enemies
from player import Player

def play():
    os.system('cls')
    print "\n\nYour quest is to defeat the evil spider in the Dungeon of Doom."
    print "-" * 20
    print rooms[player.room].description()
    
    while player.is_alive() and not player.victory:
        try:
            print "-" * 20
            prompt = raw_input("\nWhat do you want to do?\n> ")
            os.system('cls')
            parse(prompt)
            print "-" * 20
            print rooms[player.room].description()
        except KeyboardInterrupt:
            os.system('cls')
            print "Quitting the game.\n\n"
            exit(0)

    print "The End."
    
def parse(prompt):

    input = prompt.split()
    if input == []:
        print "You didn't enter anything!"
        return

    movements = ["move","go","travel","head"]
    directions = ["north","south","east","west","n","s","e","w"]
    fighting = ["kill","destroy","fight","slay"]
    looking = ["look","see","inspect","view"]
    taking = ["take","get","steal"]

    if get_first_word(input) in movements or get_first_word(input) in directions:
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

    else:
        print "\nI don't understand."


def get_first_word(input):
    return input[0].lower()

player = Player("hero", 20, 8, "entrance_room")        
play()