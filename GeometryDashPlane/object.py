# 게임에 사용되는 객체를 관리하는 파일

import os, sys, pygame, random
from manage import *
from pygame.locals import K_SPACE, Rect
import numpy as np
import math

class Geo(pygame.sprite.Sprite):
    def __init__(self, size_x = -1, size_y = -1, screen = None):
        pygame.sprite.Sprite.__init__(self)
        
        self.geo_image, self.rect  = load_image(FileName.geo.value, size_x, size_y, None) # 이미지 로드
        self.image= self.geo_image
        self.x,self.y = self.rect.topleft
        self.velocity = 0
        self.isUp = False
        self.rect.move_ip(geo_pos,2*height/5) # 처음 좌표 이동
    
    def trans(self):
        (self.x, self.y) = self.rect.center
        self.image = pygame.transform.rotate(self.geo_image, math.degrees(math.atan(-self.velocity / x_speed)))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
    def move(self, key, gamespeed):
        if key == K_SPACE: # 스페이스바를 누르면 올라가기
            self.isUP = True
        else:
            self.isUP = False
        

        if self.velocity < x_speed:
            if self.isUP:
                self.velocity -= gravity * (1 - math.atan(-self.velocity / x_speed))
            else:
                self.velocity += gravity * (1 - math.atan(self.velocity / x_speed))
        self.trans()
        self.rect.move_ip(0,self.velocity) # geo_image_rect를 옮겨 줌
        
        if self.rect.bottom >= height:
            if not self.isUP or self.velocity > 0 :
                self.velocity=0
                self.trans()
                bottom = self.rect.bottom
                self.rect.move_ip(0, height - bottom)
        elif self.rect.top <= 0 :
            if self.isUP or self.velocity < 0:
                self.velocity=0
                self.trans()
                top = self.rect.top
                self.rect.move_ip(0, -top)
        
        return self.rect.topleft # geo_image_rect의 왼쪽 위의 좌표를 반환


class Thorn(pygame.sprite.Sprite):
    def __init__(self, size_x=-1, size_y=-1, screen=None, gamespeed = x_speed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.thorn_image, self.rect = load_image(FileName.thorn.value, size_x, size_y, None) # 이미지 로드
        self.image=self.thorn_image
        self.x, self.y = self.rect.topleft
        self.velocity = -gamespeed
        self.rect.left = width
        self.rect.bottom = 0.98*height
    
    def draw(self):
        self.screen.blit(self.thorn_image,self.rect)
        
    def update(self):
        self.rect.move_ip(self.velocity,0)
        if self.rect.right<0:
            self.kill()
            return (-1, -1)
        else:
            return self.rect.topleft

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        