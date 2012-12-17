import random

suits = ["suits", "clubs", "hearts", "diamonds"]
ranks = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
deck = []

def create_deck():
        for i in range(4):
                card = []
                for j in range(13):
                        suit = suits[i]
                        rank = ranks[j]
                        card.append(suit)
                        card.append(rank)
                        deck.append(card)
                        card = []
                        
def shuffle_deck(deck):
        new_deck = []
        random_index = []
        for i in range(52):
                random_index.append(i)
        for i in range(len(random_index)-1):
                r = random_index[random.randint(0, len(random_index)-1)]
                new_deck.append(deck[r])
                random_index.remove(r)
        return new_deck        
                
create_deck()
deck = shuffle_deck(deck)
print deck
