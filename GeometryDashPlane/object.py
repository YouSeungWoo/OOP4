# 게임에 사용되는 객체를 관리하는 파일

import os, sys, pygame, random
from manage import *

class Geo(pygame.sprite.Sprite):
    def __init__(self, size_x = -1, size_y = -1, screen = None):
        pygame.sprite.Sprite.__init__(self)
        self.geo_image = pygame.image.load(FileName.geo)          # image file name 추가
        self.geo_image_rect                             # rect 찾아주는 함수 만들기
        
        self.isUp = False
        self.isDown = False