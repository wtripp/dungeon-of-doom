import enemies

class Item(object):

    def __init__(self, name, isGettable):
        self.name = name
        self.isGettable = isGettable
        self.useWith = []
        
    def use(self):
        return "The %s does nothing." % self.name
    
    def useOn(self, otherObject):
        return "You can't use the %s on the %s!" % (self.name, otherObject.name)
    
class Ruby(Item):
    
    def __init__(self):
        super(Ruby, self).__init__(name="ruby", isGettable=True)
        
    def useOn(self, otherItem):
        
        if type(otherItem) == Rod:
            return Wand()
            
        else:
            super(Ruby, self).useOn(otherObject)
    
class Rod(Item):
    
    def __init__(self):
        super(Ruby, self).__init__(name="rod", isGettable=True)

class Hook(Item):

    def __init__(self):
        super(Hook, self).__init__(name="hook", isGettable=False)
        self.isPulled = False

    def use(self):
        
        if self.isPulled:
            print "You pull the %s" % self.name
            self.isPulled = True
            
        else:
            print "You already pulled the %s" % self.name
            
class Door(Item):

    def __init__(self, lock_status):
        super(Door, self).__init__(name="door", isGettable=False)
        self.lock_status = lock_status
        
    def use(self):
    
        if self.lock_status == False:
            print "The door is locked. You cannot open it."
            
        else:
            print "You unlock the door."
            self.lock_status = True
            
class Key(Item):

    def __init__(self):
        super(Door, self).__init__(name="door", isGettable=False)
        
    def useOn(self, otherItem):
        
        if type(otherItem) == Door:
        
            if otherItem.lock_status == True:
                otherItem.lock_status == False
                return "You unlock the %s." % otherItem.name
                
            else:
                return "The %s is already unlocked." % otherItem.name
            
        else:
            super(Door, self).useOn(otherObject)

class Wand(Item):
    
    def __init__(self):
        super(Ruby, self).__init__(name="wand", isGettable=True)
        self.dmg = 100

    def use(self):
        return "Use the %s on what?" % self.name
        
    def useOn(self, otherItem):
        
        if type(otherItem) == Enemy:
            print "You use the %s on the %s."
            print "The %s does %s damage to the %s." % \
                  (self.name, self.dmg, otherItem.name)
            
            if not otherItem.is_alive():
                print "The %s is dead!" % otherItem.name
                
        else:
            super(Ruby, self).useOn(otherObject)