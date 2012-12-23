# This program is a simple game of Blackjack made in Python

import random
import sys
import time

suits = ["spades", "clubs", "hearts", "diamonds"]
ranks = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
player_hand = []
dealer_hand = []
HOUSELIMIT = 20
player_chips = 200


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
        
def print_hand(hand): # This function is ran to print the hand to the user as well as the score 
        print "Your hand contains:"
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
        print "Your hand has a score of: %s" % (score_hand(hand))
        
def score_hand(hand): # This function returns the score of the inputted hand
        score = 0
        number_aces = 0
        for i in range(len(hand)):
                rank = hand[i][1]
                if rank == 'K':
                        score += 10
                elif rank == 'Q':
                        score += 10
                elif rank == 'J':
                        score += 10
                elif rank == 'A':
                        number_aces += 1
                        score += 11
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
        print "You have %s chips." % (player_chips)
        print "The house allows a maximum bet of %s chips" % (HOUSELIMIT)
        bet = raw_input("How much will you bet?")
        try:
                bet = int(bet)
        except ValueError:
                print "Please enter a whole number"
                time.sleep(0.5)
                return make_bet()
        if bet < 1 or bet > HOUSELIMIT:
                print "Please enter an amount between 1 and " + str(HOUSELIMIT)
                time.sleep(0.5)
                return make_bet()
        else:
                return bet

def stick_twist(hand): # This function will show the user the cards and ask them to stick or twist
        print_hand(hand)
        if score_hand(hand) == 21:
                if len(hand) == 2:
                        print "You have blackjack. That pays out 1.5x."
                else:
                        print "You have the maximum score of 21"
                return
        elif score_hand(hand) > 21:
                return
        elif len(hand) == 2:
                decision = raw_input("Stick(S), Twist(T) or Double Down(DD)?")
                if decision.upper() == "DOUBLE" or decision.upper() == "DOUBLE DOWN" or decision.upper() == "DD" or decision.upper() == "D":
                        global player_bet
                        print "You double down"
                        hand.append(deal_card(deck))
                        player_bet *= 2
                        print_hand(hand)
                        return
                        
                elif decision.upper() == "TWIST" or decision.upper() == "T":
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
        else:
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

def dealer_decision(hand): # This function will act as a basic dealer
        if score_hand(hand) >= 17:
                return
        else:
                dealer_hand.append(deal_card(deck))
                dealer_decision(dealer_hand)

def find_winner(pHand, dHand): # This function checks to see what the outcome of the game is
        global player_chips
        global player_bet
        if score_hand(pHand) == 21 and len(pHand) == 2:
                print "You earned %s chips for blackjack" % (str(int(round(player_bet * 1.5))))
                player_chips += int(round(player_bet * 1.5))
        elif score_hand(pHand) > 21:
                print "You're bust. You lose."
                player_chips -= player_bet
        elif score_hand(dHand) > 21:
                print "Dealer is bust. You win."
                player_chips += player_bet
        elif score_hand(dHand) == score_hand(pHand):
                print "You both score %s. You push." % (score_hand(pHand))
        else:
                if score_hand(pHand) > score_hand(dHand):
                        print "You score %s, dealer scores %s. You win." % (score_hand(pHand), score_hand(dHand))
                        player_chips += player_bet
                else:
                        print "You score %s, dealer scores %s. You lose." % (score_hand(pHand), score_hand(dHand))
                        player_chips -= player_bet

def play_again(): # This functions asks the user whether to play another hand
        print ""
        decision = raw_input("Wow, that was fun. Do you want to play again? (Yes/No)")
        if decision.upper() == "YES" or decision.upper() == "Y":
                print "Good, let us start"
                return True
        elif decision.upper() == "NO" or decision.upper() == "N":
                print "Goodbye"
                time.sleep(0.5)
                sys.exit()
        else:
                print "I'm sorry I didn't understand"
                print ""
                play_again()  

deck = new_deck()
deck = shuffle_deck(deck)

player_hand.append(deal_card(deck))
player_hand.append(deal_card(deck))

dealer_hand.append(deal_card(deck))
dealer_hand.append(deal_card(deck))
game_intro()
play = True


while play:
        # These are the main functions of the game 
        player_bet = make_bet()
        stick_twist(player_hand)
        dealer_decision(dealer_hand)
        find_winner(player_hand, dealer_hand)
        play = play_again()
        
        # The next section resets the deck and creates new hands for the user and deaker
        deck = new_deck()
        deck = shuffle_deck(deck)
        
        player_hand = []
        dealer_hand = []
        
        player_hand.append(deal_card(deck))
        player_hand.append(deal_card(deck))
        
        dealer_hand.append(deal_card(deck))
        dealer_hand.append(deal_card(deck))
        

