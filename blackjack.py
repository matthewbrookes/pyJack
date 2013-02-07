# This program is a simple game of Blackjack made in Python

import random
import sys
import time
import math

# Creates arrays to hold hands and the different suits and ranks
suits = ["spades", "clubs", "hearts", "diamonds"]
ranks = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
player_hand = []
player_hand2 = []
dealer_hand = []

split = False # This variable holds the boolean value of whether the player has split or not

#These variables relate to betting
HOUSELIMIT = 80
player_chips = 400

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
        rIndex = random.randint(0,len(deck)-1) # Random card from pack
        c = deck[rIndex] # Gets this card
        deck.remove(deck[rIndex]) # And removes it rrom the deck
        return c # Returns card
        
def print_hand(hand): # This function is ran to print the hand to the user as well as the score 
        print "Your hand contains:"
        print ""
        for i in range(len(hand)):
                suit = hand[i][0]
                rank = hand[i][1]
                
                #Prints the rank in a more friendly format
                if rank == 'K':
                        rank = "King"
                elif rank == 'Q':
                        rank = "Queen"
                elif rank == 'J':
                        rank = "Jack"
                elif rank == 'A':
                        rank = "Ace"
                print "%s of %s" % (rank, suit) 
        print ""
        print "Your hand has a score of: %s" % (score_hand(hand))

def print_dealer_hand(hand): # This function will print the dealer's hand
        print "The dealer's hand contains:"
        print ""
        for i in range(len(hand)):
                suit = hand[i][0]
                rank = hand[i][1]
                if rank == 'K':
                        rank = "King"
                elif rank == 'Q':
                        rank = "Queen"
                elif rank == 'J':
                        rank = "Jack"
                elif rank == 'A':
                        rank = "Ace"
                print "%s of %s" % (rank, suit) 
        print ""
        print "The hand has a score of: %s" % (score_hand(hand))
        
def check_insurance(hand): # This function will check if the player needs to add an insurance bet and will print the dealer's face up card if not
        #These variables need to refer to the global variables
        global player_bet
        global player_chips
        
        contains_ace = False # Boolean will be true if the hand contains an ace
        if hand[0][1] == 'A': # If the dealer's first card is an ace
                contains_ace = True
        if contains_ace == True:
                print ""
                print "The dealer shows an Ace"
                print "You can choose to place a bet upto %s chips" % (int(math.floor(player_bet/2))) # Gets an insurance bet from player
                insurance = raw_input("How much will you bet?")
                try: #Try to convert inputted insurance to an integer
                        insurance = int(insurance)
                except ValueError:
                        print "Please enter a whole number"
                        time.sleep(0.5)
                        check_insurance(hand)
                if insurance > math.floor(player_bet/2) or insurance < 0: # If the bet is invalid
                        print "Please enter a valid bet"
                        time.sleep(0.5)
                        check_insurance(hand)
                else:
                        print_dealer_hand(hand)
                        if score_hand(hand) == 21:
                                print "The dealer shows blackjack. You will be paid %s chips" % (int(insurance * 2))
                                player_chips += (insurance * 2) # Pay the player the insurance bet
                                time.sleep(0.5)
                                print ""
                                return
                        else:
                                print "The dealer did not show blackjack. You will lose %s chips" % (int(insurance))
                                player_chips -= insurance # Subtract the insurance bet from the player's chips
                                time.sleep(0.5)
                                print ""
                                return
        else: # The player has no aces in his hand
                print ""
                rank = hand[0][1]
                if rank == 'K':
                        rank = "King"
                elif rank == 'Q':
                        rank = "Queen"
                elif rank == 'J':
                        rank = "Jack"
                elif rank == 'A':
                        rank = "Ace"
                print "The dealer's face up card is the %s of %s" % (rank, hand[0][0])
                print ""
                return                
                
def score_hand(hand): # This function returns the score of the inputted hand
        score = 0
        number_aces = 0
        for i in range(len(hand)):
                rank = hand[i][1]
                # Picture cards have a value of 10
                if rank == 'K':
                        score += 10
                elif rank == 'Q':
                        score += 10
                elif rank == 'J':
                        score += 10
                # Aces are first given a value of 11 so we can subtract 10 is necessary
                elif rank == 'A':
                        number_aces += 1
                        score += 11
                # Otherwise it's a normal card
                else:
                        score += rank
        for i in range(number_aces): # This loop will only be executed for each ace in the hand
                if score > 21: # If the score is greater than 21 then we want to remove 10
                        score -= 10
                        number_aces -= 1
                else:
                        number_aces -= 1
        return score        
        
def game_intro(): # This function is ran at the start to introduce the game
        print "Welcome to pyJack, a game of blackjack made in Python"
        print "You will play against an AI dealer programmed like a professional"
        decision = str(raw_input("Shall we begin? (Yes/No)"))
        if decision.upper() == "YES" or decision.upper() == "Y":
                print "Good, let us start"
        elif decision.upper() == "NO" or decision.upper() == "N":
                print "Goodbye"
                time.sleep(0.5)
                sys.exit()
        else:
                print "I'm sorry I didn't understand"
                print ""
                game_intro()       
                        
def make_bet(): # This function will ask the user how much to bet this hand  
        print "You have %s chips." % (player_chips) # Tells the user how many chips he has
        if player_chips > 0: # If the player has chips remaining
                print "The house allows a maximum bet of %s chips" % (HOUSELIMIT)
                bet = raw_input("How much will you bet?")
                try: # Try to convert inputted bet to an integer 
                        bet = int(bet)
                except ValueError:
                        print "Please enter a whole number"
                        time.sleep(0.5)
                        return make_bet()
                if bet < 1 or bet > HOUSELIMIT: # If the bet is less than 0 or more than house limit
                        print "Please enter an amount between 1 and " + str(HOUSELIMIT)
                        time.sleep(0.5)
                        return make_bet()
                elif bet > player_chips: # If the player bets more than he has chips remaining
                        print "Please enter an amount between 1 and " + str(player_chips)
                        return make_bet()
                else:
                        return bet
        else: #The player has no more chips and the game must close
                print "You have run out of chips"
                print "pyJack will now close"
                time.sleep(0.5)
                sys.exit()

def stick_twist(hand): # This function will show the user the cards and ask them to stick, twist double down or split
        #Use global variables
        global player_chips 
        global player_bet
        global split
        
        print_hand(hand)
        if score_hand(hand) == 21: 
                if len(hand) == 2: # If player has blackjack
                        print "You have blackjack. That pays out 1.5x."
                else:
                        print "You have the maximum score of 21"
                return
        elif score_hand(hand) > 21: # If player is bust
                return
        elif len(hand) == 2 and player_bet * 2 <= player_chips: # If player has two cards and can double down
                if hand[0][1] == hand[1][1] and split == False: #If player's first two cards are the same rank and he has not split
                        decision = raw_input("Stick(S), Twist(T), Split(SP) or Double Down(DD)?") # Presents player with options
                        if decision.upper() == "DOUBLE" or decision.upper() == "DOUBLE DOWN" or decision.upper() == "DD" or decision.upper() == "D": # If player chooses the double down
                                print "You double down"
                                hand.append(deal_card(deck)) # Add 1 more card
                                player_bet *= 2 # Double bet
                                print_hand(hand) # Print hand
                                return       
                        elif decision.upper() == "TWIST" or decision.upper() == "T": # If player chooses to twist
                                hand.append(deal_card(deck)) # Add 1 more card
                                print "You Twist."
                                stick_twist(hand) #Repeats function
                        elif decision.upper() == "STICK" or decision.upper() == "S": # If player sticks
                                print "You stick."
                                return
                        elif decision.upper() == "SPLIT" or decision.upper() == "SP": # If player splits
                                split = True # So the program knows the player has split
                                # Use the global variables
                                global player_hand2
                                global player_hand
                                
                                player_hand2.append(hand[1]) # Adds player's second card to second hand
                                player_hand2.append(deal_card(deck)) # Adds another card
                                player_hand.remove(hand[1]) # Removes player's second card from first hand
                                player_hand.append(deal_card(deck)) # Adds another card
                                split_hand(player_hand, player_hand2) # Function is only for a split hand
                                
                        else: # If the user entered an invalid option
                                print "I'm sorry I didn't understand"
                                print ""
                                time.sleep(0.5)
                                stick_twist(hand)
                elif split == False: # If the player hasn't split and cards aren't the same rank
                        decision = raw_input("Stick(S), Twist(T) or Double Down(DD)?")
                        if decision.upper() == "DOUBLE" or decision.upper() == "DOUBLE DOWN" or decision.upper() == "DD" or decision.upper() == "D": # If player chooses the double down
                                print "You double down"
                                hand.append(deal_card(deck)) # Add 1 more card
                                player_bet *= 2 # Double bet
                                print_hand(hand) # Print hand
                                return       
                                
                        elif decision.upper() == "TWIST" or decision.upper() == "T": # If player chooses to twist
                                hand.append(deal_card(deck)) # Add 1 more card
                                print "You Twist."
                                stick_twist(hand) #Repeats function
                        elif decision.upper() == "STICK" or decision.upper() == "S": # If player chooses to stick
                                print "You stick."
                                return
                        else: # Player has entered something invlid
                                print "I'm sorry I didn't understand"
                                print ""
                                time.sleep(0.5)
                                stick_twist(hand)
                else: # Display the basic options
                        decision = raw_input("Stick(S) or Twist(T)?")
                        if decision.upper() == "TWIST" or decision.upper() == "T":
                                hand.append(deal_card(deck))
                                print "You Twist."
                                stick_twist(hand)
                        elif decision.upper() == "STICK" or decision.upper() == "S":
                                print "You stick."
                                return
                        else:
                                print "I'm sorry I didn't understand"
                                print ""
                                time.sleep(0.5)
                                stick_twist(hand)
        else: # The player has more than 2 cards
                decision = raw_input("Stick(S) or Twist(T)?")
                if decision.upper() == "TWIST" or decision.upper() == "T":
                        hand.append(deal_card(deck))
                        print "You Twist."
                        stick_twist(hand)
                elif decision.upper() == "STICK" or decision.upper() == "S":
                        print "You stick."
                        return
                else:
                        print "I'm sorry I didn't understand"
                        print ""
                        time.sleep(0.5)
                        stick_twist(hand)

def split_hand(hand1, hand2): # This function walks the user through a split hand
        # Goes through the first hand
        print "This is your first hand"
        stick_twist(hand1)
        time.sleep(1)
        print ""
        # Goes through the second hand
        print "This is your second hand"
        stick_twist(hand2)
        print ""
        time.sleep(1)
        # Process the dealer
        dealer_decision(dealer_hand)
        # Show how the first hand did
        print "How does your first hand fair?"
        find_winner(hand1, dealer_hand)
        print ""
        # Shows how the second hand did
        print "How does your second hand fair?"
        find_winner(hand2, dealer_hand)

def dealer_decision(hand): # This function will act as a basic dealer
        print_dealer_hand(hand)
        if score_hand(hand) > 16: # If the score is greater than 16 another card shouldn't be added
                return
        else: #The dealer should be dealt a new card
                dealer_hand.append(deal_card(deck))
                time.sleep(0.5)
                print ""
                dealer_decision(dealer_hand)

def find_winner(pHand, dHand): # This function checks to see what the outcome of the game is
        # Use the global variables
        global player_chips
        global player_bet
        
        if score_hand(pHand) == 21 and len(pHand) == 2: # If the player has blackjack
                print "You earned %s chips for blackjack" % (str(int(round(player_bet * 1.5))))
                player_chips += int(round(player_bet * 1.5)) # Payout 1.5x your bet
        elif score_hand(pHand) > 21: # If player is bust
                print "You're bust. You lose."
                player_chips -= player_bet # Subtract bet from chips
        elif score_hand(dHand) > 21: # If dealer is bust
                print "Dealer is bust. You win."
                player_chips += player_bet # Add bet to chips
        elif score_hand(dHand) == score_hand(pHand): # If the scores are equal
                print "You both score %s. You push." % (score_hand(pHand))
        else:
                if score_hand(pHand) > score_hand(dHand): # If the player scores higher than the dealer
                        print "You score %s, dealer scores %s. You win." % (score_hand(pHand), score_hand(dHand))
                        player_chips += player_bet # Adds bet to chips
                else: # If dealer scores higher than the player
                        print "You score %s, dealer scores %s. You lose." % (score_hand(pHand), score_hand(dHand))
                        player_chips -= player_bet # Subtracts bet from chips

def play_again(): # This functions asks the user whether to play another hand
        print ""
        decision = raw_input("Wow, that was fun. Do you want to play again? (Yes/No)")
        if decision.upper() == "YES" or decision.upper() == "Y": # If player chooses yes
                print "Good, let us start"
                return True
        elif decision.upper() == "NO" or decision.upper() == "N": # If player chooses no
                print "Goodbye"
                time.sleep(0.5)
                sys.exit()
        else: # If player makes an invalid decision
                print "I'm sorry I didn't understand"
                print ""
                play_again()  

# Create a new deck and shuffle it
deck = new_deck()
deck = shuffle_deck(deck)

# Make a new hand
player_hand.append(deal_card(deck))
player_hand.append(deal_card(deck))

# Make a dealer's hand
dealer_hand.append(deal_card(deck))
dealer_hand.append(deal_card(deck))

game_intro() # Show the intro
play = True


while play:
        # These are the main functions of the game
        player_bet = make_bet()
        check_insurance(dealer_hand)
        stick_twist(player_hand)
        time.sleep(0.5)
        if split == False: # If the player didn't split
                dealer_decision(dealer_hand)
                find_winner(player_hand, dealer_hand)
        
        play = play_again() # Does the user want to play again
        
        # The next section resets the deck and creates new hands for the user and dealer
        deck = new_deck()
        deck = shuffle_deck(deck)
        
        player_hand = []
        player_hand2 = []
        dealer_hand = []
        split = False
        
        player_hand.append(deal_card(deck))
        player_hand.append(deal_card(deck))
        
        dealer_hand.append(deal_card(deck))
        dealer_hand.append(deal_card(deck))
        

