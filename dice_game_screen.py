import time

import pygame

from dice import Dice
from screen import Screen


class DiceGameScreen(Screen, Dice):
    def __init__(self):
        super().__init__("Dice game")
        self.game_state = "choose_player_2_or_ai"
        self.isPlayer2 = False
        self.isAI = False
        self.game_state_started_at = 0
        start_time = pygame.time.get_ticks()

        self.diceFont = pygame.font.Font(None, 36)
        self.player_1_turn = False
        self.player_2_turn = False
        self.player1pile = 0
        self.player2pile = 0
        self.ante = 1000
        self.anteXero = 0
        self.player_1_won_game = False
        self.player_2_won_game = False

        self.roll_state = ""
        self.player_1_lost_game = False
        self.player_2_lost_game = False
        self.its_a_draw = False
        self.start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_delay = 500  # input delay in milliseconds
        self.input_time = 0  # time when input was last read
        self.chiliWilleyMoney = 500
        self.chiliWilleyIsDefeated = False

    def refresh(self):
        self.player1pile = 0
        self.player2pile = 0
        self.ante = 1000
        self.game_state = "choose_player_2_or_ai"

    def hot_bet(self):

        if self.game_state == "player_1_going_hot":
            self.roll_two_d_six()
            if self.rolls[0] == self.rolls[1]:

                self.player2pile += self.ante + self.player1pile
                self.player1pile = 0
                self.ante = 0
                self.roll_state = "you got a double at the wrong time, you lose"
                print("you rolled a double get ready for trouble")
                self.player_1_lost_game = True
                self.game_state = "player_1_results"



            elif self.add() == 5 or self.add() == 6 or self.add() == 7 or self.add() == 8 or self.add() == 9:
                self.roll_one_d_hundred()
                subtracted_amount = min(self.one_hundred_rolls[0],
                                        self.player2pile)
                self.player2pile -= subtracted_amount * 3
                self.player1pile += subtracted_amount * 3
                self.roll_state = "attacking enemy player pile"

                if self.player2pile < 0:
                    self.player2pile = 0
                    print("if its 0:")
                    print(self.player2pile)
                self.game_state = "player_2_declare_intent_stage"

            else:
                self.roll_state = "Your roll was wasted"

        ########player 2 below

        if self.game_state == "player_2_going_hot":
            self.roll_two_d_six()
            if self.rolls[0] == self.rolls[1]:

                self.player1pile += self.ante + self.player2pile
                self.ante = 0
                self.roll_state = "you got a double at the wrong time, you lose"

                self.player2pile = 0
                self.player_2_lost_game = True

            elif self.add() == 5 or self.add() == 6 or self.add() == 7 or self.add() == 8 or self.add() == 9:

                self.roll_one_d_hundred()
                print("you rolled the dice as an AI")
                subtracted_amount = min(self.one_hundred_rolls[0],
                                        self.player1pile)
                self.player2pile += subtracted_amount * 3
                self.player1pile -= subtracted_amount * 3
                self.roll_state = "attacking enemy player pile"

                if self.player1pile < 0:
                    self.player1pile = 0

                self.game_state = "player_1_declare_intent_stage"

            else:
                self.roll_state = "Your roll was wasted"



        elif self.game_state == "player_1_going_hot":
            print("no dice you wasted your chance")
            self.game_state = "player_2_declare_intent_stage"

        elif self.game_state == "player_2_going_hot":
            print("no dice you wasted your chance")

        print("end state: " + self.game_state)

    def cold_bet(self):

        self.roll_two_d_six()
        if self.rolls[0] == 1 and self.rolls[1] == 1:
            if self.game_state == "player_1_rolls":
                print(self.game_state)
                self.player2pile = self.player2pile + self.player1pile + self.ante
                self.player1pile = 0
                self.ante = 0
                self.roll_state = "You got the wrong kind of double, you lose everything player 1!"
                print(self.player1pile)
                self.player_2_won_game = True



            elif self.game_state == "player_2_rolls":
                print(self.game_state)

                self.player1pile = self.player2pile + self.player1pile + self.ante
                self.player1pile = 0
                self.ante = 0
                self.roll_state = "You got the wrong kind of double, you lose everything player 2!"
                print(self.player2pile)
                self.player_1_won_game = True


        elif self.rolls[0] == 6 and self.rolls[1] == 6:
            if self.game_state == "player_1_rolls":
                print(
                    "you win =======================================================================")
                self.player1pile = self.player2pile + self.player1pile + self.ante
                self.player2pile = 0
                self.ante = 0
                self.roll_state = "lucky double 6, player 1 wins!"
                self.game_state = "player_1_wins"
                self.player_1_won_game = True



            elif self.game_state == "player_2_rolls":
                print(
                    "you win ==================================================================")
                self.player2pile = self.player2pile + self.player1pile + self.ante
                self.player1pile = 0
                self.ante = 0
                self.roll_state = "lucky double 6, player 2 wins!"
                self.game_state = "player_2_wins"
                self.player_2_won_game = True


        #
        elif self.add() == 6:
            if self.game_state == "player_1_rolls":
                self.roll_state = "Devil's 6 go after enemy pile."

                self.roll_one_d_hundred()
                if self.one_hundred_rolls[0] > self.player2pile:
                    self.one_hundred_rolls[0] = self.player2pile
                self.player1pile += self.one_hundred_rolls[0]
                self.player2pile -= self.one_hundred_rolls[0]
                if self.player2pile < 0:
                    self.player2pile = 0
                self.game_state = "player_2_intent_stage"
            elif self.game_state == "player_2_rolls":
                self.roll_state = "Devil's 6 go after enemy pile"
                self.roll_one_d_hundred()
                if self.one_hundred_rolls[0] > self.player2pile:
                    self.one_hundred_rolls[0] = self.player2pile
                self.player2pile += self.one_hundred_rolls[0]

                self.player1pile -= self.one_hundred_rolls[0]
                if self.player1pile < 0:
                    self.player1pile = 0
                self.game_state = "player_1_intent_stage"

        #
        elif self.add() == 7 or self.add() == 8 or self.add() == 9 or self.add() == 10 or self.add() == 11:
            if self.game_state == "player_1_rolls":
                self.roll_state = "Go after the ante"

                self.roll_one_d_hundred()
                subtracted_amount = min(self.one_hundred_rolls[0], self.ante)
                self.ante -= subtracted_amount
                self.player1pile += subtracted_amount

                if self.ante < 0:
                    self.ante = 0
                self.game_state = "player_2_intent_stage"



            elif self.game_state == "player_2_rolls":
                self.roll_state = "Go after the ante"

                self.roll_one_d_hundred()
                subtracted_amount = min(self.one_hundred_rolls[0], self.ante)
                self.ante -= subtracted_amount
                self.player2pile += subtracted_amount

                if self.ante < 0:
                    self.ante = 0
                self.game_state = "player_1_intent_stage"
        else:
            self.roll_state = "wasted roll"

    def start_state(self, gamestate):
        self.game_state = gamestate
        self.game_state_started_at = pygame.time.get_ticks()

    def update(self, state: "GameState"):
        if self.chiliWilleyMoney <= 0:
            self.chiliWilleyIsDefeated = True
        # delta between last update time in milliseconds
        delta = pygame.time.get_ticks() - self.game_state_started_at
        # this is to track what state we currently in DO NOT DELTE THIS
        # print("update() - state: " + str(self.game_state) + ", start at: " + str(delta))

        controller = state.controller
        controller.update()
        print("HERE WE GOO OOOOOO")

        if self.game_state == "player_1_wins":

            pygame.time.delay(5000)
            self.refresh()

            state.player.money += 500
            self.chiliWilleyMoney -= 500
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

        elif self.game_state == "player_2_wins":

            pygame.time.delay(5000)
            self.refresh()

            state.player.money -= 500
            self.chiliWilleyMoney += 500
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)


        elif self.game_state == "choose_player_2_or_ai":
            if controller.is1Pressed:
                self.isPlayer2 = True
                self.game_state = "player_1_declare_intent_stage"
                print("player 2")

            else:
                if controller.isOPressed:
                    self.isAI = True
                    self.game_state = "player_1_declare_intent_stage"

        elif self.game_state == "player_1_declare_intent_stage":
            self.one_hundred_rolls = 0
            # if delta > 500: # don't read keyboard input for at least 500 ms.

            if controller.isTPressed:

                self.start_state("player_1_rolls")
                # print(self.game_state)

            elif controller.isPPressed:
                self.start_state("player_1_going_hot")




        elif self.game_state == "player_1_rolls":
            # if delta > 1500: # don't read keyboard input for at least 500 ms.

            if controller.isEPressed:

                print("pressing T")
                self.cold_bet()
                if self.one_hundred_rolls == 0:
                    self.start_state("player_1_results")

                    if self.player_1_won_game == True:
                        self.start_state("player_1_wins")
                        pygame.time.delay(2000)



                else:
                    self.start_state("player_1_results_one_hundred")



        elif self.game_state == "player_1_going_hot":
            if controller.is1Pressed:
                print("pressing 1")
                self.hot_bet()
                if self.one_hundred_rolls == 0:
                    self.game_state = "player_1_results"
                    print("Player 1 got set to 1player 1 rsults")
                else:
                    self.game_state = "player_1_results_one_hundred"



        elif self.game_state == "player_1_results" or self.game_state == "player_1_results_one_hundred":
            print("player jadfllasf;jslfjls;jaf")
            if self.player_1_lost_game == True:
                pygame.time.delay(3000)
                state.player.money -= 500
                self.chiliWilleyMoney += 500

                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)

            elif controller.isBPressed:
                print("Houstan we got a problem here")
                self.game_state = "player_2_declare_intent_stage"


        ######player 2 stuff down here

        elif self.game_state == "player_2_declare_intent_stage":
            self.one_hundred_rolls = 0

            if self.isPlayer2 == True:

                if controller.isTPressed:
                    print("WE in update")
                    self.game_state = "player_2_rolls"

                elif controller.isPPressed:
                    self.game_state = "player_2_going_hot"

            elif self.isAI == True:
                time.sleep(2)
                if self.player1pile < 300:
                    controller.isTPressed = True
                    self.game_state = "player_2_rolls"
                    controller.isTPressed = False
                else:
                    controller.isPPressed = True
                    self.game_state = "player_2_going_hot"
                    controller.isPPressed = False




        elif self.game_state == "player_2_rolls":
            if self.isPlayer2 == True:
                if controller.isEPressed:
                    print("pressing T")
                    self.cold_bet()
                    if self.one_hundred_rolls == 0:
                        self.game_state = "player_2_results"
                    else:
                        self.game_state = "player_2_results_one_hundred"

            elif self.isAI == True:
                time.sleep(2)
                controller.isEPressed = True
                print("pressing T")
                self.cold_bet()
                controller.isEPressed = False
                if self.one_hundred_rolls == 0:
                    self.game_state = "player_2_results"
                else:
                    self.game_state = "player_2_results_one_hundred"


        ####PLAYER 2 HOT PHASE DOWN HERE!!!!!!!

        elif self.game_state == "player_2_going_hot":
            if self.isPlayer2 == True:
                if controller.is1Pressed:
                    print("pressing 1")
                    self.hot_bet()
                    if self.one_hundred_rolls == 0:
                        self.game_state = "player_2_results"
                    else:
                        self.game_state = "player_2_results_one_hundred"

            elif self.isAI == True:
                time.sleep(2)
                controller.is1Pressed = True

                self.hot_bet()
                controller.is1Pressed = False
                if self.one_hundred_rolls == 0:
                    self.game_state = "player_2_results"
                else:
                    self.game_state = "player_2_results_one_hundred"






        elif self.game_state == "player_2_results" \
                or self.game_state == "player_2_results_one_hundred":
            print("we're walking here")
            print(str(self.isPlayer2))
            # if self.isPlayer2 == True:
            print("We're sitting here")
            if self.isPlayer2 == True:
                if controller.isBPressed:
                    print("HEY THER YOU U YO UYOU YOU YOU YO U ;sdfakl;sfd")
                    self.game_state = "player_1_declare_intent_stage"

            elif self.isAI == True:
                time.sleep(2)
                controller.isBPressed = True
                self.game_state = "player_1_declare_intent_stage"
                controller.isBPressed = False

        if self.ante == 0:
            print("THE ANTIE IS AT 00000000000000000000o0-o0o00o0o0o0o0o0o")
            if self.player1pile > self.player2pile:
                self.game_state = "player_1_wins"
                self.player_2_lost_game = True

            elif self.player1pile < self.player2pile:
                self.game_state = "player_2_wins"
                self.player_1_lost_game = True

            elif self.player1pile == self.player2pile:
                self.roll_state = "It's a draw,  you both walk away whole"
                self.its_a_draw = True
                print("its a draw")

    def draw(self, state: "GameState"):
        state.DISPLAY.fill((0, 0, 0))

        if self.game_state == "choose_player_2_or_ai":
            state.DISPLAY.blit(
                self.diceFont.render(f"Press 1 key for human or O key for AI",
                                     True, (255, 255, 255)),
                (10, 10))

        if self.game_state == "player_1_declare_intent_stage":
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1: press T for cold P For hot",
                                     True, (255, 255, 255)), (10, 10))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True,
                                     (255, 255, 255)), (200, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True,
                                     (255, 255, 255)), (300, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True,
                                              (255, 255, 255)), (400, 400))

        elif self.game_state == "player_2_declare_intent_stage":
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2: press T for cold P for hot",
                                     True, (255, 255, 255)), (10, 10))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True,
                                     (255, 255, 255)), (200, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True,
                                     (255, 255, 255)), (300, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True,
                                              (255, 255, 255)), (400, 400))



        elif self.game_state == "player_1_going_cold":
            state.DISPLAY.blit(self.diceFont.render(f"Player 1 is going cold. ", True,
                                              (255, 255, 255)), (10, 10))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True,
                                     (255, 255, 255)), (200, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True,
                                     (255, 255, 255)), (300, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True,
                                              (255, 255, 255)), (400, 400))

        elif self.game_state == "player_2_going_cold":
            state.DISPLAY.blit(self.diceFont.render(f"Player 1 is going cold. ", True,
                                              (255, 255, 255)), (10, 10))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True,
                                     (255, 255, 255)), (200, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True,
                                     (255, 255, 255)), (300, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True,
                                              (255, 255, 255)), (400, 400))

        elif self.game_state == "player_1_going_hot":
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 is going hot PRESS 1", True,
                                     (255, 255, 255)), (10, 10))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True,
                                     (255, 255, 255)), (200, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True,
                                     (255, 255, 255)), (300, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True,
                                              (255, 255, 255)), (400, 400))

        elif self.game_state == "player_2_going_hot":
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 is going hot PRESS 1", True,
                                     (255, 255, 255)), (10, 10))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True,
                                     (255, 255, 255)), (200, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True,
                                     (255, 255, 255)), (300, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True,
                                              (255, 255, 255)), (400, 400))

        elif self.game_state == "player_1_wins":
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True,
                                     (255, 255, 255)), (200, 10))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 MONEY: {state.player.money}",
                                     True, (255, 255, 255)), (200, 100))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True,
                                     (255, 255, 255)), (200, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 MONEY: {self.chiliWilleyMoney}",
                                     True, (255, 255, 255)), (200, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True,
                                              (255, 255, 255)), (200, 400))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 wins", True, (255, 255, 255)),
                (200, 500))


        elif self.game_state == "player_2_wins":
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True, (255, 255, 255)), (155, 10))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Money: {state.player.money}", True, (255, 255, 255)), (155, 100))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True, (255, 255, 255)), (155, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Money: {self.chiliWilleyMoney}", True, (255, 255, 255)), (155, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True, (255, 255, 255)), (155, 400))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 wins", True, (255, 255, 255)), (155, 500))


        elif self.game_state == "player_1_rolls":
            state.DISPLAY.blit(
                self.diceFont.render(f"PLAYER 1 PRESS E to roll the dice", True,
                                     (255, 255, 255)), (255, 255))

        elif self.game_state == "player_2_rolls":
            state.DISPLAY.blit(
                self.diceFont.render(f"PLAYER 2 PRESS E to roll the dice", True,
                                     (255, 255, 255)), (255, 255))


        elif self.game_state == "player_1_results":
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True,
                                     (255, 255, 255)), (200, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True,
                                     (255, 255, 255)), (300, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True,
                                              (255, 255, 255)), (400, 400))
            state.DISPLAY.blit(
                self.diceFont.render(
                    f" Player 1 rolls a {self.rolls} PRESS B when ready", True,
                    (255, 255, 255)),
                (155, 255))
            state.DISPLAY.blit(self.diceFont.render(f" {self.roll_state}", True,
                                              (255, 255, 255)), (5, 355))
            if self.player_1_lost_game == True:
                state.DISPLAY.blit(
                    self.diceFont.render(f"Sorry player 1: GAME OVER!!!: ",
                                         True, (255, 255, 255)),
                    (1, 555))


            elif self.its_a_draw == True:
                state.DISPLAY.blit(
                    self.diceFont.render(f"It's a draw sorry player 1: ", True,
                                         (255, 255, 255)),
                    (1, 555))
                pygame.time.delay(5000)

                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)


        elif self.game_state == "player_2_results":
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True,
                                     (255, 255, 255)), (200, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True,
                                     (255, 255, 255)), (300, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True,
                                              (255, 255, 255)), (400, 400))
            state.DISPLAY.blit(
                self.diceFont.render(
                    f" Player 2 rolls a {self.rolls} PRESS B when ready", True,
                    (255, 255, 255)),
                (155, 255))
            state.DISPLAY.blit(self.diceFont.render(f" {self.roll_state}", True,
                                              (255, 255, 255)), (5, 355))
            if self.player_2_lost_game == True:
                state.DISPLAY.blit(
                    self.diceFont.render(f"Sorry player 2: GAME OVER!!!: ",
                                         True, (255, 255, 255)),
                    (1, 555))

            elif self.its_a_draw == True:
                state.DISPLAY.blit(
                    self.diceFont.render(f"It's a draw sorry player 2: ", True,
                                         (255, 255, 255)),
                    (1, 555))




        elif self.game_state == "player_1_results_one_hundred":
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True,
                                     (255, 255, 255)), (200, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True,
                                     (255, 255, 255)), (300, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True,
                                              (255, 255, 255)), (400, 400))
            state.DISPLAY.blit(
                self.diceFont.render(
                    f" Player 1 rolls a {self.rolls} PRESS B when ready", True,
                    (255, 255, 255)),
                (155, 255))
            state.DISPLAY.blit(self.diceFont.render(f" {self.roll_state}", True,
                                              (255, 255, 255)), (5, 355))
            state.DISPLAY.blit(
                self.diceFont.render(f"1d100 ROLLED: {self.one_hundred_rolls}",
                                     True, (255, 255, 255)),
                (5, 555))



        elif self.game_state == "player_2_results_one_hundred":
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 1 Pile: {self.player1pile}", True,
                                     (255, 255, 255)), (200, 200))
            state.DISPLAY.blit(
                self.diceFont.render(f"Player 2 Pile: {self.player2pile}", True,
                                     (255, 255, 255)), (300, 300))
            state.DISPLAY.blit(self.diceFont.render(f"Ante: {self.ante}", True,
                                              (255, 255, 255)), (400, 400))
            state.DISPLAY.blit(
                self.diceFont.render(
                    f" Player 2 rolls a {self.rolls} PRESS B when ready", True,
                    (255, 255, 255)),
                (155, 255))
            state.DISPLAY.blit(self.diceFont.render(f" {self.roll_state}", True,
                                              (255, 255, 255)), (5, 355))
            state.DISPLAY.blit(
                self.diceFont.render(f"1d100 ROLLED: {self.one_hundred_rolls}",
                                     True, (255, 255, 255)),
                (5, 555))

        pygame.display.flip()
