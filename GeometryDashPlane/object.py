# 게임에 사용되는 객체를 관리하는 파일

import os, sys, pygame, random
from manage import *

class Geo(pygame.sprite.Sprite):
    def __init__(self, size_x=-1, size_y=-1, screen = None):