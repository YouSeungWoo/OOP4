import pygame
from manage import *
from object import Geo, Spike, Brick
from maplinker import MapLinker

class MapParser():
    def __init__(self):
        self.arr = [] # list에 담겨 있는 문자열을 숫자들로 바꿔 줌
        self.objs = []
        self.bricks = []
        self.spikes = []
        self.map_width = int(list[0])
    
    def parse(self, list, screen):
        del list[0]
        del list[1]
        del list[2]
        for s in list:
            line = s.split(' ')
            num = []
            for i in range(0,5):
                num.append(int(line[i]))
            self.arr.append(num)
            
        for obj in self.arr:
            if obj[0] == 0 :
                temp = Brick(FileSize.brick[obj[1]].value[0], FileSize.brick[obj[1]].value[1], obj[1], obj[2], obj[3], obj[4])
                self.bricks.append(temp)
            elif obj[0] == 1 :
                temp = Spike(FileSize.spike[obj[1]].value[0], FileSize.spike[obj[1]].value[0], obj[1], obj[2], obj[3], obj[4])
                self.spikes.append(temp)
        self.objs.append(self.bricks)
        self.objs.append(self.spikes)

        return (self.objs, self.map_width)
