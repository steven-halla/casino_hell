import random

import pygame

from screen.screen import Screen


#### no need to "defeat"people, but in doing so with some people you can complete quest
####or have it to where you only need to defeat 1 of each type as a quest.hmmmmm not sure
class CoinFlipSandyScreen(Screen):
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
        self.choices = ["Heads", "Tails", "Magic"]
        self.yes_or_no_menu = ["Yes", "No"]
        self.game_state = "welcome_screen"
        self.choice_sequence = True
        self.bet = 0
        self.font = pygame.font.Font(None, 36)
        self.coinFlipSandyMoney = 700
        self.coinFlipSandyDefeated = False
        self.current_index = 0
        self.yes_no_current_index = 0
        self.magic_menu_selector = ["Bluff", "Reveal", "Lucky", "Back"]
        self.magic_menu_index = 0
        self.leave_or_replay_index = 0
        self.high_exp = False
        self.low_exp = False

        self.bluff_text_list = ["I bet you triple my bet that your coin will land on tails 3 times in a row", "Hehehe, your on sucker"]
        self.luck_activated = 0
        self.sandy_focus_points = 30
        self.reveal_hand = False
        self.cheating_alert = False

    def giveExp(self, state: "GameState"):
        if state.player.level == 1:
            if self.high_exp == True:
                state.player.exp += 15
            elif self.low_exp == True:
                state.player.exp += 50
        elif state.player.level == 2:
            if self.high_exp == True:
                state.player.exp += 5
            elif self.low_exp == True:
                state.player.exp += 15
        else:
            print("your level is too high no exp for you")

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

    def flipCoin(self):
        # currently at .6 because heads is favored
        # in the future will have states to handle coin flip percentages
        # an item can add .1 to your rolls for heads, or -.1 for tails
        coin = random.random()
        if coin < 0.1:
            print("coin landed on heads")
            self.result = "heads"
        else:
            print("coin landed on tails")
            self.result = "tails"

    def update(self, state: "GameState"):
        if self.coinFlipSandyMoney <= 0:
            self.coinFlipSandyDefeated = True
        # Update the controller
        controller = state.controller
        controller.update()

        if state.player.stamina_points < 3:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

        if self.game_state == "welcome_screen":

            self.message_display = "This is the welcome screen. Press R to continue"
            self.second_message_display = ""
            self.third_message_display = ""
            self.reveal_hand = False

            if controller.isRPressed:
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
            self.flipCoin()
            self.game_state = "choose_heads_or_tails_message"





        #############fix bug with current index below and our yes and no gui to leave or replay a game

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


            elif self.current_index == 2:
                if controller.isTPressed:
                    print("This is how you pick magic")
                    self.game_state = "magic_menu"





        elif self.game_state == "magic_menu":
            self.message_display = "Pick a magic spell and wreck havic. Press K to cast"

            if controller.isUpPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) - 1
                else:
                    self.magic_menu_index -= 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) + 1
                else:
                    self.magic_menu_index += 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isDownPressed = False

            if self.magic_menu_index == 0:
                if controller.isKPressed:
                    if self.luck_activated < 1:
                        if state.player.focus_points >= 10:
                            state.player.focus_points -= 10

                            print("You cast bluff")
                            self.game_state = "bluff_state"

                        else:
                            self.third_message_display = "Sorry but you dont have enough focus points to cast"
                    elif self.luck_activated > 0 or self.reveal_hand == True:
                        self.third_message_display = "sorry but you can't stack magic spells"


            elif self.magic_menu_index == 1:
                if controller.isKPressed:
                    if self.luck_activated < 1:
                        print("You cast reveal")
                        if controller.isKPressed:
                            if state.player.focus_points >= 10:
                                state.player.focus_points -= 10
                                self.reveal_hand = True

                                print("You cast bluff")
                                self.game_state = "reveal_state"

                            elif state.player.focus_points < 10:
                                self.third_message_display = "Sorry but you dont have enough focus points to cast"
                    elif self.luck_activated > 0:
                        self.third_message_display = "sorry but you can't stack magic spells"





            ##########################have a message state reserved for buff states

            ##### boss enemies will use magic under more strict conditions
            elif self.magic_menu_index == 2:
                if controller.isKPressed:
                    print("you cast avatar of luck")
                    self.third_message_display = "Your luck is now increased for 5 losses"
                    self.luck_activated = 3
                    state.player.focus_points -= 20
                    self.game_state = "choose_heads_or_tails_message"


            elif self.magic_menu_index == 3:
                if controller.isKPressed:
                    print("going back")
                    self.game_state = "choose_heads_or_tails_message"

        elif self.game_state == "reveal_state":
            self.message_display = "time to reveal your coin"
            self.third_message_display = f"The coin will be on the {self.result}"
            if state.controller.isAPressed:
                self.game_state = "choose_heads_or_tails_message"
                state.controller.isAPressed = False




        elif self.game_state == "bluff_state":
            self.message_display = "Triple my bet that tails will land 3 times in a  row."
            bluffalo = random.random()

            if bluffalo < 0.7:
                print("you win tripple bet")
                state.player.money += self.bet * 3
                self.game_state = "welcome_screen"


            else:
                print("your bet lost")
                state.player.money -= self.bet
                self.game_state = "welcome_screen"






        elif self.game_state == "results_screen":
            self.second_message_display = " "
            if self.result == self.players_side:
                # self.third_message_display = "You won"
                state.player.money += self.bet
                self.coinFlipSandyMoney -= self.bet
                pygame.time.delay(1000)

                self.game_state = "you_won_the_toss"

                if self.coinFlipSandyMoney <= 0 or state.player.money <= 0:
                    print("At 0 ending match")
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)





            elif self.result != self.players_side:
                if self.luck_activated > 0:
                    lucky_draw = random.random()
                    if lucky_draw < 0.9:
                        self.third_message_display = f"Your feeling lucky.{self.luck_activated}remains. Push A"

                        if controller.isAPressed:
                            self.luck_activated -= 1
                            state.player.money += self.bet
                            self.coinFlipSandyMoney -= self.bet
                            self.result = self.players_side

                            self.game_state = "you_won_the_toss"
                    else:
                        # self.third_message_display = f"Your luck didn't pan out.{self.luck_activated}remains. Push A"
                        if controller.isAPressed:
                            self.luck_activated -= 1

                            state.player.money -= self.bet
                            self.coinFlipSandyMoney += self.bet

                            self.game_state = "you_lost_the_toss"

                elif self.luck_activated == 0:
                    pygame.time.delay(500)
                    state.player.money -= self.bet
                    self.coinFlipSandyMoney += self.bet

                    self.game_state = "you_lost_the_toss"











        elif self.game_state == "you_won_the_toss":
            if self.players_side == "tails" and self.sandy_focus_points > 0 and self.luck_activated < 1 and self.cheating_alert == False:
                self.players_side = "heads"
                print("I could have sworn I picked tails. Did they switch my bet?")
                if self.reveal_hand == True:
                    print("The other person is cheating. I'll hold up my hands to signafy which side I'll guess")
                    self.cheating_alert = True

                self.game_state = "you_lost_the_toss"

            self.message_display = f"choice  {self.players_side} coin landed  {self.result} You WON"
            self.second_message_display = f"Play again? Press T on your choice"

            if self.coinFlipSandyMoney <= 0 or state.player.money <= 0:
                print("At 0 ending match")
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)





            elif controller.isUpPressed:
                if not hasattr(self, "leave_or_replay_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) - 1
                else:
                    self.leave_or_replay_index -= 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "yes_no_current_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) + 1
                else:
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
            self.second_message_display = f"Play again?Yes to continue and No to exi. Press T on your choice"
            if self.coinFlipSandyMoney <= 0 or state.player.money <= 0:
                print("At 0 ending match")
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)




            elif controller.isUpPressed:
                if not hasattr(self, "leave_or_replay_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) - 1
                else:
                    self.leave_or_replay_index -= 1
                self.leave_or_replay_index %= len(self.yes_or_no_menu)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "yes_no_current_index"):
                    self.leave_or_replay_index = len(self.yes_or_no_menu) + 1
                else:
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
        # Fill the screen with a solid color
        state.DISPLAY.fill((0, 0, 0))

        state.DISPLAY.blit(self.new_font.render(
            f" CoinFlipSandysMoney: {self.coinFlipSandyMoney}",
            True, (255, 255, 255)), (10, 150))
        state.DISPLAY.blit(self.new_font.render(
            f" player Money: {state.player.money}",
            True, (255, 255, 255)), (10, 190))

        # Draw the welcome message or choose bet message based on the game state

        state.DISPLAY.blit(self.font.render(f"{self.message_display}", True, (255, 255, 255)), (10, 10))
        state.DISPLAY.blit(self.font.render(f"{self.second_message_display}", True, (255, 255, 255)), (10, 50))
        state.DISPLAY.blit(self.font.render(f"{self.third_message_display}", True, (255, 255, 255)), (10, 230))
        state.DISPLAY.blit(self.font.render(f"Your current bet is:{self.bet}", True, (255, 255, 255)), (10, 260))
        state.DISPLAY.blit(self.font.render(f"player health:{state.player.stamina_points}", True, (255, 255, 255)), (10, 290))
        state.DISPLAY.blit(self.font.render(f"player magic:{state.player.focus_points}", True, (255, 255, 255)), (10, 320))

        if self.game_state == "magic_menu":
            if self.magic_menu_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.magic_menu_index == 1:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.magic_menu_index == 2:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

            elif self.magic_menu_index == 3:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 305))

            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[0]}", True, (255, 255, 255)),
                (700, 160))

            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[1]}", True, (255, 255, 255)),
                (700, 210))

            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[2]}", True, (255, 255, 255)),
                (700, 260))

            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[3]}", True, (255, 255, 255)),
                (700, 310))

        elif self.game_state != "you_won_the_toss" and self.game_state != "you_lost_the_toss":
            state.DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (700, 160))

            state.DISPLAY.blit(
                self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                (700, 210))

            state.DISPLAY.blit(
                self.font.render(f"{self.choices[2]}", True, (255, 255, 255)),
                (700, 260))

        if self.game_state == "bet_screen":

            state.DISPLAY.blit(self.font.render(f"^", True, (255, 255, 255)), (240, 235))
            state.DISPLAY.blit(self.font.render(f"v", True, (255, 255, 255)), (240, 288))


        elif self.game_state == "choose_heads_or_tails_message":

            if self.current_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.current_index == 1:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.current_index == 2:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

        elif self.game_state == "you_won_the_toss" or self.game_state == "you_lost_the_toss":
            state.DISPLAY.blit(
                self.font.render(f"{self.yes_or_no_menu[0]}", True, (255, 255, 255)),
                (700, 160))

            state.DISPLAY.blit(
                self.font.render(f"{self.yes_or_no_menu[1]}", True, (255, 255, 255)),
                (700, 210))

            if self.yes_no_current_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.yes_no_current_index == 1:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))

        pygame.display.flip()

        ########have deals notice if player is low on stamina and magic and thus react to it
        #### have a dealer make a comment to player on this a few times.
