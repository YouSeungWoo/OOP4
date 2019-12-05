from maplinker import *
from mapparser import *
from manage import *

class MapLoader():
    def __init__(self, screen):
        self.scroll = 0
        self.map_width = 10
        self.next_width = 10
        self.linker = MapLinker()
        self.parser = MapParser()
        self.screen = screen

    def get_obj(self, speed):
        d_obj = {}
        ret, width = self.parser.parse(self.linker.get_next(), self.screen, speed)
        self.map_width = self.next_width
        self.next_width = (width + 1) * (scr_size[0] // 20)

        for i in ret:
            for j in i:
                j.rect.topleft = (scr_size[0] + self.map_width + j.x * (scr_size[0] // 21), j.y * (scr_size[1] // 10)) # optimize

        return ret

    def check_scroll(self, speed):
        self.scroll += speed

        if self.scroll >= self.map_width:
            self.scroll = 0
            return True
        else:
            return False