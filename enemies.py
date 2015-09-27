"""Enemies in the game."""
from sys import exit
from random import randint

        
class Enemy(object):
    """
    Base class for enemies.
    1) Enemies have a name.
    2) Enemies have a specified number of hit points.
    3) Enemies do a specified amount of damage.
    4) Enemies have an inventory.
    5) Enemies have a description.
    """

    def __init__(self, name, hp, dmg):
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.inventory = {}
    
    def is_alive(self):
        """Check if enemy is alive."""
        return self.hp > 0
        
    def description(self):
        
        # Description when the enemy is alive.
        if self.is_alive():
            return "An evil %s stands before you." % self.name
            
        # Description when the enemy is dead.
        else:
            desc = []
            desc.append("A dead %s lies before you." % self.name)
            
            # Description of items in the enemy's inventory.
            for item_name, item in self.inventory.items():
                desc.append("You see a %s in its possessions." % item_name)

            return "\n".join(desc)

            
class Goblin(Enemy):
    def __init__(self):
        super(Goblin, self).__init__(name="goblin", hp=10, dmg=6)


class Spider(Enemy):
    def __init__(self):
        super(Spider, self).__init__(name="spider", hp=100, dmg=10)