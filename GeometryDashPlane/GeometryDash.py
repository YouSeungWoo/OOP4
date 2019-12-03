# 실제 게임을 진행하는 파일
import pygame, random, copy, os, sys
from generation import Generation
from manage import *
from object import Geo, Spike, Brick
import numpy as np
from input_layer import input_layer
from pygame.locals import QUIT, Rect, KEYDOWN, KEYUP, K_SPACE, K_LEFT
from maploader import MapLoader

class Game():
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(5,5)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(FileName.sprites.value[2], FileName.BGM_title.value))
        
        # AI variable
        self.generation = None
        self.population = 0
        self.ai_input_len = 6
        
        # game variable
        self.high_score = 0
        self.current_score = 0
        self.gamespeed = x_speed
        self.bgcolor = BLACK
        self.mode = True
        
        # list
        self.geo = []
        self.genomes = []
        self.layers = []
        
        # setup etc.
        self.screen = pygame.display.set_mode(scr_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Geometry Dash: Plain')
        self.maploader = MapLoader(self.screen)

    def calc_ai_input(self, obs): # calc inputs for AI
        # setup initial condition
        ret = []
        obstacles = []
        obs_origin = obs

        if len(obs) > 0:
            for i in range(self.ai_input_len):
                temp = []
                obs.sort(key = lambda x: x.rect.centerx, reverse = False)
                temp.append(obs[0])
                obs = obs[1:]

                for o in obs:
                    if(temp[0].rect.centerx == o.rect.centerx):
                        temp.append(o)
                    else:
                        break

                obstacles.append(temp)
                obs = obs[len(temp) - 1:]

                if len(obs) <= 0:
                    break

            for obs in obstacles:
                obs.sort(key = lambda x: x.rect.centery, reverse = False)
                ttemp = [0]
                ttemp1 = []
                ttemp2 = []

                for o in obs:
                    ttemp.append(o.rect.centery)
                
                ttemp.append(height)

                for i in range(len(ttemp) - 1):
                    ttemp2.append(ttemp[i] - ttemp[i + 1])
                    ttemp1.append((ttemp[i] + ttemp[i + 1]) / 2)

                min_ = min(ttemp2)

                for i in range(len(ttemp2)):
                    if(min_ == ttemp2[i]):
                        break

                ret.append(ttemp1[i])

        ret = ret[0: self.ai_input_len]

        for i in range(self.ai_input_len - len(ret)):
                ret.append(0)
        for j in range(self.ai_input_len):
            ret[j] = (ret[j] - height * 0.5) / (0.5 * height)
        
        return ret

    def update(self):
        self.bricks.update()
        self.spikes.update()
        self.spikes.draw(self.screen)
        self.bricks.draw(self.screen)

    def playgame(self):
        # setup initial condition
        game_over = False # gameover flag
        game_ing = True # game palying flag
        
        # setup images and fonts
        sysfont = pygame.font.SysFont(None, 25)
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
        self.screen.blit(score_image, (width * 0.8, 0))

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
                    inputs = [(self.geo[idx].rect.centery - height * 0.5) / (0.5 * height), \
                                self.geo[idx].rad * 4 / np.pi]
                    inputs.extend(input_ai)

                    if not ly.usermode:
                        ly.ai.forward(inputs)

                ly.get_input() # checking all layers
            
            # playing loop
            if game_ing:
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
                self.update()
                
                # move & print all geo
                for idx, geo in enumerate(self.geo):
                    if not geo.isDead:
                        self.screen.blit(geo.image, geo.move(self.layers[idx], self.gamespeed)) # move & print

                        if not self.layers[idx].usermode:
                            self.layers[idx].ai.fitness += 1

                # check that is geo dead
                for idx, geo in enumerate(self.geo):
                    if not geo.isDead:
                        if geo.colli_Check(self.spikes):
                            geo.isDead = True
                            self.survivors -= 1

                self.screen.blit(score_image, (width * 0.8, 0)) # print score
                self.screen.blit(gen_image, (width * 0.8, 25))
                pygame.display.update()
                self.clock.tick(FPS)
                
                # check that is game end
                if self.survivors == 0:
                    game_over = True
                    break

        if self.current_score > self.high_score:
            self.high_score = self.current_score
        self.current_score = 0
        self.clock.tick(1)

        self.bgcolor = (255, 0, 0)
        self.screen.fill(self.bgcolor)
        self.screen.blit(gameover_image, (width / 2 - gameover_image.get_rect().width / 2, \
                                            height / 2 - gameover_image.get_rect().height / 2))
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
        # setup initial condition
        game_start = False
        sysfont = pygame.font.SysFont(None,30)
        mod2 = 1
        pygame.mixer.music.play()

        while not game_start:
            self.screen.fill(BLACK)
            self.print_intro()

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

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            print("hi")
                            x, y = event.pos

                            if self.play_image_rect.collidepoint(x, y):
                                self.mode = True
                                game_start = True
                            if self.team_image_rect.collidepoint(x, y):
                               self.mode = False
                               game_start = True
                            if self.CSED442_rect.collidepoint(x, y) or self.CSED232_rect.collidepoint(x, y):
                                mod2 += 1

            pygame.display.update()
            self.clock.tick(FPS)
        pygame.mixer.music.stop()

        return True

    def print_intro(self):
        self.start_image, self.start_image_rect = load_image(FileName.background.value, FileSize.background.value[0], FileSize.background.value[1], -1)
        self.screen.blit(self.start_image, (0, 0))

        self.intro_image, self.intro_image_rect = load_image(FileName.title.value, FileSize.title.value[0], FileSize.title.value[1], -1)
        self.screen.blit(self.intro_image, (width * 0.05, height * 0.1))

        self.play_image, self.play_image_rect = load_image(FileName.play.value, FileSize.play.value[0], FileSize.play.value[1], -1)
        self.screen.blit(self.play_image, (width * 0.41, height * 0.43))
        self.play_image_rect.topleft = (width * 0.41, height * 0.43)

        self.team_image, self.team_image_rect = load_image(FileName.team_name.value, FileSize.team_name.value[0], FileSize.team_name.value[1], -1)
        self.screen.blit(self.team_image, (width * 0.88, height * 0.85))
        self.team_image_rect.topleft = (width * 0.88, height * 0.85)

        self.CSED232, self.CSED232_rect = load_image(FileName.course.value[0], FileSize.course.value[0], FileSize.course.value[1], -1)
        self.CSED442, self.CSED442_rect = load_image(FileName.course.value[1], FileSize.course.value[0], FileSize.course.value[1], -1)
    
    def gen_geo(self):
        del self.geo
        self.geo = []

        if not self.mode:
            for i in range(self.population):
                self.geo.append(Geo(FileSize.geo.value[0], FileSize.geo.value[1], self.screen))
        else:
            self.geo.append(Geo(FileSize.geo.value[0], FileSize.geo.value[1], self.screen))
    
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
            pygame.mixer.music.load(os.path.join(FileName.sprites.value[2], FileName.BGM_map.value[random.randrange(0, len(FileName.BGM_map.value))]))
            pygame.mixer.music.play(-1)

            while True:
                self.playgame()

# ====================================================
g = Game()
g.start()
