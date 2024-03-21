import pygame
from pygame.locals import *

#import sys


import mm_2_5.logic as mm


attempt = 10  # you have 10 attempts
value = 8  # value can be 1 , 2, 3, 4, 5, 6, 7
digit = 5  # 5 digits of secret code
time = 5  # 5 minutes to break code
the_game = mm.MasterMind(attempt, value, digit, time)

pygame.init()
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
bg_color= 0xb0e0e6
run = True
while run:

	screen.fill(bg_color)



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
