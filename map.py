import enemies
import items

class MapTile(object):    
    N = None
    S = None
    E = None
    W = None
    contents  = {}
    
    def update_room_conditions(self):
        pass
    
    def description(self):
        return "Override this object with a specific Room object."
    
    def directions(self):
        """Get the directions available from the room."""
        NSEW = [a for a in dir(self) if len(a) == 1 and a in "NSEW"]
        dir_names = {'N': 'north', 'S': 'south', 'E': 'east', 'W': 'west'}
        dir_desc = []
        for a in NSEW:
            if getattr(self, a) is not None:
                dir_desc.append("You can go %s." % dir_names[a])
        return "\n".join(dir_desc)

    def contents_desc(self):
        """Get the descriptions of the room's contents."""
        contents_desc = []
        for item_name, item in self.contents.items():
            contents_desc.append(item.description())
        return "\n".join(contents_desc)
    
class EntranceRoom(MapTile):
    N = "door_room"
    W = "goblin_ruby_room"
    E = "goblin_rod_room"
    
    def description(self):
        return room_description(self,"You are at the entrance to the Dungeon of Doom.")

class SpiderRoom(MapTile):
    S = "door_room"
    spider = enemies.Spider()
    contents = {"spider" : spider}
    
    def description(self):
        return room_description(self, "You are in the Giant Spider room.")
        
class GoblinRubyRoom(MapTile):
    E = "entrance_room"
    goblin = enemies.Goblin()
    goblin.inventory["ruby"] = items.Ruby()
    contents = {"goblin" : goblin}    

    def description(self):
        return room_description(self,"You are in the Goblin Ruby room.")
        
        
class GoblinRodRoom(MapTile):
    W = "entrance_room"
    goblin = enemies.Goblin()
    goblin.inventory["rod"] = items.Rod()
    contents = {"goblin" : goblin}

    def description(self):
        return room_description(self,"You are in the Goblin Rod room.")

class KeyRoom(MapTile):
    W = "door_room"
    contents = {"key" : items.Key()}
    
    def description(self):
        return room_description(self,"You are in the key room.")

    
class DoorRoom(MapTile):
    S = "entrance_room"

    contents = {"door" : items.Door(True, "north"),
                "hook" : items.Hook()}
                
    def description(self):
        return room_description(self,"You are in the door room.")

    def update_room_conditions(self):    
        if self.contents["door"].is_locked == False:
            print "The door to the north is now open.\n"
            self.N = "spider_room"
        
        if self.contents["hook"].is_pulled == True:
            print "A room to the east is now open.\n"
            self.E = "key_room"

            
rooms = {'entrance_room' : EntranceRoom(),
         'spider_room' : SpiderRoom(),
         'goblin_ruby_room' : GoblinRubyRoom(),
         'goblin_rod_room' : GoblinRodRoom(),
         'key_room' : KeyRoom(),
         'door_room' : DoorRoom()}
        
def room_description(room,room_desc):
    desc = []
    desc.append(room_desc)
    desc.append(super(type(room),room).contents_desc())
    desc.append(super(type(room),room).directions())
    return "\n".join(desc)