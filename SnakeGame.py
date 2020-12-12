import random
import pygame
import sys
from pygame.locals import *
from settingsGame import *
from threading import Thread
from detection import play
import time

# biến global
snakeCoords = None
oldBestScore = None
bestScore = None
score = None
colorScore = None
CLOCK = None
SCREEN = None
FONT = None

background_image = pygame.image.load('./assets/background-start1.jpg')
background_image = pygame.transform.scale(background_image, (WINDOWWIDTH, WINDOWHEIGHT))

def main():
	global CLOCK, SCREEN, FONT
	
	pygame.init()
	CLOCK = pygame.time.Clock()
	SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	FONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption('Snake Game - Team 20')

	showStartScreen()

	while True:
		#pygame.mixer.music.play(-1, 0.0)
		runGame()
		#pygame.mixer.music.stop()
		showGameOverScreen()


def runGame():
	with open('bestscore.txt') as log:
		global bestScore, oldBestScore
		bestScore = int(log.read())
		oldBestScore = bestScore
		#print(bestScore)

	# Màu score in trên màn hinh
	#Lưu điểm
	global score, colorScore
	score = 0
	colorScore = WHITE
	# Khởi tạo vị trí ban đầu 
	startx = random.randint(3, CELLWIDTH - 3)
	starty = random.randint(3, CELLHEIGHT - 3)
	# Danh sách vị trí các khối tạo nên con rắn, khởi tạo với 3 khối
	global snakeCoords
	snakeCoords = [{'x' : startx, 'y' : starty}, {'x': startx - 1, 'y':starty},  {'x': startx - 2, 'y':starty}]
	direction = RIGHT
	# Random vị trí táo, hiện tai đang để 2 táo
	food = getRandomFood()
	food2 = getRandomFood()
	

	while True:
		
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				# K_LEFT là mũi tên sang trái, K_a là phím a
				# Nếu đang đi sang phải thì KHÔNG cho phép chuyển hướng sang trái
				if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
					direction = LEFT
					break
				elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
					direction = RIGHT
					break
				elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
					direction = UP
					break
				elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
					direction = DOWN
					break
				elif event.key == K_ESCAPE:
					#terminate()
					return
				elif event.key == KSCAN_Q or event.key == K_q:
					terminate()
			
		# Kiểm tra va chạm với thân rắn
		if snakeCoords[HEAD] in snakeCoords[1:]:
			drawSnakeDie(snakeCoords)
			drawGameOver(WINDOWWIDTH/2, 30, 100, WHITE)
			pygame.display.update()
			time.sleep(2)
			return
		# Kiểm tra khi chạm vào táo
		if snakeCoords[HEAD] == food[1]:
			time.sleep(0.1)
			APPLEEATSOUND.play()
			food = getRandomFood()
			drawFood(*food)
			score += 10
		# test 2 táo
		elif snakeCoords[HEAD] == food2[1]:
			time.sleep(0.1)
			APPLEEATSOUND.play()
			food2 = getRandomFood()
			drawFood(*food2)
			score += 10
		else:
			# Bỏ đi khối ở cuối thân rắn
			# Vì ngay bên dưới ta sẽ chèn khối mới vào đầu rắn => tạo sự di chuyển
			del snakeCoords[-1]

		# Di chuyển rắn
		if direction == UP:
			newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] - 1}
		elif direction == DOWN:
			newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] + 1}
		elif direction == RIGHT:
			newHead = {'x': snakeCoords[HEAD]['x'] + 1, 'y': snakeCoords[HEAD]['y']}
		elif direction == LEFT:
			newHead = {'x': snakeCoords[HEAD]['x'] - 1, 'y': snakeCoords[HEAD]['y']}
		# fix lỗi đi quá 1 bước khi đi qua cạnh
		if newHead['x'] == -1 or newHead['x'] == CELLWIDTH or newHead['y'] == -1 or newHead['y'] == CELLHEIGHT:
			# snakeCoords[HEAD]['x'] = -1 =>  cộng thêm CELLWIDTH = CELLWIDTH - 1 <=> (-1 + CELLWIDTH) % CELLWIDTH
			# snakeCoords[HEAD]['x'] = CELLWIDTH => trừ đi CELLWIDTH = 0 <=> (CELLWIDTH + CELLWIDTH) % CELLWIDTH
			# snakeCoords[HEAD]['x'] = x mà -1 < x < CELLWIDTH thì (x + CELLWIDTH) % CELLWIDTH vẫn = x
			x = (newHead['x'] + CELLWIDTH) % (CELLWIDTH)
			y = (newHead['y'] + CELLHEIGHT) % (CELLHEIGHT)
			newHead = {'x': x, 'y': y}
		snakeCoords.insert(0, newHead)

		# Vẽ màn hình
		if(score > bestScore):
			bestScore = score
		if(score == bestScore):
			colorScore = GREEN

		SCREEN.fill(BGCOLOR)
		drawGrid()
		

		drawFood(*food)
		drawFood(*food2)

		# draw Snake sau food để khi ăn food thì đầu rắn sẽ che food
		#debug khi đi xuyên tường
		#print(snakeCoords[HEAD])
		drawSnake(snakeCoords)
		drawScore(score, colorScore)
		drawBestScore(bestScore)
		pygame.display.update()
		CLOCK.tick(FPS)

def drawPressKeyMsg():
	pressKeyText = FONT.render('Press A Key To Play', True, YELLOW)
	pressKeyRect = pressKeyText.get_rect()
	pressKeyRect.center = (WINDOWWIDTH - 200, WINDOWHEIGHT - 100)
	SCREEN.blit(pressKeyText, pressKeyRect)

def drawGameOver(x, y, size, color):
	gameOverFont = pygame.font.Font('freesansbold.ttf', size)
	gameOverText = gameOverFont.render('Game Over', True, color)
	gameOverRect = gameOverText.get_rect()
	gameOverRect.midtop = (x, y)
	SCREEN.blit(gameOverText, gameOverRect)

def checkForKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		terminate()
	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None
	if keyUpEvents[0].key in (K_q, KSCAN_Q):
		terminate()
	return keyUpEvents[0].key


def showStartScreen():
	titlefont = pygame.font.Font('freesansbold.ttf', 100)
	titleText = titlefont.render('SNAKE GAME', True, TITLE_COLOR)
	while True:
		SCREEN.fill(BGCOLOR)
		drawGrid()
		titleTextRect = titleText.get_rect()
		titleTextRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
		SCREEN.blit(titleText, titleTextRect)

		drawPressKeyMsg()
		if checkForKeyPress() in (K_a, KSCAN_A):
			pygame.event.get()
			return
		pygame.display.update()
		CLOCK.tick(FPS)

def terminate():
	pygame.quit()
	sys.exit()

def getRandomFood():
	image = LIST[random.randint(0, len(LIST) - 1)]
	while(True):
		pos = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
		if(pos not in snakeCoords):
			break
	return [image, pos]

def showGameOverScreen():
	with open('bestscore.txt', 'w') as log:
		print(bestScore, file=log)

	SCREEN.fill(BGCOLOR)

	totalscoreFont = pygame.font.Font('freesansbold.ttf', 40)
	if(score > oldBestScore):
		totalscoreText = totalscoreFont.render('High Score: %s' % (score), True, GREEN)
	else:
		totalscoreText = totalscoreFont.render('Your Score: %s' % (score), True, WHITE)
		bestscoreFont = pygame.font.Font('freesansbold.ttf', 40)
		bestscoreText = bestscoreFont.render('Best Score: %s' % (bestScore), True, RED)
		bestscoreRect = bestscoreText.get_rect()
		bestscoreRect.midtop = (WINDOWWIDTH/2, 200)
		SCREEN.blit(bestscoreText, bestscoreRect)

	totalscoreRect = totalscoreText.get_rect()
	totalscoreRect.midtop = (WINDOWWIDTH/2, 150)

	drawGameOver(WINDOWWIDTH/2, 30, 100, WHITE)
	SCREEN.blit(totalscoreText, totalscoreRect)
	drawPressKeyMsg()
	pygame.display.update()
	pygame.time.wait(1000)
	checkForKeyPress()

	while True:
		if checkForKeyPress() in (K_a, KSCAN_A):
			pygame.event.get()
			return

def drawScore(score, colorScore):
	scoreText = FONT.render('Score: %s' % (score), True, colorScore)
	scoreRect = scoreText.get_rect()
	scoreRect.center = (WINDOWWIDTH - 100, 30)
	SCREEN.blit(scoreText, scoreRect)

def drawBestScore(bestScore):
	bestScoreText = FONT.render('Best score: %s' % (bestScore), True, RED)
	bestScoreRect = bestScoreText.get_rect()
	bestScoreRect.center = (WINDOWWIDTH - 100, 50)
	SCREEN.blit(bestScoreText, bestScoreRect)

def drawSnake(snakeCoords):
	""" x = snakeCoords[HEAD]['x'] * CELLSIZE
	y = snakeCoords[HEAD]['y'] * CELLSIZE
	snakeHeadRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
	pygame.draw.rect(SCREEN, HEAD_SNAKE_COLOR, snakeHeadRect) """

	for coord in snakeCoords[1:]:
		x = coord['x'] * CELLSIZE
		y = coord['y'] * CELLSIZE
		snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
		pygame.draw.rect(SCREEN, SNAKE_COLOR, snakeSegmentRect)

	x = snakeCoords[HEAD]['x'] * CELLSIZE
	y = snakeCoords[HEAD]['y'] * CELLSIZE
	snakeHeadRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
	pygame.draw.rect(SCREEN, HEAD_SNAKE_COLOR, snakeHeadRect)

def drawSnakeDie(snakeCoords):
	x = snakeCoords[HEAD]['x'] * CELLSIZE
	y = snakeCoords[HEAD]['y'] * CELLSIZE
	snakeHeadRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
	pygame.draw.rect(SCREEN, RED, snakeHeadRect)
	pygame.display.update()
	time.sleep(0.4)

	for coord in snakeCoords[1:]:
		x = coord['x'] * CELLSIZE
		y = coord['y'] * CELLSIZE
		snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
		pygame.draw.rect(SCREEN, RED, snakeSegmentRect)
		time.sleep(0.1)
		pygame.display.update()

	

def drawFood(image, coord):
	x = coord['x'] * CELLSIZE
	y = coord['y'] * CELLSIZE
	"""foodRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
	pygame.draw.rect(SCREEN, APPLE_COLOR, foodRect) """
	SCREEN.blit(image, (x, y))


def drawGrid():
	for x in range(0, WINDOWWIDTH, CELLSIZE):
		pygame.draw.line(SCREEN, LINE_GRID_COLOR, (x, 0), (x, WINDOWHEIGHT))
	for y in range(0, WINDOWHEIGHT, CELLSIZE):
		pygame.draw.line(SCREEN, LINE_GRID_COLOR, (0, y), (WINDOWWIDTH, y))

if __name__ == '__main__':
	#Thread(target = play).start() 
	Thread(target = main).start()