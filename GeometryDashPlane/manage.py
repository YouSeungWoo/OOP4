# 게임 전체에 이용되는 변수나 기타 게임 관리에 필요한 함수를 담당하는 파일

import enum, os, pygame, sys

FPS = 120
scr_size = (width, height) = (1260, 600)
gravity = 0.3
x_speed = 8
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
background_color = (255, 255, 255)
geo_pos = width / 15

class FileName(enum.Enum):
    sprites = ['image', 'map', 'music']
    title = 'title.png'
    geo = 'character.png'
    course = ['csed232.png', 'csed442.png']
    spike = ['large_white_spike.png', 'half_white_spike.png', 'small_white_spike.png', '3_spikes_M.png', '3_spikes_L.png', '2_spikes.png', '2_spikes2.png']
    brick = ['Brick.png', 'Tile.png', 'empty_block.png', 'BeamBlock.png', 'GridBlock.png', 'CrossBlock.png', 'PatternBlock.png']
    background = 'background_main.png'
    play = 'play_button.png'
    mapfiles = ['map1.txt', 'map2.txt', 'map3.txt', 'A.txt', 'I.txt', 'map4.txt', 'map5.txt', 'map6.txt', 'hmap1.txt'] # 'empty.txt'
    team_name = 'team_name.png'
    BGM_title = 'main.mp3'
    BGM_map = ['1.mp3', '2.mp3', '3.mp3']
    jupiter = 'jupiter.png'
    party = 'party.png'
    X2 = 'x2.png'

class FileSize(enum.Enum):
    title = (1155, 155)
    geo = (172, 110)
    background = (width, height)
    spike = [(60, 60), (60, 60), (60, 60), (60, 60), (60, 60), (60, 60), (60, 60)]
    brick = [(60, 60), (60, 60), (60, 60), (60, 60), (60, 60), (60, 60), (60, 60)]
    play = (240, 240)
    course = (120,71)
    team_name = (120, 71)
    jupiter = (40, 40)
    X2 = (65, 50)
    party = (120, 65)

def load_image(name, size_x = -1, size_y = -1, colorkey = None):
    fullname = os.path.join(FileName.sprites.value[0], name)
    image = pygame.image.load(fullname)
    image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))

    image.set_colorkey(colorkey, pygame.RLEACCEL)
    
    if size_x != -1 or size_y != -1:
        image = pygame.transform.scale(image, (size_x, size_y))
    
    return (image, image.get_rect())