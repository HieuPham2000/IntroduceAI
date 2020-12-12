import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.font.init()

FPS = 2
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
CELLSIZE = 50
assert WINDOWHEIGHT % CELLSIZE == 0, "Height phai la boi so cua Cell Size"
assert WINDOWWIDTH % CELLSIZE == 0, "Width phai la boi so cua Cell Size"

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# Mã màu
#			 R    G    B
WHITE    = (255, 255, 255)
BLACK    = (0,     0,   0)
RED      = (255,   0,   0)
GREEN    = (0,   255,   0)
BLUE     = (0,   0,   255)
DARKGREEN= (0,   155,   0)
DARKGRAY = (40,   40,  40)
YELLOW   = (255, 255,   0)
VIOLET   = (128,   0, 128)
# Thêm 1 số màu
RED2 	 = (224,  62,  30)
GREEN1   = (208, 240, 208)
GREEN2   = (60,   95,  74)  

BGCOLOR          = BLACK
TITLE_COLOR      = DARKGREEN
LINE_GRID_COLOR  = DARKGRAY
APPLE_COLOR      = RED2
HEAD_SNAKE_COLOR = GREEN1
SNAKE_COLOR      = GREEN2


# Phím điều khiển
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # Index đầu rắn

# Nhạc game
APPLEEATSOUND = pygame.mixer.Sound(r"sounds/appleEatSound.wav")
BGMUSIC = pygame.mixer.music.load(r"sounds/bgmusic.mid")

""" def levelSelect():
	global FPS
	if level == "EASY":
		FPS = 4
	elif level == "MEDIUM":
		FPS = 7
	elif level == "HARD":
		FPS = 10 """

list_food = []
list_food.append(pygame.image.load('./assets/frog.png'))
list_food.append(pygame.image.load('./assets/rat.png'))
list_food.append(pygame.image.load('./assets/bird.png'))
list_food.append(pygame.image.load('./assets/rabbit.png'))
list_food.append(pygame.image.load('./assets/rabbit2.png'))
list_food.append(pygame.image.load('./assets/a-plus.png'))
for i in range(len(list_food)):
	list_food[i] = pygame.transform.scale(list_food[i], (CELLSIZE, CELLSIZE))

LIST = list_food
