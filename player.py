from sys import exit
from random import randint
import time

import enemies
import items
from map import rooms

def delay():
    return time.sleep(0)

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
        self.inventory = {}
        self.victory = False
    
    def description(self):
        return "You are a noble hero on a quest for glory."

    def is_alive(self):
        return self.hp > 0


    def use(self, use_prompt, object, use_connecter=None, other_object=None):    
        if use_connecter and other_object:
            
            if object and other_object in self.inventory:
                useResult = self.inventory[object].useOn(self.inventory[other_object])
                if useResult:
                    self.inventory[useResult.name] = useResult
                    del self.inventory[object]
                    del self.inventory[other_object]
            
            elif object in self.inventory and other_object in rooms[self.room].contents:
                self.inventory[object].useOn(rooms[self.room].contents[other_object])
                
            
            else:
                print "You can't do that!"

        else:
        
            if object in self.inventory:
                useResult = self.inventory[object].use()
                if useResult:
                    self.inventory[useResult.name] = useResult
                    del self.inventory[object]

            else:
                print "You don't have the %s!" % object

        
    def fight(self, enemy):
        
        if not enemy.is_alive():
            print "The %s is already dead." % enemy.name
            
        else:
        
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
                    rooms[self.room].update_room_conditions()
                
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
            print "You see the room your are in."
            
        elif thing == "me" or thing == "myself" or thing == "self":
            print self.description()
            
        elif thing in self.inventory:
            print self.inventory[thing].description()
            
        elif thing == "inventory":
            if self.inventory:
                print "Inventory:"
                print "\n".join(self.inventory.keys())
            else:
                print "You have nothing in your inventory."
        
        else:            
            try:
                print rooms[self.room].contents[thing].description()
            except KeyError:
                print "There's nothing like that here."
                                
    def take(self, take_prompt, thing):
        
        room_contents = rooms[self.room].contents
        
        if thing == take_prompt:
            print "What do you want to %s?" % take_prompt 
            
        elif thing in ["room", "myself", "me"]:
            print "You can't %s that!" % take_prompt

        elif thing in room_contents:
        
            item = room_contents[thing]
        
            if hasattr(item,'isGettable'):
                print "You %s the %s." % (take_prompt, item.name)
                self.inventory[thing] = item
                del item
            else:
                print "You can't %s the %s." % (take_prompt, item.name)
        
        else:
            for content_name, content in room_contents.items():
                if hasattr(content,'inventory'):
                    for item_name, item in content.inventory.items():
                        if item_name == thing:
                            print "You %s the %s." % (take_prompt, item_name)
                            self.inventory[item_name] = item
                            del content.inventory[item_name]
                            return        
            else:
                print "There's nothing like that here."


    def move(self, direction):
        
        directions = {"N" : "north",
                      "S" : "south",
                      "E" : "east",
                      "W" : "west"}
        
        current_room = rooms[self.room]
        next_room = getattr(current_room, direction)

        if next_room is not None:
            print "You go %s." % directions[direction]
            self.room = next_room
        else:
            print "\nYou cannot go that way!"