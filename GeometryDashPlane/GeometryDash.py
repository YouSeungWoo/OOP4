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
        
        self.generation = None
        self.population = 0
        self.ai_input_len = 6
        
        self.high_score = 0
        
        self.current_score = 0
        self.gamespeed = x_speed
        self.bgcolor = BLACK
        
        self.geo = []
        self.genomes = []
        self.layers = []
        
        self.mode = True
    
        self.screen = pygame.display.set_mode(scr_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Geometry Dash: Plain')

        self.maploader = MapLoader(self.screen)
    
    def calc_ai_input(self, obs):
        # calc inputs for ai
        ret = []
        obstacles = []
        if len(obs) > 0:
            for i in range(self.ai_input_len):
                temp = []
                obs.sort(key = lambda x: x.rect.centerx, reverse = False)
                temp.append(obs[0])
                obs = obs[1:]
                for o in obs:
                    if(temp[0].rect.centerx == o.rect.centerx):
                        temp.append(o)
                    else: break
                obstacles.append(temp)
            for obs in obstacles:
                obs.sort(key = lambda x: x.rect.centery, reverse=False)
                ttemp = [0]
                ttemp1 = []
                ttemp2 = []
                for o in obs:
                    ttemp.append(o.rect.centery)
                ttemp.append(height)
                for i in range(len(ttemp)-1):
                    ttemp2.append(ttemp[i]-ttemp[i+1])
                    ttemp1.append((ttemp[i]+ttemp[i+1])/2)
                min_ = min(ttemp2)
                for i in range(len(ttemp2)):
                    if(min_ == ttemp2[i]):
                        break
                ret.append(ttemp1[i])
        ret = ret[0:self.ai_input_len]
        for i in range(self.ai_input_len-len(ret)):
                ret.append(0)
        for j in range(self.ai_input_len):
            ret[j] = (ret[j]-height*0.5)/(0.5*height)
        
        return ret
    
    def playgame(self):
        # setup initial condition
        game_over = False # gameover flag
        game_ing = True # game palying flag
        
        # setup images and fonts
        sysfont = pygame.font.SysFont(None, 25) # 출력할 문장의 폰트
        gameover_image = sysfont.render("Game Over...", True, BLACK)
        score_image = sysfont.render("High score : {}     score : {}".format(int(self.high_score), int(self.current_score)), True, WHITE) # color changed
        if not self.mode:
            gen_image = sysfont.render("Gen : {}   Survivors :  {}".format(self.n_gen, self.survivors), True, WHITE)

        # setup sprites
        self.bricks = pygame.sprite.Group()
        Brick.containers = self.bricks
        self.spikes = pygame.sprite.Group()
        Spike.containers = self.spikes
        obstacles = []
        obs = []
      
        # initial image draw
        self.screen.fill(self.bgcolor) # default background color setup
        self.screen.blit(score_image, (width * 0.8, 0)) # 점수판 출력
        if not self.mode:
            self.screen.blit(gen_image, (width * 0.8, 25))
        self.screen.blit(self.geo[-1].image, self.geo[-1].rect.topleft)
        pygame.display.update()
        if not self.mode:
            input_ai = [0 for _ in range(self.ai_input_len)]
        
        # game loop
        while not game_over:
            self.bgcolor = BLACK
            
            for idx, ly in enumerate(self.layers): # input check
                if not self.mode:
                    inputs = [(self.geo[idx].rect.centery-height*0.5)/(0.5*height), self.geo[idx].rad*4 / np.pi]
                    inputs.extend(input_ai)
                    if not ly.usermode:
                        ly.ai.forward(inputs)
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
                if not self.mode:
                    spikes_all = self.spikes.sprites()
                    for s in spikes_all:
                        if s.rect.centerx > width * 0.3:
                            obs.append(s)
                    input_ai = self.calc_ai_input(obs)
                
                self.current_score += 0.15
                score_image = sysfont.render("High score : {}   score : {}".format(int(self.high_score), int(self.current_score)), True, WHITE)
                gen_image = sysfont.render("Gen : {}   Survivors :  {}".format(self.n_gen, self.survivors), True, WHITE)
                self.bricks.update()
                self.spikes.update()
                self.spikes.draw(self.screen)
                self.bricks.draw(self.screen)
                for idx, geo in enumerate(self.geo): # 모든 geo에 대해서 입력 처리 및 그리기 작업 수행
                    if not geo.isDead:
                        self.screen.blit(geo.image, geo.move(self.layers[idx], self.gamespeed)) # self.geo.move(key, gamespeed)를 이용해서 geo를 이동시키고 그것을 출력
                        if not self.layers[idx].usermode:
                            self.layers[idx].ai.fitness += 1
                for idx, geo in enumerate(self.geo):
                    if not geo.isDead:
                        if geo.colli_Check(self.spikes):
                            geo.isDead = True
                            self.survivors -= 1
                self.screen.blit(score_image, (width * 0.8, 0)) # 점수판 출력
                self.screen.blit(gen_image, (width * 0.8, 25))
                pygame.display.update()
                self.clock.tick(FPS)
                if self.survivors == 0:
                    game_over = True
                    break
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
        
        self.gen_geo() # reset geos
        
        self.survivors = len(self.geo)
        if not self.mode:
            self.generation.keep_best_genomes()
            for g in self.genomes:
                g.fitness = 0
            self.generation.mutations()
            
    def intro(self, user_mode):
        game_start = False
        sysfont = pygame.font.SysFont(None,30)
        mod2 = 1

        while not game_start:
            self.screen.fill(BLACK)
            self.print_intro() # 12/03 추가. AI 모드를 위해 위치 조정
            if mod2 % 2:
                self.screen.blit(self.CSED232, (width * 0.03, height * 0.85))
                self.CSED232_rect.topleft = (width * 0.03, height * 0.85)
            else:
                 self.screen.blit(self.CSED442, (width * 0.03, height * 0.85))
                 self.CSED442_rect.topleft = (width * 0.03, height * 0.85)

            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                return True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        self.mode = True # 12/03 추가. AI 모드 인덱스
                        game_start = True
                    elif event.type == pygame.MOUSEBUTTONDOWN: # 12/03 추가. AI 모드 마우스 클릭으로 실행
                        print("hi")
                        x, y = event.pos
                        mod2 += 1
                        if self.team_image_rect.collidepoint(x, y):
                            self.mode = False
                            game_start = True

            pygame.display.update()
                        # 아무 키나 누르면 스테이지 생성하고 geo 출력해서 게임 시작
            self.clock.tick(FPS)
            
        return True

    # course_image 추가
    def print_intro(self):
        self.start_image, self.start_image_rect = load_image(FileName.background.value, FileSize.background.value[0], FileSize.background.value[1], -1) # sysfont.render("Press any key to Start...", True, (255,255,255))   
        self.screen.blit(self.start_image, (0, 0))
        self.intro_image, self.intro_image_rect = load_image(FileName.title.value, FileSize.title.value[0], FileSize.title.value[1], -1)
        self.screen.blit(self.intro_image, (width * 0.05, height * 0.1))
        self.start_txt_image, self.start_txt_rect = load_image(FileName.start_txt.value, FileSize.start_txt.value[0], FileSize.start_txt.value[1], -1)
        self.screen.blit(self.start_txt_image, (width * 0.3, height * 0.7))
        self.team_image, self.team_image_rect = load_image(FileName.team_name.value, FileSize.team_name.value[0], FileSize.team_name.value[1], -1)
        self.screen.blit(self.team_image, (width * 0.88, height * 0.85))
        self.team_image_rect.topleft = (width * 0.88, height * 0.85) # 12/03 추가. AI 모드 마우스 클릭으로 실행을 위해 rect 위치 조정
        self.CSED232, self.CSED232_rect = load_image(FileName.course.value[0], FileSize.course.value[0], FileSize.course.value[1], -1)
        self.CSED442, self.CSED442_rect = load_image(FileName.course.value[1], FileSize.course.value[0], FileSize.course.value[1], -1)
    
    def gen_geo(self):
        del self.geo
        self.geo = []
        if not self.mode:
            for i in range(self.population):
                self.geo.append(Geo(FileSize.geo.value[0], FileSize.geo.value[1], self.screen)) # geo 생성
        else :self.geo.append(Geo(FileSize.geo.value[0], FileSize.geo.value[1], self.screen))
    
    def start(self):
        is_start = self.intro(True)
        self.n_gen = 1
        self.survivors = 0
        self.geo = []
        if not self.mode:
            self.generation = Generation(10, 2, 4, 0.1)
            self.population = self.generation.population
            self.genomes, self.layers = self.generation.set_initial_genomes(self.ai_input_len + 2)
            
        else: 
            self.layers.append(input_layer(True))
            
        self.gen_geo()
        self.survivors = len(self.geo)
        
        assert len(self.geo) == len(self.layers)
        
        if is_start:
            while True:
                self.playgame()
# ====================================================
g= Game()
g.start()
