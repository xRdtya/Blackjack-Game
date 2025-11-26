import pygame

pygame.init()

# --- UKURAN LAYAR ---
display_width = 1000
display_height = 700

# --- WARNA DASAR (FIX ERROR) ---
white = (255, 255, 255)
black = (0, 0, 0)
grey = (220, 220, 220)

# --- PALET WARNA (CASINO THEME) ---
# Background Meja (Emerald Green)
TABLE_COLOR = (39, 119, 88) 
# Warna Pinggiran Meja (Coklat Gelap)
BORDER_COLOR = (86, 54, 53)

# Sidebar (Charcoal Blue)
SIDEBAR_COLOR = (44, 62, 80)

# Teks
TEXT_COLOR = (236, 240, 241) # Putih tulang
TEXT_GOLD = (241, 196, 15)   # Emas
TEXT_RED = (231, 76, 60)     # Merah soft

# Tombol
BTN_MAIN_COLOR = (52, 152, 219) # Biru
BTN_MAIN_HOVER = (41, 128, 185)

BTN_ACTION_COLOR = (46, 204, 113) # Hijau
BTN_ACTION_HOVER = (39, 174, 96)

BTN_STOP_COLOR = (230, 126, 34)   # Oranye
BTN_STOP_HOVER = (211, 84, 0)

BTN_EXIT_COLOR = (192, 57, 43)    # Merah bata
BTN_EXIT_HOVER = (150, 40, 40)

# Kartu
CARD_SLOT_COLOR = (30, 90, 65) 

# --- FONTS ---
font_ui = pygame.font.SysFont('verdana', 20, bold=True) 
font_card = pygame.font.SysFont('georgia', 24, bold=True)
font_result = pygame.font.SysFont('impact', 60)

# --- LAIN-LAIN ---
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

CARD_SIZE = (72, 96)