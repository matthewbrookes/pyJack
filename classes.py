import random

class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image = str(self.suit[0] + str(self.rank))
    
    def __repr__(self):
        return str(self.suit + str(self.rank))
    
    def return_suit(self):
        return self.suit
    
    def return_rank(self):
        return self.rank
    
    def return_file(self):
        return self.image
        
class Deck(object):
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
                
class Hand(object):
    def __init__(self):
        self.hand = []
    
    def twist(self, deck):
        self.hand.append(deck.return_card())
    
    def add_card(self, card):
        self.hand.append(card)
    
    def print_hand(self):
        for i in range(len(self.hand)):
                suit = self.hand[i].return_suit()
                rank = self.hand[i].return_rank()
                
                if rank == 'K':
                        rank = "King"
                elif rank == 'Q':
                        rank = "Queen"
                elif rank == 'J':
                        rank = "Jack"
                elif rank == 'A':
                        rank = "Ace"
                print "%s of %s" % (rank, suit) 
                
class DealerHand(Hand):
    def return_first_card(self):
        return self.hand[0]        