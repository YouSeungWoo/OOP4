# 실제 게임을 진행하는 파일

import pygame
from generation import Generation
from manage import *
from object import Geo, Spike, Brick
import numpy as np
import random, copy, os, sys
from input_layer import input_layer
from pygame.locals import QUIT, Rect, KEYDOWN, KEYUP, K_SPACE, K_LEFT # 입력받을 키(spacebar), spacebar가 아닌 다른 키(일단 임의로 left key로 정함)


class Game():
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(5,5) # 누르고 있을 것을 대비
        
        self.high_score = 0
        self.n_gen = 0
        self.current_score = 0
        self.gamespeed = x_speed
    
        self.screen = pygame.display.set_mode(scr_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Geometry Dash: Plain')
        
        # 유전정보 생성하기
        self.geo = [Geo(FileSize.geo.value[0], FileSize.geo.value[1], self.screen)] # geo 생성
        self.layers = [input_layer()]

        assert len(self.geo) == len(self.layers)

    def playgame(self):
        # setup initial condition
        game_over = False # gameover flag
        game_ing = False # game palying flag
        sysfont=pygame.font.SysFont(None, 25) # 출력할 문장의 폰트
        self.screen.fill(WHITE) # default background color setup
        
        self.bricks = pygame.sprite.Group()
        Brick.containers = self.bricks
        self.spikes = pygame.sprite.Group()
        Spike.containers = self.spikes
        
        # initial image draw
        gameover_image = sysfont.render("Game Over...", True, BLACK)
        score_image = sysfont.render("High score : {}     score : {}".format(int(self.high_score), int(self.current_score)), True, BLACK)
        self.screen.blit(score_image, (width * 0.7, 0)) # 점수판 출력
        self.screen.blit(geo.image, geo.rect.topleft)
        pygame.display.update()
        
        # game loop
        while not game_over:
            for ly in self.layers: # input check
                print(ly.get_input()) #  모든 레이어에 대해 입력 확인
            
            if game_ing: # playing loop
                self.current_score += 0.15
                score_image = sysfont.render("High score : {}     score : {}".format(int(self.high_score), int(self.current_score)), True, BLACK)
                self.screen.blit(score_image, (width * 0.7, 0)) # 점수판 출력
                for idx, geo in enumerate(self.geo): # 모든 geo에 대해서 입력 처리 및 그리기 작업 수행
                    self.screen.blit(geo.image, geo.move(self.layers[idx],self.gamespeed)) # self.geo.move(key, gamespeed)를 이용해서 geo를 이동시키고 그것을 출력
                if int(self.current_score) % 5 == 0:
                    self.spike = Spike(80,80,self.screen)
                    self.spikes.add(self.spike)
                self.spikes.update()
                self.spikes.draw(self.screen)
                if self.geo[0].colli_Check(self.spikes):
                    game_ing = False
                    game_over = True
                pygame.display.update()
                self.clock.tick(FPS)
                
            else: # game start check
                if (self.layers[0].get_key() and self.layers[0].usermode == True) or self.layers[0].usermode == False:
                    game_ing = True # game start
                    self.screen.fill(BLACK) # background set
        # game over : out of game loop
        self.screen.blit(gameover_image, (width/2-gameover_image.get_rect().width/2,height/2-gameover_image.get_rect().height/2))
        pygame.display.update()

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
            # intro에 필요한 이미지 구성
            self.start_image, self.start_image_rect = load_image(FileName.background.value, FileSize.background.value[0], FileSize.background.value[1], -1)# sysfont.render("Press any key to Start...", True, (255,255,255))   
            self.screen.blit(self.start_image, (0, 0))
            self.intro_image, self.intro_image_rect = load_image(FileName.title.value, FileSize.title.value[0], FileSize.title.value[1], -1)
            self.screen.blit(self.intro_image, (width * 0.05, height * 0.1))
            self.start_txt_image, self.start_txt_rect = load_image(FileName.start_txt.value, FileSize.start_txt.value[0], FileSize.start_txt.value[1], -1)
            self.screen.blit(self.start_txt_image, (width * 0.3, height * 0.7))
            pygame.display.update()
                        # 아무 키나 누르면 스테이지 생성하고 geo 출력해서 게임 시작
            self.clock.tick(FPS)
            
        return True

    def start(self):
        is_start = self.intro(True)
        if is_start:
            self.playgame()

            
# ====================================================
g= Game()
g.start()







