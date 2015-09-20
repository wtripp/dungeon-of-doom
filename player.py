from sys import exit
from random import randint
import time

import enemies
import items
from map import rooms

def delay():
    return time.sleep(0.5)

def dead():    
    quips = ["Ding Dong, the Hero's Dead","Aw, don't cry, hero."]
    print quips[randint(0,len(quips)-1)]
    print "Game Over."
    exit(1)

class Player(object):
    
    def __init__(self, name, hp, dmg, room):
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.room = room
        self.inventory = []
        self.victory = False
    
    def description(self):
        return "You are a noble hero on a quest for glory."

    def is_alive(self):
        return self.hp > 0
    
    def fight(self, enemy):
        while self.is_alive() and enemy.is_alive():
    
            print "You attack!"
            delay()
            damage = randint(1,self.dmg)
            enemy.hp -= damage
            print "You do %d damage to the %s." % (damage,enemy.name)
            delay()
            
            if enemy.hp <= 0:
                print "You killed the %s!" % enemy.name
                enemy.isAlive = False
            
            else:
                print "The %s attacks!" % enemy.name
                delay()
                damage = randint(1,enemy.dmg)
                self.hp -= damage
                print "The %s does %d damage to you." % (enemy.name,damage)
                print "You have %d hp left." % (max(0,self.hp))
                delay()

                if self.hp <= 0:
                    print "The %s killed you!" % enemy.name
                    dead()

    def look(self, look_prompt, thing):

        if thing == look_prompt or thing == "room":
            print rooms[self.room].description()
            
        elif thing == "me" or thing == "myself" or thing == "self":
            print self.description()
        
        else:

            for content in rooms[self.room].contents:
                if content.name == thing:
                    print content.description()
                    break

            else:
                print "There's nothing like that here."     

                
    def take(self, take_prompt, thing):

        if thing == take_prompt:
            print "What do you want to %s?" % take_prompt 
            
        elif thing == "room" or thing == "myself" or thing == "me":
            print "You can't take that!"

############### take            
        elif isinstance(thing, items.Item):
            
            #item = 
            if thing in contents:
                if thing.isGettable:
                    print "You take the %s" % thing.name
                    thing.append()
            for content in rooms[self.room].contents:
                if thing.name == thing:
                    print content.description()
                    break
############### end take

        else:
            print "There's nothing like that here."     

    def move(self, direction):
        
        current_room = rooms[self.room]
        next_room = getattr(current_room, direction)

        if next_room is not None:
            self.room = next_room
        else:
            print "\nYou cannot go that way!"