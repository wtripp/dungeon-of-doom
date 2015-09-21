import enemies
import items

class MapTile(object):    
    N = None
    S = None
    E = None
    W = None
    contents  = {}
    
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

    def room_contents(self):
        """Get the descriptions of the room's contents."""
        contents_desc = []
        for k, v in self.contents.items():
            contents_desc.append(v.description())
        return "\n".join(contents_desc)
    
class EntranceRoom(MapTile):
    N = "spider_room"
    W = "goblin_ruby_room"
    
    def description(self):
        return room_description(self,"You are at the entrance to the Dungeon of Doom.")
    
class SpiderRoom(MapTile):
    S = "entrance_room"
    spider = enemies.Spider()
    contents = {"spider" : spider}
    
    def description(self):
        return room_description(self,"You are in the Giant Spider room.")

        
class GoblinRubyRoom(MapTile):
    E = "entrance_room"
    goblin = enemies.Goblin()
    ruby = items.Ruby()
    goblin.inventory.append(ruby)
    contents = {"goblin" : goblin}
    
    if not goblin.is_alive:
        contents["ruby"] = ruby
    
    
    def description(self):
        return room_description(self,"You are in the Goblin Ruby room.")
        

rooms = {'entrance_room' : EntranceRoom(),
         'spider_room' : SpiderRoom(),
         'goblin_ruby_room' : GoblinRubyRoom()}
        
def room_description(room,room_desc):
    desc = []
    desc.append(room_desc)
    desc.append(super(type(room),room).room_contents())
    desc.append(super(type(room),room).directions())
    return "\n".join(desc)