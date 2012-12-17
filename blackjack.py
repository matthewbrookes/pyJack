import random

suits = ["suits", "clubs", "hearts", "diamonds"]
ranks = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
cards = []

def create_deck():
        for i in range(4):
                card = []
                for j in range(13):
                        suit = suits[i]
                        rank = ranks[j]
                        card.append(suit)
                        card.append(rank)
                        cards.append(card)
                        card = []
                        

create_deck()
print cards
