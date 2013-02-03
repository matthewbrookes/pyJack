import random, sys, time, math, os, pygame
from pygame.locals import *

pygame.init()

def draw_start_screen(font, surface, w, h, color): #Draws the screen at the very beginning
    draw_text('pyJack', font, surface, (w / 2 ), (h / 5), color)
    draw_text('Press a key to start.', font, surface, w / 2, (h / 3) + 50, color )

def wait_for_player_to_press_key(): #Game pauses whilst waiting for user to press a key
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return
                
def draw_text(text, font, surface, x, y, color): #Draws text with these parameters
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_hand(hand, coords, surface, pause): #Draw the hand on the screen, requires the coordinates in an array
    for i in range(len(hand.return_hand())):
        imagefile = hand.return_hand()[i].return_file() + ".png"
        card_image = pygame.image.load(os.path.join('assets', imagefile))
        card_rect = card_image.get_rect()
        card_rect.topleft = coords[i]
        surface.blit(card_image, card_rect)
        pygame.display.update()
        time.sleep(pause)
        
def draw_dealer_hand(hand,coords, surface, pause):
    dealer_image = pygame.image.load(os.path.join('assets', hand.return_first_card_hand().return_hand()[0].return_file() + ".png"))
    dealer_rect = dealer_image.get_rect()
    dealer_rect.topleft = coords[0]
    surface.blit(dealer_image, dealer_rect)
    pygame.display.update()
    time.sleep(pause) 
    back_image = pygame.image.load(os.path.join('assets', 'back.png'))
    dealer_rect2 = back_image.get_rect()
    dealer_rect2.topleft = coords[1]
    surface.blit(back_image, dealer_rect2)
    pygame.display.update()
    time.sleep(pause)

def deal_cards(p_hand, d_hand, p_coords, d_coords, surface, pause): #Deals the cards at the beginning of the game
    time.sleep(pause)
    #Show the back of the 1st card for player
    back_image = pygame.image.load(os.path.join('assets', 'back.png'))
    player_back_rect1 = back_image.get_rect()
    player_back_rect1.topleft = p_coords[0]
    surface.blit(back_image, player_back_rect1)
    pygame.display.update()
    time.sleep(pause)
    
    #Show the front of dealer's 1st card
    dealer_image = pygame.image.load(os.path.join('assets', d_hand.return_first_card_hand().return_hand()[0].return_file() + ".png"))
    dealer_rect = dealer_image.get_rect()
    dealer_rect.topleft = d_coords[0]
    surface.blit(dealer_image, dealer_rect)
    pygame.display.update()
    time.sleep(pause)
    
    #Show the back of player's 2nd card
    player_back_rect2 = back_image.get_rect()
    player_back_rect2.topleft = p_coords[1]
    surface.blit(back_image, player_back_rect2)
    pygame.display.update()
    time.sleep(pause)
    
    #Show the back of dealer's 2nd card
    dealer_rect2 = back_image.get_rect()
    dealer_rect2.topleft = d_coords[1]
    surface.blit(back_image, dealer_rect2)
    pygame.display.update()
    time.sleep(pause)
    
    #Show the player's cards
    draw_hand(p_hand, p_coords, surface, pause)
    
def get_choice(hand, deck): #Allows the user to choose what to do
    while True:
        event = pygame.event.poll()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            coords = list(event.pos)
            if coords[0] > 11 and coords[1] > 283 and coords[0] < 120 and coords[1] < 355: #In the Stick box
                print "Stick"
                break
            if coords[0] > 142 and coords[1] > 283 and coords[0] < 251 and coords[1] < 355 and hand.can_twist(): #In the Twist box
                twist(hand, deck)
                break
            if coords[0] > 354 and coords[1] > 283 and coords[0] < 463 and coords[1] < 355: #In the double down box
                print "Double Down"
                break
            if coords[0] > 483 and coords[1] > 283 and coords[1] < 592 and coords[1] < 355: #In the Split box
                print "Split"
                break
                
        elif event.type == QUIT:
                terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: # pressing escape quits
                terminate()

def twist(hand, deck): #Function when twist box is pressed
    hand.twist(deck)
    
def game_loop(p_hand, p_coords, d_hand, d_coords, surface, deck): #The main loop of the game
    deal_cards(p_hand, d_hand, p_coords, d_coords, surface, 0.4) #Deal cards
    while True:

        #Show the availabe options
        background = os.path.join("assets","background_options.png") 
        background_surface = pygame.image.load(background)
        surface.blit(background_surface, (0,0))
        
        #Display hands
        draw_dealer_hand(d_hand, d_coords, surface, 0)
        draw_hand(p_hand, p_coords, surface, 0)
        
        pygame.display.update() #Refresh display
        
        get_choice(p_hand, deck) #Let user make a choice
        
        #Set default background
        background = os.path.join("assets","background.png")
        background_surface = pygame.image.load(background)
        surface.blit(background_surface, (0,0))
        
        pygame.display.update()
        
        #Display hands
        draw_dealer_hand(d_hand, d_coords, surface, 0)
        draw_hand(p_hand, p_coords, surface, 0)
        
        pygame.display.update() #Refresh display
        time.sleep(1) #Pause
    