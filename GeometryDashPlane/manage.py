# 게임 전체에 이용되는 변수나 기타 게임 관리에 필요한 함수를 담당하는 파일

import enum, os, pygame, sys
from collision import *

FPS = 120
scr_size = (width, height) = (1280, 600)
gravity = 0.2
x_speed = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
background_color = (255, 255, 255)
geo_pos = width / 15

class FileName(enum.Enum):
    sprites = 'image'               # 이미지 파일이 들어있는 폴더 경로
    title = 'title.png'             # 이미지 파일 이름들
    start_txt = 'key_text.png'
    geo = 'character.png'
    thorn = ''
    background = 'background_main.png'

class FileSize(enum.Enum):
    title = (1155, 155)
    start_txt = (498, 67)
    geo = (90, 58)
    background = (width, height)

class Hitbox(enum.Enum):
    v = Vector
    geo = Concave_Poly(v(width * 0.3, height * 0.7), \
            [v(-25, -17), v(-25, -15), v(-23, -13), v(-23, -12), v(-18, -7), v(-18, -5), v(-22, -5), v(-23, -4), v(-24, -4), v(-25, -3), \
           v(-23, 1), v(-24, 2), v(-24, 5), v(-23, 6), v(-21, 6), v(-21, 8), v(-22, 9), v(-22, 10), v(-20, 12), \
          v(0,0), v(0, 330), v(0, 0)])

class BackgroundImage(enum.Enum):
    stage1 = None;


def load_image(name, size_x = -1, size_y = -1, colorkey = None):
    fullname = os.path.join('image', name)      # sprites와 name을 결합시켜 fullname에 저장
    image = pygame.image.load(fullname)           # fullname을 load해 image에 저장

    image.convert()                       # 그냥 해줘야 한다고 함
    if colorkey is not None:                      # colorkey: 투명하게 처리할 색
        if colorkey is -1:                          # colorkey = -1이면
            colorkey = image.get_at((0, 0))           # image의 (0, 0)에 있는 색을 가져와서
    image.set_colorkey(colorkey, pygame.RLEACCEL) # image의 해당 색을 전부 투명하게 처리
    
    if size_x != -1 or size_y != -1:
        image = pygame.transform.scale(image, (size_x, size_y))   # image size 변경
    
    return (image, image.get_rect())
