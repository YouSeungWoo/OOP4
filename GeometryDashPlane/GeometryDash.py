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

    def intro(self, user_mode):
        game_start = False

        title, title_rect = load_image(FileName.title, -1)
        # title 위치 설정 추가하기

        text, text_rect = load_image(FileName.title_text, -1)
        # text 위치 설정 추가하기

        while not game_start:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                return true;
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return true
                    if event.key == pygame.KEYDOWN:
                        self.screen.fill(WHITE)
                        self.screen.blit(BackgroundImage.stage1, 0, 0)
                        pygame.display.update()
                        # 아무 키나 누르면 스테이지 생성하고 geo 출력해서 게임 시작

            self.clock.tick(FPS)
            game_start = True