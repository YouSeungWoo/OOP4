# 게임 전체에 이용되는 변수나 기타 게임 관리에 필요한 함수를 담당하는 파일

import enum, os, pygame, sys

FPS = 120
scr_size = (width, height) = (1260, 600) # 11/24 수정. 화면 사이즈 조정
gravity = 0.3
x_speed = 8 # 11/24 수정. 게임 속도 적당히 맞게 조정

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
background_color = (255, 255, 255)
geo_pos = width / 15

class FileName(enum.Enum):
    sprites = 'image'               # 이미지 파일이 들어있는 폴더 경로
    title = 'title.png'             # 이미지 파일 이름들
    start_txt = 'key_text.png'
    geo = 'character.png'
    spike = ['large_white_spike.png', 'half_white_spike.png', 'small_white_spike.png', '3_spikes_M.png', '3_spikes_L.png', '2_spikes.png', '2_spikes2.png'] # 11/24 수정. 파일 이름 잘못 되어 있어 수정
    brick = ['Brick.png', 'Tile.png', 'empty_block.png', 'BeamBlock.png', 'GridBlock.png', 'CrossBlock.png', 'PatternBlock.png', ] # 11/24 수정. 파일 추가
    background = 'background_main.png'
    map_sprites = 'map'
    mapfiles = ['map1.txt', 'map2.txt', 'map3.txt', 'A.txt', 'I.txt', 'map4.txt', 'map5.txt', 'hmap1.txt'] # 11/24 수정. 파일 추가
    sawblade = ['SpikedBulbSawblade.png']
    team_name = 'team_name.png'

class FileSize(enum.Enum):
    title = (1155, 155)
    start_txt = (498, 67)
    geo = (172, 110)
    background = (width, height)
    spike = [(60, 60), (60, 60), (60, 60), (60, 60), (60, 60), (60, 60), (60, 60)] # 11/24 수정. 모든 가시 사이즈를 (60, 60)으로 고정
    brick = [(60, 60), (60, 60), (60, 60), (60, 60), (60, 60), (60, 60), (60, 60)] # 11/24 수정. 모든 블럭 사이즈를 (60, 60)으로 고정
    sawblade = [(60, 60)]
    team_name = (120, 71)

def load_image(name, size_x = -1, size_y = -1, colorkey = None):
    fullname = os.path.join(FileName.sprites.value, name)      # sprites와 name을 결합시켜 fullname에 저장
    image = pygame.image.load(fullname)           # fullname을 load해 image에 저장

    image.convert()                       # 그냥 해줘야 한다고 함
    if colorkey is not None:                      # colorkey: 투명하게 처리할 색
        if colorkey is -1:                          # colorkey = -1이면
            colorkey = image.get_at((0, 0))           # image의 (0, 0)에 있는 색을 가져와서
    image.set_colorkey(colorkey, pygame.RLEACCEL) # image의 해당 색을 전부 투명하게 처리
    
    if size_x != -1 or size_y != -1:
        image = pygame.transform.scale(image, (size_x, size_y))   # image size 변경
    
    return (image, image.get_rect())