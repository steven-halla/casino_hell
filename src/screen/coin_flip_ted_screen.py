import random

import pygame
import sys

from screen.screen import Screen


class CoinFlipTedScreen(Screen):
    def __init__(self):
        super().__init__("Casino Coin flip  Screen")
        self.result = ""
        self.play_again = True
        self.players_side = ""
        self.new_font = pygame.font.Font(None, 36)
        self.message_display = ""
        self.second_message_display = ""
        self.third_message_display = ""
        self.magic_player_message_display = ""
        self.magic_enemy_message_display = ""
        self.choices = ["Heads", "Tails"]
        self.yes_or_no_menu = ["Yes", "No"]
        self.magic_menu_selector = []
        self.game_state = "welcome_screen"
        self.choice_sequence = True
        self.bet = 0
        self.font = pygame.font.Font(None, 36)
        self.coinFlipTedMoney = 100
        self.coinFlipTedDefeated = False
        self.current_index = 0
        self.yes_no_current_index = 0
        self.magic_menu_index = 0
        self.leave_or_replay_index = 0
        self.high_exp = False
        self.low_exp = False
        self.bluff_text_list = [
            "I bet you triple my bet that your coin will land on tails 3 times in a row",
            "Hehehe, your on sucker"]
        self.reveal_hand = False

    def giveExp(self, state: "GameState"):
        if self.high_exp == True:
            state.player.exp += 15
        elif self.low_exp == True:
            state.player.exp += 50

    def place_bet(self, state: "GameState"):
        controller = state.controller
        controller.update()

        if controller.isUpPressed:
            self.bet += 10
            pygame.time.delay(200)
            self.isUpPressed = False

        elif controller.isDownPressed:
            self.bet -= 10
            pygame.time.delay(200)
            self.isDownPressed = False

        if self.bet < 10:
            self.bet = 10

        if self.bet > 100:
            self.bet = 100

        if self.bet > self.coinFlipTedMoney:
            self.bet = self.coinFlipTedMoney

    def flipCoin(self):
        coin = random.random()

        if coin < 0.6:
            print("coin landed on tails")
            self.result = "tails"
        else:
            print("coin landed on heads")
            self.result = "heads"

    def update(self, state: "GameState"):
        if self.coinFlipTedMoney <= 0:
            self.coinFlipTedDefeated = True
        # Update the controller
        controller = state.controller
        controller.update()

        if state.player.stamina_points < 2:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

        if self.game_state == "welcome_screen":

            self.message_display = "This is the welcome screen. Press R to continue"
            self.second_message_display = ""
            self.third_message_display = ""
            self.reveal_hand = False

            if controller.isRPressed:
                if self.bet >= 10 and self.bet <= 30:
                    state.player.stamina_points -= 1
                elif self.bet >= 40 and self.bet <= 70:
                    state.player.stamina_points -= 2
                elif self.bet >= 80 and self.bet <= 100:
                    state.player.stamina_points -= 3

                self.game_state = "bet_screen"


        elif self.game_state == "bet_screen":
            self.message_display = "This is the bet screen. Press up and down to change your bet."
            self.second_message_display = "When you are ready press T to continue."
            controller = state.controller
            self.place_bet(state)
            if controller.isTPressed:
                print("t pressed")
                self.game_state = "coin_flip_time"


        elif self.game_state == "coin_flip_time":
            self.message_display = "I'm flipping the coin now."
            pygame.time.delay(500)
            if self.bet < 110:
                self.flipCoin()
                self.game_state = "choose_heads_or_tails_message"


        elif self.game_state == "choose_heads_or_tails_message":
            self.message_display = "Now Choose heads or tails. Make your choice"
            if controller.isUpPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) - 1
                else:
                    self.current_index -= 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) + 1
                else:
                    self.current_index += 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isDownPressed = False

            if self.current_index == 0:
                if controller.isTPressed:
                    self.players_side = "heads"
                    self.game_state = "results_screen"

            elif self.current_index == 1:
                if controller.isTPressed:
                    self.players_side = "tails"
                    self.game_state = "results_screen"



        elif self.game_state == "reveal_state":
            self.message_display = "time to reveal your coin"
            self.third_message_display = f"The coin will be on the {self.result}"
            if state.controller.isAPressed:
                self.game_state = "choose_heads_or_tails_message"
                state.controller.isAPressed = False



        elif self.game_state == "results_screen":
            self.second_message_display = " "
            if self.result == self.players_side:
                # self.third_message_display = "You won"
                state.player.money += self.bet
                self.coinFlipTedMoney -= self.bet
                pygame.time.delay(1000)

                self.game_state = "you_won_the_toss"

                if self.coinFlipTedMoney <= 0 or state.player.money <= 0:
                    print("At 0 ending match")
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)


            elif self.result != self.players_side:


                pygame.time.delay(500)
                state.player.money -= self.bet
                self.coinFlipTedMoney += self.bet

                self.game_state = "you_lost_the_toss"



        elif self.game_state == "you_won_the_toss":
            self.message_display = f"choice  {self.players_side} coin landed  {self.result} You WON"
            self.second_message_display = f"Play again? Press T on your choice"

            if self.coinFlipTedMoney <= 0 or state.player.money <= 0:
                print("At 0 ending match")
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)

            elif controller.isUpPressed:
                self.leave_or_replay_index -= 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                self.leave_or_replay_index += 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isDownPressed = False

            if self.leave_or_replay_index == 0:
                if controller.isTPressed:
                    self.game_state = "welcome_screen"

            elif self.leave_or_replay_index == 1:
                if controller.isTPressed:
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)

        elif self.game_state == "you_lost_the_toss":
            self.message_display = f"choice  {self.players_side} coin landed  {self.result} lost! "
            self.second_message_display = f"Play again? Yes to continue and No to exit. Press T on your choice"

            if self.coinFlipTedMoney <= 0 or state.player.money <= 0:
                print("At 0 ending match")
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)

            elif controller.isUpPressed:
                self.leave_or_replay_index -= 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                self.leave_or_replay_index += 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isDownPressed = False

            if self.leave_or_replay_index == 0:
                if controller.isTPressed:
                    self.game_state = "welcome_screen"

            elif self.leave_or_replay_index == 1:
                if controller.isTPressed:
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)

    ########################we want up and down arrows on bet. have arrow disapear when an item is not in use

    def draw(self, state: "GameState"):
        state.DISPLAY.fill((0, 0, 0))

        state.DISPLAY.blit(self.new_font.render(f"CoinFlipTedsMoney: {self.coinFlipTedMoney}", True, (255, 255, 255)), (10, 150))
        state.DISPLAY.blit(self.new_font.render(f"Player Money: {state.player.money}", True, (255, 255, 255)), (10, 190))

        state.DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (10, 10))
        state.DISPLAY.blit(self.font.render(f"{self.second_message_display}", True, (255, 255, 255)), (10, 50))
        state.DISPLAY.blit(self.font.render(f"{self.third_message_display}", True, (255, 255, 255)), (10, 230))
        state.DISPLAY.blit(self.font.render(f"Your current bet is:{self.bet}", True, (255, 255, 255)), (10, 260))
        state.DISPLAY.blit(self.font.render(f"Player health:{state.player.stamina_points}", True, (255, 255, 255)), (10, 290))
        state.DISPLAY.blit(self.font.render(f"Player magic:{state.player.focus_points}", True, (255, 255, 255)), (10, 320))

        if self.game_state != "you_won_the_toss" and self.game_state != "you_lost_the_toss":
            state.DISPLAY.blit(self.font.render(f"{self.choices[0]}", True, (255, 255, 255)), (700, 160))
            state.DISPLAY.blit(self.font.render(f"{self.choices[1]}", True, (255, 255, 255)), (700, 210))

        if self.game_state == "bet_screen":
            state.DISPLAY.blit(self.font.render(f"^", True, (255, 255, 255)), (240, 235))
            state.DISPLAY.blit(self.font.render(f"v", True, (255, 255, 255)), (240, 288))

        elif self.game_state == "choose_heads_or_tails_message":
            if self.current_index == 0:
                state.DISPLAY.blit(self.font.render(f"->", True, (255, 255, 255)), (650, 155))
            elif self.current_index == 1:
                state.DISPLAY.blit(self.font.render(f"->", True, (255, 255, 255)), (650, 205))


        elif self.game_state == "you_won_the_toss" or self.game_state == "you_lost_the_toss":
            state.DISPLAY.blit(self.font.render(f"{self.yes_or_no_menu[0]}", True, (255, 255, 255)), (700, 160))
            state.DISPLAY.blit(self.font.render(f"{self.yes_or_no_menu[1]}", True, (255, 255, 255)), (700, 210))

            if self.leave_or_replay_index == 0:
                state.DISPLAY.blit(self.font.render(f"->", True, (255, 255, 255)), (650, 160))  # Adjusted the y-coordinate for 'No'
            elif self.leave_or_replay_index == 1:
                state.DISPLAY.blit(self.font.render(f"->", True, (255, 255, 255)), (650, 210))  # Adjusted the y-coordinate for 'Yes'

        pygame.display.flip()



