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
        self.coinFlipTedMoney = 100
        self.coinFlipTedDefeated = False
        self.win_exp = False
        self.flip_timer = pygame.time.get_ticks() + 4000  # Initialize with a future time (2 seconds from now)
        self.pause_timer = 0  # Initialize with a future time (2 seconds from now)
        self.heads_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/heads.png")
        self.tails_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/tails.png")

        self.lose_exp = False
        self.game_state = "welcome_screen"
        self.coin_flip_messages = {
            "welcome_message": TextBox(
                ["Welcome to black jack where you get all the best stuff", "press T to select", ""],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "bet_message": TextBox(
                ["Min Bet is 10 and Max Bet is 100. The more you bet the more your  stamina is drained. "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "flip_message": TextBox(
                ["Flipping the coin now hold your breath . "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "results_message": TextBox(["  " ], (50, 450, 700, 130), 36, 500),
            "play_again_message": TextBox(
                ["Would you like to play again? Hit T on your answer. "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),

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
            print(self.bet)


        elif controller.isDownPressed:
            self.bet -= 10
            pygame.time.delay(200)
            self.isDownPressed = False
            print(self.bet)


        if self.bet < 10:
            self.bet = 10

        if self.bet > 100:
            self.bet = 100

        if self.bet > self.coinFlipTedMoney:
            self.bet = self.coinFlipTedMoney

        if controller.isTPressed:
            self.game_state = "flip_screen"
            print(self.game_state)

    def flipCoin(self):
        coin = random.random()

        if coin < 0.6:
            print("coin landed on tails")
            self.result = "tails"
            self.game_state = "results_screen"
        else:
            print("coin landed on heads")
            self.result = "heads"
            self.game_state = "results_screen"


    def update(self, state: "GameState"):

        if state.controller.isQPressed:
            # Transition to the main screen
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return



        if self.game_state == "welcome_screen":
            # Update the welcome screen text box
            self.coin_flip_messages["welcome_message"].update(state)

            # Check if the text box message index is at the second element (index 1)
            if self.coin_flip_messages["welcome_message"].message_index == 2:
                # Change the game state to "bet"
                self.game_state = "bet_screen"
            
        if self.game_state == "bet_screen":
            self.coin_flip_messages["bet_message"].update(state)
            self.place_bet(state)  # Call the place_bet method to handle bet adjustments
                # Add other game state updates here

        if self.game_state == "flip_screen":
            elapsed_time = pygame.time.get_ticks() - self.pause_timer
            self.pause_timer += elapsed_time
            self.coin_flip_messages["flip_message"].update(state)

            print("Timer set to:", self.flip_timer)  # Add this line to check the timer value

            if self.pause_timer >= self.flip_timer:  # Check if pause_timer exceeds flip_timer
                print("am i gett called")
                print(self.game_state)

                self.flipCoin()
                self.pause_timer = 0
                # Add other game state updates here


        if self.game_state == "results_screen":
            self.coin_flip_messages["results_message"].update(state)

            # Construct the result message
            result_message = f"Here you go, the result of your flip: {self.result}"
            # bet_message = f"Bet amount: {self.bet}"

            # Update the messages in the TextBox
            self.coin_flip_messages["results_message"].messages = [result_message]

            if state.controller.isTPressed:
                self.game_state = "play_again_screen"
                print(str(self.game_state))

        if self.game_state == "play_again_screen":
            self.coin_flip_messages["play_again_message"].update(state)



            # print("here are the results")

            # Add other game state updates here

            # Print the current game state for debugging
        # print("Current game state:", self.game_state)






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
            self.coin_flip_messages["welcome_message"].update(state)
            self.coin_flip_messages["welcome_message"].draw(state)


        if self.game_state == "bet_screen":
            # print("Game state is 'bet'")  # Debugging
            self.coin_flip_messages["bet_message"].update(state)
            self.coin_flip_messages["bet_message"].draw(state)
            state.DISPLAY.blit(self.font.render(f"Your Current bet:{self.bet}", True,
                                                (255, 255, 255)), (50, 530))

            state.DISPLAY.blit(self.font.render(f"v", True, (255, 255, 255)),
                               (260, 550))
            state.DISPLAY.blit(self.font.render(f"^", True, (255, 255, 255)),
                               (257, 510))




        if self.game_state == "flip_screen":
            self.coin_flip_messages["flip_message"].update(state)
            self.coin_flip_messages["flip_message"].draw(state)

        # if self.game_state == "results_screen":
        #     self.coin_flip_messages["results_message"].update(state)
        #     self.coin_flip_messages["results_message"].draw(state)
        if self.game_state == "results_screen":
            self.coin_flip_messages["results_message"].update(state)
            self.coin_flip_messages["results_message"].draw(state)

            # Display the image based on self.result
            image_to_display = self.heads_image if self.result == "heads" else self.tails_image
            image_rect = image_to_display.get_rect()
            image_rect.center = (state.DISPLAY.get_width() // 2, state.DISPLAY.get_height() // 2)
            state.DISPLAY.blit(image_to_display, image_rect)
            state.DISPLAY.blit(self.font.render(f"Your Current hand :{self.result}", True,
                                                (255, 255, 255)), (70, 460))

            # Call the update method for the results_message TextBox
            self.coin_flip_messages["results_message"].update(state)

            # Now, draw the results_message TextBox
            self.coin_flip_messages["results_message"].draw(state)

        if self.game_state == "play_again_screen":
            self.coin_flip_messages["play_again_message"].update(state)
            self.coin_flip_messages["play_again_message"].draw(state)
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
            # Draw the box on the screen
            state.DISPLAY.blit(white_border, (bet_box_x, bet_box_y))

            # Draw the text on the screen (over the box)
            state.DISPLAY.blit(self.font.render(f"Yes ", True, (255, 255, 255)), (text_x, text_y_yes))
            state.DISPLAY.blit(self.font.render(f"No ", True, (255, 255, 255)), (text_x , text_y_yes + 40))

        pygame.display.flip()












