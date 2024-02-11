import random

import pygame

from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen



class CoinFlipTedScreen(Screen):
    def __init__(self):
        super().__init__("Casino Coin flip  Screen")
        self.flip_screen_initialized = True
        self.has_run_money_logic = False
        self.result = ""
        self.play_again = True
        self.players_side = ""
        self.new_font = pygame.font.Font(None, 36)
        self.message_display = ""
        self.second_message_display = ""
        self.third_message_display = ""
        self.magic_player_message_display = ""
        self.magic_enemy_message_display = ""

        self.headstailsindex = 0

        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)


        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)


        self.magicindex = 0
        self.yes_or_no_menu = ["Yes", "No"]
        self.heads_or_tails_Menu = ["Heads", "Tails"]
        self.magic_menu_selector = ["Back"]
        self.choice_sequence = True
        self.player_choice = ""
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.debuff_vanish = False
        self.debuff_counter = 0
        self.game_reset = False
        self.message_printed = False

        self.flip_screen_initialized = False  # Add this line


        self.coin_leaning_counter = 0

        self.coin_leaning_tracker = ""  # Initialize to "none" or similar


        self.bet = 0
        self.font = pygame.font.Font(None, 36)
        self.coinFlipTedMoney = 100

        self.coinFlipTedDefeated = False

        self.win_exp = False
        self.flip_timer = pygame.time.get_ticks() + 4000  # Initialize with a future time (2 seconds from now)
        self.pause_timer = 0  # Initialize with a future time (2 seconds from now)
        self.heads_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/heads.png")
        self.tails_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/tails.png")

        self.enemy_desperate_counter = False
        self.enemy_defeated_counter = False
        self.hero_desperate_counter = False

        self.entered_shield_screen = False  # Add this flag
        self.shield_triggered = False

        self.lose_exp = False

        self.music_file = "/Users/stevenhalla/code/casino_hell/assets/music/coin_flip_screen.mp3"
        self.music_volume = 0.5  # Adjust as needed
        self.initialize_music()
        self.music_on = True


        self.game_state = "welcome_screen"


        self.coin_flip_messages = {
            "welcome_message": TextBox(
                ["Press T to select options and go through T messages", "Welcome to Coin flip I'll make you flip!", ""],
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
            "heads_tails_message": TextBox(
                ["Choose heads or tails. "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "magic_message": TextBox(
                ["Choose your spell . "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "flip_message": TextBox(
                ["Flipping the coin now hold your breath. "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "results_message": TextBox(["  " ], (50, 450, 700, 130), 36, 500),
            "shield_message1": TextBox(
                ["A bird came down and stole the coin, who knows who won now. "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "shield_message2": TextBox(
                ["someone just took the coin "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "shield_message3": TextBox(
                ["now the coin is gone :(. "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "play_again_message": TextBox(
                [
                  " Would you like to play again or quit?"
                 ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "game_over_no_money": TextBox(
                ["Looks like your out of money, sorry time for you to go. "

                 ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "game_over_no_stamina": TextBox(
                ["Hero: I'm so tired, if I keep gambling i'll pass out at the dealer table. "

                 ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "enemy_desperate_message": TextBox(
                ["Enemy: NOOoooooo....Do you know how many years i've spent coin flipping!!! This is impossible! ",
                 "Hero: It's not,  either you've been doing it wrong for years, or you reached you best a long time ago",
                 "Enemy: Please...don't take my coins......you don't know what they do to people who lose all their coins!!!",
                 "Hero: Sadly for you I'm ruthless, I'm taking you out!", ""

                 ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "hero_desperate_message": TextBox(
                ["Hero: Why am I having so much trouble with this chump? ",
                 "I wonder if any of the towns people has a clue to defeat him?",
                 "Should I leave, or stay with it and trust in my luck?", ""

                 ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "enemy_defeated_message": TextBox(
                ["Hero: Well looks like I'm done with you! ",
                 "Enemy: Looks like it's back to an all chili diet for me!",
                 "Enemy: I bet Cindy will be happy to  hear that I lost my standing.....", ""

                 ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),


            # You can add more game state keys and TextBox instances here
        }



    def stop_music(self):
        pygame.mixer.music.stop()

    def initialize_music(self):
        # Initialize the mixer
        pygame.mixer.init()

        # Load the music file
        pygame.mixer.music.load(self.music_file)

        # Set the volume for the music (0.0 to 1.0)
        pygame.mixer.music.set_volume(self.music_volume)

        # Play the music, -1 means the music will loop indefinitely
        pygame.mixer.music.play(-1)

    def giveExp(self, state: "GameState"):
        # print("Player exp is: " + str(state.player.exp))
        if self.result == self.player_choice:

            if self.bet < 11:
                state.player.stamina_points -= 1
                print("Your before  total exp is: " + str(state.player.exp))

                state.player.exp += 10
                print("you gained: " + str(10) + "exp")
                print("Your after total exp is: " + str(state.player.exp))

            elif self.bet >= 50:
                state.player.stamina_points -= 1
                print("Your before  total exp is: " + str(state.player.exp))

                state.player.exp += 100
                print("you gained: " + str(100) + "exp")

                print("Your after total exp is: " + str(state.player.exp))


            elif self.bet < 50:
                state.player.stamina_points -= 1
                print("Your before  total exp is: " + str(state.player.exp))

                state.player.exp += 50
                print("you gained: " + str(50) + "exp")

                print("Your after  total exp is: " + str(state.player.exp))



        elif self.result != self.player_choice:
            if self.bet < 11:
                state.player.stamina_points -= 2
                print("Your before  total exp is: " + str(state.player.exp))

                state.player.exp += 5
                print("you gained: " + str(5) + "exp")

                print("Your after total exp is: " + str(state.player.exp))

            elif self.bet >= 50:
                state.player.stamina_points -= 3
                print("Your before  total exp is: " + str(state.player.exp))

                state.player.exp += 50
                print("you gained: " + str(50) + "exp")

                print("Your after total exp is: " + str(state.player.exp))


            elif self.bet < 50:
                state.player.stamina_points -= 2
                print("Your before  total exp is: " + str(state.player.exp))

                state.player.exp += 25
                print("you gained: " + str(25) + "exp")

                print("Your after total exp is: " + str(state.player.exp))

    def place_bet(self, state: "GameState"):
        controller = state.controller
        controller.update()

        if controller.isUpPressed:
            self.bet += 10
            self.menu_movement_sound.play()  # Play the sound effect once

            pygame.time.delay(200)
            self.isUpPressed = False
            print(self.bet)


        elif controller.isDownPressed:
            self.bet -= 10
            self.menu_movement_sound.play()  # Play the sound effect once

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

            self.game_state = "heads_tails_choose_screen"
            state.controller.isTPressed = False  # Reset the button state

    def flipCoin(self, state: "GameState"):
        # Check if we need to determine a new bias
        # coin = random.random()
        # if coin < 0.9:
        #     print("coin landed on tails")
        #     self.result = "tails"
        print("coin counter at:" + str(self.coin_leaning_counter))
        if self.coin_leaning_counter == 0:
            self.coin_leaning_counter += 5
            coin_fate = random.randint(1, 2)
            print("your coin fate is" + str(coin_fate))
            # print("coin counter at:" + str(self.coin_leaning_counter))
            if coin_fate == 1:
                self.coin_leaning_tracker = "tails"
                # self.coin_leaning_counter -= 1
            else:
                self.coin_leaning_tracker = "heads"
                # self.coin_leaning_counter -= 1

        if self.coin_leaning_tracker == "tails":
            coin_flip = random.randint(1, 100)
            print(str(coin_flip))
            if coin_flip <= 80:
                self.result = "tails"
                # self.coin_leaning_counter -= 1
                print("Your result is " + str(self.result))
            else:
                self.result = "heads"


        elif self.coin_leaning_tracker == "heads":
            coin_flip = random.randint(1, 100)
            print(str(coin_flip))

            if coin_flip <= 80:
                self.result = "heads"
                print(self.result)
            else:
                self.result = "tails"
                print(self.result)



    # Adjust for the player's luck

        self.coin_leaning_counter -= 1  # Decrement the counter after each coin flip


        self.game_state = "results_screen"

    def update(self, state: "GameState"):

        if self.music_on == True:
            self.stop_music()
            self.initialize_music()
            self.music_on = False



        # if self.coinFlipTedMoney <= 100 and self.enemy_desperate_counter == False:
        #     self.game_state = "enemy_desperate_screen"

        if self.coinFlipTedMoney < 10:
            self.coinFlipTedDefeated = True



        if state.controller.isQPressed:
            # Transition to the main screen
            state.currentScreen = state.startScreen
            state.startScreen.start(state)
            return



        if self.game_state == "welcome_screen":


            # Update the welcome screen text box
            self.coin_flip_messages["welcome_message"].update(state)

            # Check if the text box message index is at the second element (index 1)
            if self.coin_flip_messages["welcome_message"].message_index == 2:
                # Change the game state to "bet"
                self.game_state = "bet_screen"


        if self.game_state == "bet_screen":

            self.has_run_money_logic = False
            self.player_choice = ""
            self.message_printed = False

            self.coin_flip_messages["bet_message"].update(state)
            self.place_bet(state)  # Call the place_bet method to handle bet adjustments

        if self.game_state == "heads_tails_choose_screen":
            # print("welcome to the choice screen")
            self.coin_flip_messages["heads_tails_message"].update(state)

            # Handling Up Press
            if state.controller.isUpPressed:
                self.headstailsindex -= 1
                self.menu_movement_sound.play()  # Play the sound effect once

                if self.headstailsindex < 0:
                    self.headstailsindex = len(self.heads_or_tails_Menu) - 1  # Wrap around to the last item

                print(self.heads_or_tails_Menu[self.headstailsindex])  # Print the current menu item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses

            # Handling Down Press
            elif state.controller.isDownPressed:
                self.headstailsindex += 1
                self.menu_movement_sound.play()  # Play the sound effect once

                if self.headstailsindex >= len(self.heads_or_tails_Menu):
                    self.headstailsindex = 0  # Wrap around to the first item

                print(self.heads_or_tails_Menu[self.headstailsindex])  # Print the current menu item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses




        if self.game_state == "flip_screen":



            if not self.flip_screen_initialized:
                # print("Initializing flip timer")
                self.flip_timer = 2500  # Duration for the pause
                self.pause_timer = pygame.time.get_ticks()  # Current time
                self.flip_screen_initialized = True

            elapsed_time = pygame.time.get_ticks() - self.pause_timer


            if elapsed_time >= self.flip_timer:
                self.flipCoin(state)
                self.flip_screen_initialized = False
                self.pause_timer = 0  # Reset pause timer for the next use
            if elapsed_time >= self.flip_timer:
                self.flip_screen_initialized = False

            self.coin_flip_messages["flip_message"].update(state)


        if self.game_state == "results_screen":

            if not self.has_run_money_logic:
                if self.player_choice == self.result:
                    state.player.money += self.bet
                    self.coinFlipTedMoney -= self.bet
                elif self.player_choice != self.result:


                    state.player.money -= self.bet
                    self.coinFlipTedMoney += self.bet
                    if self.debuff_vanish == True:
                        import random
                        roll = random.randint(1, 100)
                        if roll > 10:
                            print("gotcha")
                            state.player.money += self.bet
                            self.coinFlipTedMoney -= self.bet

                            self.game_state = "shield_screen"

                self.has_run_money_logic = True

            self.coin_flip_messages["results_message"].update(state)

            # Construct the result message
            result_message = f"Here you go, the result of your flip: {self.result}"
            # bet_message = f"Bet amount: {self.bet}"

            # Update the messages in the TextBox
            self.coin_flip_messages["results_message"].messages = [result_message]



        if self.game_state == "play_again_screen":
            if self.coinFlipTedMoney < 10:
                self.coinFlipTedDefeated = True
                self.game_state = "enemy_defeated_screen"

            self.coin_flip_messages["play_again_message"].update(state)
            if not self.message_printed:
                self.giveExp(state)
                # Set the flag to True after printing the message
                self.message_printed = True

            if state.controller.isUpPressed:
                self.arrow_index -= 1
                self.menu_movement_sound.play()  # Play the sound effect once

                if self.arrow_index < 0:
                    self.arrow_index = len(self.yes_or_no_menu) - 1  # Wrap around to the last item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses
            elif state.controller.isDownPressed:
                self.arrow_index += 1
                self.menu_movement_sound.play()  # Play the sound effect once

                if self.arrow_index >= len(self.yes_or_no_menu):
                    self.arrow_index = 0  # Wrap around to the first item
                pygame.time.delay(200)

        if self.game_state == "game_over_screen":
            if state.controller.isTPressed:
                self.music_on = True

                state.currentScreen = state.startScreen
                state.startScreen.start(state)

        if self.game_state == "enemy_desperate_screen":
            if self.coin_flip_messages["enemy_desperate_message"].message_index == 3:
                self.enemy_desperate_counter = True
                self.game_state = "bet_screen"


        if self.game_state == "enemy_defeated_screen":
            if self.coin_flip_messages["enemy_defeated_message"].message_index == 3:
                self.enemy_defeated_counter = True
                self.coinFlipTedDefeated = True
                state.currentScreen = state.startScreen
                state.startScreen.start(state)


        controller = state.controller
        controller.update()


    def draw(self, state: "GameState"):

        # background
        state.DISPLAY.fill((0, 0, 51))

        # Box for hero money, bet amount, and other info
        # Original dimensions
        box_width = 200 - 10
        box_height = 180 - 10

        # New height: 40 pixels taller
        new_box_height = box_height + 40

        # Create the black box with the new height
        black_box = pygame.Surface((box_width, new_box_height))
        black_box.fill((0, 0, 0))

        border_width = 5

        # Adjust the dimensions of the white border surface to fit the new black box size
        white_border = pygame.Surface((box_width + 2 * border_width, new_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))

        # Blit the black box onto the white border
        white_border.blit(black_box, (border_width, border_width))

        # Blit the white border (with the black box) onto the state display at the adjusted position
        state.DISPLAY.blit(white_border, (25, 235 - 40))  # Position moved up by 40 pixels

        # Box for hero name
        black_box = pygame.Surface((200 - 10, 45 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 195 - 40))  # Moved up by 40 pixels

        # Adjusting text positions accordingly
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

        state.DISPLAY.blit(self.font.render(f"Choice: {self.player_choice}", True, (255, 255, 255)), (37, 370))

        state.DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)),
                           (37, 205 - 40))

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
        # Original dimensions
        box_width = 200 - 10
        box_height = 130 - 10

        # New height: 40 pixels smaller
        new_box_height = box_height - 40

        # Create the black box with the new height
        black_box = pygame.Surface((box_width, new_box_height))
        black_box.fill((0, 0, 0))

        border_width = 5

        # Adjust the dimensions of the white border surface to fit the new black box size
        white_border = pygame.Surface((box_width + 2 * border_width, new_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))

        # Blit the black box onto the white border
        white_border.blit(black_box, (border_width, border_width))

        # Blit the white border (with the black box) onto the state display
        state.DISPLAY.blit(white_border, (25, 60))

        state.DISPLAY.blit(self.font.render(f"Money: {self.coinFlipTedMoney}", True,
                                            (255, 255, 255)), (37, 70))

        if self.debuff_counter == 0:
            state.DISPLAY.blit(self.font.render(f"Status: normal", True,
                                                (255, 255, 255)), (37, 110))
        elif self.debuff_counter > 0:
            state.DISPLAY.blit(self.font.render(f"unlucky: {self.debuff_counter}  ", True,
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



        if self.game_state == "heads_tails_choose_screen":
            self.coin_flip_messages["heads_tails_message"].update(state)
            self.coin_flip_messages["heads_tails_message"].draw(state)
            bet_box_width = 150
            bet_box_height = 100 + 40  # Increased height by 40 pixels
            border_width = 5

            screen_width, screen_height = state.DISPLAY.get_size()
            bet_box_x = screen_width - bet_box_width - border_width - 30
            bet_box_y = screen_height - 130 - bet_box_height - border_width - 60

            bet_box = pygame.Surface((bet_box_width, bet_box_height))
            bet_box.fill((0, 0, 0))
            white_border = pygame.Surface((bet_box_width + 2 * border_width, bet_box_height + 2 * border_width))
            white_border.fill((255, 255, 255))
            white_border.blit(bet_box, (border_width, border_width))

            # Calculate text positions - adjust if necessary
            text_x = bet_box_x + 40 + border_width
            text_y_yes = bet_box_y + 20
            text_y_no = text_y_yes + 40  # Consider adjusting this if needed due to the taller box
            # Draw the box on the screen
            state.DISPLAY.blit(white_border, (bet_box_x, bet_box_y))

            # Draw the text on the screen (over the box)
            state.DISPLAY.blit(self.font.render(f"Heads ", True, (255, 255, 255)), (text_x, text_y_yes))
            state.DISPLAY.blit(self.font.render(f"Tails ", True, (255, 255, 255)), (text_x, text_y_yes + 40))
            if "Shield" in state.player.magicinventory and self.debuff_counter == 0:
                state.DISPLAY.blit(self.font.render(f"Magic ", True, (255, 255, 255)), (text_x, text_y_yes + 80))
            elif self.debuff_counter > 0:
                state.DISPLAY.blit(self.font.render(f"Locked ", True, (255, 255, 255)), (text_x, text_y_yes + 80))

            arrow_x = text_x + 20 - 40  # Adjust the arrow position to the left of the text
            arrow_y = text_y_yes + self.headstailsindex * 40  # Adjust based on the item's height

            pygame.draw.polygon(state.DISPLAY, (255, 255, 255),
                                [(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y + 10)])

            if state.controller.isTPressed:
                if self.headstailsindex == 0:
                    print("Heads")
                    self.player_choice = "heads"
                    self.game_state = "flip_screen"
                    state.controller.isTPressed = False  # Reset the button state

                elif self.headstailsindex == 1:
                    print("Tails")
                    self.player_choice = "tails"
                    self.game_state = "flip_screen"
                    state.controller.isTPressed = False  # Reset the button state

                else:
                    print("Magic")  # Added print statement for consistency
                    if self.debuff_counter == 0:
                        self.player_choice = "magic"
                        self.game_state = "magic_screen"
                        state.controller.isTPressed = False  # Reset the button state
                    elif self.debuff_counter > 0:
                        print("stay here")

        if self.game_state == "magic_screen":
            self.coin_flip_messages["magic_message"].update(state)
            self.coin_flip_messages["magic_message"].draw(state)

            # Define new_box_x

            # Updated dimensions
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
            arrow_y = text_y_yes + self.headstailsindex * 40  # Arrow position adjusted based on selected menu item

            # Draw text
            # Draw text
            if "Shield" in self.magic_menu_selector:
                state.DISPLAY.blit(self.font.render(f"{self.magic_menu_selector[1]} ", True, (255, 255, 255)), (text_x, text_y_yes))
            state.DISPLAY.blit(self.font.render(f"{self.magic_menu_selector[0]} ", True, (255, 255, 255)), (text_x, text_y_yes + 40))
            # Y position for "Shield" text, using self.magic_menu_selector[1]
            text_y_shield = text_y_yes  # Assuming "Shield" is rendered at this position

            # Draw the arrow on the same Y coordinate as "Shield"
            # Adjust arrow_x if necessary to position it correctly relative to the "Shield" text
            arrow_x = text_x - 20  # Arrow position adjusted to the left of the text
            arrow_y = text_y_shield + self.magicindex * 40  # Update arrow Y position based on selected item

            pygame.draw.polygon(state.DISPLAY, (255, 255, 255),
                                [(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y + 10)])

            magic_text = self.font.render("Magic", True, (255, 255, 255))  # Render "Magic" in white color
            text_margin = 10  # Margin from the left edge of the top box for the text

            # Position for the "Magic" text inside the top box
            magic_text_x = new_box_x + text_margin
            magic_text_y = new_box_y + (top_box_height - magic_text.get_height()) // 2  # Vertically center inside the top box

            # Blit the "Magic" text onto the screen
            state.DISPLAY.blit(magic_text, (magic_text_x, magic_text_y))

            if state.controller.isTPressed:
                if self.magicindex == 0:

                    print(str(self.magic_menu_selector[0]))
                    print(str(self.magic_menu_selector))
                    state.player.focus_points -= 10
                    state.controller.isTPressed = False  # Reset the button state
                    self.game_state = "heads_tails_choose_screen"



                elif self.magicindex == 1:
                    print(str(self.magic_menu_selector[1]))
                    self.game_state = "heads_tails_choose_screen"
                    state.controller.isTPressed = False  # Reset the button state


        if self.game_state == "flip_screen":
            self.coin_flip_messages["flip_message"].update(state)
            self.coin_flip_messages["flip_message"].draw(state)


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

            if state.controller.isTPressed:
                self.game_state = "play_again_screen"
                state.controller.isTPressed = False  # Reset the button state


        if self.game_state == "play_again_screen":


            if self.coinFlipTedDefeated == False:
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
                arrow_x = text_x + 20 - 40  # Adjust the arrow position to the left of the text
                arrow_y = text_y_yes + self.arrow_index * 40  # Adjust based on the item's height

                pygame.draw.polygon(state.DISPLAY, (255, 255, 255),
                                    [(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y + 10)])

            if state.controller.isTPressed:
                if self.arrow_index == 0:

                    if self.debuff_counter > 0:
                        self.debuff_counter -= 1

                        if self.debuff_counter == 0:
                            self.debuff_vanish = False
                            print(self.debuff_vanish)

                    state.controller.isTPressed = False  # Reset the button state

                    if state.player.stamina_points < 2 or state.player.money < 10:
                        self.game_state = "game_over_screen"
                        print("game over")

                    elif state.player.stamina_points > 1 or state.player.money > 9:
                        self.game_state = "bet_screen"


                else:
                    self.arrow_index = 0
                    self.game_state ="bet_screen"
                    self.music_on = True

                    state.currentScreen = state.startScreen
                    state.startScreen.start(state)

        if self.game_state == "game_over_screen":
            print("your game state is: " + str(self.game_state))
            if state.player.stamina_points < 2:
                print("no stamina")
                self.coin_flip_messages["game_over_no_stamina"].update(state)
                self.coin_flip_messages["game_over_no_stamina"].draw(state)


            elif state.player.money < 10:
                print("no money")
                self.coin_flip_messages["game_over_no_money"].update(state)
                self.coin_flip_messages["game_over_no_money"].draw(state)


        if self.game_state == "enemy_desperate_screen":
            self.coin_flip_messages["enemy_desperate_message"].update(state)
            self.coin_flip_messages["enemy_desperate_message"].draw(state)


        if self.game_state == "enemy_defeated_screen":
            # print("you won the game")
            self.coin_flip_messages["enemy_defeated_message"].update(state)
            self.coin_flip_messages["enemy_defeated_message"].draw(state)


        pygame.display.flip()












