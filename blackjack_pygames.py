import pygame as pygame
from blackjack_deck import *
from constants import *
import sys
import time
pygame.init()

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('BlackJack')
gameDisplay.fill(background_color)
pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))


def text_objects(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def end_text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def game_texts(text, x, y, color=black):
    TextSurf, TextRect = text_objects(text, textfont, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def game_finish(text, x, y, color):
    TextSurf, TextRect = end_text_objects(text, game_end, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def black_jack(text, x, y, color):
    TextSurf, TextRect = end_text_objects(text, blackjack, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    
def button(msg, x, y, w, h, ic, ac, action=None, args=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            pygame.time.delay(100)
            if args is not None:
                action(args)
            else:
                action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    TextSurf, TextRect = text_objects(msg, font)
    TextRect.center = ((x + (w/2)), (y + (h/2)))
    gameDisplay.blit(TextSurf, TextRect)


class Play:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        self.hp = 100
        self.enemy_hp = 100
        self.amount = 5

    def display_stats(self):
        game_texts(f"Nyawa musuh: {self.enemy_hp}", 120, 80, dark_red)
        game_texts(f"Nyawa kamu: {self.hp}", 120, 40, white)
        
    def blackjack(self):

        self.dealer.calc_hand()
        self.player.calc_hand()

        show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
        
        if self.player.value == 21 and self.dealer.value == 21:
            gameDisplay.blit(show_dealer_card, (410, 200))
            black_jack("SERI!", 500, 250, grey)
            self.hp += self.player.value * 2
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value == 21:
            gameDisplay.blit(show_dealer_card, (410, 200))
            black_jack("Kamu dapat BlackJack!", 500, 250, green)
            winnings = self.player.value * 2
            self.enemy_hp -= int(winnings)
            self.hp += self.player.value
            time.sleep(4)
            self.play_or_exit()
        elif self.dealer.value == 21:
            gameDisplay.blit(show_dealer_card, (410, 200))
            black_jack("Musuh dapat BlackJack!", 500, 250, red)
            winnings = self.player.value * 2
            self.hp -= int(winnings)
            self.enemy_hp += self.player.value
            time.sleep(4)
            self.play_or_exit()
            
        self.player.value = 0
        self.dealer.value = 0

    def deal(self, amount):
        if self.hp == 0:
            game_texts("Nyawa mu telah habis!", 570, 320, red)
            time.sleep(1)
            pygame.draw.rect(gameDisplay, background_color, (250, 300, 800, 50))
            pygame.display.update()
            return
        
        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())
        self.dealer.display_cards()
        self.player.display_cards()
        self.player_card = 1
        self.dealer_card = 1
        dealer_card = pygame.image.load('img/' + self.dealer.card_img[0] + '.png').convert()
        dealer_card_2 = pygame.image.load('img/back.png').convert()
            
        player_card = pygame.image.load('img/' + self.player.card_img[0] + '.png').convert()
        player_card_2 = pygame.image.load('img/' + self.player.card_img[1] + '.png').convert()

        self.player.calc_hand()

        dealerCards = self.dealer.cards[0][0]
        visible_score = 0
        if dealerCards in ['J', 'Q', 'K', '10']:
            visible_score = 10
        elif dealerCards == 'A':
            visible_score = 11
        else:
            visible_score = int(dealerCards)        

        game_texts(f"Kartu musuh adalah: {visible_score}", 500, 150)

        gameDisplay.blit(dealer_card, (300, 200))
        gameDisplay.blit(dealer_card_2, (410, 200))

        game_texts(f"Kartu mu adalah: {self.player.value}", 500, 400)
        
        gameDisplay.blit(player_card, (300, 450))
        gameDisplay.blit(player_card_2, (410, 450))
        self.blackjack()
            

    def hit(self):
        # --- FITUR BATAS KARTU ---
        # Cek: Jika kartu sudah ada 5 (atau angka lain yang kamu mau), stop.
        if len(self.player.card_img) >= 5:
            # Tampilkan pesan peringatan sebentar
            game_texts("Maksimal 5 Kartu!", 500, 350, red)
            time.sleep(0.5)
            
            # Hapus pesan peringatannya (timpa dengan kotak background)
            # Koordinat (350, 330) disesuaikan agar menutupi teks "Maksimal..."
            pygame.draw.rect(gameDisplay, background_color, (350, 330, 300, 50))
            pygame.display.update()
            
            return # BERHENTI DI SINI (Jangan jalankan kode di bawahnya)
        # -------------------------

        # 1. Tambah Kartu
        self.player.add_card(self.deck.deal())
        self.player.calc_hand()
        
        # 2. HAPUS Area Player
        pygame.draw.rect(gameDisplay, background_color, (250, 360, 800, 250))
        game_texts(f"Kartu mu adalah: {self.player.value}", 500, 400)

        # 3. GAMBAR ULANG SEMUA
        for i, card_name in enumerate(self.player.card_img):
            try:
                img = pygame.image.load('img/' + card_name + '.png').convert()
                gameDisplay.blit(img, (300 + (i * 110), 450))
            except: pass
            
        pygame.display.update()

        # 4. Cek Bust
        if self.player.value > 21:
            self.stand()
            
            
    def stand(self):
        pygame.draw.rect(gameDisplay, background_color, (410, 200, 110, 160))

        try:
            dealer_card_img = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
            gameDisplay.blit(dealer_card_img, (410, 200))
        except :
            pass

        self.dealer.calc_hand()
        pygame.draw.rect(gameDisplay, background_color, (360, 130, 300, 50)) 
        game_texts(f"Kartu musuh adalah: {self.dealer.value}", 500, 150)
        pygame.display.update()
        time.sleep(1)

        # Fitur ngejar score player
        while self.dealer.value < 17 and len(self.dealer.card_img) < 6 :
            self.dealer.add_card(self.deck.deal())
            self.dealer.calc_hand()

            print(f"Dealer Hit! Total Kartu: {len(self.dealer.card_img)}")
            print(f"List Kartu Dealer: {self.dealer.card_img}")

            pygame.draw.rect(gameDisplay, background_color, (250, 200, 800, 160))

            for i, card_name in enumerate(self.dealer.card_img):
                try:
                    img = pygame.image.load('img/' + card_name + '.png').convert()
                    x_pos = 300 + (i * 110)
                    gameDisplay.blit(img, (x_pos, 200))
                except Exception as e:
                    print(f"Gambar ilang woy: {card_name} -> {e}")

            pygame.draw.rect(gameDisplay, background_color, (360, 130, 300, 50)) 
            game_texts(f"Kartu musuh adalah: {self.dealer.value}", 500, 150)
            
            pygame.display.update()
            time.sleep(1)
        
        self.player.calc_hand()
        print(f"Final: P {self.player.value} vs D {self.dealer.value}")

        if self.player.value <= 21 and self.player.value > self.dealer.value or self.dealer.value > 21:
            game_finish("Kamu menang!", 500, 250, green)
            self.enemy_hp -= self.player.value
            self.hp += self.player.value
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value < self.dealer.value:
            game_finish("Musuh menang!", 500, 250, red)
            self.enemy_hp += self.player.value
            self.hp -= self.player.value
            time.sleep(4)
            self.play_or_exit()
        else:
            game_finish("SERI!", 500, 250, grey)
            self.hp += 10
            time.sleep(4)
            self.play_or_exit()
        
        self.dealer.value = 0
    
    def exit(self):
        sys.exit()
    
    def play_or_exit(self):
        self.player_card = 0
        self.dealer_card = 0
        game_texts("Klik main untuk bermain lagi!", 500, 80)
        time.sleep(3)
        self.player.value = 0
        self.dealer.value = 0
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        gameDisplay.fill(background_color)
        pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
        pygame.display.update()

        
play_blackjack = Play()

running = True
gameDisplay.fill(background_color)
pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))

while running:
    pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 200))
    play_blackjack.display_stats()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        button("Main", 30, 350, 170, 50, light_slat, dark_slat, play_blackjack.deal, 10)
        button("Tambah", 30, 200, 170, 50, light_slat, dark_slat, play_blackjack.hit)
        button("Berhenti", 30, 270, 170, 50, light_slat, dark_slat, play_blackjack.stand)
    button("KELUAR", 30, 500, 170, 50, light_slat, dark_red, play_blackjack.exit)
    
    pygame.display.flip()