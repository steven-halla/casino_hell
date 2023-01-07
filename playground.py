import random
import sys
from typing import *
import time
import pygame.freetype
from collections import defaultdict
import random


import pygame

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
WINDOWS_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
DISPLAY: pygame.Surface = pygame.display.set_mode(WINDOWS_SIZE)
FPS = 60
clock = pygame.time.Clock()
# pygame.time.get_ticks()



def nowMilliseconds() -> int:
    return round(time.time() * 1000)


class NewController:
    def __init__(self):
        self.is1Pressed: bool = False
        self.isUpPressed: bool = False
        self.isDownPressed: bool = False
        self.isTPressed: bool = False
        self.isPPressed: bool = False
        self.isOPressed: bool = False
        self.isEPressed: bool = False
        self.isMPressed: bool = False
        self.isBPressed: bool = False
        self.keyPressedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond
        self.keyReleasedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond
        self.t = defaultdict(lambda: 0)
        self.tPressed = 0


        pygame.init()


    def timeSinceKeyPressed(self, key: int):
        if key not in self.keyPressedTimes:
            return -1
        return pygame.time.get_ticks() - self.keyPressedTimes[key]

    def timeSinceKeyReleased(self, key: int):
        if key not in self.keyReleasedTimes:
            return -1
        return pygame.time.get_ticks() - self.keyReleasedTimes[key]



    def handle_keyboard_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.keyPressedTimes[event.key] = pygame.time.get_ticks()
                print(self.keyPressedTimes)
                if event.key == pygame.K_1:
                    self.is1Pressed = True
                elif event.key == pygame.K_t:

                    self.isTPressed = True
                elif event.key == pygame.K_p:
                    self.isPPressed = True
                elif event.key == pygame.K_o:
                    self.isOPressed = True
                elif event.key == pygame.K_e:
                    self.isEPressed = True
                elif event.key == pygame.K_b:
                    self.isBPressed = True
                elif event.key == pygame.K_UP:
                    self.isUpPressed = True
                elif event.key == pygame.K_DOWN:
                    self.isDownPressed = True

            elif event.type == pygame.KEYUP:
                self.keyReleasedTimes[event.key] = pygame.time.get_ticks()

                if event.key == pygame.K_1:
                    self.is1Pressed = False
                elif event.key == pygame.K_t:
                    self.isTPressed = False
                elif event.key == pygame.K_p:
                    self.isPPressed = False
                elif event.key == pygame.K_o:
                    self.isOPressed = False
                elif event.key == pygame.K_e:
                    self.isEPressed = False
                elif event.key == pygame.K_b:
                    self.isBPressed = False
                elif event.key == pygame.K_UP:
                    self.isUpPressed = False
                elif event.key == pygame.K_DOWN:
                    self.isDownPressed = False









ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
suits = ['spades', 'diamonds', 'clubs', 'hearts']

class Deck:
    def __init__(self, ranks, suits):
        self.ranks = ranks
        self.suits = suits
        self.rank_strings = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight",
                             9: "Nine", 10: "Ten", "Jack": "Jack", "Queen": "Queen", "King": "King", "Ace": "Ace"}
        self.suit_strings = {"spades": "Spades", "diamonds": "Diamonds", "clubs": "Clubs", "hearts": "Hearts"}
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit]) for suit in self.suits for rank in
                      self.ranks]
        self.cards.append(('Joker', 'red'))
        self.cards.append(('Joker', 'black'))



    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]

    def draw_card(self):

        card = self.cards.pop()
        return card

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_hand(self, num_cards):
        hand = []
        for i in range(num_cards):
            hand.append(self.draw_card())
        return hand

    def add_rank(self, rank):
        self.ranks.append(rank)
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit]) for suit in self.suits for rank in self.ranks]

    def add_suit(self, suit):
        self.suits.append(suit)
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit]) for suit in self.suits
                      for rank in self.ranks]




class Blackjack(Deck, NewController):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, ranks, suits):
        super().__init__(ranks, suits)
        NewController.__init__(self)
        self.font = pygame.font.Font(None, 36)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.message_display = ""
        self.game_state = "welcome_screen"
        self.bet = 10
        self.player_money = 100
        self.enemy_money = 100



    def start(self):
        running = True
        while running:
            clock.tick(FPS)


            self.update()

            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()

    def place_bet(self):
        if self.isUpPressed:
            self.bet += 10
            pygame.time.delay(100)
            self.isUpPressed = False

        elif self.isDownPressed:
            self.bet -= 10
            pygame.time.delay(100)
            self.isDownPressed = False

        if self.bet < 10:
            self.bet = 10

        if self.bet > 100:
            self.bet = 100

    def update(self):
        # print("update() - state: " + str(self.game_state) + ", start at: " )

        self.handle_keyboard_input()

        if self.game_state == "welcome_screen":
            # self.shuffle()
            self.message_display = "Press the 1 key to start game"
            if self.is1Pressed:
                self.game_state = "bet_phase"

        elif self.game_state == "bet_phase":
            self.message_display = "Place your bet 10 coin max. Press up and down "




    def draw(self):
        DISPLAY.fill((0,0,0))

        if self.game_state == "welcome_screen":
            DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (10, 10))

        elif self.game_state == "bet_phase":
            DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (10, 10))







game = Blackjack(SCREEN_WIDTH, SCREEN_HEIGHT, ranks, suits)
game.start()