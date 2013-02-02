import random, sys, time, math, os, pygame, classes
from functions import *
from pygame.locals import *
pygame.init()

suits = ["spades", "clubs", "hearts", "diamonds"]
ranks = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
player_hand = []
player_hand2 = []
dealer_hand = []
splitted = False
HOUSELIMIT = 80
player_chips = 400
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (77, 189, 51)


#Setup initial pygame window 
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('pyJack')
pygame.mouse.set_visible(True)
window_surface.fill(BACKGROUNDCOLOR)

#We want to use the standard system font
font = pygame.font.SysFont(None, 48)

draw_start_screen(font, window_surface, WINDOWWIDTH, WINDOWHEIGHT, TEXTCOLOR)

pygame.display.update()

wait_for_player_to_press_key()