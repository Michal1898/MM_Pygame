import pygame
from pygame.locals import *

#import sys


import mm_2_5.logic as mm


attempt = 10  # you have 10 attempts
value = 8  # value can be 1 , 2, 3, 4, 5, 6, 7
digit = 5  # 5 digits of secret code
time = 1  # 1 minutes to break code. ONLY FOR TESTS!
the_game = mm.MasterMind(attempt, value, digit, time)

pygame.init()
screen_width = 1000
screen_height = 1000



screen = pygame.display.set_mode((screen_width, screen_height))

text_font = pygame.font.SysFont("Arial" ,30)


pygame.display.set_caption('Master Mind')
bg_color= 0xb0e0e6

clock_img = pygame.image.load('images/stopwatch2.jpg')
clock_img = pygame.transform.scale(clock_img, (100, 100))

def draw_text(text, font, text_color, x, y):
	img = font.render(text, True, text_color)
	screen.blit(img, (x,y))

run = True
while run and the_game.is_running():
	screen.fill(bg_color)

	time_for_game=the_game.return_time_for_game()
	#print(time_for_game.total_seconds())

	time_rest=the_game.return_rest_time()
	#print(time_rest.total_seconds())
	ratio=time_rest/time_for_game

	time_rest_sec=time_rest.seconds
	time_rest_h, remainder = divmod(time_rest.seconds, 3600)
	time_rest_m, time_rest_s = divmod(remainder, 60)
	if time_rest_h:
		time_rest_text=f'Time left:{time_rest_h}:{time_rest_m:02d}:{time_rest_sec:02d}'
	else:
		time_rest_text = f'Time left:{time_rest_m:02d}:{time_rest_sec:02d}'
	print(time_rest_text)

	draw_text(time_rest_text, text_font, 0x000000, 300,210)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False



	if ratio > 0.90:
		time_color = 0x006400
	elif ratio > 0.80:
		time_color = 0x3cb371
	elif ratio > 0.60:
		time_color = 0xadff2f
	elif ratio > 0.40:
		time_color = 0xff00ff
	else:
		time_color = 0xff4500

	print(ratio, time_color, the_game.check_time_to_left())
	pygame.draw.line(screen, (255, 255, 255), (100, 200), (100, 300))
	pygame.draw.line(screen, (255, 255, 255), (200, 200), (200, 300))
	pygame.draw.line(screen, (255, 255, 255), (0, 200), (screen_width, 200))
	pygame.draw.line(screen, (255, 255, 255), (0, 300), (screen_width, 300))

	screen.blit(clock_img, (100, 200))
	pygame.draw.rect(screen, 0xffffe0	, (250, 250, 300, 40), width=3,border_radius=7)
	pygame.draw.rect(screen, time_color, (250, 250, 300 * ratio, 40), width=0, border_radius=7)


	pygame.display.update()

pygame.quit()
