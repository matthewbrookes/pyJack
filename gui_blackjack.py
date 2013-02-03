#Make required imports from system and custom modules
import random, sys, time, math, os, pygame, classes
from functions import *
from pygame.locals import *
#Start pygame
pygame.init()

#Create variables for game
deck = []
player_hand = []
player_hand2 = []
dealer_hand = []
splitted = False
player_chips = 400

#Create constants
HOUSELIMIT = 80
#These three are the coordinates where images should be placed
PLAYER_HAND_COORDINATES = [(151,375),(238,375),(325,375),(413,375),(501,375)]
PLAYER_HAND2_COORDINATES = [(151,483),(238,483),(325,483),(413,483),(501,483)]
DEALER_HAND_COORDINATES = [(151,183),(238,183),(325,183),(413,183),(501,183)]

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BGCOLOR = (77, 189, 51) 


#Setup initial pygame window 
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('pyJack')
pygame.mouse.set_visible(True)
window_surface.fill(BGCOLOR)

#We want to use the standard system font
font = pygame.font.SysFont(None, 48)


draw_start_screen(font, window_surface, WINDOWWIDTH, WINDOWHEIGHT, TEXTCOLOR) #Display the start screen
pygame.display.update() #Draw this on the screen

wait_for_player_to_press_key() #Don't begin untill user has pressed a key

#Draw custom background
background = os.path.join("assets","background.png")
background_surface = pygame.image.load(background)
window_surface.blit(background_surface, (0,0)) 

pygame.display.update() #Draw this on the screen

#Main body of game
while(True):
    deck = classes.Deck() # Create the deck
    #Create the initial hands
    player_hand = classes.Hand()
    dealer_hand = classes.DealerHand()
    #Add 2 cards to each hand
    for i in range(2):
        player_hand.twist(deck)
        dealer_hand.twist(deck)

    '''deal_cards(player_hand, dealer_hand, PLAYER_HAND_COORDINATES, DEALER_HAND_COORDINATES, window_surface, 0.4)
    time.sleep(1) #So we can see what has happened
    background = os.path.join("assets","background_options.png")
    background_surface = pygame.image.load(background)
    window_surface.blit(background_surface, (0,0))
    deal_cards(player_hand, dealer_hand, PLAYER_HAND_COORDINATES, DEALER_HAND_COORDINATES, window_surface, 0)'''
    game_loop(player_hand, PLAYER_HAND_COORDINATES, dealer_hand, DEALER_HAND_COORDINATES, window_surface, deck)
    #get_choice(player_hand, deck)
    #time.sleep(3)
    break
sys.exit()

