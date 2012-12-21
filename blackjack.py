# This program is a simple game of Blackjack made in Python

import random
import sys
import time

suits = ["suits", "clubs", "hearts", "diamonds"]
ranks = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
player_hand = []
dealer_hand = []

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
                        
def shuffle_deck(deck): # This function shuffles inputed deck
        new_deck = []
        random_index = []
        for i in range(52): # For every card
                random_index.append(i) # Add a number 0-51 to the array
        for i in range(len(random_index)-1): # For every value of the random_index array
                r = random_index[random.randint(0, len(random_index)-1)] # Selects a random value from random_index array
                new_deck.append(deck[r]) # Adds a random card to the new_deck array
                random_index.remove(r) # Removes the random number from random_index
        return new_deck        
                
def deal_card(deck): # This function returns a random card from inputed deck and removes it from deck
        rIndex = random.randint(0,len(deck)-1)
        c = deck[rIndex]
        deck.remove(deck[rIndex])
        return c
        
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
                        
def score_hand(hand): # This function returns the score of the inputed hand
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

def stick_twist(hand): # This function will show the user the cards and ask them to stick or twist
        print_hand(hand)
        if score_hand(hand) == 21:
                print "You have the maximum score of 21"
        elif score_hand(hand) > 21:
                print "You're bust"
        else:
                decision = raw_input("Stick or Twist?")
                if decision.upper() == "TWIST" or decision.upper() == "T":
                        hand.append(deal_card(deck))
                        stick_twist(hand)
                elif decision.upper() == "STICK" or decision.upper() == "S":
                        print "Stuck"
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

deck = new_deck()
deck = shuffle_deck(deck)

player_hand.append(deal_card(deck))
player_hand.append(deal_card(deck))
dealer_hand.append(deal_card(deck))
dealer_hand.append(deal_card(deck))

#game_intro()
#stick_twist(player_hand)
dealer_decision(dealer_hand)
print score_hand(dealer_hand)
