import enemies

class Item(object):

    def __init__(self, name, isGettable):
        self.name = name
        self.isGettable = isGettable
        self.useWith = []

    def description(self):
        print "This item has no description.\n"
        
    def use(self):
        print "The %s does nothing." % self.name
    
    def useOn(self, otherItem):
        print "You can't use the %s on the %s." % (self.name, otherItem.name)
        
    
class Ruby(Item):
    
    def __init__(self):
        super(Ruby, self).__init__(name="ruby", isGettable=True)

    def description(self):
        print "You see a red, sparkly ruby.\n"       

    def useOn(self, otherItem):
    
        if type(otherItem) == Rod:
            print "You combine the ruby and rod to form a wand!"
            return Wand()
            
        else:
            super(Ruby, self).useOn(otherItem)

            
class Rod(Item):
    
    def __init__(self):
        super(Rod, self).__init__(name="rod", isGettable=True)

    def description(self):
        print "You see a long, straight wooden rod.\n"       

    def useOn(self, otherItem):
    
        if type(otherItem) == Rod:
            print Wand()
            
        else:
            super(Rod, self).useOn(otherItem)
            print "Try the other way around..."
        
class Hook(Item):

    def __init__(self):
        super(Hook, self).__init__(name="hook", isGettable=False)
        self.isPulled = False

    def description(self):
    
        if not self.isPulled:
            print "You see a hook on the wall. It looks like it can be pulled.\n"
            
        else:
            print "You see a hook on the wall. It has been pulled.\n"

    def use(self):
        
        if self.isPulled:
            print "You pull the %s" % self.name
            self.isPulled = True
            
        else:
            print "You already pulled the %s." % self.name
            
class Door(Item):

    def __init__(self, lock_status):
        super(Door, self).__init__(name="door", isGettable=False)
        self.lock_status = lock_status

    def description(self):
        
        if self.lock_status == False:
            print "You see a door. It is locked.\n"
            
        else:
            print "You see a door. It is unlocked.\n"
        
    def use(self):
    
        if self.lock_status == False:
            print "The door is locked. You cannot open it."
            
        else:
            print "You unlock the door."
            self.lock_status = True
            
class Key(Item):

    def __init__(self):
        super(Key, self).__init__(name="key", isGettable=False)

    def description(self):
        print "You see a small key.\n"        

    def useOn(self, otherItem):
        
        if type(otherItem) == Door:
        
            if otherItem.lock_status == True:
                otherItem.lock_status == False
                print "You unlock the %s." % otherItem.name
                
            else:
                print "The %s is already unlocked." % otherItem.name
            
        else:
            super(Key, self).useOn(otherItem)

class Wand(Item):
    
    def __init__(self):
        super(Wand, self).__init__(name="wand", isGettable=True)
        self.dmg = 100

    def description(self):
        print "You see a powerful wand with a red ruby at the top.\n"   

    def use(self):
        print "Use the %s on what?" % self.name
        
    def useOn(self, otherItem):

        if enemies.Enemy in otherItem.__class__.__bases__ and \
           otherItem.is_alive():
            print "You use the %s on the %s." % (self.name, otherItem.name)
            print "The %s does %s damage to the %s." % \
                  (self.name, self.dmg, otherItem.name)
            otherItem.hp -= self.dmg
            
            if not otherItem.is_alive():
                print "The %s is dead!" % otherItem.name
                
        else:
            super(Wand, self).useOn(otherItem)