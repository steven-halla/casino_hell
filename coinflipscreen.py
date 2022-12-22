# import pygame
# import random
#
# # Set up the pygame display
# pygame.init()
# DISPLAY = pygame.display.set_mode((600, 600))
#
# class Screen:
#     def __init__(self, title):
#         self.title = title
#         pygame.display.set_caption(title)
#
# class CoinFlipScreen(Screen):
#     def __init__(self, min_bet, max_bet):
#         super().__init__("Casino Coin Flip Screen")
#         self.min_bet = min_bet
#         self.max_bet = max_bet
#         self.balance = 0
#         self.font = pygame.font.Font(None, 36)
#
#     def start(self):
#         self.welcomeText()
#         bet = self.placeBet()
#         result = self.flipCoin()
#         self.displayResult(result, bet)
#         self.displayBalance()
#
#     def welcomeText(self):
#         welcome_text = self.font.render(
#             f"Welcome to Coin Flip! Minimum bet is {self.min_bet} and maximum bet is {self.max_bet}.",
#             True, (255, 255, 255))
#         DISPLAY.fill((0, 0, 0))
#         DISPLAY.blit(welcome_text, (10, 10))
#         pygame.display.flip()
#
#     def placeBet(self):
#         # Prompt the player for their bet amount
#         bet_text = self.font.render("Enter your bet amount:", True, (255, 255, 255))
#         DISPLAY.blit(bet_text, (10, 50))
#         pygame.display.flip()
#
#         # Get the player's bet amount and check if it is within the limits
#         bet = int(input())
#         if bet < self.min_bet or bet > self.max_bet:
#             print("Invalid bet amount. Please enter a bet amount between the minimum and maximum limits.")
#             self.placeBet()
#         else:
#             return bet
#
#     def flipCoin(self):
#         # Generate a random number between 0 and 1 to simulate the coin flip
#         coin = random.random()
#         if coin < 0.5:
#             return "heads"
#         else:
#             return "tails"
#
#     def displayResult(self, result, bet):
#         # Display the result of the coin flip and update the player's balance
#         result_text = self.font.render(f"The coin landed on {result}!", True, (255, 255, 255))
#         DISPLAY.blit(result_text, (10, 90))
#         pygame.display.flip()
#         if result == "heads":
#             self.balance += bet
#         else:
#             self.balance -= bet
#
#     def displayBalance(self):
#         # Display the player's current balance
#         balance_text = self.font.render(f"Your current balance is: {self.balance}", True, (255, 255, 255))
#         DISPLAY.blit(balance_text, (10, 130))
#         pygame.display.flip()
#
#     def update(self, state: "GameState"):
#         controller = state.controller
#         player = state.player
#         money = state.money
#         controller.update(state)
#
#         if controller.isAPressed is True:
#             state.currentScreen = state.mainScreen
#             state.currentScreen.start(state)
#
#         if controller.isExitPressed is True:
#             state.isRunning = False
#
#         player.update(state)
#         money.update(state)
#
#     def draw(self, state: "GameState"):
#         print("white me")
#         # DISPLAY.fill(WHITE)
#         state.money.draw(state)
#         pygame.display.update()
import time

import pygame
import random

# Set up the pygame display
pygame.init()
DISPLAY = pygame.display.set_mode((600, 600))

bet_amounts = {
  "low": 100,
  "med": 500,
  "high": 1000
}
print(bet_amounts)

class CoinFlipGame:
    def __init__(self):
        self.result = str
        self.player_choice = "heads"
        self.bet = int
        self.low_bet = False
        # self.med_bet = False
        # self.high_bet = False
        self.isLPressed: bool = False
        self.isHPressed: bool = False
        self.isTPressed: bool = False
        # self.isMPressed: bool = False
        # self.isHPressed: bool = False
        self.balance = 0
        self.font = pygame.font.Font(None, 36)
        self.game_state = "welcome"
        self.welcome_text = self.font.render(
            f"Welcome to Coin Flip! Minimum bet is 50 and maximum bet is 100.",
            True, (255, 255, 255))
        self.bet_text = self.font.render("Enter your bet amount:", True, (255, 255, 255))
        self.bet_amount = self.font.render("Enter your bet amount:", True, (255, 255, 255))
        # self.result_text = self.font.render(f"The coin landed on {result}!", True, (255, 255, 255))
        self.heads = False
        self.tails = False

        self.result_text = None
        self.balance_text = None
        self.bet_sequence = False
        self.choice_sequence = False

    def flipCoin(self):
        # Generate a random number between 0 and 1 to simulate the coin flip
        coin = random.random()
        if coin < 0.5:
            print("heads")
            self.result = "heads"
        else:
            print("tails")
            self.result = "tails"

    # def player_coin_side_choice(self):


    def start(self):
        while True:
            DISPLAY.fill((0, 0, 0))
            DISPLAY.blit(self.welcome_text, (10, 10))
            DISPLAY.blit(self.bet_text, (10, 50))
            pygame.display.flip()
            print("place your bet ammount")
            keys = pygame.key.get_pressed()
            self.bet_sequence = True
            for event in pygame.event.get():
                if self.bet_sequence == True:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_l:
                            self.isLPressed = True
                            self.low_bet = True
                            self.bet = 50
                            self.bet_sequence = False

                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_l:
                            self.isLPressed = False
                            self.bet_sequence = False

                if self.choice_sequence == True:
                    print("choice seqeunce active dfsfsdfsffsafsfdsafsf")

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_h:
                            self.isHPressed = True

                            self.player_choice = "heads"
                            self.choice_sequence = False
                        elif event.key == pygame.K_t:
                            self.isTPressed = True
                            print("pressed t")
                            self.player_choice = "tails"
                            self.choice_sequence = False

                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_h:
                            self.isHPressed = False
                            self.choice_sequence = False
                        if event.key == pygame.K_t:
                            self.isTPressed = False
                            self.choice_sequence = False

            print("Im back")
            # print("how much would you like to bet? L for 100")
            # print(self.bet)
            pygame.display.flip()
            time.sleep(2)
            self.flipCoin()
            print("flipping coin")
            # print(self.result)
            self.choice_sequence = True
            time.sleep(4)
            print("the players choice is")
            print(str(self.player_choice))





    # def start(self):
    #     self.game_state = "welcome"
    #     while True:
    #         self.update()
    #         self.draw()

    # def update(self):
    #     if self.game_state == "welcome":
    #         # Prompt the player for their bet amount
    #         DISPLAY.fill((0, 0, 0))
    #         DISPLAY.blit(self.welcome_text, (10, 10))
    #         DISPLAY.blit(self.bet_text, (10, 50))
    #         pygame.display.flip()
    #
    #         # Check if the player has pressed a key to select their bet amount
    #         # keys = pygame.key.get_pressed()
    #         for event in pygame.event.get():
    #             if event.type == pygame.KEYDOWN:
    #                 print("Hi R")
    #                 self.bet = 50
    #                 # self.game_state = "flip"
    #                 self.isRPressed = True
    #
    #             elif event.type == pygame.KEYUP:
    #                 if event.key == pygame.K_r:
    #                     print("Bye R")
    #                     self.isRPressed = False
    #
    #
    #         # Add additional checks for other bet amounts here
    #         else:
    #             self.bet = 0
    #         if self.bet != 0:
    #             self.game_state = "flip"

    # def draw(self):
    #     if self.game_state == "welcome":
    #         DISPLAY.fill((0, 0, 0))
    #         DISPLAY.blit(self.welcome_text, (10, 10))
    #         DISPLAY.blit(self.bet_text, (10, 50))
    #         pygame.display.flip()
    #
    #     elif self.game_state == "result":
    #         DISPLAY.fill((0, 0, 0))
    #         DISPLAY.blit(self.result_text, (10, 10))
    #         DISPLAY.blit(self.balance_text, (10, 50))
    #         pygame.display.flip()


coin_flip_game = CoinFlipGame()
coin_flip_game.start()