import pygame
import sys
import time
from blackjack_deck import *
from constants import *

# Inisialisasi
pygame.init()
clock = pygame.time.Clock()

# Setup Layar
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('BlackJack Casino Royale')

# --- 1. SETUP FONT & UKURAN KARTU ---
font_ui = pygame.font.SysFont('verdana', 18, bold=True)
font_title = pygame.font.SysFont('impact', 30)
font_card_val = pygame.font.SysFont('georgia', 24, bold=True)
# Font hasil diperbesar sedikit agar lebih gagah
font_result = pygame.font.SysFont('impact', 55)

# KONFIGURASI PRESISI
NEW_CARD_W = 60  
NEW_CARD_H = 84  
CARD_GAP = 70    
CENTER_X_AREA = 625 

# --- 2. FUNGSI GAMBAR VISUAL ---

def draw_casino_table():
    """Menggambar background meja"""
    gameDisplay.fill(TABLE_COLOR)
    
    # Sidebar
    pygame.draw.rect(gameDisplay, SIDEBAR_COLOR, (0, 0, 250, display_height))
    pygame.draw.line(gameDisplay, (30, 40, 50), (250, 0), (250, display_height), 3)

    # Dekorasi Lingkaran
    pygame.draw.circle(gameDisplay, (45, 130, 95), (CENTER_X_AREA, display_height//2), 150, 5)

    # Border Kayu
    pygame.draw.rect(gameDisplay, BORDER_COLOR, (250, 0, display_width, 15)) 
    pygame.draw.rect(gameDisplay, BORDER_COLOR, (250, display_height-15, display_width, 15)) 
    pygame.draw.rect(gameDisplay, BORDER_COLOR, (display_width-15, 0, 15, display_height)) 

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def game_texts(text, x, y, color, font_type=font_ui):
    TextSurf, TextRect = text_objects(text, font_type, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

def draw_result_panel(msg, color):
    """Menggambar Popup Hasil Multi-line"""
    # 1. Overlay Gelap
    s = pygame.Surface((display_width, display_height))
    s.set_alpha(150)
    s.fill((0,0,0))
    gameDisplay.blit(s, (0,0))

    # 2. Kotak Panel
    box_w, box_h = 500, 250
    box_x = (display_width / 2) - (box_w / 2) + 125
    box_y = (display_height / 2) - (box_h / 2)

    # Shadow
    pygame.draw.rect(gameDisplay, (20, 20, 20), (box_x+10, box_y+10, box_w, box_h), border_radius=15)
    # Background Panel (Biru Gelap Sidebar)
    pygame.draw.rect(gameDisplay, SIDEBAR_COLOR, (box_x, box_y, box_w, box_h), border_radius=15)
    # Border Emas
    pygame.draw.rect(gameDisplay, TEXT_GOLD, (box_x, box_y, box_w, box_h), 4, border_radius=15)

    # 3. LOGIKA MULTI-LINE (Pemisah Baris)
    lines = msg.split('\n')
    
    # Hitung posisi Y awal
    # Tinggi font +/- 55px. Kita atur agar pas di tengah vertikal.
    start_y = box_y + (box_h / 2) - ((len(lines) * 60) / 2) + 20

    for i, line in enumerate(lines):
        TextSurf, TextRect = text_objects(line, font_result, color)
        # Jarak antar baris 60 pixel
        TextRect.center = (box_x + (box_w/2), start_y + (i * 60))
        gameDisplay.blit(TextSurf, TextRect)
    
    pygame.display.update()

def button(msg, x, y, w, h, ic, ac, events, action=None, args=None):
    mouse = pygame.mouse.get_pos()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h), border_radius=8)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if action != None:
                    if args is not None: action(args)
                    else: action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h), border_radius=8)

    text_color = white 
    TextSurf, TextRect = text_objects(msg, font_ui, text_color)
    TextRect.center = ((x + (w/2)), (y + (h/2)))
    gameDisplay.blit(TextSurf, TextRect)

# --- CLASS PERMAINAN ---

class Play:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        self.hp = 100
        self.enemy_hp = 100
        self.playing = False 

    def redraw_game_window(self, show_dealer_all=False):
        draw_casino_table()
        
        # --- LOGIKA POSISI DINAMIS ---
        def get_start_x(total_cards):
            if total_cards < 2: total_cards = 2 
            return CENTER_X_AREA - ((total_cards * CARD_GAP) / 2) + (CARD_GAP / 2) - (NEW_CARD_W / 2)

        # --- DEALER (Y=50) ---
        dealer_y = 50
        num_dealer = len(self.dealer.card_img)
        dealer_slots = max(2, num_dealer)
        start_dealer_x = get_start_x(dealer_slots)

        for i in range(dealer_slots):
             pygame.draw.rect(gameDisplay, CARD_SLOT_COLOR, (start_dealer_x + (i * CARD_GAP), dealer_y, NEW_CARD_W, NEW_CARD_H), border_radius=5)

        for i, card_name in enumerate(self.dealer.card_img):
            if i == 1 and not show_dealer_all:
                img = pygame.image.load('img/back.png').convert()
            else:
                try:
                    img = pygame.image.load('img/' + card_name + '.png').convert()
                except: continue
            
            img = pygame.transform.scale(img, (NEW_CARD_W, NEW_CARD_H))
            gameDisplay.blit(img, (start_dealer_x + (i * CARD_GAP), dealer_y))

        # Teks Skor Dealer (Y=170)
        if show_dealer_all:
            game_texts(f"DEALER: {self.dealer.value}", CENTER_X_AREA, 170, TEXT_GOLD, font_card_val)
        else:
            if len(self.dealer.cards) > 0:
                first_val = self.dealer.cards[0][0]
                val = 10 if first_val in ['J','Q','K','10'] else (11 if first_val == 'A' else int(first_val))
                game_texts(f"DEALER: {val} + ?", CENTER_X_AREA, 170, TEXT_COLOR, font_card_val)


        # --- PLAYER (Y=560) ---
        player_y = 560
        num_player = len(self.player.card_img)
        player_slots = max(2, num_player)
        start_player_x = get_start_x(player_slots)

        for i in range(player_slots):
             pygame.draw.rect(gameDisplay, CARD_SLOT_COLOR, (start_player_x + (i * CARD_GAP), player_y, NEW_CARD_W, NEW_CARD_H), border_radius=5)

        # Teks Skor Player (Y=530)
        game_texts(f"PLAYER: {self.player.value}", CENTER_X_AREA, 530, TEXT_GOLD, font_card_val)

        for i, card_name in enumerate(self.player.card_img):
            try:
                img = pygame.image.load('img/' + card_name + '.png').convert()
                img = pygame.transform.scale(img, (NEW_CARD_W, NEW_CARD_H))
                gameDisplay.blit(img, (start_player_x + (i * CARD_GAP), player_y))
            except: continue
            
        pygame.display.update()

    def display_stats(self):
        game_texts("BLACKJACK", 125, 50, TEXT_GOLD, font_title)
        pygame.draw.line(gameDisplay, (100,100,100), (30, 75), (220, 75), 2)
        game_texts(f"Musuh HP: {self.enemy_hp}", 125, 120, TEXT_RED, font_ui)
        game_texts(f"HP Kamu: {self.hp}", 125, 160, TEXT_COLOR, font_ui)

    def deal(self, amount):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        self.playing = True

        if self.hp <= 0:
            self.playing = False
            self.redraw_game_window()
            draw_result_panel("GAME OVER!\nNYAWA HABIS", TEXT_RED)
            time.sleep(3)
            self.reset_game() 
            return
        
        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())
            
        self.player.calc_hand()
        self.dealer.calc_hand()
        
        self.redraw_game_window()
        self.check_blackjack_start()

    def hit(self):
        if not self.playing: return

        if len(self.player.card_img) >= 5:
            pygame.draw.rect(gameDisplay, TABLE_COLOR, (CENTER_X_AREA - 200, 330, 400, 40))
            game_texts("Maksimal 5 Kartu!", CENTER_X_AREA, 350, TEXT_RED)
            pygame.display.update()
            time.sleep(0.5)
            self.redraw_game_window()
            return

        self.player.add_card(self.deck.deal())
        self.player.calc_hand()
        self.redraw_game_window()

        if self.player.value > 21:
            self.playing = False 
            self.redraw_game_window(show_dealer_all=True)
            time.sleep(1)
            self.calculate_winner()
            
    def stand(self):
        if not self.playing: return
        self.playing = False 

        self.redraw_game_window(show_dealer_all=True)
        time.sleep(0.5)

        while self.dealer.value < 17 and len(self.dealer.card_img) < 6:
            self.dealer.add_card(self.deck.deal())
            self.dealer.calc_hand()
            self.redraw_game_window(show_dealer_all=True)
            time.sleep(1)
        
        self.calculate_winner()

    def check_blackjack_start(self):
        finish = False
        msg = ""
        color = TEXT_COLOR

        if self.player.value == 21 and self.dealer.value == 21:
            msg = "PUSH\n(SERI)"
            self.hp += self.player.value * 2
            finish = True
        elif self.player.value == 21:
            msg = "BLACKJACK!\nKAMU MENANG!"
            color = TEXT_GOLD
            self.enemy_hp -= int(self.player.value * 2)
            self.hp += self.player.value
            finish = True
        elif self.dealer.value == 21:
            msg = "MUSUH BLACKJACK!\nKAMU KALAH"
            color = TEXT_RED
            self.hp -= int(self.player.value * 2)
            self.enemy_hp += self.player.value
            finish = True

        if finish:
            self.playing = False
            self.redraw_game_window(show_dealer_all=True)
            draw_result_panel(msg, color)
            time.sleep(3)
            self.play_or_exit()

    def calculate_winner(self):
        msg = ""
        col = TEXT_COLOR
        
        # --- FORMAT TEKS DISESUAIKAN DI SINI ---
        if self.player.value > 21:
             msg = "KAMU BUST!\nKALAH!"
             col = TEXT_RED
             self.enemy_hp += 10 
             self.hp -= 10
        elif self.dealer.value > 21:
             # FORMAT YANG KAMU MINTA:
             # Baris 1: MUSUH
             # Baris 2: BUST! MENANG!
             msg = "MUSUH\nBUST! MENANG!" 
             col = TEXT_GOLD
             self.enemy_hp -= self.player.value
             self.hp += self.player.value
        elif self.player.value > self.dealer.value:
            msg = "KAMU\nMENANG!"
            col = TEXT_GOLD
            self.enemy_hp -= self.player.value
            self.hp += self.player.value
        elif self.player.value < self.dealer.value:
            msg = "MUSUH\nMENANG!"
            col = TEXT_RED
            self.enemy_hp += self.player.value
            self.hp -= self.player.value
        else:
            msg = "PUSH\n(SERI)"
            col = TEXT_COLOR
            self.hp += 10

        draw_result_panel(msg, col)   
        time.sleep(3)
        self.play_or_exit()
    
    def exit(self):
        sys.exit()
    
    def reset_game(self):
        self.hp = 100
        self.enemy_hp = 100
        self.play_or_exit()

    def play_or_exit(self):
        self.playing = False
        draw_casino_table() 
        
        game_texts("Siap bermain lagi?", CENTER_X_AREA, 330, TEXT_COLOR, font_ui)
        game_texts("Tekan 'MAIN' di kiri.", CENTER_X_AREA, 360, TEXT_GOLD, font_ui)
        pygame.display.update()

# --- MAIN LOOP ---

play_blackjack = Play()
running = True

gameDisplay.fill(TABLE_COLOR)
play_blackjack.play_or_exit() 

while running:
    pygame.draw.rect(gameDisplay, SIDEBAR_COLOR, (0, 0, 250, display_height))
    pygame.draw.line(gameDisplay, (30, 40, 50), (250, 0), (250, display_height), 3)

    play_blackjack.display_stats()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if play_blackjack.playing:
        button("HIT", 30, 250, 190, 50, BTN_ACTION_COLOR, BTN_ACTION_HOVER, events, play_blackjack.hit)
        button("STAND", 30, 320, 190, 50, BTN_STOP_COLOR, BTN_STOP_HOVER, events, play_blackjack.stand)
    else:
        button("MAIN", 30, 250, 190, 50, BTN_MAIN_COLOR, BTN_MAIN_HOVER, events, play_blackjack.deal, 10)

    button("KELUAR", 30, 600, 190, 50, BTN_EXIT_COLOR, BTN_EXIT_HOVER, events, play_blackjack.exit)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()