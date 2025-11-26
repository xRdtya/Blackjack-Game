import pygame

pygame.init()

display_width = 1000
display_height = 700

# Color palet
white = (255, 255, 255)
black = (0, 0, 0)
grey = (220, 220, 220)

TABLE_COLOR = (39, 119, 88) 

BORDER_COLOR = (86, 54, 53)

SIDEBAR_COLOR = (44, 62, 80)

# Teks
TEXT_COLOR = (236, 240, 241)
TEXT_GOLD = (241, 196, 15)
TEXT_RED = (231, 76, 60)

# Button
BTN_MAIN_COLOR = (52, 152, 219)
BTN_MAIN_HOVER = (41, 128, 185)

BTN_ACTION_COLOR = (46, 204, 113)
BTN_ACTION_HOVER = (39, 174, 96)

BTN_STOP_COLOR = (230, 126, 34)
BTN_STOP_HOVER = (211, 84, 0)

BTN_EXIT_COLOR = (192, 57, 43)
BTN_EXIT_HOVER = (150, 40, 40)


# Font
font_ui = pygame.font.SysFont('verdana', 20, bold=True) 
font_card = pygame.font.SysFont('georgia', 24, bold=True)
font_card_val = pygame.font.SysFont('georgia', 24, bold=True)
font_result = pygame.font.SysFont('impact', 60)
font_title = pygame.font.SysFont('impact', 30)
font_copyright = pygame.font.SysFont('arial', 13)

# Kartu
CARD_SLOT_COLOR = (30, 90, 65) 
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

CARD_SIZE = (72, 96)