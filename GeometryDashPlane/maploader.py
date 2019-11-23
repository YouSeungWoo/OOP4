from maplinker import *
from mapparser import *
from manage import *

class MapLoader():
    def __init__(self):
        self.scroll=0
        self.map_width=10
        self.next_width=10
        self.linker = MapLinker()
        self.parser = MapPaser()

    def get_obj(self):
        d_obj={}
        ret, width = self.parser.parse(self.linker.get_next())
        self.map_width=self.next_width
        self.next_width=width

        for i in ret:
            for j in i:
                j.x+=scr_size[0]+map_width+j.x*scr_size[0]//20
                j.y=j.y*scr_size[1]//10
        return ret

    def check_scroll(self,speed):
        self.scroll+=speed
        if self.scroll%map_width!=0:
            return false
        else:
            scroll=0
            return true
