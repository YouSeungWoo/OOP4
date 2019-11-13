import os
import sys
import pygame
import random
from objects import *                 # objects.py의 모든 내용 추가 
from helpers import *                 # helpers.py의 모든 내용 추가
from generation import Generation     # geteration.py의 Generation 클래스 추가
import numpy as np
import copy
import matplotlib.pyplot as plt

class Game():
  def __init__(self):
    pygame.init()                       # pygame 초기화

    self.generation = Generation()      # 유전정보 생성(유전 수, 개체 수, 최고 개체 수, ??lucky_few??, 돌연변이 확률 설정)
                                        # generation이라는 객체 생성, Generation()의 __init__()에서 초기화

    self.population = self.generation.population     # 변수 population 생성 후 객체 generation의 개체 수 정보를 받아옴

    self.gamespeed = 4             # 속도
    self.max_gamespeed = 10        # 최고 속도
    self.high_score = 0            # 최고 점수
    self.n_gen = 0                 # 세대 수
    self.current_gen_score = 0     # 현재 세대 점수

    self.dinos = None              # 변수 dino 생성
    self.genomes = []              # 배열 genomes 생성

    self.screen = pygame.display.set_mode(scr_size)       # helpers.py의 변수 scr_size 값을 이용해 게임 해상도 설정
    self.clock = pygame.time.Clock()                      # 초당 프레임 출력 설정을 위해 clock 변수 설정
    pygame.display.set_caption('Genetic T-Rex Rush')      # 게임 제목 설정

    self.jump_sound = pygame.mixer.Sound('sprites/jump.wav')                # 점프 소리 설정
    self.die_sound = pygame.mixer.Sound('sprites/die.wav')                  # 죽을 때 소리 설정
    self.checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')    # 체크포인트 소리 설정
    
    # 데이터를 차트로 표시하기 위한 구문
    self.scores = []
    self.fig = plt.figure(figsize=(int(width/100), 5))
    self.ax = plt.axes()
    plt.xlabel('Generation', fontsize=18)
    plt.ylabel('Score', fontsize=16)
    plt.show(block=False)
    # 함수 

  def introscreen(self):
    Dino.containers = []                                # ??
    temp_dino = Dino(44, 47, self.screen)               # temp_dino 객체 생성
    temp_dino.isBlinking = True                         # isBlinking을 True로 변경
    gameStart = False                                   # gameStart를 False로 변경
    
    # 여기서부터는 각 오브젝트의 이미지를 불러와서 저장하고 사각형 범위 설정
    callout,callout_rect = load_image('call_out2.png',196,62,-1)      # load_image 반환 값 2개를 각각 저장
    callout_rect.left = width*0.05        # image 왼쪽의 기준은 너비 * 0.05 (screen에 보이는 image의 위치)
    callout_rect.top = height*0.3         # image 위쪽의 기준은 높이 * 0.3 

    temp_ground,temp_ground_rect = load_sprite_sheet('ground.png',15,1,-1,-1,-1)
    temp_ground_rect.left = width/20
    temp_ground_rect.bottom = height

    logo,logo_rect = load_image('logo.png',240,40,-1)
    logo_rect.centerx = width*0.6
    logo_rect.centery = height*0.6
    logo2,logo2_rect = load_image('genetic_icon.png',80,80,-1)
    logo2 = logo2.convert_alpha()
    logo2_rect.centerx = width*0.45
    logo2_rect.centery = height*0.45        # 여기까지

    while not gameStart:
      if pygame.display.get_surface() == None:        # 게임 실행 정보 창 호출 실패 시 게임 종료
        print("Couldn't load display surface")
        return True
      else:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:               # 종료 이벤트 발생 시 종료
            return True
          if event.type == pygame.KEYDOWN:            # 키보드 누를 때
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP: # 스페이스바 또는 위쪽 방향키 눌렀을 때
              temp_dino.isJumping = True              # 공룡은 점프
              temp_dino.isBlinking = False            # ?? 어떤 상태일까
              temp_dino.movement[1] = -temp_dino.jumpSpeed    # ??

      temp_dino.update()        # 공룡 상태 업데이트
      
      # 여기서부터 게임 시작 화면 출력
      if pygame.display.get_surface() != None:            # 게임 실행 창 불러왔으면
        self.screen.fill(background_col)                  # 화면 색 채우기
        self.screen.blit(temp_ground[0],temp_ground_rect) # temp_ground[0]의 객체를 좌표(rect)에 맞게 screen 위에 복사
        if temp_dino.isBlinking:
          self.screen.blit(logo2,logo2_rect)
          self.screen.blit(logo,logo_rect)
          self.screen.blit(callout,callout_rect)    # 여기까지
        temp_dino.draw()                            # 공룡 그려주는 함수(object.h)

        pygame.display.update()                     # 화면 업데이트

      self.clock.tick(FPS)                          # 화면 전환 설정
      if temp_dino.isJumping == False and temp_dino.isBlinking == False:
        gameStart = True  # 게임 시작 True

  def prepare(self): 
    self.counter = 0
    self.gamespeed = 4
    self.current_gen_score = 0

    # load sprites
    self.new_ground = Ground(-self.gamespeed, self.screen)
    self.scb = Scoreboard(screen=self.screen)
    self.highsc = Scoreboard(width - 180, screen=self.screen)
    self.sursc = Scoreboard(width - 300, screen=self.screen)
    self.gensc = Scoreboard(width - 400, screen=self.screen)

    basicfont = pygame.font.SysFont('Menlo', 15)
    self.gen_text = basicfont.render('GEN', True, (0, 0, 0), background_col)
    self.textrect = self.gen_text.get_rect()
    self.textrect.top = height * 0.095
    self.textrect.left = width - 435

    temp_images,temp_rect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
    self.HI_image = pygame.Surface((22,int(11*6/5)))
    self.HI_rect = self.HI_image.get_rect()
    self.HI_image.fill(background_col)
    self.HI_image.blit(temp_images[10],temp_rect)
    temp_rect.left += temp_rect.width
    self.HI_image.blit(temp_images[11],temp_rect)
    self.HI_rect.top = height*0.1
    self.HI_rect.left = width - 210

    temp_gen_image, self.gen_rect = load_sprite_sheet('dino.png',5,1,15,16,-1)
    self.gen_image = pygame.Surface((15, 16))
    self.gen_image.fill(background_col)
    self.gen_image.blit(temp_gen_image[0], self.gen_rect)
    self.gen_rect.top = height*0.08
    self.gen_rect.left = width - 320

    self.dinos = pygame.sprite.Group()
    Dino.containers = self.dinos
    for i in range(self.population):
      self.dinos.add(Dino(44,47, self.screen))
    if self.n_gen == 0:
      self.genomes = self.generation.set_initial_genomes()

    self.cacti = pygame.sprite.Group()
    self.pteras = pygame.sprite.Group()
    self.clouds = pygame.sprite.Group()
    self.last_obstacle = pygame.sprite.Group()
    self.all_obstacles = pygame.sprite.Group()

    Cactus.containers = self.cacti
    Ptera.containers = self.pteras
    Cloud.containers = self.clouds

  def update(self):
    # move self.cacti
    for c in self.cacti:
      c.movement[0] = -self.gamespeed # movement (xspeed, yspeed)
      for d in self.dinos:
        if pygame.sprite.collide_mask(d, c): # mask(히트박스) 가 선인장과 디노가 겹치면
          d.isDead = True # 죽음

    # move self.pteras
    for p in self.pteras: # 마찬가지
      p.movement[0] = -self.gamespeed
      for d in self.dinos:
        if pygame.sprite.collide_mask(d, p):
          d.isDead = True

    # add more self.cacti
    if len(self.all_obstacles) == 0: # 장애물 없을 때
      new_object = Ptera(self.gamespeed, 46, 40, self.screen) # 46 x 40 크기의 Ptera 생성

      self.all_obstacles.add(new_object) # 추가
      self.last_obstacle.empty() # 비우기
      self.last_obstacle.add(new_object) # 추가
    elif len(self.all_obstacles) < 3: # 2개밖에 없다면
      for l in self.last_obstacle:
        if l.rect.right < width * 0.7: # 만든지 얼마 안 된 장애물이 아닐 경우
          r = random.randrange(0, 100) # 확률, 선인장과 까마귀 랜덤생성
          if r < 40:
            new_object = Cactus(self.gamespeed,40, 40, self.screen)
          elif r >= 40:
            new_object = Ptera(self.gamespeed, 46, 40, self.screen)

          self.all_obstacles.add(new_object)
          self.last_obstacle.empty()
          self.last_obstacle.add(new_object)

          break

    # add cloud
    if len(self.clouds) < 10 and random.randrange(0,100) == 10:
      Cloud(width,random.randrange(height/5,height/2), self.screen)

    # update motions
    self.dinos.update()
    self.cacti.update()
    self.pteras.update()
    self.clouds.update()
    self.new_ground.update()
    self.scb.update(self.current_gen_score)
    self.highsc.update(self.high_score)
    self.gensc.update(self.n_gen)
    self.sursc.update(self.n_survivors)

    # draw background
    if pygame.display.get_surface() != None:
      self.screen.fill(background_col) # bgcolor 로 배경 채우기
      self.new_ground.draw()
      self.clouds.draw(self.screen)
      self.scb.draw()
      self.highsc.draw()
      self.screen.blit(self.HI_image,self.HI_rect)
      self.gensc.draw()
      self.screen.blit(self.gen_image, self.gen_rect)
      self.screen.blit(self.gen_text, self.textrect)
      self.sursc.draw()
      self.cacti.draw(self.screen)
      self.pteras.draw(self.screen)
      self.dinos.draw(self.screen)

      pygame.display.update() # 업데이트

    self.clock.tick(FPS)

    # make faster
    if self.counter % 70 == 69 and self.gamespeed < 10:
      self.new_ground.speed -= 0.05
      self.gamespeed += 0.05

    self.counter = (self.counter + 1)

  def gameplay(self):
    game_over = False

    self.prepare() # 준비

    print('===== %sth Generation =====' % self.n_gen)

    # game loop
    while not game_over:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()

      # compute closest obstacle's distance
      first_obstacle = None
      obs_distance, obs_top, obs_bottom = width, 0, 0
      dino_rect_right = dino_position + 40
      for obs in self.all_obstacles:
        this_obs_distance = obs.rect.left - dino_position

        if this_obs_distance > 0 and this_obs_distance < obs_distance:
          obs_distance = this_obs_distance
          obs_top = obs.rect.top
          obs_bottom = obs.rect.bottom
          first_obstacle = obs

      # who are survived
      self.n_survivors = 0
      for di, dino in enumerate(self.dinos):
        # compute fitness
        self.genomes[di].fitness = dino.score

        if dino.isDead:
          continue

        # count survivors
        self.n_survivors += 1

        # decide action
        inputs = np.array([
          obs_distance / width,
          obs_top / height
        ], dtype=np.float32)
        outputs = self.genomes[di].forward(inputs)[0]
        # print(inputs, outputs)

        # execute action
        if outputs < 0: # do nothing
          dino.isDucking = False
        elif outputs < 0.5: # duck
          if not dino.isJumping and not dino.isDead:
            dino.isDucking = True
        else: # jump
          if dino.rect.bottom == int(0.98*height):
            dino.isJumping = True
            dino.movement[1] = -dino.jumpSpeed

        self.current_gen_score = dino.score

      # no survivors, kill this session
      if self.n_survivors == 0:
        if self.current_gen_score > self.high_score:
          self.high_score = self.current_gen_score

        game_over = True

      if game_over:
        break

      self.update()
      # end of while not game_over:

    # game over
    # crossover and mutate
    self.generation.set_genomes(self.genomes)
    self.generation.keep_best_genomes()
    self.genomes = self.generation.mutations()

    self.scores.append(self.current_gen_score)
    self.ax.plot(np.array(list(range(self.n_gen + 1))), np.array(self.scores), color='#225b85')
    self.fig.canvas.draw()
    self.fig.canvas.flush_events()

    print('Score: %s' % self.current_gen_score)

    # run next generation
    self.n_gen += 1
    self.gameplay()

    pygame.quit()
    exit()

  def start(self):
    isGameQuit = self.introscreen()     # introscreen함수에서 게임 종료 여부 판단
    if not isGameQuit:
      self.gameplay()                   # 게임 종료상태가 아니면 게임 진행

g = Game()            # 객체 g 설정
g.start()             # 게임 시작
