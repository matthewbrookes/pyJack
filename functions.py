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
    if len(hand.return_hand()) > 1:
        for i in range(len(hand.return_hand())):
            imagefile = hand.return_hand()[i].return_file() + ".png"
            card_image = pygame.image.load(os.path.join('assets', imagefile))
            card_rect = card_image.get_rect()
            card_rect.topleft = coords[i]
            surface.blit(card_image, card_rect)
    else:
            imagefile = hand.return_hand()[0].return_file() + ".png"
            card_image = pygame.image.load(os.path.join('assets', imagefile))
            card_rect = card_image.get_rect()
            card_rect.topleft = coords[0]
            back_image = pygame.image.load(os.path.join('assets', 'back.png'))
            back_rect = back_image.get_rect()
            back_rect.topleft = coords[1]
            surface.blit(card_image, card_rect)  
            surface.blit(back_image, back_rect)                    
    pygame.display.update()