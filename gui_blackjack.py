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


#Draw icon and captions
icon_surface = pygame.Surface((32, 32))
icon = pygame.image.load(os.path.join('assets','logo32x32.png'))
icon_surface.set_colorkey((0,0,0))
icon_surface.blit(icon, (0,0))
pygame.display.set_icon(icon_surface)
pygame.display.set_caption('pyJack')

#Setup initial pygame window
window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.mouse.set_visible(True)
window_surface.fill(BGCOLOR)

# We want to use the standard system font
font = pygame.font.SysFont(None, 48)


draw_start_screen(font, window_surface, WINDOWWIDTH, WINDOWHEIGHT, TEXTCOLOR) # Display the start screen
pygame.display.update() # Draw start screen on the screen

wait_for_player_to_press_key(window_surface) # Don't begin untill player has pressed a key



#Main body of game
while True: #Main loop of game
    split = False
    dealer_blackjack = False # Will be true if the dealer has a blackjack on his first two cards
    if player_chips < 1: # If the player has less than 1 chips
        window_surface.fill(BGCOLOR) # Fill the screen with the background colour
        # Tells player what has happened and that the game will close
        draw_text("You have run out of chips", font, window_surface, 300, 200, TEXTCOLOR)
        draw_text("The game will now close", pygame.font.SysFont(None, 42), window_surface, 300, 350, TEXTCOLOR)
        pygame.display.update() # Shows text
        time.sleep(2) # Gives player chance to read message
        sys.exit() # Close game
    deck = classes.Deck() # Create the deck
    # Create the initial hands
    player_hand = classes.Hand()
    dealer_hand = classes.DealerHand()
    # Add 2 cards to each hand
    for i in range(2):
        player_hand.twist(deck)
        dealer_hand.twist(deck)

    # Get the bet
    bet = get_bet(HOUSELIMIT, 1, player_chips, font, window_surface, 1, os.path.join("assets","background_make_bet.png"), False)
    # Draw custom background
    background = os.path.join("assets","background.png")
    background_surface = pygame.image.load(background)
    window_surface.blit(background_surface, (0,0))
    time.sleep(0.4) # Mimics time taken to deal first card
    deal_cards(player_hand, dealer_hand, PLAYER_HAND_COORDINATES, DEALER_HAND_COORDINATES, window_surface, 0.4) # Deal cards

    if dealer_hand.return_first_card().return_rank() == 'A': # If the dealer shows an Ace
        window_surface.fill(BGCOLOR) # Fill screen with BGCOLOR
        draw_text("You need to make an insurance bet", font, window_surface, 300, 200, TEXTCOLOR)
        pygame.display.update()
        time.sleep(1.5) # Pause to give reader time to read message

        background = os.path.join("assets","background_insurance.png")
        background_surface = pygame.image.load(background)
        window_surface.blit(background_surface, (0,0))

        insurance_bet = get_bet(int(math.floor(bet/2)), 0, "", font, window_surface, 0, background, True)

        s = "" #Will hold an "s" if the insurance bet is more than one
        if bet != 1:
            s = "s"

        if dealer_hand.return_score() == 21: # If the dealer has blackjack
            dealer_blackjack = True

            #Draw default background
            background = os.path.join("assets", "background.png")
            background_surface = pygame.image.load(background)
            window_surface.blit(background_surface, (0,0))

            #Display hands
            draw_hand(dealer_hand, DEALER_HAND_COORDINATES, window_surface, 0)
            draw_hand(player_hand, PLAYER_HAND_COORDINATES, window_surface, 0)

            pygame.display.update() # Show hands to player
            time.sleep(1)

            window_surface.fill(BGCOLOR) # Fill screen with BGCOLOR
            draw_text("Dealer shows blackjack", font, window_surface, 300, 200, TEXTCOLOR)
            draw_text("You've won %s chip%s" % (insurance_bet, s), font, window_surface, 300, 300, TEXTCOLOR)
            pygame.display.update()
            player_chips += insurance_bet
            time.sleep(1.5)

        else: # If dealer doesn't have blackjack
            dealer_blackjack = False
            window_surface.fill(BGCOLOR) # Fill screen with BGCOLOR
            draw_text("Dealer doesn't have blackjack", font, window_surface, 300, 200, TEXTCOLOR)
            draw_text("You've lost %s chip%s" % (insurance_bet, s), font, window_surface, 300, 300, TEXTCOLOR)
            pygame.display.update()
            player_chips -= insurance_bet
            time.sleep(2)
    window_surface.fill(BGCOLOR)
    draw_text('pyJack', font, window_surface, (WINDOWWIDTH / 2 ), (WINDOWHEIGHT / 5), TEXTCOLOR)
    draw_text('This is your go', font, window_surface, (WINDOWWIDTH / 2), (WINDOWHEIGHT / 3) + 50, TEXTCOLOR )
    pygame.display.update()
    time.sleep(3)
    while True: # Main interface for game
        # Display hands
        draw_dealer_hand(dealer_hand, DEALER_HAND_COORDINATES, window_surface, 0)
        draw_hand(player_hand, PLAYER_HAND_COORDINATES, window_surface, 0)

        pygame.display.update() #Refresh display
        while True: # Let player make a choice
            # Show options
            background = os.path.join("assets","background_options.png")
            background_surface = pygame.image.load(background)
            window_surface.blit(background_surface, (0,0))
            # Show hands
            draw_dealer_hand(dealer_hand, DEALER_HAND_COORDINATES, window_surface, 0)
            draw_hand(player_hand, PLAYER_HAND_COORDINATES, window_surface, 0)

            choice = get_choice(player_hand, deck, split, window_surface) #Get choice

            if choice == "Twist":
                pass
            elif choice == "Stick":
                break
            elif choice == "DoubleDown":
                player_hand.twist(deck) # Add card to player's hand
                draw_hand(player_hand, PLAYER_HAND_COORDINATES, window_surface, 0) # Draw player's hand
                bet *= 2 # Double bet
                time.sleep(1) # Pause before calculating outcome
                break
            elif choice == "Split":
                split = True
                split_card = player_hand.return_hand()[1] # The card which will be added to the second hand

                player_hand.delete_card(1) # Delete this card from the first hand
                player_hand2 = classes.Hand() # Create a new hand
                player_hand2.add_card(split_card) # Add the card to the second hand
                player_hand.twist(deck) # Add another card to the first hand
                player_hand2.twist(deck) # Add another card to the second hand

                #Change to the two hands background
                background = os.path.join("assets", "background_two_hands.png")
                background_surface = pygame.image.load(background)
                window_surface.blit(background_surface, (0,0))

                #Draw hands on screen
                draw_dealer_hand(dealer_hand, DEALER_HAND_COORDINATES, window_surface, 0)
                draw_hand(player_hand, PLAYER_HAND_COORDINATES, window_surface, 0)
                draw_hand(player_hand2, PLAYER_HAND2_COORDINATES, window_surface, 0)
                pygame.display.update()
                time.sleep(1) # Pause so player can see cards

                #Tell the player they are using the first hand
                window_surface.fill(BGCOLOR)
                draw_text("This is your first hand", font, window_surface, 300, 200, TEXTCOLOR)
                pygame.display.update()
                time.sleep(2) # Pause for player to read message

                #Change to the two hands background
                background = os.path.join("assets", "background_options_two_hands.png")
                background_surface = pygame.image.load(background)
                window_surface.blit(background_surface, (0,0))

                #Draw hands on screen
                draw_dealer_hand(dealer_hand, DEALER_HAND_COORDINATES, window_surface, 0)
                draw_hand(player_hand, PLAYER_HAND_COORDINATES, window_surface, 0)
                draw_hand(player_hand2, PLAYER_HAND2_COORDINATES, window_surface, 0)
                pygame.display.update()

                while True:
                    choice = get_choice(player_hand, deck, split, window_surface)
                    if choice == "Twist":
                        draw_hand(player_hand, PLAYER_HAND_COORDINATES, window_surface, 0) # Draw player's hand
                    elif choice == "Stick":
                        break

                #Tell the player they are using the first hand
                window_surface.fill(BGCOLOR)
                draw_text("This is your second hand", font, window_surface, 300, 200, TEXTCOLOR)
                pygame.display.update()
                time.sleep(2) # Pause for player to read message

                #Change to the two hands background
                background = os.path.join("assets", "background_options_two_hands.png")
                background_surface = pygame.image.load(background)
                window_surface.blit(background_surface, (0,0))

                #Draw hands on screen
                draw_dealer_hand(dealer_hand, DEALER_HAND_COORDINATES, window_surface, 0)
                draw_hand(player_hand, PLAYER_HAND_COORDINATES, window_surface, 0)
                draw_hand(player_hand2, PLAYER_HAND2_COORDINATES, window_surface, 0)
                pygame.display.update()

                while True:
                    choice = get_choice(player_hand2, deck, split, window_surface)
                    if choice == "Twist":
                        draw_hand(player_hand2, PLAYER_HAND2_COORDINATES, window_surface, 0) # Draw player's hand
                    elif choice == "Stick":
                        break
                break

        if split == False and player_hand.return_score() < 22: # Dealer should only get more cards if player isn't bust and hasn't split
            background = os.path.join("assets","background.png")
            background_surface = pygame.image.load(background)
            window_surface.blit(background_surface, (0,0))
            draw_hand(player_hand, PLAYER_HAND_COORDINATES, window_surface, 0)
            draw_dealer_hand(dealer_hand, DEALER_HAND_COORDINATES, window_surface, 0)
            dealer_hand = dealer_decision(dealer_hand, DEALER_HAND_COORDINATES, window_surface, deck)
        elif split == True: # If player has split
            background = os.path.join("assets","background_two_hands.png")
            background_surface = pygame.image.load(background)
            window_surface.blit(background_surface, (0,0))
            pygame.display.update()
            draw_hand(player_hand, PLAYER_HAND_COORDINATES, window_surface, 0)
            draw_hand(player_hand2, PLAYER_HAND2_COORDINATES, window_surface, 0)
            draw_dealer_hand(dealer_hand, DEALER_HAND_COORDINATES, window_surface, 0)
            dealer_hand = dealer_decision(dealer_hand, DEALER_HAND_COORDINATES, window_surface, deck)
            pygame.display.update()
        s = "" #Will hold an "s" if the bet is more than one
        if bet != 1:
            s = "s"

        if split == False: # If the player hasn't split
            # Get the outcome of the round and change player's chips
            outcome = find_winner(player_hand, dealer_hand)
            window_surface.fill(BGCOLOR)
            if outcome == "Blackjack":
                player_chips += int(round(bet * 1.5))
                text = "You have won %s chip%s for blackjack" % (int(round(bet * 1.5)), s)
                display_winner(text, font, window_surface, TEXTCOLOR) # Displays the result to the player
            elif outcome == "PlayerWin" or outcome == "DealerBust":
                player_chips += bet
                text = "You have won %s chip%s" % (bet, s)
                display_winner(text, font, window_surface, TEXTCOLOR)
            elif outcome == "DealerWin" or outcome == "PlayerBust":
                text = "You have lost %s chip%s" % (bet, s)
                display_winner(text, font, window_surface, TEXTCOLOR)
                player_chips -= bet
            else:
                text = "You have pushed"
                display_winner(text, font, window_surface, TEXTCOLOR)
            break
        elif split == True:
            # Get outcomes for both hands
            outcome1 = find_winner(player_hand, dealer_hand)
            outcome2 = find_winner(player_hand2, dealer_hand)

            window_surface.fill(BGCOLOR)

            #Tells player about first hand
            draw_text("On your first hand", font, window_surface, 300, 100, TEXTCOLOR)
            pygame.display.update()
            time.sleep(1) # Gives player time to read message
            if outcome1 == "Blackjack":
                player_chips += int(round(bet * 1.5))
                text = "You have won %s chip%s for blackjack" % (int(round(bet * 1.5)), s)
                display_winner(text, font, window_surface, TEXTCOLOR) # Displays the result to the player
            elif outcome1 == "PlayerWin" or outcome1 == "DealerBust":
                player_chips += bet
                text = "You have won %s chip%s" % (bet, s)
                display_winner(text, font, window_surface, TEXTCOLOR)
            elif outcome1 == "DealerWin" or outcome1 == "PlayerBust":
                text = "You have lost %s chip%s" % (bet, s)
                display_winner(text, font, window_surface, TEXTCOLOR)
                player_chips -= bet
            else:
                text = "You have pushed"
                display_winner(text, font, window_surface, TEXTCOLOR)

            window_surface.fill(BGCOLOR)

            # Tells player about second hand
            draw_text("On your second hand", font, window_surface, 300, 100, TEXTCOLOR)
            pygame.display.update()
            time.sleep(1) # Gives player time to read message
            if outcome2 == "Blackjack":
                player_chips += int(round(bet * 1.5))
                text = "You have won %s chip%s for blackjack" % (int(round(bet * 1.5)), s)
                display_winner(text, font, window_surface, TEXTCOLOR) # Displays the result to the player
            elif outcome2 == "PlayerWin" or outcome2 == "DealerBust":
                player_chips += bet
                text = "You have won %s chip%s" % (bet, s)
                display_winner(text, font, window_surface, TEXTCOLOR)
            elif outcome2 == "DealerWin" or outcome2 == "PlayerBust":
                text = "You have lost %s chip%s" % (bet, s)
                display_winner(text, font, window_surface, TEXTCOLOR)
                player_chips -= bet
            else:
                text = "You have pushed"
                display_winner(text, font, window_surface, TEXTCOLOR)
            time.sleep(1) # Gives time to read message

            break
sys.exit()

