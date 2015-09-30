import enemies
"""Items in the game."""


class Item(object):
    """
    Base class for items.
    1) Items can have a description.
    2) Items can be used.
    3) Items can be used on something else.
   """

    def __init__(self, name, is_gettable):
        self.name = name
        self.is_gettable = is_gettable
        self.useWith = []

    def description(self):
        return "This item has no description."
        
    def use(self):
        print "The %s does nothing." % self.name
    
    def useOn(self, otherItem):
        print "You can't use the %s on the %s." % (self.name, otherItem.name)
        
    
class Ruby(Item):
    """The Ruby can be combined with the Rod to form a Wand."""
    def __init__(self):
        super(Ruby, self).__init__(name="ruby", is_gettable=True)

    def description(self):
        return "You see a red, sparkly ruby."      

    def useOn(self, otherItem):
    
        if type(otherItem) == Rod:
            print "You combine the ruby and rod to form a wand!"
            return Wand()
            
        else:
            super(Ruby, self).useOn(otherItem)

            
class Rod(Item):
    """The Rod can be combined with the Ruby to form a Wand."""    
    def __init__(self):
        super(Rod, self).__init__(name="rod", is_gettable=True)

    def description(self):
        return "You see a long, straight wooden rod."       

    def useOn(self, otherItem):
    
        if type(otherItem) == Ruby:
            super(Rod, self).useOn(otherItem)
            print "Try the other way around..."
            
        else:
            super(Rod, self).useOn(otherItem)

            
class Hook(Item):
    """ The Hook can be pulled."""
    def __init__(self):
        super(Hook, self).__init__(name="hook", is_gettable=False)
        self.is_pulled = False

    def description(self):
    
        if not self.is_pulled:
            return "You see a hook on the wall. It looks like it can be pulled."
            
        else:
            return "You see a hook on the wall. It has been pulled."

    def use(self):
        
        if not self.is_pulled:
            print "You pull the %s." % self.name
            self.is_pulled = True
            
        else:
            print "You already pulled the %s." % self.name
            
class Door(Item):
    """The Door can be locked and can be opened up to a specified direction."""
    def __init__(self, is_locked, direction):
        super(Door, self).__init__(name="door", is_gettable=False)
        self.is_locked = is_locked
        self.direction = direction

    def description(self):
        
        if self.is_locked == True:
            return "You see a door on the %s wall. It is locked." \
                   % self.direction
            
        else:
            return "You see a door on the %s wall. It is unlocked." \
                   % self.direction
        
    def use(self):
    
        if self.is_locked == True:
            print "The door is locked. You cannot open it."
            
        else:
            print "You unlock the door."
            self.is_locked = False
            
class Key(Item):
    """The Key can open a locked Door."""
    def __init__(self):
        super(Key, self).__init__(name="key", is_gettable=True)

    def description(self):
        return "You see a small key."        

    def useOn(self, otherItem):
        
        if type(otherItem) == Door:
        
            if otherItem.is_locked == True:
                print "You unlock the %s." % otherItem.name
                otherItem.is_locked = False
                
            else:
                print "The %s is already unlocked." % otherItem.name
            
        else:
            super(Key, self).useOn(otherItem)

class Wand(Item):
    """The Wand can do a specified amount of damage"""  
    def __init__(self):
        super(Wand, self).__init__(name="wand", is_gettable=True)
        self.dmg = 100

    def description(self):
        return "You see a powerful wand with a red ruby at the top."   

    def use(self):
        print "Use the %s on what?" % self.name
        
    def useOn(self, otherItem):
        
        # If the item's base class is Enemy and the enemy is alive,
        # use the wand on the enemy.
        if enemies.Enemy in otherItem.__class__.__bases__ and \
           otherItem.is_alive():
            print "You use the %s on the %s." % (self.name, otherItem.name)
            print "The %s does %s damage to the %s." % \
                  (self.name, self.dmg, otherItem.name)
            otherItem.hp -= self.dmg
            
            # If the enemy is dead, don't use the wand.
            if not otherItem.is_alive():
                print "The %s is dead!" % otherItem.name
        
        # Otherwise print the standard "You can't use the wand" message.
        else:
            super(Wand, self).useOn(otherItem)