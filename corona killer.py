import pygame, sys
from pygame import *
import random
import math
from pygame import mixer

# initialization of the screen
pygame.init()
# background image
background = pygame.image.load('space.jpg')

# background music
mixer.music.load('Saya_Thari_Baja_bg.mp3')
mixer.music.play(-1)

# setting the screen size, caption and the icon
screen = pygame.display.set_mode((1000,700))
caption = pygame.display.set_caption('CORONA SMASHER')
icon = pygame.image.load('enemy.png')
pygame.display.set_icon(icon)


# setting the image for the player
playerImg = pygame.image.load('nepal.png')
playerX =460
playerY = 550
playerX_change = 0

# to create empty list 
enemyImg = []
enemyX = []
enemyY = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 7

# to create 6 no of enemies
for i in range(no_of_enemies):
	# setting the image for the enemy
	enemyImg.append(pygame.image.load('enemy.png'))
	# the value for randint is 1-919 because
	# to avoid the enemy from falling vertically 
	enemyX.append(random.randint(1,919))
	enemyY.append(random.randint(25,100))
	enemyX_change.append(3)
	enemyY_change.append(40)

# setting the image for the bullet
# no bulletX && bulletX_change because
# it uses the value of x in player position
# Ready - you can't see the bullet on the screen
# Fire - the bullet is currently moving
bulletImg = pygame.image.load('bulletImg.png')
bulletX = 0
bulletY = 600
bulletY_change = 30
bullet_position = "hidden"

# considering the score to be 0 in the begining
score_value = 0
font = pygame.font.Font('Love Monday.ttf',30)
textX = 10
textY = 10
# game over text
game_over_font = pygame.font.Font('Love Monday.ttf',64)

def score_score(x,y):
	# instead of blitting first 
	# render the score
	# type casting known as doing int to str by as follow
	# value, true(antialias), color
	score = font.render("score: " + str(score_value),True, (255,255,0))
	screen.blit(score,(x,y))

def game_over_text():
	over_text = game_over_font.render("GAME  OVER",True, (255,255,0))
	screen.blit(over_text,(340,250))

# choices of color to choose from
WHITE = (255,255,255)


# function that defines the player
def player(x,y):
	screen.blit(playerImg,(int(x),int(y)))

# function that defines the enemy
def enemy(x,y,i):
	screen.blit(enemyImg[i],(int(x),int(y)))

# function that defines the bullet
def fire_bullet(x,y):
	global bullet_position
	bullet_position = "action"
	screen.blit(bulletImg,(x,y))

# to check for the collision in the game
def isCollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt((math.pow((enemyX-bulletX),2))+(math.pow((enemyY-bulletY),2)))
	if distance <30:
		return True
	else:
		return False

# main program that runs on the while loop
running = True
while running:

	# color background
	screen.fill(WHITE)
	# background image
	screen.blit(background, (0,0))

	# 600 minus results upward
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -7

			if event.key == pygame.K_RIGHT:
				playerX_change = 7

			# if the bullet crosses the screen then !!
			if event.key == pygame.K_SPACE:
				if bullet_position is "hidden":
					bulletX = playerX
					fire_bullet(bulletX, bulletY)

		if event.type == pygame.KEYUP:
			if event.key == K_LEFT or event.key == K_RIGHT:
				playerX_change = 0

	# setting the boundries to the player
	playerX +=playerX_change
	if playerX<=0:
		playerX=0
	elif playerX>=920:
		playerX=920	


	for i in range(no_of_enemies):

		# Game Over
		if enemyY[i] > 500:
			for j in range(no_of_enemies):
				enemyY[j] = 2000
			game_over_text()
			score_score(450,350)
			break


		# enemy movement
		enemyX[i] +=enemyX_change[i]
		if enemyX[i]<=0:
			enemyX_change[i]=5
			enemyY[i]+=enemyY_change[i]
		elif enemyX[i]>=920:
			enemyX_change[i]=-5
			enemyY[i]+=enemyY_change[i]

		# Collision
		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			collision_sound = mixer.Sound('bomb.wav')
			collision_sound.play()
			bulletY=600
			bullet_position = "hidden"
			score_value += 1
			enemyX[i] = (random.randint(1,919))
			enemyY[i] = (random.randint(25,100))

		enemy(enemyX[i],enemyY[i], i)
		score_score(textX,textY)

	# Bullet Movement
	if bulletY <= -50:
		# ressetting the bullet into the player again
		bulletY = playerY
		# changing the bullet position to be hidden again
		bullet_position = "hidden"

	# so that the bullet doesn't follow the player lane
	if bullet_position is "action":
		bullet_sound = mixer.Sound('bullet.wav')
		bullet_sound.play()
		fire_bullet(bulletX, bulletY)
		# to travel in straight path upwards 
		bulletY -=bulletY_change


	player(playerX,playerY)
	
	pygame.display.update()
