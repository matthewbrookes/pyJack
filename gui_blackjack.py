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
BGCOLOR = (77,189,51)


#Setup initial pygame window 
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('pyJack')
pygame.mouse.set_visible(True)
window_surface.fill(BGCOLOR)
#We want to use the standard system font
font = pygame.font.SysFont(None, 48)

background = os.path.join("assets","background.png")
background_surface = pygame.image.load(background)


draw_start_screen(font, window_surface, WINDOWWIDTH, WINDOWHEIGHT, TEXTCOLOR) #Display the start screen
pygame.display.update() #Draw this on the screen

wait_for_player_to_press_key() #Don't begin untill user has pressed a key
window_surface.blit(background_surface, (0,0)) 
pygame.display.update() #Draw this on the screen
time.sleep(1)