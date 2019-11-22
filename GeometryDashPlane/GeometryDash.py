# -*- coding: cp949 -*-

# ���� ������ �����ϴ� ����

import pygame
from generation import Generation
from manage import *
from object import Geo
import numpy as np
import random, copy, os, sys
from input_layer import input_layer
from pygame.locals import QUIT, Rect, KEYDOWN, KEYUP, K_SPACE, K_LEFT # �Է¹��� Ű(spacebar), spacebar�� �ƴ� �ٸ� Ű(�ϴ� ���Ƿ� left key�� ����)


class Game():
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(5,5) # ������ ���� ���� ���
        
        self.high_score = 0
        self.n_gen = 0
        self.current_score = 0

        
        self.gamespeed = x_speed
        self.screen = pygame.display.set_mode(scr_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Geometry Dash: Plain')
        self.geo = [Geo(FileSize.geo.value[0], FileSize.geo.value[1], self.screen)] # geo ����
        
        # �������� �����ϱ�
        self.layers = [input_layer()]

        assert len(self.geo) == len(self.layers)


    def playgame(self):
        game_over = False
        sysfont=pygame.font.SysFont(None, 25) # ����� ������ ��Ʈ
        
        while not game_over:
            self.screen.fill(WHITE)

            # ���� �����Է� Ȯ��
            """for event in pygame.event.get():
                if event.type == QUIT: # ���� ��ư�� ������ ������
                    pygame.quit()
                    sys.exit()
            """
            for ly in self.layers:
                print(ly.get_input()) #  ��� ���̾ ���� �Է� Ȯ��
            
            if not game_over:
                self.current_score += 0.15
                score_image = sysfont.render("High score : {}     score : {}".format(int(self.high_score), int(self.current_score)), True, BLACK)
                self.screen.blit(score_image, (width * 0.7, 0)) # ������ ���
                
                for idx, geo in enumerate(self.geo): # ��� geo�� ���ؼ� �Է� ó�� �� �׸��� �۾� ����
                    self.screen.blit(geo.image, geo.move(self.layers[idx],self.gamespeed)) # self.geo.move(key, gamespeed)�� �̿��ؼ� geo�� �̵���Ű�� �װ��� ���
                pygame.display.update()
                self.clock.tick(FPS)

    def intro(self, user_mode):
        game_start = False
        sysfont = pygame.font.SysFont(None,30)

        while not game_start:
            self.screen.fill(BLACK)
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                return True;
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        game_start = True 

            # intro�� �ʿ��� �̹��� ����
            self.start_image, self.start_image_rect = load_image(FileName.background.value, FileSize.background.value[0], FileSize.background.value[1], -1)# sysfont.render("Press any key to Start...", True, (255,255,255))   
            self.screen.blit(self.start_image, (0, 0))
            self.intro_image, self.intro_image_rect = load_image(FileName.title.value, FileSize.title.value[0], FileSize.title.value[1], -1)
            self.screen.blit(self.intro_image, (width * 0.05, height * 0.1))
            self.start_txt_image, self.start_txt_rect = load_image(FileName.start_txt.value, FileSize.start_txt.value[0], FileSize.start_txt.value[1], -1)
            self.screen.blit(self.start_txt_image, (width * 0.3, height * 0.7))

            pygame.display.update()
                        # �ƹ� Ű�� ������ �������� �����ϰ� geo ����ؼ� ���� ����
            self.clock.tick(FPS)
            
        return True

    def start(self):
        is_start=self.intro(0)
        if is_start:
            self.playgame()
        
            
g= Game()
g.start()
