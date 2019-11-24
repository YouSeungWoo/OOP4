from maplinker import *
from mapparser import *
from manage import *

class MapLoader():
    def __init__(self, screen):
        self.scroll=0
        self.map_width=10
        self.next_width=10
        self.linker = MapLinker()
        self.parser = MapParser()
        self.screen = screen

    def get_obj(self):
        d_obj={}
        ret, width = self.parser.parse(self.linker.get_next(), self.screen)
        self.map_width = self.next_width
        self.next_width = (width + 1) * (scr_size[0]//20)
        for i in ret:
            for j in i:
                print("DATA")
                print((j.x, j.y))
                j.x=scr_size[0]+self.map_width+j.x*(scr_size[0]//21) # 11/24 수정. width 분할을 21개로 해야 한다.
                j.y=j.y*(scr_size[1]//10)
                j.rect.topleft = (j.x, j.y)
        return ret

    def check_scroll(self,speed):
        self.scroll += speed
        print("SCR : " + str(self.scroll))
        if self.scroll >= self.map_width:
            self.scroll = 0
            return True
        else:
            return False
