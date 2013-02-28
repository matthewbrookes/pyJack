import sys, time, os, pygame, string, csv
from pygame.locals import *
from pygame import surface

pygame.init()

def draw_start_screen(font, surface, w, h, color):  # Draws the screen at the very beginning
    draw_text('pyJack', font, surface, (w / 2), (h / 5), color)
    draw_text('Press a key to start.', font, surface, w / 2, (h / 3) + 50, color)
    draw_text("Or press 'H' to show help.", font, surface, w / 2, (h / 2), color)

def wait_for_player_to_press_key(surface):  # Game pauses whilst waiting for player to press a key
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    pygame.quit()
                    sys.exit()
                elif event.key == K_h:  # pressing h shows help
                    show_help(surface)
                return

def draw_text(text, font, surface, x, y, color):  # Draws text with these parameters
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_hand(hand, coords, surface, pause):  # Draw the hand on the screen, requires the coordinates in an array
    for i in range(len(hand.return_hand())):
        imagefile = hand.return_hand()[i].return_file() + ".png"
        card_image = pygame.image.load(os.path.join('assets', imagefile))
        card_rect = card_image.get_rect()
        card_rect.topleft = coords[i]
        surface.blit(card_image, card_rect)
        pygame.display.update()
        time.sleep(pause)

def draw_dealer_hand(hand, coords, surface, pause):
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

def deal_cards(p_hand, d_hand, p_coords, d_coords, surface, pause):  # Deals the cards at the beginning of the game
    time.sleep(pause)
    # Show the back of the 1st card for player
    back_image = pygame.image.load(os.path.join('assets', 'back.png'))
    player_back_rect1 = back_image.get_rect()
    player_back_rect1.topleft = p_coords[0]
    surface.blit(back_image, player_back_rect1)
    pygame.display.update()
    time.sleep(pause)

    # Show the front of dealer's 1st card
    dealer_image = pygame.image.load(os.path.join('assets', d_hand.return_first_card_hand().return_hand()[0].return_file() + ".png"))
    dealer_rect = dealer_image.get_rect()
    dealer_rect.topleft = d_coords[0]
    surface.blit(dealer_image, dealer_rect)
    pygame.display.update()
    time.sleep(pause)

    # Show the back of player's 2nd card
    player_back_rect2 = back_image.get_rect()
    player_back_rect2.topleft = p_coords[1]
    surface.blit(back_image, player_back_rect2)
    pygame.display.update()
    time.sleep(pause)

    # Show the back of dealer's 2nd card
    dealer_rect2 = back_image.get_rect()
    dealer_rect2.topleft = d_coords[1]
    surface.blit(back_image, dealer_rect2)
    pygame.display.update()
    time.sleep(pause)

    # Show the player's cards
    draw_hand(p_hand, p_coords, surface, pause)

def get_choice(hand, deck, split, surface):  # Allows the player to choose what to do
    while True:
        if hand.return_hand()[0].return_rank() == hand.return_hand()[1].return_rank() and split == False and len(hand.return_hand()) == 2 and hand.can_twist():  # If the player has two cards of equal rank, hasn't split, only has two cards in hand and can twist
            draw_options([0, 1, 2, 3], surface)  # Draw all 4 options
            pygame.display.update()
            event = pygame.event.poll()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                coords = list(event.pos)
                if coords[0] > 11 and coords[1] > 283 and coords[0] < 120 and coords[1] < 355:  # In the Stick box
                    return "Stick"
                if coords[0] > 142 and coords[1] > 283 and coords[0] < 251 and coords[1] < 355:  # In the Twist box
                    twist(hand, deck)
                    return "Twist"
                if coords[0] > 354 and coords[1] > 283 and coords[0] < 463 and coords[1] < 355:  # In the double down box
                    return "DoubleDown"
                if coords[0] > 483 and coords[1] > 283 and coords[1] < 592 and coords[1] < 355:  # In the Split box
                    return "Split"
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    pygame.quit()
                    sys.exit()

        elif hand.can_twist() and split == False and len(hand.return_hand()) == 2:  # If the player has two cards, can twist and hasn't split
            draw_options([0, 1, 2], surface)  # Draw 3 options
            event = pygame.event.poll()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                coords = list(event.pos)
                if coords[0] > 11 and coords[1] > 283 and coords[0] < 120 and coords[1] < 355:  # In the Stick box
                    return "Stick"
                if coords[0] > 142 and coords[1] > 283 and coords[0] < 251 and coords[1] < 355:  # In the Twist box
                    twist(hand, deck)
                    return "Twist"
                if coords[0] > 354 and coords[1] > 283 and coords[0] < 463 and coords[1] < 355:  # In the double down box
                    return "DoubleDown"
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    pygame.quit()
                    sys.exit()

        elif hand.can_twist():  # If the player can twist
            draw_options([0, 1], surface)  # Draw 2 options
            event = pygame.event.poll()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                coords = list(event.pos)
                if coords[0] > 11 and coords[1] > 283 and coords[0] < 120 and coords[1] < 355:  # In the Stick box
                    return "Stick"
                if coords[0] > 142 and coords[1] > 283 and coords[0] < 251 and coords[1] < 355:  # In the Twist box
                    twist(hand, deck)
                    return "Twist"
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    pygame.quit()
                    sys.exit()

        elif hand.return_score() > 21:  # If the player is bust
            time.sleep(1)
            return "Stick"  # Auto sticks for the player

        else:  # If the player can only stick
            pygame.display.update()
            event = pygame.event.poll()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                coords = list(event.pos)
                if coords[0] > 11 and coords[1] > 283 and coords[0] < 120 and coords[1] < 355:  # In the Stick box
                    return "Stick"
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    pygame.quit()
                    sys.exit()



def get_bet(upper_limit, lower_limit, chips, font, surface, bet, background, insurance):  # Gets the amount player wants to bet
    background_surface = pygame.image.load(background)
    surface.blit(background_surface, (0, 0))
    draw_text(str(chips), font, surface, 160, 157, (255, 255, 255))  # Display number of chips
    if insurance == False:
        draw_text(str(upper_limit), font, surface, 473, 157, (255, 255, 255))  # Displays upper_limit
    else:
        draw_text(str(upper_limit), font, surface, 473, 207, (255, 255, 255))  # Displays upper_limit
    draw_text(str(bet), font, surface, 160, 207, (255, 255, 255))  # Displays bet
    pygame.display.update()
    while True:
        event = pygame.event.poll()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            coords = list(event.pos)
            if coords[0] > 144 and coords[1] > 251 and coords[0] < 233 and coords[1] < 317:  # +1 box
                if bet + 1 <= upper_limit and bet + 1 <= chips:
                    return get_bet(upper_limit, lower_limit, chips, font, surface, bet + 1, background, insurance)
                    break
            elif coords[0] > 144 and coords[1] > 348 and coords[0] < 233 and coords[1] < 414:  # -1 box
                if bet - 1 >= lower_limit:
                    return get_bet(upper_limit, lower_limit, chips, font, surface, bet - 1, background, insurance)
                    break
            elif coords[0] > 291 and coords[1] > 251 and coords[0] < 380 and coords[1] < 317:  # +5 box
                if bet + 5 <= upper_limit and bet + 5 <= chips:
                    return get_bet(upper_limit, lower_limit, chips, font, surface, bet + 5, background, insurance)
                    break
            elif coords[0] > 291 and coords[1] > 348 and coords[0] < 380 and coords[1] < 414:  # -5 box
                if bet - 5 >= lower_limit:
                    return get_bet(upper_limit, lower_limit, chips, font, surface, bet - 5, background, insurance)
                    break
            elif coords[0] > 438 and coords[1] > 251 and coords[0] < 527 and coords[1] < 317:  # +10 box
                if bet + 10 <= upper_limit and bet + 10 <= chips:
                    return get_bet(upper_limit, lower_limit, chips, font, surface, bet + 10, background, insurance)
                    break
            elif coords[0] > 291 and coords[1] > 348 and coords[0] < 527 and coords[1] < 414:  # -10 box
                if bet - 10 >= lower_limit:
                    return get_bet(upper_limit, lower_limit, chips, font, surface, bet - 10, background, insurance)
                    break
            elif coords[0] > 291 and coords[1] > 441 and coords[0] < 380 and coords[1] < 507:  # Return box
                return bet
                break
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # pressing escape quits
                pygame.quit()
                sys.exit()
    # time.sleep(2)

def twist(hand, deck):  # Function when twist box is pressed
    hand.twist(deck)

def find_winner(pHand, dHand):  # This function checks to see what the outcome of the game is
    if pHand.return_score() == 21 and len(pHand.return_hand()) == 2:  # If player scores 21 and has two cards
            return "Blackjack"
    elif pHand.return_score() > 21:  # If player is bust
            return "PlayerBust"
    elif dHand.return_score() > 21:  # If dealer is bust
            return "DealerBust"
    elif dHand.return_score() == pHand.return_score():  # If scores are equal
            return "Push"
    else:
            if pHand.return_score() > dHand.return_score():  # If player scores higher
                    return "PlayerWin"
            else:  # If dealer scores higher
                    return "DealerWin"

def dealer_decision(hand, coords, surface, deck):  # This function will add cards to dealer's hand untill he scores 17 or more
    while True:
        draw_hand(hand, coords, surface, 0.4)  # Draw the complete dealer's hand
        if hand.return_score() < 17 and len(hand.return_hand()) < 5:  # If the score is 17 or more
                hand.twist(deck)
        else:
                time.sleep(1.5)
                return hand

def display_winner(text, font, surface, color):  # This functions shows the player how many chips he has lost
    draw_text(text, font, surface, 300, 200, color)  # Draw the message
    pygame.display.update()
    time.sleep(3)  # Give the player the chance to see how much they have won/lost

def show_help(surface):  # Show help
    # Creates images and rects
    tutorial1 = pygame.image.load(os.path.join('assets', 'tutorial1.png'))
    tutorial1_rect = tutorial1.get_rect()
    tutorial2 = pygame.image.load(os.path.join('assets', 'tutorial2.png'))
    tutorial2_rect = tutorial2.get_rect()
    tutorial3 = pygame.image.load(os.path.join('assets', 'tutorial3.png'))
    tutorial3_rect = tutorial3.get_rect()
    tutorial4 = pygame.image.load(os.path.join('assets', 'tutorial4.png'))
    tutorial4_rect = tutorial4.get_rect()
    tutorial5 = pygame.image.load(os.path.join('assets', 'tutorial5.png'))
    tutorial5_rect = tutorial5.get_rect()
    tutorial6 = pygame.image.load(os.path.join('assets', 'tutorial6.png'))
    tutorial6_rect = tutorial6.get_rect()
    tutorial7 = pygame.image.load(os.path.join('assets', 'tutorial7.png'))
    tutorial7_rect = tutorial7.get_rect()
    tutorial8 = pygame.image.load(os.path.join('assets', 'tutorial8.png'))
    tutorial8_rect = tutorial8.get_rect()

    # Draw each tutorial image and wait for the user to press a key
    surface.blit(tutorial1, tutorial1_rect)
    pygame.display.update()
    wait_for_player_to_press_key(surface)

    surface.blit(tutorial2, tutorial2_rect)
    pygame.display.update()
    wait_for_player_to_press_key(surface)

    surface.blit(tutorial3, tutorial3_rect)
    pygame.display.update()
    wait_for_player_to_press_key(surface)

    surface.blit(tutorial4, tutorial4_rect)
    pygame.display.update()
    wait_for_player_to_press_key(surface)

    surface.blit(tutorial5, tutorial5_rect)
    pygame.display.update()
    wait_for_player_to_press_key(surface)

    surface.blit(tutorial6, tutorial6_rect)
    pygame.display.update()
    wait_for_player_to_press_key(surface)

    surface.blit(tutorial7, tutorial7_rect)
    pygame.display.update()
    wait_for_player_to_press_key(surface)

    surface.blit(tutorial8, tutorial8_rect)
    pygame.display.update()
    wait_for_player_to_press_key(surface)

def enter_username_box(screen, message):  # Displays a box for the player to enter a user name
    fontobject = pygame.font.Font(os.path.join('assets', 'font.ttf'), 36)  # Creates a new font
    screen.fill((77, 189, 51))  # Fill screen green
    draw_text('pyJack', fontobject, screen, (screen.get_width() / 2), (screen.get_height() / 5), (255, 255, 255))  # Draw title
    draw_text('Enter a username:', fontobject, screen, (screen.get_width() / 2), (screen.get_height() / 3 - 30), (255, 255, 255))
    pygame.draw.rect(screen, (77, 189, 51),
                   ((screen.get_width() / 2) - 225,
                    (screen.get_height() / 2) - 10,
                    450, 25), 0)  # Draws field where user will enter name
    if len(message) != 0:  # If there is a message
        message_size = list(fontobject.size(message))  # How much space the message wil take up
        screen.blit(fontobject.render(message, 1, (255, 255, 255)), ((screen.get_width() / 2 - (message_size[0] / 2)), (screen.get_height() / 4) + 50))  # Draw message in user name field
    pygame.display.flip()

def get_key():  # Gets a key from the player
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event
        else:
            pass

def get_username(screen, question):  # Get player to enter a username
    current_string = []  # List holds the username letters
    enter_username_box(screen, question + "" + string.join(current_string, ""))  # Draw username box
    while True:  # Continuous loop
        inkey = get_key()  # Get key press
        if inkey.key == K_BACKSPACE:  # If key is backspace
            current_string = current_string[0:-1]  # Delete last letter
        elif inkey.key == K_RETURN:  # If key is return
            break  # Break loop
        elif inkey.key == K_ESCAPE:  # If key is escape
            pygame.quit()
            sys.exit()
        elif is_valid_letter(inkey.key) and len(current_string) < 10:  # If key is a valid letter and username is less than 10 letters
            current_string.append(inkey.unicode)  # Add the unicode letter from the key
        enter_username_box(screen, question + "" + string.join(current_string, ""))  # Prompt user for next letter
    return string.join(current_string, "")  # Return username as string

def is_valid_letter(key):  # Checks the key was a valid letter
    if key > 96 and key < 123:  # If it's a capital letter
        return True
    elif key > 140 and key < 173:  # If it's a lowercase letter
        return True
    else:  # If it's not a letter
        return False

def get_chips(username):  # Gets the number of chips from file 
    try:  # Attempt to open the save file
        save_file = open('scores.csv', 'r')  # Opens the save file for reading
    except IOError:  # If the file doesn't exist
        new_file = open('scores.csv', 'w')  # Creates a file called scores.csv
        new_file.close()  # Close the file
        save_file = open('scores.csv', 'r')  # Opens the save file for reading
    finally:  # When the file is opened
        reader = csv.reader(save_file)  # Creates a CSV reader
        for row in reader:
            if row[0] == username.lower():  # If the first column in the row is equal to the username
                return int(row[1])  # Return the corresponding chip amount
        return 400  # If it's a new username return 400
        save_file.close()  # Close file

def save_chips(username, chips):  # Writes the number of chips to file
    read_save_file = open('scores.csv', 'r')  # Opens save file for reading
    reader = csv.reader(read_save_file)  # Creates CSV reader
    
    lines = [l for l in reader]  # Creates array of lines in file
    read_save_file.close()  # Close file
    
    current_character = False  # Boolean shows if the character already exists
    new_lines = list(lines)
    for i in range(len(lines)):  # Iterates over each line
        if lines[i][0] == username.lower():  # If the line corresponds to the username
            new_lines[i][1] = chips  # Change the chip value to new one
            current_character = True  # The character obviously exists
            if chips == 0:
                del new_lines[i]
    
    if current_character == False:  # If the character doesn't exist
        lines.append([username.lower(), chips])  # Add the new character and chip value
    write_save_file = open('scores.csv', 'w')  # Opens file for writing
    writer = csv.writer(write_save_file)  # Creates CSV writer
    writer.writerows(new_lines)  # Writes the rows
    write_save_file.close()  # Closes file
    
def draw_options(options, surface):  # Draws the options on screen 
    stick_option = pygame.image.load(os.path.join('assets', 'stick.png'))  # Loads the stick button image 
    stick_rect = stick_option.get_rect()  # Creates a rect from this image
    stick_rect.topleft = (11, 283)  # Sets the top left of the image to this point on the screen
    twist_option = pygame.image.load(os.path.join('assets', 'twist.png')) 
    twist_rect = twist_option.get_rect()
    twist_rect.topleft = (142, 283)
    double_down_option = pygame.image.load(os.path.join('assets', 'doubledown.png')) 
    double_down_rect = double_down_option.get_rect()
    double_down_rect.topleft = (354, 283)
    split_option = pygame.image.load(os.path.join('assets', 'split.png')) 
    split_rect = split_option.get_rect()
    split_rect.topleft = (483, 283)
    
    if len(options) == 2:  # If the array has two values
        surface.blit(stick_option, stick_rect)  # Draw the stick button
        surface.blit(twist_option, twist_rect)  # Draw the twist button
    elif len(options) == 3:  # If the array has three values
        surface.blit(stick_option, stick_rect)
        surface.blit(twist_option, twist_rect)
        surface.blit(double_down_option, double_down_rect)  # Draw the double down button
    elif len(options) == 4:  # If the array has four values
        surface.blit(stick_option, stick_rect)
        surface.blit(twist_option, twist_rect)
        surface.blit(double_down_option, double_down_rect)
        surface.blit(split_option, split_rect)  # Draw the split button
        
    pygame.display.update()  # Update the display
