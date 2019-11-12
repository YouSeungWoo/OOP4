# 실제 게임을 진행하는 파일

import pygame
from generation import Generation
from manage import *
import numpy as np
import random, copy, os, sys


class Game():
    def __init__(self):
        pygame.init()

        self.high_score = 0
        self.n_gen = 0
        self.current_score = 0

        self.game_speed = 4
        self.max_speed = 10

        self.geo = None

        self.screen = pygame.display.set_mode(scr_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Geometry Dash: Plain')
        
        # 유전정보 생성하기


    def playgame(self):
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                pygame.display.update()
                clock.tick(FPS)