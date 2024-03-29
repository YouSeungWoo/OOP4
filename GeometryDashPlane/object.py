# 게임에 사용되는 객체를 관리하는 파일
import pygame, os, sys, random, copy, math
from manage import *
from pygame.locals import K_SPACE, Rect

class ImageCache: # image caching class
    def __init__(self):
        self.d = dict() # cache

    def load_image(self, file, szx, szy, arg): # caching method
        if (file, szx, szy, arg) in self.d:
            ret = self.d[(file, szx, szy, arg)]
            return (ret[0], ret[1].copy())

        img = load_image(file, szx, szy, arg)
        self.d[(file, szx, szy, arg)] = img

        return (img[0], img[1].copy())

g_cache = ImageCache() # cache object

class Geo(pygame.sprite.Sprite):
    def __init__(self, size_x = -1, size_y = -1, screen = None):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        
        # setup image
        self.geo_image, self.rect = g_cache.load_image(FileName.geo.value, size_x, size_y, None) # 이미지 로드
        self.image = self.geo_image
        self.rect.center = (width * 0.3, height * 0.7)

        # setup statement
        self.x, self.y = self.rect.center
        self.velocity = 0
        self.isUp = False
        self.isDead = False

        # setup etc.
        self.score = 0
        self.fitness = 0
        self.rad = 0
    
    def trans(self):
        (self.x, self.y) = self.rect.center
        self.image = pygame.transform.rotate(self.geo_image, math.degrees(self.rad))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
    def move(self, layer, gamespeed, gravity):
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
        
        if self.rect.bottom >= height + 32: # not to exceed the lower boundary
            if self.velocity > 0 :
                if gravity  < 1:
                    self.velocity *= 0.6
                else:
                    self.velocity *= 0.25
                self.trans()
                bottom = self.rect.bottom
                self.rect.move_ip(0, height + 32 - bottom)

        elif self.rect.top <= -20 : # not to exceed the upper boundary
            if self.velocity < 0:
                if gravity < 1:
                    self.velocity *= 0.57
                else:
                    self.velocity *= 0.23
                self.trans()
                top = self.rect.top
                self.rect.move_ip(0, -top - 20)

        self.trans()
        self.rect.move_ip(0, self.velocity)

        return self.rect.topleft
    
    def colli_Check(self, group):
        if not len(pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_mask)) == 0:
            return True
        return False

class Spike(pygame.sprite.Sprite):
    def __init__(self, size_x = -1, size_y = -1, type = 0, rotate = 0, x_coord = -1, y_coord = -1, screen = None, gamespeed = x_speed):
        pygame.sprite.Sprite.__init__(self, self.containers)

        # setup image
        self.spike_image, self.rect = g_cache.load_image(FileName.spike.value[type], size_x, size_y, None)
        self.images = [self.spike_image, pygame.transform.rotate(self.spike_image, rotate)]
        self.image = self.images[1]
        
        # setup statement
        self.x, self.y = (x_coord, y_coord)
        self.velocity = -gamespeed
        
    def draw(self):
        self.screen.blit(self.spike_image, self.rect)
        
    def update(self):
        self.rect.move_ip(self.velocity, 0)
        if self.rect.right < 0:
            self.kill()
    
    def is_collidable(self):
        if self.rect.left < (width * 0.3 + 86):
            return True
        return False

    def set_velocity(self, v):
        self.velocity
        
class Brick(pygame.sprite.Sprite):
    def __init__(self, size_x = -1, size_y = -1, type = 0, rotate = 0, x_coord = -1, y_coord = -1, screen = None, gamespeed = x_speed):
        pygame.sprite.Sprite.__init__(self, self.containers)

        # setup image
        self.brick_image, self.rect = g_cache.load_image(FileName.brick.value[type], size_x, size_y, None)
        self.images = [self.brick_image, pygame.transform.rotate(self.brick_image, rotate)]        
        self.image = self.images[1]

        # setup statement
        self.x, self.y = (x_coord, y_coord)
        self.velocity = -gamespeed
    
    def draw(self):
        screen.blit(self.brick_image, self.rect)
        
    def update(self):
        self.rect.move_ip(self.velocity, 0)
        if self.rect.right < 0:
            self.kill()