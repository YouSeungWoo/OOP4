# 맵뷰어

import pygame
from manage import *
from object import Geo, Spike, Brick
import numpy as np
import random, copy, os, sys
from pygame.locals import QUIT, Rect, KEYDOWN, KEYUP, K_SPACE, K_LEFT, K_RIGHT, K_DOWN, K_UP
from mapparser import MapParser
from mapparser import MapParser

class GeoMapViewer:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(5,5)

        self.gamespeed = 0
        self.bgcolor = BLACK
        self.xscroll = 0
        self.maxwidth = 0
        self.mapfile_name = ""
        self.map_parser = MapParser()
        self.lines = []

        self.screen = pygame.display.set_mode(scr_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Geometry Dash: MapViewer')

    def screen_loop(self):
        sysfont = pygame.font.SysFont(None, 25)
        message = sysfont.render("GMD Map Viewer      Space : Load Map File/Save      Left/Right key : scroll map      Up Key : Undo      Down Key : Make Object", True, WHITE)

        self.bricks = pygame.sprite.Group()
        Brick.containers = self.bricks
        self.spikes = pygame.sprite.Group()
        Spike.containers = self.spikes

        helpme = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        if len(self.mapfile_name) != 0:
                            with open(self.mapfile_name, "r") as f:
                                tmp = f.readlines()

                            print(tmp)
                            tmp[0] = str(self.maxwidth) + "\n"

                            if tmp[-1][-1] != "\n":
                                tmp[-1] += "\n"

                            with open(self.mapfile_name, "w") as f:
                                f.writelines(tmp)

                                for idx, i in enumerate(self.lines):
                                    if i[-1] != "\n" and idx != len(self.lines) - 1:
                                        i += "\n"

                                    f.write(i)

                        self.lines = []
                        self.xscroll = 0

                        print("Map to READ : ")
                        self.load_map("map\\" + input())
                        print("Load Complete!")

                        helpme = False

                    elif event.key == pygame.K_LEFT:
                        self.xscroll -= 1
                        self.set_coord(-1)

                    elif event.key == pygame.K_RIGHT:
                        self.xscroll += 1
                        self.set_coord(1)

                    elif event.key == pygame.K_DOWN:
                        print("Add Element : ")
                        self.load_obj(input())
                        print("Load Complete!")

                    elif event.key == pygame.K_UP:
                        self.undo_obj()
                        print("Undo Complete!")

                elif event.type == pygame.QUIT:
                    print("EXIT GAME")
                    pygame.quit()
                    sys.exit()

            self.screen.fill(self.bgcolor) # default background color setup

            if helpme:
                self.screen.blit(message, (scr_size[0] / 2 - message.get_rect().width / 2,scr_size[1] / 2 - message.get_rect().height / 2))

            self.spikes.draw(self.screen)
            self.bricks.draw(self.screen)
            pygame.display.update()
    
    def set_coord(self, diff):
        for o in self.spikes:
            o.rect.topleft = (o.rect.topleft[0] + diff * scr_size[0] // 20, o.rect.topleft[1])
        for o in self.bricks:
            o.rect.topleft = (o.rect.topleft[0] + diff * scr_size[0] // 20, o.rect.topleft[1])
    
    def add_objs(self, objs):
        for i in objs:
            for j in i:
                j.rect.topleft = (j.x * (scr_size[0] // 21), j.y * (scr_size[1] // 10))

        for o in objs[0]:
            self.bricks.add(o)
        for o in objs[1]:
            self.spikes.add(o)
    
    def load_map(self, map_file):
        self.mapfile_name = map_file
        self.spikes.empty()
        self.bricks.empty()

        try:
            with open(map_file, "r") as f: # open file
                data = str(f.read()).split("\n")
                assert len(data) >= 4
        except:
            print("No FILE!")
            return

        objs, self.maxwidth = self.map_parser.parse(data, self.screen)
        self.add_objs(objs)
        self.set_coord(self.xscroll)

    def load_obj(self, obj_str):
        x = int(obj_str.split(" ")[3]) # x

        if x - self.xscroll < 0:
            print("OUT OF RANGE!")
            return

        objs = self.map_parser.parse([str(x),"","",obj_str], self.screen)[0]
        temp = obj_str.split(" ")
        temp[3] = str(x - self.xscroll)

        if self.maxwidth < x - self.xscroll:
            self.maxwidth = x - self.xscroll
            print("MAXWIDTH CHANGED : " + str(self.maxwidth))
        
        self.add_objs(objs)
        objs = ""

        for i in temp:
            objs += i
            objs += " "

        objs = objs[0: -1]
        self.lines.append(objs) # change list
        print("Current Changes")
        print(self.lines)
    
    def load_obj_undo(self, obj_str):
        x = int(obj_str.split(" ")[3]) # x
        objs = self.map_parser.parse([str(x), "", "", obj_str], self.screen)[0]

        for i in objs:
            for j in i:
                j.x = j.x + self.xscroll

        self.add_objs(objs)
        
    def undo_obj(self):
        if len(self.lines) == 0:
            print("List Empty!")
            return

        print(self.lines)
        self.lines.pop()

        print(self.lines)
        self.load_map(self.mapfile_name)

        for l in self.lines:
            self.load_obj_undo(l)

# ====================================================
g = GeoMapViewer()
g.screen_loop()