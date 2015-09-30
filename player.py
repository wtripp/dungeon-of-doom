from sys import exit
from random import randint

import enemies
import items
from map import rooms
from util import delay
"""The player that the user operates."""


class Player(object):
    """Base class for players.
    1) Players have a name.
    2) Players have a specified number of hit points.
    3) Players do a specified amount of damage.
    4) Players have a room, which is their current location.
    5) Players have an inventory
    6) Players have a description.
    7) Players can use things, look at things, and take things.
    8) Players can move to a new room.
    9) Players can fight enemies.
    """

    def __init__(self, name, hp, dmg, room):
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.room = room
        self.inventory = {}
    
    def description(self):
        return"""You are a noble hero on a quest for glory.
You have %s hit points left.""" % self.hp

    def is_alive(self):
        """Check if player is alive."""
        return self.hp > 0

    def use(self, use_prompt, object, use_connecter=None, other_object=None):
        """
            Use an object, or use one object on another, based on the
            specified prompt. Prompts are of the form 'Use X' or 'Use X on Y'.
        """
        
        # Prompt is of the form 'Use X on Y'.
        if use_connecter and other_object:
            
            # X and Y are in the player's inventory.
            if object in self.inventory and other_object in self.inventory:
                useResult = self.inventory[object].useOn(
                self.inventory[other_object])
                
                # Use X on Y. Add the result of this command to the player's
                # inventory. Then delete X and Y from the player's inventory.
                if useResult:
                    self.inventory[useResult.name] = useResult
                    del self.inventory[object]
                    del self.inventory[other_object]
            
            # X is in the player's inventory and Y is in the room.
            elif object in self.inventory and \
            other_object in rooms[self.room].contents:
                # Use X on Y.
                self.inventory[object].useOn(
                rooms[self.room].contents[other_object])
            
            else:
                print "You can't do that!"
        
        # Prompt is of the form 'Use X'.
        else:
            
            # X is in the player's inventory.
            if object in self.inventory:
            
                # If you can use X, add the result to the player's inventory.
                # Then delete X from the inventory.
                useResult = self.inventory[object].use()
                if useResult:
                    self.inventory[useResult.name] = useResult
                    del self.inventory[object]
            
            # X is in the room.
            elif object in rooms[self.room].contents:
                # Use X.
                rooms[self.room].contents[object].use()
            
            # X is neither in the inventory nor the room.
            else:
                print "There is no %s!" % object

        
    def fight(self, enemy):
        """Fight an enemy."""
        
        if not enemy.is_alive():
            print "The %s is already dead." % enemy.name
            
        else:
            
            # Keep fighting the enemy until either the player or enemy dies.
            while self.is_alive() and enemy.is_alive():
        
                print "You attack!"
                delay()
                damage = randint(1, self.dmg)
                enemy.hp -= damage
                print "You do %d damage to the %s." % (damage, enemy.name)
                delay()
                
                if enemy.hp <= 0:
                    print "You killed the %s!" % enemy.name
                    enemy.isAlive = False
                
                else:
                    print "The %s attacks!" % enemy.name
                    delay()
                    damage = randint(1, enemy.dmg)
                    self.hp -= damage
                    print "The %s does %d damage to you." % (enemy.name, damage)
                    print "You have %d hp left." % (max(0, self.hp))
                    delay()

                    if self.hp <= 0:
                        print "The %s killed you!" % enemy.name
                        dead()

    def look(self, thing):
        """Look at the specified thing."""
        
        # Look at the room.
        if thing == "room":
            room_desc = rooms[self.room].description()
            print room_desc.split("\n")[0]
        
        # Look at the player.
        elif thing in ["me", "myself", "self"]:
            print self.description()
        
        # Look at an item in the player's inventory.
        elif thing in self.inventory:
            print self.inventory[thing].description()
        
        # Look at everything in the inventory.
        elif thing == "inventory":
            if self.inventory:
                print "Inventory:"
                print "\n".join(self.inventory.keys())
            else:
                print "You have nothing in your inventory."
        
        # Try looking at an item in the room, if it exists.
        else:
            try:
                print rooms[self.room].contents[thing].description()
            except KeyError:
                print "There's nothing like that here."
                                
    def take(self, take_prompt, thing):
        """Take the specified thing."""
        
        room_contents = rooms[self.room].contents
        
        # No thing entered, only a take prompt.
        if thing == take_prompt:
            print "What do you want to %s?" % take_prompt 
        
        # The things is the player.
        elif thing in ["room", "myself", "me"]:
            print "You can't %s that!" % take_prompt
        
        # The thing is in the room.
        elif thing in room_contents:
        
            item = room_contents[thing]
            
            # If the item is in the room (and gettable), take it.
            if hasattr(item,'is_gettable') and item.is_gettable == True:
                print "You %s the %s." % (take_prompt, item.name)
                self.inventory[thing] = item
                del room_contents[thing]
            else:
                print "You can't %s the %s." % (take_prompt, item.name)
        
        # Look at the items within a room's items, such as an enemy's inventory.
        else:
        
            for content_name, content in room_contents.items():
            
                # The item has an inventory and is a living thing (an enemy).
                if hasattr(content,'inventory') and hasattr(content,'is_alive'):
                    for item_name, item in content.inventory.items():
                        
                        # If the item is there and the enemy (content) is dead,
                        # add the item to the player's inventory
                        # and delete it from the enemy's inventory.
                        if item_name == thing and not content.is_alive():
                            print "You %s the %s." % (take_prompt, item_name)
                            self.inventory[item_name] = item
                            del content.inventory[item_name]
                            return        
            else:
                print "There's nothing like that here."


    def move(self, direction):
        """Move in the specified direction."""
        
        directions = {"N" : "north",
                      "S" : "south",
                      "E" : "east",
                      "W" : "west"}
        
        try:
            current_room = rooms[self.room]
            next_room = getattr(current_room, direction)

            if next_room is not None:
                print "You go %s." % directions[direction]
                self.room = next_room
            else:
                print "You cannot go that way!"
                
        except AttributeError:
            print "You want to do what?"
            
def dead():
    """Prints a quip about the player's death and then exits the game."""
    quips = ["Ding Dong, the Hero's Dead","Aw, don't cry, hero."]
    print quips[randint(0,len(quips)-1)]
    print "Game Over."
    exit(1)