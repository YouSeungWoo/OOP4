import pygame

from network import Network     # network 클래스

class input_layer:
    usermode = True # usermode
    ai = None
    def __init__(self, usmode = True):
        self.usermode = usmode
        self.ai = None
    
    def set_ai(self, ai):
        self.ai = ai
    
    def get_input(self):
        if self.usermode == True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return True
            return False
        else:
            assert self.ai != None
            return self.ai.get_decision()
    
