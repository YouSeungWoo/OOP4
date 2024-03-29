import pygame
from manage import *
from object import Geo, Spike, Brick
from maplinker import MapLinker

class MapParser():
    def __init__(self):
        self.arr = [] # convert strings in list to numbers
        self.objs = []
        self.bricks = []
        self.spikes = []
        self.map_width = 0
    
    def parse(self, list_, screen, speed):
        self.arr = []  # convert strings in list to numbers
        self.objs = []
        self.bricks = []
        self.spikes = []
        self.map_width = 0
        self.map_width = int(list_[0])
        list_ = list_[3:]

        for s in list_:
            line = s.split(' ')
            num = []

            for i in range(0, 5):
                num.append(int(line[i]))
            self.arr.append(num)
            
        for obj in self.arr:
            if obj[0] == 0 :
                temp = Brick(FileSize.brick.value[obj[1]][0], FileSize.brick.value[obj[1]][1], obj[1], obj[2], obj[3], obj[4], screen, speed)
                self.bricks.append(temp)

            elif obj[0] == 1 :
                temp = Spike(FileSize.spike.value[obj[1]][0], FileSize.spike.value[obj[1]][0], obj[1], obj[2], obj[3], obj[4], screen, speed)
                self.spikes.append(temp)

        self.objs.append(self.bricks)
        self.objs.append(self.spikes)

        return (self.objs, self.map_width)