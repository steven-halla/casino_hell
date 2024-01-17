import random
import time
from typing import List

import pygame

from entity.gui.textbox.text_box import TextBox
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

        self.opossumInACanMessages = {
            "welcome_message": TextBox(
                ["Press T to select options and go through T messages", "Welcome to Opossum in a can !", "Can you spell Opossum, i sure can't", ""],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "bet_message": TextBox(
                ["Put one bet of 100 coins down. You can win big with opossum in a can. Yes you can. "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "heads_tails_message": TextBox(
                ["Get ready for some fun! "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),


            # You can add more game state keys and TextBox instances here
        }
        self.result = "win"
        self.bet = 20
        self.insurance = 200
        self.X3 = False

        self.game_state = "welcome_screen"

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


    def check_results(self, state: "GameState"):
        pass

    def update(self, state: "GameState"):
        if self.fill_cans == True:
            self.initializeGarbageCans()
            self.fill_cans = False

        if state.controller.isQPressed:
            # Transition to the main screen
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return


        if self.game_state == "welcome_screen":
            self.opossumInACanMessages["welcome_message"].update(state)

            if self.opossumInACanMessages["welcome_message"].message_index == 3:

                self.game_state = "pick_screen"

        if self.game_state == "pick_screen":
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



        controller = state.controller
        controller.update()


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

        print(str(self.game_state))

        if self.game_state == "welcome_screen":
            # self.opossumInACanMessages["welcome_message"].update(state)

            self.opossumInACanMessages["welcome_message"].draw(state)





        pygame.display.flip()
