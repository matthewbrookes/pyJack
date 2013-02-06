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
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    sys.exit()
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
                return "Stick"
            if coords[0] > 142 and coords[1] > 283 and coords[0] < 251 and coords[1] < 355 and hand.can_twist(): #In the Twist box
                twist(hand, deck)
                return "Twist"
            if coords[0] > 354 and coords[1] > 283 and coords[0] < 463 and coords[1] < 355: #In the double down box
                print "Double Down"
                return "DoubleDown"
            if coords[0] > 483 and coords[1] > 283 and coords[1] < 592 and coords[1] < 355: #In the Split box
                print "Split"
                return "Split"
                
        elif event.type == QUIT:
                sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: # pressing escape quits
                sys.exit()

def get_bet(limit, chips, font, surface, bet): #Gets the amount user wants to bet
    background = os.path.join("assets","background_make_bet.png") 
    background_surface = pygame.image.load(background)
    surface.blit(background_surface, (0,0))
    draw_text(str(chips), font, surface, 160, 157, (255,255,255)) # Display number of chips
    draw_text(str(limit), font, surface, 473, 157, (255,255,255)) # Displays limit
    draw_text(str(bet), font, surface, 160, 207, (255,255,255)) # Displays bet
    pygame.display.update()
    while True:
        event = pygame.event.poll()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            coords = list(event.pos)
            if coords[0] > 144 and coords[1] > 251 and coords[0] < 233 and coords[1] < 317:# +1 box
                if bet +1 <= limit and bet +1<= chips:
                    return get_bet(limit, chips, font, surface, bet+1)
                    break
            elif coords[0] > 144 and coords[1] > 348 and coords[0] < 233 and coords[1] < 414:# -1 box
                if bet-1 > 0:
                    return get_bet(limit, chips, font, surface, bet-1)
                    break
            elif coords[0] > 291 and coords[1] > 251 and coords[0] < 380 and coords[1] < 317:# +5 box
                if bet +5<= limit and bet +5<= chips:
                    return get_bet(limit, chips, font, surface, bet+5)
                    break
            elif coords[0] > 291 and coords[1] > 348 and coords[0] < 380 and coords[1] < 414:# -5 box
                if bet -5 > 0:
                    return get_bet(limit, chips, font, surface, bet-5)
                    break
            elif coords[0] > 438 and coords[1] > 251 and coords[0] < 527 and coords[1] < 317:# +10 box
                if bet +10<= limit and bet +10<= chips:
                    return get_bet(limit, chips, font, surface, bet+10)
                    break
            elif coords[0] > 291 and coords[1] > 348 and coords[0] < 527 and coords[1] < 414:# -10 box
                if bet -10 > 0:
                    return get_bet(limit, chips, font, surface, bet-10)
                    break
            elif coords[0] > 291 and coords[1] > 441 and coords[0] < 380 and coords[1] < 507:# Return box
                return bet
                break
        elif event.type == QUIT:
                sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: # pressing escape quits
                sys.exit()
    #time.sleep(2)
                
def twist(hand, deck): #Function when twist box is pressed
    hand.twist(deck)
    
def find_winner(pHand, dHand): #This function checks to see what the outcome of the game is
    if pHand.return_score() == 21 and len(pHand.return_hand()) == 2: #If player scores 21 and has two cards
            return "Blackjack"
    elif pHand.return_score() > 21: #If player is bust
            return "PlayerBust"
    elif dHand.return_score() > 21: #If dealer is bust
            return "DealerBust"
    elif dHand.return_score() == pHand.return_score(): #If scores are equal
            return "Push"
    else:
            if pHand.return_score() > dHand.return_score(): #If player scores higher
                    return "PlayerWin"
            else: #If dealer scores higher
                    return "DealerWin"
                    
def dealer_decision(hand, coords, surface, deck): #This function will add cards to dealer's hand untill he scores 17 or more
    while True:
        draw_hand(hand, coords, surface, 0.4) #Draw the complete dealer's hand
        if hand.return_score() > 16: #If the score is 17 or more
                return hand
        else:
                hand.twist(deck)

def display_winner(text, font, surface, color, bgcolor): #This functions shows the player how many chips he has lost
    surface.fill(bgcolor) #Set default background
    draw_text(text, font, surface, 300, 200, color) #Draw the message
    pygame.display.update()
    time.sleep(3) #Give the player the chance to see how much they have won/lost