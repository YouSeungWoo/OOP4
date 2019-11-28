# 실제 게임을 진행하는 파일

import pygame
from generation import Generation
from manage import *
from object import Geo, Spike, Brick
import numpy as np
import random, copy, os, sys
from input_layer import input_layer
from pygame.locals import QUIT, Rect, KEYDOWN, KEYUP, K_SPACE, K_LEFT # 입력받을 키(spacebar), spacebar가 아닌 다른 키(일단 임의로 left key로 정함)
from maploader import MapLoader

class Game():
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(5,5) # 누르고 있을 것을 대비
        
        self.generation = Generation()
        self.population = self.generation.population
        self.survivors = 0
        
        self.high_score = 0
        self.n_gen = 0
        self.current_score = 0
        self.gamespeed = x_speed
        self.bgcolor = WHITE
        
        self.geo = []
        self.genomes = []
        self.layers = []
        self.genomes, self.layers = self.generation.set_initial_genomes()
        self.layers.append(input_layer(True))
    
        self.screen = pygame.display.set_mode(scr_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Geometry Dash: Plain')

        self.maploader = MapLoader(self.screen)

        # 유전정보 생성하기
        for i in range(self.population):
            self.geo.append(Geo(FileSize.geo.value[0], FileSize.geo.value[1], self.screen)) # geo 생성
        self.geo.append(Geo(FileSize.geo.value[0], FileSize.geo.value[1], self.screen))
        
        self.survivors = len(self.geo)
        
        assert len(self.geo) == len(self.layers)

    def playgame(self):
        # setup initial condition
        game_over = False # gameover flag
        game_ing = False # game palying flag
        
        # setup images and fonts
        sysfont = pygame.font.SysFont(None, 25) # 출력할 문장의 폰트
        gameover_image = sysfont.render("Game Over...", True, BLACK)
        score_image = sysfont.render("High score : {}     score : {}".format(int(self.high_score), int(self.current_score)), True, WHITE) # color changed

        # setup sprites
        self.bricks = pygame.sprite.Group()
        Brick.containers = self.bricks
        self.spikes = pygame.sprite.Group()
        Spike.containers = self.spikes
      
        # initial image draw
        self.screen.fill(self.bgcolor) # default background color setup
        self.screen.blit(score_image, (width * 0.7, 0)) # 점수판 출력
        self.screen.blit(self.geo[0].image, self.geo[0].rect.topleft)
        pygame.display.update()

        # game loop
        while not game_over:
            for ly in self.layers: # input check
                ly.get_input() #  모든 레이어에 대해 입력 확인
                            
            if game_ing: # playing loop
                self.screen.fill(self.bgcolor) #draw background

                if self.maploader.check_scroll(self.gamespeed):
                    objs = self.maploader.get_obj()
                    for o in objs[0]:
                        self.bricks.add(o)
                    for o in objs[1]:
                        if o.is_collidable():
                            self.spikes.add(o)
           #     print("1")
                self.current_score += 0.15
                score_image = sysfont.render("High score : {}     score : {}".format(int(self.high_score), int(self.current_score)), True, WHITE)
                self.bricks.update()
                self.spikes.update()
                self.spikes.draw(self.screen)
                self.bricks.draw(self.screen)
           #     print("2")
                for idx, geo in enumerate(self.geo): # 모든 geo에 대해서 입력 처리 및 그리기 작업 수행
                    if not geo.isDead:
                        self.screen.blit(geo.image, geo.move(self.layers[idx], self.gamespeed)) # self.geo.move(key, gamespeed)를 이용해서 geo를 이동시키고 그것을 출력
         #           pygame.draw.rect(self.screen, WHITE, (geo.rect.left, geo.rect.top, geo.rect.width, geo.rect.height), 10)
          #      print("3")
                for geo in self.geo:
                    if not geo.isDead:
                        if geo.colli_Check(self.spikes):
                            geo.isDead = True
                            self.survivors -= 1
                self.screen.blit(score_image, (width * 0.7, 0)) # 점수판 출력
                pygame.display.update()
           #     print("4")
                self.clock.tick(FPS)
                print(self.survivors)
                if self.survivors == 0:
                    game_over = True
                    break
            else: # game start check
                if (self.layers[-1].get_key() and self.layers[-1].usermode == True) or self.layers[-1].usermode == False:
                    game_ing = True # game start
                    self.bgcolor = BLACK # background set
        # game over : out of game loop
        if self.current_score > self.high_score:
            self.high_score = self.current_score
        self.current_score = 0
        self.clock.tick(1)
        self.bgcolor = (255,0,0)
        self.screen.fill(self.bgcolor)
        self.screen.blit(gameover_image, (width/2-gameover_image.get_rect().width/2, height/2-gameover_image.get_rect().height/2))
        pygame.display.update()
        self.clock.tick(1)
        self.n_gen += 1
        
        self.geo = []
        
        for i in range(self.population):
            self.geo.append(Geo(FileSize.geo.value[0], FileSize.geo.value[1], self.screen)) # geo 생성
        self.geo.append(Geo(FileSize.geo.value[0], FileSize.geo.value[1], self.screen))
        self.survivors = len(self.geo)

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
            
            self.print_intro() # 11/25추가. 이미지 출력부 분리

            pygame.display.update()
                        # 아무 키나 누르면 스테이지 생성하고 geo 출력해서 게임 시작
            self.clock.tick(FPS)
            
        return True

    def print_intro(self):
        self.start_image, self.start_image_rect = load_image(FileName.background.value, FileSize.background.value[0], FileSize.background.value[1], -1) # sysfont.render("Press any key to Start...", True, (255,255,255))   
        self.screen.blit(self.start_image, (0, 0))
        self.intro_image, self.intro_image_rect = load_image(FileName.title.value, FileSize.title.value[0], FileSize.title.value[1], -1)
        self.screen.blit(self.intro_image, (width * 0.05, height * 0.1))
        self.start_txt_image, self.start_txt_rect = load_image(FileName.start_txt.value, FileSize.start_txt.value[0], FileSize.start_txt.value[1], -1)
        self.screen.blit(self.start_txt_image, (width * 0.3, height * 0.7))
        self.team_image, self.team_image_rect = load_image(FileName.team_name.value, FileSize.team_name.value[0], FileSize.team_name.value[1], -1)
        self.screen.blit(self.team_image, (width * 0.88, height * 0.85))

    def start(self):
        is_start = self.intro(True)
        if is_start:
            while True:
                self.playgame()

            
# ====================================================
g= Game()
g.start()
