import random

class Card(object): #Each card will be an object of this class
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image = str(self.suit[0] + str(self.rank))
    
    def __repr__(self): #What to display when printing raw object
        return str(self.suit + str(self.rank))
    
    def return_suit(self):
        return self.suit
    
    def return_rank(self):
        return self.rank
    
    def return_file(self):
        return self.image
        
class Deck(object): #The deck is an object (allows support for multiple decks)
    def __init__(self):
        self.suits = ["spades", "clubs", "hearts", "diamonds"]
        self.ranks = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
        self.deck = []
        for i in range(len(self.suits)):
            for j in range(len(self.ranks)):
                card = Card(self.suits[i], self.ranks[j])
                self.deck.append(card)
                
    def shuffle(self):
        random.shuffle(self.deck)
        
    def return_deck(self):
        return self.deck
        
    def return_card(self): # This function returns a random card from inputted deck and removes it from deck
        rIndex = random.randint(0,len(self.deck)-1)
        c = self.deck[rIndex]
        self.deck.remove(self.deck[rIndex])
        return c
                
class Hand(object): #The player's hand will be a direct object of this class
    def __init__(self):
        self.hand = []
    
    def twist(self, deck): #Randomly add card from pack
        self.hand.append(deck.return_card())
    
    def add_card(self, card): #Add card manually
        self.hand.append(card)
    
    def return_hand(self):
        return self.hand
                
class DealerHand(Hand): #The dealer's hand inherits fom hand as it has special methods
    def return_first_card(self): #Returns the first card as a card object
        return self.hand[0] 

    def return_first_card_hand(self): #Returns a new hand containing only the first card
        hand = Hand()
        hand.add_card(self.hand[0])
        return hand