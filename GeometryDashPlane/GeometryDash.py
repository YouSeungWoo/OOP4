# 실제 게임을 진행하는 파일

import pygame
from generation import Generation
from manage import *
from object import Geo
import numpy as np
import random, copy, os, sys
from pygame.locals import QUIT, Rect, KEYDOWN, KEYUP, K_SPACE, K_LEFT # 입력받을 키(spacebar), spacebar가 아닌 다른 키(일단 임의로 left key로 정함)


class Game():
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(5,5) # 누르고 있을 것을 대비
        
        self.high_score = 0
        self.n_gen = 0
        self.current_score = 0

    

        self.gamespeed=x_speed
        self.screen = pygame.display.set_mode(scr_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Geometry Dash: Plain')
        self.geo = Geo(FileSize.geo.value[0], FileSize.geo.value[1], self.screen) # 50 50 크기의 Geo 생성
        # 유전정보 생성하기


    def playgame(self):
        game_over = False
        sysfont=pygame.font.SysFont(None, 25) # 출력할 문장의 폰트
        
        self.key=K_LEFT
        while not game_over:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT: # 종료 버튼을 누르면 끝내기
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN: # key가 눌리면
                    self.key = event.key # 입력받는 key를 self.key에 넣어 준다
                elif event.type == KEYUP:
                    self.key = K_LEFT # 스페이스바가 아닌 키를 넣어 줘야 하는데 어떻게 할지 몰라서 일단 이렇게 넣어 줬습니다.
            
            if not game_over:
                self.current_score += 0.15
                score_image = sysfont.render("High score : {}     score : {}".format(int(self.high_score),int(self.current_score)),True,(0,0,0))
                self.screen.blit(score_image, (650,10)) # 점수판 출력
                self.screen.blit(self.geo.geo_image,self.geo.move(self.key,self.gamespeed)) # self.geo.move(key, gamespeed)를 이용해서 geo를 이동시키고 그것을 출력
                pygame.display.update()
                self.clock.tick(FPS)

    def intro(self, user_mode):
        game_start = False
        sysfont=pygame.font.SysFont(None,30)

     #   title, title_rect = load_image(FileName.title, -1)
        # title 위치 설정 추가하기

     #   text, text_rect = load_image(FileName.title_text, -1)
        # text 위치 설정 추가하기

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
#                        self.screen.blit(BackgroundImage.stage1, 0, 0)

            intro_image, intro_image_rect=load_image(FileName.title.value, FileSize.title.value[0], FileSize.title.value[1])
            self.screen.blit(intro_image, (0,0))
            start_image, start_image_rect = load_image(FileName.background.value, FileSize.background.value[0], FileSize.background.value[1])# sysfont.render("Press any key to Start...", True, (255,255,255))   
            self.screen.blit(start_image, (3,127))

            pygame.display.update()
                        # 아무 키나 누르면 스테이지 생성하고 geo 출력해서 게임 시작
            self.clock.tick(FPS)
            
        return True

    def start(self):
        is_start=self.intro(0)
        if is_start:
            self.playgame()
        
            
g= Game()
g.start()