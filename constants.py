import pygame as pygame

display_width = 900
display_height = 700

background_color = (34,139,34)
grey = (220,220,220)
black = (0,0,0)
green = (0, 200, 0)
red = (255,0,0)
light_red = (200, 0, 0)
light_slat = (119,136,153)
dark_slat = (47, 79, 79)
dark_red = (255, 0, 0)
gold = (255, 215, 0)
white = (255, 255, 255)
pygame.init()
font = pygame.font.SysFont("Arial", 20)
textfont = pygame.font.SysFont('Comic Sans MS', 25)
game_end = pygame.font.SysFont('dejavusans', 100)
blackjack = pygame.font.SysFont('roboto', 70)
font_result = pygame.font.SysFont('impact', 50)
font_ui = pygame.font.SysFont('arial', 20, bold=True)
font_card_text = pygame.font.SysFont('timesnewroman', 25, bold=True) 


SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)

