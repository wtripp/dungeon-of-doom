from sys import exit
from random import randint
        
class Enemy(object):

    def __init__(self, name, hp, dmg):
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.inventory = {}

    def is_alive(self):
        return self.hp > 0
        
    def description(self):

        desc = []
        if self.is_alive():
            desc.append("An evil %s stands before you.\n" % self.name)
        else:
            desc.append("A dead %s lies before you.\n" % self.name)
            for k,v in self.inventory.items():
                desc.append("It has a %s in its possession.\n" % k)
        
        return "\n".join(desc)

        
class Goblin(Enemy):
    def __init__(self):
        super(Goblin, self).__init__(name="goblin", hp=10, dmg=6)


class Spider(Enemy):
    def __init__(self):
        super(Spider, self).__init__(name="spider", hp=100, dmg=10)