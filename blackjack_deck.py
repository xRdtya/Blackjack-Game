import random
from constants import *

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for value in RANKS:
            for suit in SUITS:
                self.cards.append((value, suit))

    def shuffle(self):
        random.shuffle(self.cards)
        

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else : 
            return None
            
class Hand(Deck):
    def __init__(self):
        self.cards = []
        self.card_img = []
        self.value = 0 

    def add_card(self, card):
        if card is None : return

        self.cards.append(card)
        
        card_name = "".join((card[0], card[1]))
        self.card_img.append(card_name)

    def calc_hand(self):
        self.value = 0

        first_card_index = [a_card[0] for a_card in self.cards]
        non_aces = [c for c in first_card_index if c != 'A']
        aces = [c for c in first_card_index if c == 'A']

        for card in non_aces:
            if card in 'JQK':
                self.value += 10
            else:
                self.value += int(card)

        for card in aces:
            if self.value <= 10:
                self.value += 11
            else:
                self.value += 1


    def display_cards(self):
        pass
