import random
import time
from typing import List

import pygame

from screen.screen import Screen


class OpossumInACanNellyScreen(Screen):
    def __init__(self):
        super().__init__("Opossum in a can screen")
        self.third_message_display = ""
        self.desperate = False
        # we can set this as a variable that can get toggled on and off depending on who you are playing aginst
        self.sallyOpossumMoney = 100
        self.sallyOpossumIsDefeated = False
        self.opossum_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 36)
        self.game_state = "welcome_opposum"
        self.winner_or_looser: List[str] = ["win", "win", "insurance_eater",
                                            "win", "win", "win", "win",
                                            "lucky_star", "lucky_star",
                                            "X3_star", "lose", "win",

                                            "win", "insurance_eater", "lose"]
        self.result = "win"
        self.bet = 20
        self.insurance = 200
        self.X3 = False
        self.has_opossum_insurance = True

        self.choices = ["Grab", "Magic", "Quit"]
        self.choices_index = 0

        self.bet_or_flee = ["bet", "flee"]
        self.bet_or_flee_index = 0

        self.magic_menu_selector = ["Reveal", "Lucky", "Back"]
        self.magic_menu_index = 0

        self.play_again_or_quit = ["Play Again", "Quit"]

        self.play_again_or_quit_index = 0

        self.bluff_activated = 0
        self.bottom_message = ""
        self.opossum_rader = False

        self.luck_activated = 0

    def refresh(self):
        self.bet = 20
        self.has_opossum_insurance = True
        self.insurance = 200

        self.winner_or_looser = ["win", "win", "insurance_eater", "win", "win",
                                 "win", "win", "lucky_star", "lucky_star",
                                 "X3_star", "lose", "win",

                                 "win", "insurance_eater", "lose"]

    def shuffle_opposums(self) -> List[str]:
        """Creates a new list in a random order"""

        random.shuffle(self.winner_or_looser)
        if self.luck_activated > 0:
            self.luck_activated -= 1

        print(str(self.winner_or_looser))
        return self.winner_or_looser

    def check_results(self, state: "GameState"):
        if self.result == "X3_star":
            self.X3 = True
            print(self.game_state)
            self.game_state = "play_again_or_bail"


        elif self.result == "win":
            if self.X3 == False:
                self.bet = self.bet * 2
                self.sallyOpossumMoney -= self.bet // 2
                print("you win")
                print(self.bet)
                self.game_state = "play_again_or_bail"
            else:
                self.bet = self.bet * 3
                self.sallyOpossumMoney -= self.bet // 3 * 2
                self.X3 = False
                self.game_state = "play_again_or_bail"

        elif self.result == "lucky_star":
            self.insurance = self.insurance + 200
            self.sallyOpossumMoney -= 200
            self.game_state = "play_again_or_bail"


        elif self.result == "insurance_eater":

            if self.insurance <= 0:
                self.sallyOpossumMoney += self.bet

                print("oh no your in trouble")
                print(self.game_state)
                self.game_state = "loser_screen"
            else:
                print("what are you doing here?")
                self.sallyOpossumMoney += self.insurance
                self.insurance -= 200
                self.game_state = "play_again_or_bail"

        elif self.result == "lose":
            print("This is the losing screen")
            self.sallyOpossumMoney += self.bet
            self.sallyOpossumMoney += self.insurance
            self.bet = 0

            self.game_state = "loser_screen"

    def update(self, state: "GameState"):
        if self.sallyOpossumMoney <= 0:
            self.sallyOpossumIsDefeated = True
        controller = state.controller
        controller.update()
        if self.sallyOpossumMoney <= 300:
            self.desperate = True
        elif self.sallyOpossumMoney > 300:
            self.desperate = False

        if self.game_state == "welcome_opposum":

            if controller.isTPressed:
                pygame.time.delay(150)
                self.game_state = "choose_can"

        elif self.game_state == "choose_can":
            if controller.isUpPressed:
                if not hasattr(self, "choices_index"):
                    self.choices_index = len(self.choices) - 1
                else:
                    self.choices_index -= 1
                self.choices_index %= len(self.choices)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "choices_index"):
                    self.choices_index = len(self.choices) + 1
                else:
                    self.choices_index += 1
                self.choices_index %= len(self.choices)
                controller.isDownPressed = False

            elif self.choices_index == 0:
                if controller.isTPressed:
                    pygame.time.delay(150)
                    self.shuffle_opposums()
                    self.result = self.winner_or_looser[0]
                    if self.opossum_rader == True:
                        print("HEY THERE YOU GUY ITS POSSUM TIIIIIIME")
                        self.bottom_message = f"The next draw is a {self.winner_or_looser[0]}Press T to continue"
                        if self.result == "lose":
                            print("you notice this dealer is cheating")
                            state.player.money += self.sallyOpossumMoney
                            self.sallyOpossumMoney = 0
                            print("time to leave we got the  cheater")
                        if controller.isTPressed:
                            self.game_state = "choose_or_flee"
                            self.opossum_rader = False

                    else:
                        del self.winner_or_looser[0]
                        self.check_results(state)
                        print("Get that opossum")

            elif self.choices_index == 1:
                if controller.isTPressed:
                    self.game_state = "magic_menu"
                    print("cast magic")


            elif self.choices_index == 2:
                if controller.isTPressed:
                    print("Quitting")



        elif self.game_state == "choose_or_flee":
            self.message_display = f"Will you go forward or retreat?"
            if controller.isUpPressed:
                if not hasattr(self, "bet_or_flee_index"):
                    self.bet_or_flee_index = len(self.bet_or_flee) - 1
                else:
                    self.bet_or_flee_index -= 1
                self.bet_or_flee_index %= len(self.bet_or_flee)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "bet_or_flee_index"):
                    self.bet_or_flee_index = len(self.bet_or_flee) + 1
                else:
                    self.bet_or_flee_index += 1
                self.bet_or_flee_index %= len(self.bet_or_flee)
                controller.isDownPressed = False

            elif self.bet_or_flee_index == 0:
                if controller.isTPressed:
                    print("lets go with it")
                    self.game_state = "choose_can"

            elif self.bet_or_flee_index == 1:
                if controller.isTPressed:
                    print("lets get out")




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
                if controller.isKPressed and self.luck_activated == 0:
                    print("You cast reveal")
                    if state.player.focus_points >= 10:
                        state.player.focus_points -= 10
                        self.opossum_rader = True

                        self.game_state = "choose_can"

                    elif state.player.focus_points < 10:
                        self.third_message_display = "Sorry but you dont have enough focus points to cast"
                else:
                    self.third_message_display = "sorry but you can't stack magic spells"

            elif self.magic_menu_index == 1:
                if controller.isKPressed and self.luck_activated == 0:
                    print("you cast avatar of luck")
                    self.third_message_display = "The god of luck shines on you, looks like another trash can was hiding behind one of the others"
                    state.player.focus_points -= 20
                    self.winner_or_looser.append("win")

                    self.game_state = "choose_can"
                    self.luck_activated = 5






            ##########################have a message state reserved for buff states

            ##### boss enemies will use magic under more strict conditions
            elif self.magic_menu_index == 2:
                if controller.isKPressed:
                    print("going back")
                    self.game_state = "choose_can"





        elif self.game_state == "play_again_or_bail":
            if controller.isUpPressed:
                if not hasattr(self, "play_again_or_quit_index"):
                    self.play_again_or_quit_index = len(
                        self.play_again_or_quit) - 1
                else:
                    self.play_again_or_quit_index -= 1
                self.play_again_or_quit_index %= len(self.play_again_or_quit)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                if not hasattr(self, "play_again_or_quit_index"):
                    self.play_again_or_quit_index = len(
                        self.play_again_or_quit) + 1
                else:
                    self.play_again_or_quit_index += 1
                self.play_again_or_quit_index %= len(self.play_again_or_quit)
                controller.isDownPressed = False

            elif self.play_again_or_quit_index == 0:
                if controller.isTPressed:
                    print("lets go with it")
                    pygame.time.delay(150)
                    self.game_state = "choose_can"

            elif self.play_again_or_quit_index == 1:
                if controller.isTPressed:
                    print("lets get out")



        elif self.game_state == "loser_screen":
            time.sleep(3)
            self.refresh()
            self.game_state = "welcome_opposum"
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)

    def draw(self, state: "GameState"):
        state.DISPLAY.fill((0, 0, 0))

        if self.desperate == True:
            state.DISPLAY.blit(self.font.render(
                f" I Take care of the nelly here Please think of the children!",
                True, (255, 255, 255)), (10, 530))

        state.DISPLAY.blit(
            self.font.render(f"{self.winner_or_looser}", True, (255, 255, 255)),
            (1, 333))

        state.DISPLAY.blit(self.font.render(
            f" SallyOpossum Money: {self.sallyOpossumMoney}",
            True, (255, 255, 255)), (10, 190))
        state.DISPLAY.blit(self.font.render(
            f" player Money: {state.player.money}",
            True, (255, 255, 255)), (10, 290))

        state.DISPLAY.blit(self.font.render(
            f" Players Bet: {self.bet}",
            True, (255, 255, 255)), (10, 390))
        state.DISPLAY.blit(self.font.render(
            f" player Insurance: {self.insurance} here is your luck duck : {self.luck_activated}",
            True, (255, 255, 255)), (10, 490))

        state.DISPLAY.blit(self.font.render(
            f" bottom message: {self.bottom_message}  rader is: {self.opossum_rader}",
            True, (255, 255, 255)), (10, 33))

        if self.game_state == "choose_can":

            state.DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (700, 160))

            state.DISPLAY.blit(
                self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                (700, 210))

            state.DISPLAY.blit(
                self.font.render(f"{self.choices[2]}", True, (255, 255, 255)),
                (700, 260))

            if self.choices_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.choices_index == 1:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))




            elif self.choices_index == 2:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 255))

        elif self.game_state == "choose_or_flee":
            if self.bet_or_flee_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.bet_or_flee_index == 1:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))

            state.DISPLAY.blit(
                self.font.render(f"{self.bet_or_flee[0]}", True,
                                 (255, 255, 255)),
                (700, 160))

            state.DISPLAY.blit(
                self.font.render(f"{self.bet_or_flee[1]}", True,
                                 (255, 255, 255)),
                (700, 210))



        elif self.game_state == "magic_menu":
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

            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[0]}", True,
                                 (255, 255, 255)),
                (700, 160))

            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[1]}", True,
                                 (255, 255, 255)),
                (700, 210))

            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[2]}", True,
                                 (255, 255, 255)),
                (700, 260))




        elif self.game_state == "welcome_opposum":
            state.DISPLAY.blit(self.font.render(f"press T", True, (255, 255, 255)),
                         (10, 10))
        elif self.game_state == "choose_can":
            state.DISPLAY.blit(self.font.render(f"Press 1 to choose  a opossum", True,
                                          (255, 255, 255)), (100, 10))



        elif self.game_state == "play_again_or_bail":
            state.DISPLAY.blit(self.font.render(f"your result is {self.result}", True,
                                          (255, 255, 255)), (388, 50))
            if self.play_again_or_quit_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 155))



            elif self.play_again_or_quit_index == 1:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (650, 205))

            state.DISPLAY.blit(
                self.font.render(f"{self.play_again_or_quit[0]}", True,
                                 (255, 255, 255)),
                (700, 160))

            state.DISPLAY.blit(
                self.font.render(f"{self.play_again_or_quit[1]}", True,
                                 (255, 255, 255)),
                (700, 210))

        elif self.game_state == "loser_screen":
            state.DISPLAY.blit(
                self.font.render(f"You drew the {self.result} you lose goodbye",
                                 True, (255, 255, 255)), (210, 50))

        pygame.display.flip()
