import random
import time
from typing import List

import pygame

from entity.gui.textbox.text_box import TextBox
from screen.screen import Screen


#
#
#
#   ON LOSS OR IF ALL EMPTY BUT LOSE, LOCK OUT GRAB UNTIL PLAYER HITS RESHUFFLE
#

## PRESS B TO GET OUT FOR OPTIONS

class OpossumInACanScreen(Screen):
    def __init__(self):
        super().__init__("Opossum in a can screen")
        self.third_message_display = ""
        self.desperate = False
        self.debuff_keen_perception = False
        # we can set this as a variable that can get toggled on and off depending on who you are playing aginst
        self.sallyOpossumMoney = 1200
        self.opossumBite = False
        self.sallyOpossumIsDefeated = False
        self.opossum_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 36)
        self.player_score = 0
        self.opossum_index = 0
        self.magic_menu_selector_index = 0
        self.game_state = "welcome_opposum"
        self.winner_or_looser: List[str] = ["win", "win",
                                            "win", "win", "lose",
                                            "lucky_star",
                                            "X3_star", "lose",

                                     ]

        self.opossumInACanMessages = {
            "welcome_message": TextBox(
                ["Press T to select options and go through T messages", "Welcome to Opossum in a can !", "No take backs on your bet, I had to set up the cans after all", ""],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "pick_message": TextBox(
                ["Keep picking boxes I believe in you......Dont forget that B opens the menu ", ""],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "play_again_or_leave_message": TextBox(
                ["Get ready for some fun! "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "rapid_opossum_ message": TextBox(
                ["Oh no you got bite!!! Wrong Trash can!!!! ", ""],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "opossum_defeated_message": TextBox(
                ["WEll since you beat me I have a super secret item just for you hero take it!! ", "you open the treash can and get bit by a rapid opossom;)", "Ooops I didn't meanto do that, oh well i'll be seeing you soon enjoy your lat bit of humanity", ""],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "hero_defeated_stamina_message": TextBox(
                ["if i gamble anymore i'll pass out right in front of the dealer", ""],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "hero_defeated_money_message": TextBox(
                ["i need more money to play i should leave ", ""],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),


            # You can add more game state keys and TextBox instances here
        }
        self.result = "win"
        self.bet = 200
        self.insurance = 200
        self.X3 = False
        self.trash_can_pick = ""
        self.magic_menu_opossum_index = 0

        self.game_state = "welcome_screen"

        self.box_color = (255, 0, 0)  # Initially red

        self.has_opossum_insurance = True

        self.choices = ["Grab", "Magic", "Quit"]
        self.choices_index = 0

        self.bet_or_flee = ["bet", "flee"]
        self.bet_or_flee_index = 0
        self.menu_selector = ["grab", "magic", "reshuffle", "quit"]


        self.magic_menu_selector = ["Back", "Keen"]
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



    def reveal_selected_box_content(self, state):
        selected_can_attribute = f'can{self.green_box_index + 1}'
        selected_box_content = getattr(self, selected_can_attribute)
        print(f"Selected box content: {selected_box_content}")

        if selected_box_content == "win":
            self.trash_can_pick = "win"
            self.player_score += 50

        if selected_box_content == "X3_star":
            self.trash_can_pick = "X3_star"

            self.player_score *= 3

        if selected_box_content == "lucky_star":
            self.trash_can_pick = "lucky_star"
            self.player_score += 200

        if selected_box_content == "lose":
            self.trash_can_pick = "lose"

            self.player_score = 0
            self.opossumBite = True


        # Remove the item from the can (set it to an empty string)
        setattr(self, selected_can_attribute, "")

    def update(self, state: "GameState"):
        if self.fill_cans == True:
            self.initializeGarbageCans()
            self.fill_cans = False
            state.player.money -= 200

        if state.controller.isQPressed:
            # Transition to the main screen
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return




        if self.game_state == "welcome_screen":
            self.opossumInACanMessages["welcome_message"].update(state)

            if self.opossumInACanMessages["welcome_message"].message_index == 3:

                self.game_state = "menu_screen"


        if self.game_state == "menu_screen":

            if state.controller.isUpPressed:
                self.opossum_index -= 1
                if self.opossum_index < 0:
                    self.opossum_index = len(self.menu_selector) - 1  # Wrap around to the last item
                    print(str(self.opossum_index))

                # print(self.magic_menu_selector[self.magicindex])  # Print the current menu item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses

            elif state.controller.isDownPressed:
                self.opossum_index += 1
                if self.opossum_index >= len(self.menu_selector):
                    self.opossum_index = 0  # Wrap around to the first item
                    print(str(self.opossum_index))

                # print(self.magic_menu_selector[self.magicindex])  # Print the current menu item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses




        if self.game_state == "pick_screen":
            if state.controller.isBPressed:
                self.game_state = "menu_screen"


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

            # Check for 'T' key press
            if state.controller.isTPressed:
                # Call the function to reveal the selected box content
                self.reveal_selected_box_content(state)

            self.opossumInACanMessages["pick_message"].update(state)

        if self.game_state == "magic_menu_screen":
            if state.controller.isUpPressed:
                self.magic_menu_opossum_index -= 1
                if self.magic_menu_opossum_index < 0:
                    self.magic_menu_opossum_index = len(self.magic_menu_selector) - 1  # Wrap around to the last item
                    print(str(self.magic_menu_opossum_index))

                # print(self.magic_menu_selector[self.magicindex])  # Print the current menu item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses

            elif state.controller.isDownPressed:
                self.magic_menu_opossum_index += 1
                if self.magic_menu_opossum_index >= len(self.magic_menu_selector):
                    self.magic_menu_opossum_index = 0  # Wrap around to the first item
                    print(str(self.magic_menu_opossum_index))

                # print(self.magic_menu_selector[self.magicindex])  # Print the current menu item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses




        if self.game_state == "play_again_or_leave_screen":
            self.opossumInACanMessages["play_again_or_leave_message"].update(state)

        if self.game_state == "opossum_defeated_screen":
            self.opossumBite = True
            self.opossumInACanMessages["opossum_defeated_message"].update(state)
            if self.opossumInACanMessages["opossum_defeated_message"].message_index == 3:
                # Change the game state to "bet"
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)


        if self.game_state == "hero_defeated_stamina_screen":
            self.opossumInACanMessages["hero_defeated_stamina_message"].update(state)
            if self.opossumInACanMessages["hero_defeated_stamina_message"].message_index == 1:
                # Change the game state to "bet"
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)

        if self.game_state == "hero_defeated_money_screen":
            self.opossumInACanMessages["hero_defeated_money_message"].update(state)
            if self.opossumInACanMessages["hero_defeated_money_message"].message_index == 1:
                # Change the game state to "bet"
                state.currentScreen = state.mainScreen
                state.mainScreen.start(state)




            # if self.opossumInACanMessages["defeat_message"].message_index == 2:
            #
            #     self.game_state = "pick_screen"



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
        # ... [your previous code for setup and calculating positions]

        # Draw the boxes
        for i, pos in enumerate(positions):
            # Determine the color based on the green box index
            box_color = (0, 255, 0) if i == self.green_box_index else (255, 0, 0)

            # Check if the current box contains an opossum
            current_can_content = getattr(self, f'can{i + 1}')

            # If debuff is active, apply the shaking effect
            if self.debuff_keen_perception == True:
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

        # print(str(self.game_state))

        if self.game_state == "welcome_screen":
            # self.opossumInACanMessages["welcome_message"].update(state)

            self.opossumInACanMessages["welcome_message"].draw(state)

        if self.game_state == "menu_screen":
            bet_box_width = 150
            # Increase the bet box height by an additional 40 pixels
            bet_box_height = 100 + 40 + 40  # Increased height by 40 pixels initially and 40 more now
            border_width = 5

            screen_width, screen_height = state.DISPLAY.get_size()
            bet_box_x = screen_width - bet_box_width - border_width - 30
            # Adjust the Y position of the bet box to accommodate the increased height
            bet_box_y = screen_height - 130 - bet_box_height - border_width - 60

            bet_box = pygame.Surface((bet_box_width, bet_box_height))
            bet_box.fill((0, 0, 0))
            white_border = pygame.Surface((bet_box_width + 2 * border_width, bet_box_height + 2 * border_width))
            white_border.fill((255, 255, 255))
            white_border.blit(bet_box, (border_width, border_width))

            # Calculate text positions - you might want to adjust these further if needed
            text_x = bet_box_x + 40 + border_width
            text_y_yes = bet_box_y + 20
            text_y_no = text_y_yes + 40  # Consider adjusting this if needed due to the taller box
            # Draw the box on the screen
            state.DISPLAY.blit(white_border, (bet_box_x, bet_box_y))

            # Draw the text on the screen (over the box)
            state.DISPLAY.blit(self.font.render(f"Grab ", True, (255, 255, 255)), (text_x, text_y_yes))
            if self.debuff_keen_perception == False:
                state.DISPLAY.blit(self.font.render(f"Magic ", True, (255, 255, 255)), (text_x, text_y_yes + 40))
            elif self.debuff_keen_perception == True:
                state.DISPLAY.blit(self.font.render("Locked", True, (255, 255, 255)), (text_x, text_y_yes + 40))

            state.DISPLAY.blit(self.font.render(f"Reshuffle ", True, (255, 255, 255)), (text_x, text_y_yes + 80))
            state.DISPLAY.blit(self.font.render(f"Quit ", True, (255, 255, 255)), (text_x, text_y_yes + 120))

            arrow_x = text_x + 20 - 40  # Adjust the arrow position to the left of the text
            arrow_y = text_y_yes + self.opossum_index * 40  # Adjust based on the item's height
            # Set the initial arrow position to "Yes"

            # Draw the arrow next to the selected option
            # state.DISPLAY.blit(self.font.render(">", True, (255, 255, 255)), (arrow_x, arrow_y))
            # arrow_x = text_x - 40  # Adjust the position of the arrow based on your preference
            # arrow_y = text_y_yes + self.arrow_index * 40  # Adjust based on the item's height
            #
            # # Draw the arrow using pygame's drawing functions (e.g., pygame.draw.polygon)
            # Here's a simple example using a triangle:
            pygame.draw.polygon(state.DISPLAY, (255, 255, 255),
                                [(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y + 10)])

            if state.controller.isTPressed:
                if self.opossum_index == 0:
                    print(str(self.game_state))
                    state.controller.isTPressed = False

                    self.game_state = "pick_screen"

                    print(str(self.game_state))
                elif self.opossum_index == 1 and self.debuff_keen_perception == False:
                    state.controller.isTPressed = False
                    self.game_state = "magic_menu_screen"
                elif self.opossum_index == 2:
                    state.player.money += self.player_score
                    self.sallyOpossumMoney -= self.player_score
                    state.controller.isTPressed = False
                    self.refresh()
                    self.initializeGarbageCans()
                    self.game_state = "pick_screen"
                elif self.opossum_index == 3:
                    state.player.money += self.player_score
                    self.sallyOpossumMoney -= self.player_score
                    state.controller.isTPressed = False
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)





        if self.game_state == "pick_screen":


            # self.opossumInACanMessages["welcome_message"].update(state)
            if self.opossumInACanMessages["pick_message"].message_index == 1:
                state.DISPLAY.blit(self.font.render(f"Your pick equals :{self.trash_can_pick}", True,
                                                    (255, 255, 255)), (70, 460))


                    # if state.controller.isTPressed:
                    #     state.controller.isTPressed = False  # Reset the button state
                    #
                    #     self.game_state = "play_again_or_leave_screen"


            self.opossumInACanMessages["pick_message"].draw(state)


        if self.game_state == "magic_menu_screen":

            bet_box_width = 150  # Width for both boxes
            top_box_height = 50  # Height for top box
            bet_box_height = 100 + 40 - 50  # Height for bottom box, now 50 pixels shorter
            border_width = 5

            # Screen dimensions
            screen_width, screen_height = state.DISPLAY.get_size()

            # Positions for the top and bottom boxes
            new_box_x = screen_width - bet_box_width - border_width - 30  # X position for both top and bottom boxes
            magic_box_y = 320 - 40
            new_box_y = magic_box_y - top_box_height - border_width + 50  # Adjusted Y position for top box

            # Create the top box (black box with white border but no bottom border)
            black_box_top = pygame.Surface((bet_box_width, top_box_height))
            black_box_top.fill((0, 0, 0))
            white_border_top = pygame.Surface((bet_box_width + 2 * border_width, top_box_height + border_width))
            white_border_top.fill((255, 255, 255))
            white_border_top.blit(black_box_top, (border_width, border_width))
            state.DISPLAY.blit(white_border_top, (new_box_x, new_box_y))

            # Adjusted bottom box positions
            bet_box_x = new_box_x  # Aligning with the top box
            bet_box_y = screen_height - 130 - bet_box_height - border_width - 60 + 50 - 40  # Raised by 40 pixels, accounting for borders

            # Create the bottom box (now shorter)
            bottom_box = pygame.Surface((bet_box_width, bet_box_height))
            bottom_box.fill((0, 0, 0))
            white_border_bottom = pygame.Surface((bet_box_width + 2 * border_width, bet_box_height + 2 * border_width))
            white_border_bottom.fill((255, 255, 255))
            white_border_bottom.blit(bottom_box, (border_width, border_width))
            state.DISPLAY.blit(white_border_bottom, (bet_box_x, bet_box_y))

            # Adjust text and arrow positions relative to the bottom box
            text_x = bet_box_x + 40 + border_width
            text_y_yes = bet_box_y + 20  # Adjusted back to the original position
            text_y_no = text_y_yes + 40
            # Adjust arrow positions relative to the bottom box
            arrow_x = text_x - 20  # Arrow position adjusted to the left of the text
            arrow_y = text_y_yes + self.magic_menu_selector_index * 40  # Arrow position adjusted based on selected menu item

            # Draw text
            # Draw text
            if "Keen" in self.magic_menu_selector:
                state.DISPLAY.blit(self.font.render(f"{self.magic_menu_selector[1]} ", True, (255, 255, 255)), (text_x, text_y_yes))
            else:
                state.DISPLAY.blit(self.font.render(" ", True, (255, 255, 255)), (text_x, text_y_yes))

            state.DISPLAY.blit(self.font.render(f"{self.magic_menu_selector[0]} ", True, (255, 255, 255)), (text_x, text_y_yes + 40))
            # Y position for "Shield" text, using self.magic_menu_selector[1]
            text_y_shield = text_y_yes  # Assuming "Shield" is rendered at this position

            # Draw the arrow on the same Y coordinate as "Shield"
            # Adjust arrow_x if necessary to position it correctly relative to the "Shield" text
            arrow_x = text_x - 20  # Arrow position adjusted to the left of the text
            arrow_y = text_y_shield + self.magic_menu_opossum_index * 40  # Update arrow Y position based on selected item
            # print(str(self.magic_menu_selector))
            # Draw the arrow using pygame's drawing functions
            pygame.draw.polygon(state.DISPLAY, (255, 255, 255),
                                [(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y + 10)])

            magic_text = self.font.render("Magic", True, (255, 255, 255))  # Render "Magic" in white color
            text_margin = 10  # Margin from the left edge of the top box for the text

            # Position for the "Magic" text inside the top box
            magic_text_x = new_box_x + text_margin
            magic_text_y = new_box_y + (top_box_height - magic_text.get_height()) // 2  # Vertically center inside the top box

            # Blit the "Magic" text onto the screen
            state.DISPLAY.blit(magic_text, (magic_text_x, magic_text_y))
            print(str(self.debuff_keen_perception))
            if state.controller.isTPressed:
                if self.magic_menu_opossum_index == 0:
                    self.debuff_keen_perception = True
                    state.player.focus_points -= 10
                    self.game_state = "menu_screen"
                    state.controller.isTPressed = False  # Reset the button state

                elif self.magic_menu_opossum_index == 1:
                    state.controller.isTPressed = False  # Reset the button state

                    self.game_state = "menu_screen"


            #     elif self.magicindex == 1:
            #         print(str(self.magic_menu_selector[1]))
            #         self.game_state = "heads_tails_choose_screen"
            #         state.controller.isTPressed = False  # Reset the button state





        if self.game_state == "play_again_or_leave_screen":
            self.opossumInACanMessages["play_again_or_leave_message"].draw(state)

        if self.game_state == "opossum_defeated_screen":
            self.opossumInACanMessages["opossum_defeated_message"].draw(state)


        if self.game_state == "hero_defeated_stamina_screen":
            self.opossumInACanMessages["hero_defeated_stamina_message"].draw(state)

        if self.game_state == "hero_defeated_money_screen":
            self.opossumInACanMessages["hero_defeated_stamina_screen"].draw(state)










        pygame.display.flip()
