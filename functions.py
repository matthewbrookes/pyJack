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

def draw_hand(hand, coords, surface): #Draw the hand on the screen, requires the coordinates in an array
    for i in range(len(hand.return_hand())):
        imagefile = hand.return_hand()[i].return_file() + ".png"
        card_image = pygame.image.load(os.path.join('assets', imagefile))
        card_rect = card_image.get_rect()
        card_rect.topleft = coords[i]
        surface.blit(card_image, card_rect)
        pygame.display.update()
        time.sleep(0.4)


def deal_cards(p_hand, d_hand, p_coords, d_coords, surface):
    time.sleep(0.4)
    #Show the back of the 1st card for player
    back_image = pygame.image.load(os.path.join('assets', 'back.png'))
    player_back_rect1 = back_image.get_rect()
    player_back_rect1.topleft = p_coords[0]
    surface.blit(back_image, player_back_rect1)
    pygame.display.update()
    time.sleep(0.4)
    
    #Show the front of dealer's 1st card
    dealer_image = pygame.image.load(os.path.join('assets', d_hand.return_first_card_hand().return_hand()[0].return_file() + ".png"))
    dealer_rect = dealer_image.get_rect()
    dealer_rect.topleft = d_coords[0]
    surface.blit(dealer_image, dealer_rect)
    pygame.display.update()
    time.sleep(0.4)
    
    #Show the back of player's 2nd card
    player_back_rect2 = back_image.get_rect()
    player_back_rect2.topleft = p_coords[1]
    surface.blit(back_image, player_back_rect2)
    pygame.display.update()
    time.sleep(0.4)
    
    #Show the back of dealer's 2nd card
    dealer_rect2 = back_image.get_rect()
    dealer_rect2.topleft = d_coords[1]
    surface.blit(back_image, dealer_rect2)
    pygame.display.update()
    time.sleep(0.4)
    
    #Show the player's cards
    draw_hand(p_hand, p_coords, surface)