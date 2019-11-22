# 게임에 사용되는 객체를 관리하는 파일

import os, sys, pygame, random
from manage import *
from pygame.locals import K_SPACE, Rect
import numpy as np

class Geo(pygame.sprite.Sprite):
    def __init__(self, size_x = -1, size_y = -1, screen = None):
        pygame.sprite.Sprite.__init__(self)
        
        self.geo_image, self.geo_image_rect  = load_image(FileName.geo.value, size_x, size_y, None) # 이미지 로드
        self.xpos,self.ypos=self.geo_image_rect.topleft
        self.velocity = 0
        self.isUp = False
    
    def move(self, key, gamespeed):
        if key == K_SPACE: # 스페이스바를 누르면 올라가기
            self.isUP = True
        else:
            self.isUP = False
        
        if self.velocity < gamespeed:
            self.velocity += -gravity if self.isUP else 0.5 * gravity
        self.geo_image_rect.move_ip(0,self.velocity) # geo_image_rect를 옮겨 줌
        return self.geo_image_rect.topleft # geo_image_rect의 왼쪽 위의 좌표를 반환


class thorn(pygame.sprite.Sprite):
    def __init__(self, size_x=-1, size_y=-1, screen=None):
        pygame.sprite.Sprite.__init__(self)
        self.thorn_image, self.thorn_image_rect = pygame.image.load(FileName.thorn)