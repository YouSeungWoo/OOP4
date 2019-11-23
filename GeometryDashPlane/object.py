# 게임에 사용되는 객체를 관리하는 파일

import os, sys, pygame, random
from manage import *
from pygame.locals import K_SPACE, Rect
import numpy as np
import math
from collision import *

class Geo(pygame.sprite.Sprite):
    def __init__(self, size_x = -1, size_y = -1, screen = None):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.geo_image, self.rect  = load_image(FileName.geo.value, size_x, size_y, None) # 이미지 로드
        self.image= self.geo_image
        self.rect.center = (width * 0.3, height * 0.7) #처음 좌표 이동
        self.x,self.y = self.rect.center
        self.velocity = 0
        self.isUp = False
    
    def trans(self):
        (self.x, self.y) = self.rect.center
        self.image = pygame.transform.rotate(self.geo_image, math.degrees(self.rad))
        self.outline()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
    def move(self, layer, gamespeed):
        self.isUP = layer.get_key() # get keypress value

        if self.velocity > gamespeed:
            self.velocity = +gamespeed
        if self.velocity < -gamespeed:
            self.velocity = -gamespeed

        self.rad = math.atan(-self.velocity / gamespeed)

        if self.isUP:
            self.velocity -= gravity * (1 - abs(self.rad))
        else:
            self.velocity += gravity * (1 - abs(self.rad))
            
        
        
        if self.rect.bottom >= height: #밑으로 안 넘어가기
            if not self.isUP or self.velocity > 0 :
                self.velocity = 0
                self.trans()
                bottom = self.rect.bottom
                self.rect.move_ip(0, height - bottom)
        elif self.rect.top <= 0 : #위로 안 넘어가기
            if self.isUP or self.velocity < 0:
                self.velocity=0
                self.trans()
                top = self.rect.top
                self.rect.move_ip(0, -top)
        self.trans()
        self.rect.move_ip(0 , self.velocity) # geo_image_rect를 옮겨 줌
        return self.rect.topleft # geo_image_rect의 왼쪽 위의 좌표를 반환
    
    def outline(self):
        self.v = Vector
        self.poly = Hitbox.geo.value
        self.poly.angle = -self.rad
        
        self.poly.pos.x = self.x
        self.poly.pos.y = self.y
        
        pygame.draw.polygon(self.screen, BLACK, self.poly.points, 3)
    
    def colli_Check(self, group):
        if not len(pygame.sprite.spritecollide(self,group,False,pygame.sprite.collide_mask)) == 0:
            return True
        return False

class Spike(pygame.sprite.Sprite):
    def __init__(self, size_x=-1, size_y=-1, screen = None, gamespeed = x_speed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spike_image, self.rect = load_image(FileName.spike.value, size_x, size_y, None) # 이미지 로드
        self.images = [self.spike_image, pygame.transform.rotate(self.spike_image, 180)]
        self.x, self.y = self.rect.topleft
        self.velocity = -gamespeed
        self.point = [(width, 0.9*height), (width, 0.1*height)]
        r = random.randint(0,1)
        self.image = self.images[r]
        self.rect.bottomleft = self.point[r]
    
    def draw(self):
        self.screen.blit(self.spike_image,self.rect)
        
    def update(self):
        self.rect.move_ip(self.velocity,0)
        if self.rect.right < 0:
            self.kill()

        
class Brick(pygame.sprite.Sprite):
    def __init__(self, size_x=-1, size_y=-1, screen = None, gamespeed = x_speed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.brick_image, self.rect = load_image(FileName.brick.value, size_x, size_y, None)
        self.image = self.brick_image
        self.x, self.y = self.rect.topleft
        self.velocity = -gamespeed
    
    def draw(self):
        self.screen.blit(self.brick_image, self.rect)
        
    def update(self):
        self.rect.move_ip(self.velocity, 0)
        if self.rect.right < 0:
            self.kill()
        
        
        
        
        
        
        
        
        
        
        
        
        