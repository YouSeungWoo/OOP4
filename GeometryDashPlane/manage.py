# 게임 전체에 이용되는 변수나 기타 게임 관리에 필요한 함수를 담당하는 파일

import enum, os, pygame

FPS = 60
scr_size = (width, height) = (900, 150)
gravity = 0.6
x_speed = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
background_color = (255, 255, 255)
geo_pos = width / 15

class FileName(enum.Enum):
    title = ('', 0, 0)
    title_text = ('', 0, 0)
    geo = ('', 0, 0)
    background = ('', 0, 0)


class BackgroundImage(enum.Enum):
    stage1 = None;


def load_image(name, size_x = -1, size_y = -1, colorkey = None):
    fullname = os.path.join('sprites', name)      # sprites와 name을 결합시켜 fullname에 저장
    image = pygame.image.load(fullname)           # fullname을 load해 image에 저장
    
    image = image.convert()                       # 그냥 해줘야 한다고 함
    if colorkey is not None:                      # colorkey: 투명하게 처리할 색
        if colorkey is -1:                          # colorkey = -1이면
            colorkey = image.get_at((0, 0))           # image의 (0, 0)에 있는 색을 가져와서
    image.set_colorkey(colorkey, pygame.RLEACCEL) # image의 해당 색을 전부 투명하게 처리
    
    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))   # image size 변경
    
    return (image, image.get_rect())