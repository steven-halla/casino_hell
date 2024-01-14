import random

import pygame
import sys

from entity.gui.textbox.text_box import TextBox
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
        self.choice_sequence = True
        self.bet = 0
        self.font = pygame.font.Font(None, 36)
        self.coinFlipTedMoney = 10
        self.coinFlipTedDefeated = False
        self.win_exp = False
        self.lose_exp = False
        self.game_state = "welcome_screen"
        self.coin_flip_messages = {
            "welcome_screen": TextBox(
                ["Welcome to black jack where you get all the best stuff", "press T to select", ""],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            )
            # You can add more game state keys and TextBox instances here
        }


    def giveExp(self, state: "GameState"):
        if self.win_exp == True:
            state.player.exp += 30
        elif self.lose_exp == True:
            state.player.exp += 20

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
        if state.controller.isQPressed:
            # Transition to the main screen
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

        if self.game_state == "welcome_screen":
            # Update the welcome screen text box
            self.coin_flip_messages["welcome_screen"].update(state)

            # Check if the text box message index is at the second element (index 1)
            if self.coin_flip_messages["welcome_screen"].message_index == 2:
                # Change the game state to "bet"
                self.game_state = "bet"

            # Add other game state updates here

            # Print the current game state for debugging
        print("Current game state:", self.game_state)






                # Update the controller
        controller = state.controller
        controller.update()


























    ########################we want up and down arrows on bet. have arrow disapear when an item is not in use

    def draw(self, state: "GameState"):
        # background
        state.DISPLAY.fill((0, 0, 51))
        #this box is for hero money , bet amount and other info
        black_box = pygame.Surface((200 - 10, 180 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 235))
        #holds horo name
        black_box = pygame.Surface((200 - 10, 45 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 195))

        state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True,
                                            (255, 255, 255)), (37, 250))
        state.DISPLAY.blit(
            self.font.render(f"HP: {state.player.stamina_points}", True,
                             (255, 255, 255)), (37, 290))

        state.DISPLAY.blit(self.font.render(f"MP: {state.player.focus_points}", True,
                                            (255, 255, 255)), (37, 330))
        state.DISPLAY.blit(
            self.font.render(f"Bet: {self.bet}", True, (255, 255, 255)),
            (37, 370))

        state.DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)),
                           (37, 205))
        #holds enemy name
        black_box = pygame.Surface((200 - 10, 110 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 20))

        state.DISPLAY.blit(self.font.render("Enemy", True, (255, 255, 255)), (37, 33))

        #holds enemy status, money and other info
        black_box = pygame.Surface((200 - 10, 130 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 130 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 60))

        state.DISPLAY.blit(self.font.render(f"Money: {self.coinFlipTedMoney}", True,
                                            (255, 255, 255)), (37, 70))

        state.DISPLAY.blit(self.font.render(f"Status: ", True,
                                            (255, 255, 255)), (37, 110))

        black_box_height = 130
        black_box_width = 700
        border_width = 5  # Width of the white border

        # Create the black box
        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill((0, 0, 0))  # Fill the box with black color

        # Create a white border
        white_border = pygame.Surface((black_box_width + 2 * border_width, black_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))  # Fill the border with white color
        white_border.blit(black_box, (border_width, border_width))

        # Determine the position of the white-bordered box
        # Assuming you want it centered horizontally and at the bottom of the screen
        screen_width, screen_height = state.DISPLAY.get_size()
        black_box_x = (screen_width - black_box_width) // 2 - border_width
        black_box_y = screen_height - black_box_height - 20 - border_width  # Subtract 20 pixels and adjust for border

        # Blit the white-bordered box onto the display
        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

        if self.game_state == "welcome_screen":
            self.coin_flip_messages["welcome_screen"].update(state)
            self.coin_flip_messages["welcome_screen"].draw(state)

            # heads_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/tails.png")

            # Get the size of the screen and the image
            # screen_width, screen_height = state.DISPLAY.get_size()
            # image_width, image_height = heads_image.get_size()
            #
            # # Calculate the position to center the image
            # image_x = (screen_width - image_width) // 2
            # image_y = (screen_height - image_height) // 2
            #
            # # Blit the image onto the screen at the calculated position
            # state.DISPLAY.blit(heads_image, (image_x, image_y))
            #
            # # Update and draw the welcome screen text box
            # self.coin_flip_messages["welcome_screen"].update(state)
            # self.coin_flip_messages["welcome_screen"].draw(state)'

        if self.game_state == "bet":
            print("Game state is 'bet'")  # Debugging

            bet_box_width = 150
            bet_box_height = 100
            border_width = 5

            screen_width, screen_height = state.DISPLAY.get_size()
            bet_box_x = screen_width - bet_box_width - border_width - 30
            bet_box_y = screen_height - 130 - bet_box_height - border_width - 60

            bet_box = pygame.Surface((bet_box_width, bet_box_height))
            bet_box.fill((0, 0, 0))
            white_border = pygame.Surface((bet_box_width + 2 * border_width, bet_box_height + 2 * border_width))
            white_border.fill((255, 255, 255))
            white_border.blit(bet_box, (border_width, border_width))

            # Calculate text positions
            text_x = bet_box_x + 40 + border_width
            text_y_yes = bet_box_y + 20
            text_y_no = text_y_yes + 40

            print(f"Text positions - Yes: ({text_x}, {text_y_yes}), No: ({text_x}, {text_y_no})")  # Debugging

            # Draw the box on the screen
            state.DISPLAY.blit(white_border, (bet_box_x, bet_box_y))

            # Draw the text on the screen (over the box)
            state.DISPLAY.blit(self.font.render(f"Yes ", True, (255, 255, 255)), (text_x, text_y_yes))

        pygame.display.flip()












