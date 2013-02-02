import random, sys, time, math, pygame
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

def new_deck(): # This function creates a deck of 52 cards
        deck = []
        for i in range(4): # Iterates over number of suits in classic deck
                card = []
                for j in range(13): # Iterates over number of ranks in classic deck
                        suit = suits[i] # Assigns suit to the value from the array 
                        rank = ranks[j]
                        card.append(suit) # Appends suit to the temporary card array
                        card.append(rank)
                        deck.append(card) # Appends the card to the deck array
                        card = [] # Resets card array for next iteration
        return deck
        
def shuffle_deck(deck): # This function shuffles inputted deck
        new_deck = []
        random_index = []
        for i in range(52): # For every card
                random_index.append(i) # Add a number 0-51 to the array
        for i in range(len(random_index)-1): # For every value of the random_index array
                r = random_index[random.randint(0, len(random_index)-1)] # Selects a random value from random_index array
                new_deck.append(deck[r]) # Adds a random card to the new_deck array
                random_index.remove(r) # Removes the random number from random_index
        return new_deck      
        
def deal_card(deck): # This function returns a random card from inputted deck and removes it from deck
        rIndex = random.randint(0,len(deck)-1)
        c = deck[rIndex]
        deck.remove(deck[rIndex])
        return c

def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return
                
def draw_text(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_start_screen():
    draw_text('pyJack', font, windowSurface, (WINDOWWIDTH / 2 ), (WINDOWHEIGHT / 5))
    draw_text('Press a key to start.', font, windowSurface, WINDOWWIDTH / 2 , (WINDOWHEIGHT / 3) + 50)

#Setup initial pygame window 
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('pyJack')
pygame.mouse.set_visible(True)
windowSurface.fill(BACKGROUNDCOLOR)

#We want to use the standard system font
font = pygame.font.SysFont(None, 48)

draw_start_screen()

pygame.display.update()

wait_for_player_to_press_key()