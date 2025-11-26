import pygame
import sys
import time
from blackjack_deck import *
from constants import *

pygame.init()
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('BlackJack Pro')

def text_objects(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def game_texts(text, x, y, color=black, font_type=font_ui):
    TextSurf, TextRect = text_objects(text, font_type, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

def alert(msg, color):
    s = pygame.Surface((display_width, display_height))
    s.set_alpha(128)
    s.fill((0,0,0))
    gameDisplay.blit(s, (0,0))

    box_width, box_height = 500, 200
    box_x = (display_width / 2) - (box_width / 2) + 125
    box_y = (display_height / 2) - (box_height / 2)

    pygame.draw.rect(gameDisplay, (30, 30, 30), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(gameDisplay, white, (box_x, box_y, box_width, box_height), 3)

    TextSurf, TextRect = text_objects(msg, font_result, color)
    TextRect.center = (box_x + (box_width/2), box_y + (box_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def button(msg, x, y, w, h, ic, ac, events, action=None, args=None):
    mouse = pygame.mouse.get_pos()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if action != None:
                    if args is not None:
                        action(args)
                    else:
                        action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    TextSurf, TextRect = text_objects(msg, font_ui, black)
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
        self.playing = False 

    def newGame(self, show_dealer_all=False):
        pygame.draw.rect(gameDisplay, background_color, (250, 0, display_width-250, display_height))

        # Kartu musuh
        for i, card_name in enumerate(self.dealer.card_img):
            if i == 1 and not show_dealer_all:
                img = pygame.image.load('img/back.png').convert()
            else:
                try:
                    img = pygame.image.load('img/' + card_name + '.png').convert()
                except: continue
            gameDisplay.blit(img, (300 + (i * 110), 200))

        # Skor musuh
        if show_dealer_all:
            game_texts(f"Kartu musuh: {self.dealer.value}", 550, 150, black, font_card_text)
        else:
            if len(self.dealer.cards) > 0:
                first_val = self.dealer.cards[0][0]
                val = 10 if first_val in ['J','Q','K','10'] else (11 if first_val == 'A' else int(first_val))
                game_texts(f"Kartu musuh: {val} + ?", 550, 150, black, font_card_text)

        # Kartu player
        for i, card_name in enumerate(self.player.card_img):
            try:
                img = pygame.image.load('img/' + card_name + '.png').convert()
                gameDisplay.blit(img, (300 + (i * 110), 450))
            except: continue
            
        # Skor Player
        game_texts(f"Kartu Kamu: {self.player.value}", 550, 400, black, font_card_text)
        
        pygame.display.update()

    def display_stats(self):
        game_texts(f"Nyawa musuh: {self.enemy_hp}", 125, 80, dark_red, font_ui)
        game_texts(f"Nyawa kamu: {self.hp}", 125, 40, white, font_ui)

    def deal(self):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        self.playing = True

        if self.hp <= 0:
            self.playing = False
            self.newGame()
            
            alert("GAME OVER!", red)
            time.sleep(3)
            self.reset_game()
            return
        
        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())
            
        self.player.calc_hand()
        self.dealer.calc_hand()
        
        self.newGame()
        self.check_blackjack_start()

    def check_blackjack_start(self):
        finish = False
        msg = ""
        color = grey

        if self.player.value == 21 and self.dealer.value == 21:
            msg = "SERI!"
            self.hp += self.player.value * 2
            finish = True
        elif self.player.value == 21:
            msg = "BLACKJACK! MENANG!"
            color = green
            self.enemy_hp -= int(self.player.value * 2)
            self.hp += self.player.value
            finish = True
        elif self.dealer.value == 21:
            msg = "DEALER BLACKJACK!"
            color = red
            self.hp -= int(self.player.value * 2)
            self.enemy_hp += self.player.value
            finish = True

        if finish:
            self.playing = False
            self.newGame(show_dealer_all=True)
            alert(msg, color)
            time.sleep(3)
            self.play_or_exit()

    def hit(self):
        if not self.playing: return

        if len(self.player.card_img) >= 5:
            pygame.draw.rect(gameDisplay, background_color, (400, 360, 400, 40))
            game_texts("Maksimal 5 Kartu!", 600, 380, red, font_ui)
            pygame.display.update()
            time.sleep(0.5)
            self.newGame()
            return

        self.player.add_card(self.deck.deal())
        self.player.calc_hand()
        self.newGame()

        if self.player.value > 21:
            self.stand()
            
    def stand(self):
        if not self.playing: return
        self.playing = False 

        self.newGame(show_dealer_all=True)
        time.sleep(0.5)

        while self.dealer.value < 17 and len(self.dealer.card_img) < 6:
            self.dealer.add_card(self.deck.deal())
            self.dealer.calc_hand()
            self.newGame(show_dealer_all=True)
            time.sleep(1)
        
        self.calculate_winner()

    def calculate_winner(self):
        msg = ""
        col = grey
        
        if self.player.value > 21:
            msg = "KAMU KALAH"
            col = red
            self.enemy_hp += 10 
            self.hp -= 10
        elif self.dealer.value > 21:
            msg = "DEALER BUST! MENANG!"
            col = green
            self.enemy_hp -= self.player.value
            self.hp += self.player.value
        elif self.player.value > self.dealer.value:
            msg = "KAMU MENANG!"
            col = green
            self.enemy_hp -= self.player.value
            self.hp += self.player.value
        elif self.player.value < self.dealer.value:
            msg = "DEALER MENANG!"
            col = red
            self.enemy_hp += self.player.value
            self.hp -= self.player.value
        else:
            msg = "SERI"
            col = grey
            self.hp += 10

        alert(msg, col)   
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
        
        pygame.draw.rect(gameDisplay, background_color, (250, 0, display_width-250, display_height))
        pygame.draw.rect(gameDisplay, grey, (0, 0, 250, 700))
        
        game_texts("Siap bermain lagi?", 600, 280, black, font_ui)
        game_texts("Tekan 'Main' di kiri.", 600, 310, black, font_ui)
        pygame.display.update()

play_blackjack = Play()
running = True

gameDisplay.fill(background_color)
play_blackjack.play_or_exit() 

while running:
    pygame.draw.rect(gameDisplay, grey, (0, 0, 250, 700))

    play_blackjack.display_stats()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if play_blackjack.playing:
        button("TAMBAH", 30, 200, 170, 50, light_slat, dark_slat, events, play_blackjack.hit)
        button("BERHENTI", 30, 270, 170, 50, light_slat, dark_slat, events, play_blackjack.stand)
    else:
        button("MAIN", 30, 200, 170, 50, light_slat, dark_slat, events, play_blackjack.deal)

    button("KELUAR", 30, 500, 170, 50, light_slat, dark_red, events, play_blackjack.exit)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()