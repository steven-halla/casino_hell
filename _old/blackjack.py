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
        self.isBlackJack =  False
        self.suits = suits
        self.rank_strings = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight",
                             9: "Nine", 10: "Ten", "Jack": "Jack", "Queen": "Queen", "King": "King", "Ace": "Ace"}
        self.suit_strings = {"spades": "Spades", "diamonds": "Diamonds", "clubs": "Clubs", "hearts": "Hearts"}
        self.rank_values = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, "Jack": 10, "Queen": 10,
                            "King": 10, "Ace": 11}
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit], self.rank_values[rank]) for suit in self.suits
                      for rank in self.ranks]
        self.black_jack_counter = 0


        for suit in self.suits:
            if "Ace" in self.ranks:
                self.cards.append(("Ace", suit, 1))
                self.cards.append(("Ace", suit, 11))
        # self.cards.append(('Joker', 'red', 0))
        # self.cards.append(('Joker', 'black', 0))

    def compute_hand_value(self, hand: List[Tuple[str, str, int]]) -> int:
        # Initialize the point value of the hand to 0
        hand_value = 0
        # Initialize a counter to track the number of aces in the hand
        num_aces = 0
        # Iterate through the cards in the hand
        for card in hand:
            # If the card is an ace, increment the counter
            if card[0] == "Ace":
                num_aces += 1
            # Add the point value of the card to the hand value
            hand_value += card[2]
        # print(f"num_aces: {num_aces}")
        # print(f"initial hand_value: {hand_value}")
        # While there is at least one ace in the hand and the hand value is more than 21,
        # subtract 10 from the hand value to give the ace a value of 1 instead of 11
        while num_aces > 0 and hand_value > 21:
            hand_value -= 10
            num_aces -= 1
        # print(f"final hand_value: {hand_value}")

        if len(hand) == 2 and (
                (hand[0][0] == "Ace" and hand[1][0] in (10, "Jack", "Queen", "King")) or
                (hand[1][0] == "Ace" and hand[0][0] in (10, "Jack", "Queen", "King"))
        ):
            print("you got the black jack")
            self.black_jack_counter += 1

            print("black jack counter at:" + str(self.black_jack_counter))

        # if len(hand) == 2 and (self.rank_values[hand[0][0]] == 10 or self.rank_values[hand[1][0]] == 10):
        #     print("Player has a 10-point value card")
        #
        #     print("The player has 1 ace and 1 10-point card in their hand, and there are only 2 cards in the hand.")
        # Return the final hand value

        # if len(hand) == 2 and hand[0][1] == 11 and hand[1][1] == 10:
        #     print("Player has a Blackjack")

        return hand_value

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
        self.second_message_display = ""
        self.thrid_message_display = ""
        self.game_state = "welcome_screen"
        self.bet = 10
        self.player_money = 100
        self.enemy_money = 100
        self.player_score = 0
        self.enemy_score = 0
        self.player_hand = [(5, 'Diamonds', 5), (5, 'Spades', 5)]
        self.enemy_hand = [(10, 'Hearts', 10), (6, 'Hearts', 6)]
        self.choices = ["Ready", "Draw", "Magic"]
        self.current_index = 0
        self.ace_value = 1

        self.player_black_jack_win = False
        self.enemy_black_jack_win = False
        self.black_jack_draw = False

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
            self.shuffle()
            self.message_display = "Press the 1 key to start game or O to quit"
            if self.is1Pressed:
                self.game_state = "bet_phase"
            elif self.isOPressed:
                print("quiting game")

        elif self.game_state == "bet_phase":
            self.message_display = "Place your bet 10 coin max. Press up and down. Press T when ready "
            self.place_bet()
            if self.isTPressed:
                self.game_state = "draw_phase"
                self.isTPressed = False

        elif self.game_state == "draw_phase":
            # need to reformat have a reset function
            self.message_display = "dealing the cards"
            self.second_message_display = ""
            self.thrid_message_display = ""
            self.black_jack_counter = 0
            self.player_black_jack_win = False
            self.enemy_black_jack_win = False
            self.black_jack_draw = False


            # self.player_hand = self.draw_hand(2)
            print("Player hand is" + str(self.player_hand))
            self.player_score = self.compute_hand_value(self.player_hand)


            # print("i'm a blackjack")
            # self.thrid_message_display = "player got a black jack auto win, now you get X3 of your bet11"
            # self.game_state = "results_screen"



            print("Player score is: " + str(self.player_score))
            # Check if the player has an ACE in their hand
            if self.black_jack_counter > 0:
                print("Player black jack win set to true")
                self.player_black_jack_win = True
            else:
                self.player_black_jack_win = False

            #################################need to test aces if a player gets multiple aces



            # If the player has an ACE, check which value is better for the player

            self.black_jack_counter = 0


            # self.enemy_hand = self.draw_hand(2)
            print("Enemy hand is" + str(self.enemy_hand))
            self.enemy_score = self.compute_hand_value(self.enemy_hand)
            print("enemy score is: " + str(self.enemy_score))
            if self.black_jack_counter > 0:
                print("Enemy black jack win set to true")

                self.enemy_black_jack_win = True
            elif self.black_jack_counter == 0:
                self.enemy_black_jack_win = False

            print(self.player_black_jack_win)

            if self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                self.black_jack_draw = True
                self.thrid_message_display = "Its a draw"
                print("Its a draw")
                self.game_state = "results_screen"
            elif self.player_black_jack_win == True and self.enemy_black_jack_win == False:

                self.thrid_message_display = "player got  a black jack X 3 winnings"
                self.game_state = "results_screen"
            elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                self.thrid_message_display ="enemy got a black jack now you lose X 3 winnings"
                self.game_state = "results_screen"

            else:
                self.game_state = "menu_screen"








        elif self.game_state == "player_draw_one_card":
            self.player_hand += self.draw_hand(1)
            self.compute_hand_value(self.player_hand)
            self.player_score = self.compute_hand_value(self.player_hand)
            if self.player_score > 10:
                print("hi greater than 10")
                self.rank_values["Ace"] = 1

            print("Player hand is now" + str(self.player_hand))
            print("Player score is now" + str(self.player_score))
            if self.player_score > 21:
                self.player_money -= self.bet
                self.enemy_money += self.bet
                self.second_message_display = "player bust you lose"
                self.game_state = "results_screen"


            self.game_state = "menu_screen"

        elif self.game_state == "enemy_draw_one_card":
            while self.enemy_score < 17 and self.enemy_score <= self.player_score:


                self.enemy_hand += self.draw_hand(1)
                self.compute_hand_value(self.enemy_hand)
                self.enemy_score = self.compute_hand_value(self.enemy_hand)
                print("enemy hand is now" + str(self.enemy_hand))
                print("enemy score is now" + str(self.enemy_score))



                if self.enemy_score > 21:
                    self.player_money += self.bet
                    self.enemy_money -= self.bet
                    print("enemy bust")
                    self.second_message_display = "enemy bust player wins"
                    self.game_state = "results_screen"

            if self.enemy_score > 16 and self.enemy_score < 22:
                print("stay here")
                self.game_state = "results_screen"




        elif self.game_state == "menu_screen":
            self.message_display = "Menu screen press T to select"
            if self.player_score > 21:
                self.message_display = "You bust and lose."
                self.game_state = "results_screen"

            if self.isUpPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) - 1
                else:
                    self.current_index -= 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                self.isUpPressed = False

            if self.isDownPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) + 1
                else:
                    self.current_index += 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                self.isDownPressed = False


        elif self.game_state == "results_screen":
            if self.player_score > self.enemy_score and self.player_score < 22:
                self.second_message_display = "You win player"
            elif self.player_score < self.enemy_score and self.enemy_score < 22:
                self.second_message_display = "You lose player "

            elif self.player_score == self.enemy_score:
                self.second_message_display = "It's a draw nobody wins"

            self.message_display = "Press B to play again or O to quit"

            if self.isBPressed:
                self.game_state = "welcome_screen"
                self.isBPressed = False

            elif self.isOPressed:
                print("Exit")
                self.isOPressed = False







    def draw(self):
        DISPLAY.fill((0,0,0))

        if self.game_state == "welcome_screen":
            DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (10, 10))


        elif self.game_state == "bet_phase":
            DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.font.render(f"{self.bet}", True, (255, 255, 255)), (10, 105))


        elif self.game_state == "menu_screen":
            DISPLAY.blit(
                self.font.render(f"{self.message_display}", True, (255, 255, 255)),
                (200, 10))
            DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (700, 160))

            DISPLAY.blit(
                self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                (700, 210))

            DISPLAY.blit(
                self.font.render(f"{self.choices[2]}", True, (255, 255, 255)),
                (700, 260))

            if self.current_index == 0:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))
                if self.isTPressed:
                    print("we are going to the next phase")
                    self.game_state = "enemy_draw_one_card"
                    self.isTPressed = False
                    # self.betPhase = True
                    # self.game_state = "bet_phase"


            elif self.current_index == 1:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))
                if self.isTPressed:
                    print("Time to draw a card")
                    self.game_state = "player_draw_one_card"
                    self.isTPressed = False



            elif self.current_index == 2:
                DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))
                if self.isTPressed:
                    print("In the future you can cast magic here")
                    self.isTPressed = False

            DISPLAY.blit(self.font.render(f"Player bet:{self.bet}", True, (255, 255, 255)), (10, 100))


            DISPLAY.blit(self.font.render(f"Player Hand{self.player_hand}", True, (255, 255, 255)), (10, 300))
            DISPLAY.blit(self.font.render(f"Player score:{self.player_score}", True, (255, 255, 255)), (10, 350))
            DISPLAY.blit(self.font.render(f"Player money:{self.player_money}", True, (255, 255, 255)), (10, 400))

            DISPLAY.blit(self.font.render(f"Enemy Hand{self.enemy_hand}", True, (255, 255, 255)), (10, 450))
            DISPLAY.blit(self.font.render(f"Enemy score:{self.enemy_score}", True, (255, 255, 255)), (10, 500))
            DISPLAY.blit(self.font.render(f"Enemy money:{self.enemy_money}", True, (255, 255, 255)), (10, 550))

        elif self.game_state == "results_screen":
            DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (10, 10))
            DISPLAY.blit(self.font.render(f"{self.second_message_display}", True, (255, 255, 255)), (10, 45))
            DISPLAY.blit(self.font.render(f"{self.thrid_message_display}", True, (255, 255, 255)), (10, 100))


            DISPLAY.blit(self.font.render(f"Player bet:{self.bet}", True, (255, 255, 255)), (10, 155))


            DISPLAY.blit(self.font.render(f"Player Hand{self.player_hand}", True, (255, 255, 255)), (10, 300))
            DISPLAY.blit(self.font.render(f"Player score:{self.player_score}", True, (255, 255, 255)), (10, 350))
            DISPLAY.blit(self.font.render(f"Player money:{self.player_money}", True, (255, 255, 255)), (10, 400))

            DISPLAY.blit(self.font.render(f"Enemy Hand{self.enemy_hand}", True, (255, 255, 255)), (10, 450))
            DISPLAY.blit(self.font.render(f"Enemy score:{self.enemy_score}", True, (255, 255, 255)), (10, 500))
            DISPLAY.blit(self.font.render(f"Enemy money:{self.enemy_money}", True, (255, 255, 255)), (10, 550))





game = Blackjack(SCREEN_WIDTH, SCREEN_HEIGHT, ranks, suits)
game.start()