import random
import time
from typing import List

import pygame

from screen.screen import Screen


class OpossumInACanScreen(Screen):
    def __init__(self):
        super().__init__("Opossum in a can screen")
        self.third_message_display = ""
        self.desperate = False
        # we can set this as a variable that can get toggled on and off depending on who you are playing aginst
        self.sallyOpossumMoney = 100
        self.sallyOpossumIsDefeated = False
        self.opossum_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 36)
        self.player_score = 0
        self.game_state = "welcome_opposum"
        self.winner_or_looser: List[str] = ["win", "win",
                                            "win", "win", "lose",
                                            "lucky_star",
                                            "X3_star", "lose",

                                     ]
        self.result = "win"
        self.bet = 20
        self.insurance = 200
        self.X3 = False

        self.box_color = (255, 0, 0)  # Initially red

        self.has_opossum_insurance = True

        self.choices = ["Grab", "Magic", "Quit"]
        self.choices_index = 0

        self.bet_or_flee = ["bet", "flee"]
        self.bet_or_flee_index = 0

        self.magic_menu_selector = ["Bluff", "Reveal", "Lucky", "Back"]
        self.magic_menu_index = 0

        self.play_again_or_quit = ["Play Again", "Quit"]

        self.play_again_or_quit_index = 0

        self.bluff_activated = 0
        self.bottom_message = ""
        self.opossum_rader = False

        self.luck_activated = 0

        self.green_box_index = 0  # Index of the currently green box
        self.initializeGarbageCans()
        self.can1 = ""
        self.can2 = ""
        self.can3 = ""
        self.can4 = ""
        self.can5 = ""
        self.can6 = ""
        self.can7 = ""
        self.can8 = ""

        self.fill_cans = True
        self.shake = False

    def initializeGarbageCans(self):
        # Randomly shuffle the winner_or_looser list
        shuffled_items = random.sample(self.winner_or_looser, len(self.winner_or_looser))

        # Assign a shuffled item to each can and print the content
        self.can1 = shuffled_items[0]
        print("Can 1 contains:", self.can1)

        self.can2 = shuffled_items[1]
        print("Can 2 contains:", self.can2)

        self.can3 = shuffled_items[2]
        print("Can 3 contains:", self.can3)

        self.can4 = shuffled_items[3]
        print("Can 4 contains:", self.can4)

        self.can5 = shuffled_items[4]
        print("Can 5 contains:", self.can5)

        self.can6 = shuffled_items[5]
        print("Can 6 contains:", self.can6)

        self.can7 = shuffled_items[6]
        print("Can 7 contains:", self.can7)

        self.can8 = shuffled_items[7]
        print("Can 8 contains:", self.can8)

    def refresh(self):
        self.bet = 20
        self.has_opossum_insurance = True
        self.insurance = 200

        self.winner_or_looser = ["win", "win",  "win",
                                 "lucky_star", "lucky_star",
                                 "X3_star", "win",

                                ]

    # def giveExp(self, state: "GameState"):
    #     # print("Player exp is: " + str(state.player.exp))
    #     if self.result == self.player_choice:
    #         state.player.exp += 30
    #         if self.bet > 60:
    #             state.player.stamina_points -= 1
    #
    #     elif self.result != self.player_choice:
    #         state.player.exp += 20
    #         if self.bet > 60:
    #             state.player.stamina_points -= 2

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
        if self.fill_cans == True:
            self.initializeGarbageCans()
            self.fill_cans = False


        key_press_threshold = 80  # Example threshold, adjust as needed

        # Debugging: Print the time since the last right key press
        time_since_right_pressed = state.controller.timeSinceKeyPressed(pygame.K_RIGHT)
        # print(f"Time since right key pressed: {time_since_right_pressed}")

        # Check if enough time has passed since the last right key press
        if state.controller.isRightPressed and time_since_right_pressed >= key_press_threshold:
            # Move to the next box
            self.green_box_index = (self.green_box_index + 1) % 8

            # Print the current green box index and its content
            current_can_content = getattr(self, f'can{self.green_box_index + 1}')
            print(f"Current green box index: {self.green_box_index}, Content: {current_can_content}")

            # Reset the key pressed time
            state.controller.keyPressedTimes[pygame.K_RIGHT] = pygame.time.get_ticks()

        if state.controller.isQPressed:
            # Transition to the main screen
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

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
                if controller.isKPressed and state.player.focus_points > 9:
                    if len(self.winner_or_looser) < 6:
                        if state.player.focus_points >= 10:
                            state.player.focus_points -= 10

                            print("You cast bluff")
                            print("I'll bet you I'll get the rst of the wins")
                            state.player.money += self.sallyOpossumMoney
                            self.sallyOpossumIsDefeated = True
                            self.sallyOpossumMoney = 0
                            print("exiting now")

                        else:
                            self.third_message_display = "Sorry but you dont have enough focus points to cast"
                    else:
                        self.third_message_display = "sorry but you can't stack magic spells.Wait till 3 wins left to cast."


            elif self.magic_menu_index == 1:
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





            ##########################have a message state reserved for buff states

            ##### boss enemies will use magic under more strict conditions
            elif self.magic_menu_index == 2:
                if controller.isKPressed and self.luck_activated == 0:
                    print("you cast avatar of luck")
                    self.third_message_display = "The god of luck shines on you, looks like another trash can was hiding behind one of the others"
                    state.player.focus_points -= 20
                    self.winner_or_looser.append("win")

                    self.game_state = "choose_can"
                    self.luck_activated = 5



            elif self.magic_menu_index == 3:
                if controller.isKPressed:
                    print("going back")
                    self.game_state = "choose_can"

                    #########################################################################


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

        # self.fill_cans = True

    def draw(self, state: "GameState"):
        state.DISPLAY.fill((0, 0, 51))
        current_time = pygame.time.get_ticks()
        shake_duration = 1000  # 1 second in milliseconds
        shake_interval = 3000  # 3 seconds in milliseconds

        box_size = 64
        margin = 30

        # Calculate positions for the boxes
        positions = []
        for row in range(2):
            for col in range(4):
                x = col * (box_size + margin) + margin + 270
                y = row * (box_size + margin) + margin + 70
                positions.append((x, y))

        # Draw the boxes
        # Initialize flags to track if a "lose" can and "X3_star" can have already been shaken
        shaken_lose = False
        shaken_x3_star = False

        # ...

        # Draw the boxes
        for i, pos in enumerate(positions):
            # Determine the color based on the green box index
            box_color = (0, 255, 0) if i == self.green_box_index else (255, 0, 0)

            # Check if the current box contains an opossum
            current_can_content = getattr(self, f'can{i + 1}')

            # Check if the current can is of type "lose" and has not been shaken yet
            if current_can_content == 'lose' and not shaken_lose:
                shaken_lose = True
                time_since_last_shake = current_time % shake_interval
                if time_since_last_shake < shake_duration:
                    shake_effect = random.randint(-2, 2)  # Small random offset for shaking
                    pos = (pos[0] + shake_effect, pos[1] + shake_effect)

            # Check if the current can is of type "X3_star" and has not been shaken yet
            if current_can_content == 'X3_star' and not shaken_x3_star:
                shaken_x3_star = True
                time_since_last_shake = current_time % shake_interval
                if time_since_last_shake < shake_duration:
                    shake_effect = random.randint(-2, 2)  # Small random offset for shaking
                    pos = (pos[0] + shake_effect, pos[1] + shake_effect)

            # Draw the box with the determined color
            pygame.draw.rect(state.DISPLAY, box_color, (*pos, box_size, box_size))

        # Choose two random boxes that do not contain "lose"



        # Apply shaking effect to selected boxes









        #this box is for hero info
        box_width = 200 - 10
        box_height = 180 - 10
        new_box_height = box_height + 40
        black_box = pygame.Surface((box_width, new_box_height))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((box_width + 2 * border_width, new_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 235 - 40))

        # Box for hero name
        black_box = pygame.Surface((200 - 10, 45 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 195 - 40))  # Moved up by 40 pixels
        state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True,
                                            (255, 255, 255)), (37, 250 - 40))
        state.DISPLAY.blit(
            self.font.render(f"HP: {state.player.stamina_points}", True,
                             (255, 255, 255)), (37, 290 - 40))

        state.DISPLAY.blit(self.font.render(f"MP: {state.player.focus_points}", True,
                                            (255, 255, 255)), (37, 330 - 40))
        state.DISPLAY.blit(
            self.font.render(f"Bet: {self.bet}", True, (255, 255, 255)),
            (37, 370 - 40))

        state.DISPLAY.blit(self.font.render(f"Score: {self.player_score} ", True, (255, 255, 255)), (37, 370))

        state.DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)),
                           (37, 205 - 40))

        #the below is for enemy boxes
        # holds enemy name
        black_box = pygame.Surface((200 - 10, 110 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 20))
        state.DISPLAY.blit(self.font.render("Enemy", True, (255, 255, 255)), (37, 33))
        box_width = 200 - 10
        box_height = 130 - 10
        new_box_height = box_height - 40
        black_box = pygame.Surface((box_width, new_box_height))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((box_width + 2 * border_width, new_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 60))

        state.DISPLAY.blit(self.font.render(f"Money: {self.sallyOpossumMoney}", True,
                                            (255, 255, 255)), (37, 70))


        state.DISPLAY.blit(self.font.render(f"Status: normal", True,
                                                (255, 255, 255)), (37, 110))


        #this creates the text box for our below messages
        black_box_height = 130
        black_box_width = 700
        border_width = 5
        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill((0, 0, 0))
        white_border = pygame.Surface((black_box_width + 2 * border_width, black_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        screen_width, screen_height = state.DISPLAY.get_size()
        black_box_x = (screen_width - black_box_width) // 2 - border_width
        black_box_y = screen_height - black_box_height - 20 - border_width
        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))





        pygame.display.flip()
