# -*- coding: cp949 -*-
# 게임에 사용되는 객체를 관리하는 파일

import os, sys, pygame, random, math
from manage import *
from pygame.locals import K_SPACE, Rect
import numpy as np
from collision import *

class Geo(pygame.sprite.Sprite):
    def __init__(self, size_x = -1, size_y = -1, screen = None):
        pygame.sprite.Sprite.__init__(self)
        
        self.geo_image, self.geo_image_rect  = load_image(FileName.geo.value, size_x, size_y, None) # 이미지 로드
        self.image = self.geo_image
        self.rect = self.image.get_rect()
        self.rect.center = (width * 0.3, height * 0.7)
        self.screen = screen

        self.velocity = 0
        self.isUp = False
    
    def move(self, layer, gamespeed):
        self.isUP = layer.get_key() # get keypress value

        if self.velocity < gamespeed:
            if self.isUP:
                self.velocity -= gravity * (1 - math.atan(-self.velocity / gamespeed))
            else:
                self.velocity += gravity * (1 - math.atan(self.velocity / gamespeed))
                
        self.x, self.y = self.rect.center
        self.rad = math.atan(-self.velocity / gamespeed)
        self.image = pygame.transform.rotate(self.geo_image, math.degrees(self.rad))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.outline()

        self.rect.move_ip(0, self.velocity) # geo_image_rect를 옮겨 줌

        return self.rect.topleft # geo_image_rect의 왼쪽 위의 좌표를 반환

    def outline(self):
        self.v = Vector
        self.poly = Concave_Poly(self.v(width * 0.3, height * 0.7), [self.v(30, 0), self.v(0, 30), self.v(30, 50)])
        self.poly.angle = -self.rad
        self.poly.pos.x = self.x
        self.poly.pos.y = self.y
        self.poly.center = (self.x, self.y)
        
        pygame.draw.polygon(self.screen, BLACK, self.poly.points, 3)


class thorn(pygame.sprite.Sprite):
    def __init__(self, size_x = -1, size_y = -1, screen = None):
        pygame.sprite.Sprite.__init__(self)
        self.thorn_image, self.thorn_image_rect = pygame.image.load(FileName.thorn)
