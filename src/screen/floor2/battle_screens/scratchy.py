import random

import pygame

from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen



class CoinFlipBettyScreen(Screen):
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
        self.welcome_screen_index: int = 0


        self.headstailsindex = 0


        self.magicindex = 0
        self.yes_or_no_menu = ["Yes", "No"]
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.heads_or_tails_Menu = ["Heads", "Tails"]
        self.magic_menu_selector = ["shield",   "Back"]
        self.choice_sequence = True
        self.player_choice = ""
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.debuff_vanish = False
        self.debuff_counter = 0
        self.game_reset = False
        self.message_printed = False
        self.spell_sound = pygame.mixer.Sound("./assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)

        self.menu_movement_sound = pygame.mixer.Sound("./assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)

        self.flip_screen_initialized = False  # Add this line


        self.coin_leaning_counter = 5

        self.coin_leaning_tracker = ""  # Initialize to "none" or similar


        self.bet = 50
        self.font = pygame.font.Font(None, 36)
        self.money = 1000




        self.coinFlipFredDefeated = False
        self.food_luck = False




        self.win_exp = False
        self.flip_timer = pygame.time.get_ticks() + 4000  # Initialize with a future time (2 seconds from now)
        self.pause_timer = 0  # Initialize with a future time (2 seconds from now)
        self.heads_image = pygame.image.load("./assets/images/heads.png")
        self.tails_image = pygame.image.load("./assets/images/tails.png")

        self.enemy_desperate_counter = False
        self.enemy_defeated_counter = False
        self.hero_desperate_counter = False

        self.entered_shield_screen = False  # Add this flag
        self.shield_triggered = False

        self.lose_exp = False
        self.game_state = "welcome_screen"

        self.music_file = "./assets/music/coin_flip_screen.mp3"
        self.music_volume = 0.5  # Adjust as needed
        # self.initialize_music()
        self.music_on = True


        self.coin_flip_messages = {
            "welcome_message": TextBox(
                ["Press T to select options and go through T messages"],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "bet_message": TextBox(
                ["Min Bet is 10 and Max Bet is 100. The more you bet the more your  stamina is drained. "],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "heads_tails_message": TextBox(
                ["Choose heads or tails. "],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "magic_message": TextBox(
                [" "],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "flip_message": TextBox(
                ["Flipping the coin now hold your breath. "],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "results_message": TextBox(["  " ], (50, 450, 700, 130), 36, 500),
            "shield_message1": TextBox(
                ["A bird came down and stole the coin, who knows who won now. "],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "shield_message2": TextBox(
                ["opposum ned gobbled it down "],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "shield_message3": TextBox(
                ["A cat stole the coin. "],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "play_again_message": TextBox(
                [
                  " Would you like to play again or quit?"
                 ],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "game_over_no_money": TextBox(
                ["Looks like your out of money, sorry time for you to go...foreverrrrrrrrrr hahhaha HAHHAHAHHAHAHAHAHA. "

                 ],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "game_over_no_stamina": TextBox(
                ["Hero: I'm so tired, I'm....passing....out.......(-100 golds) "

                 ],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "enemy_desperate_message": TextBox(
                ["Enemy: NOOoooooo....Do you know how many years i've spent coin flipping!!! This is impossible! ",
                 "Hero: It's not,  either you've been doing it wrong for years, or you reached you best a long time ago",
                 "Enemy: Please...don't take my coins......you don't know what they do to people who lose all their coins!!!",
                 "Hero: Sadly for you I'm ruthless, I'm taking you out!", ""

                 ],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "hero_desperate_message": TextBox(
                ["Hero: Why am I having so much trouble with this chump? ",
                 "I wonder if any of the towns people has a clue to defeat him?",
                 "Should I leave, or stay with it and trust in my luck?", ""

                 ],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "enemy_defeated_message": TextBox(
                ["Hero: Got your last coin buddy, time for you to go to sleep buddy. ",
                 "Fred: I had a dream last night this would happen",
                 "Enemy: I'm the best coin flipper here they have to give me more coins.", ""

                 ],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),

            "magic_description_shield": TextBox(
                [
                    "Shield: Reality warps in such a way to attract animals to coins when they would land in the enmies favor."
                ],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),

            "magic_description_force": TextBox(
                [
                    "Force: Making calculations based on coin weight and gravity, put the exact amount of force required  to get your coin flip to land on heads."
                ],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "magic_description_back": TextBox(
                [
                    "Back: go back to previous menu"
                ],
                (45, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),


            # You can add more game state keys and TextBox instances here
        }
        self.coin_flip_fred_messages = {}  # Prepare the dictionary but don't fill it yet

        self.coin_flip_messages_initialized = False  # Add an initialization flag

        self.exp_gain = 0
        self.odd = False
        self.even = False
        self.turn_1 = False
        self.turn_2 = False
        self.turn_3 = False
        self.turn_4 = False
        self.turn_5 = False
        self.phase = 1
        self.magic_lock = False
        self.lock_down  = 0
        self.weighted_coin = False

        pygame.mixer.music.stop()





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


    def place_bet(self, state: "GameState"):
        controller = state.controller
        controller.update()

        if controller.isUpPressed:
            self.bet += 50
            self.menu_movement_sound.play()  # Play the sound effect once

            pygame.time.delay(200)
            self.isUpPressed = False
            print(self.bet)


        elif controller.isDownPressed:
            self.bet -= 50
            self.menu_movement_sound.play()  # Play the sound effect once

            pygame.time.delay(200)
            self.isDownPressed = False
            print(self.bet)


        if self.bet < 50:
            self.bet = 50

        if self.bet > 200:
            self.bet = 200

        if self.bet > self.money:
            self.bet = self.money

        if self.bet > state.player.money:
            self.bet = state.player.money

        if controller.isTPressed:

            self.game_state = "welcome_screen"
            state.controller.isTPressed = False  # Reset the button state

    def flipCoin(self, state: "GameState"):
        if self.phase > 5:
            self.even = False
            self.odd = False
            self.phase = 1
        # evens and odds
        if self.weighted_coin == True:
            self.result = "Heads"
        #
        if self.even == False and self.odd == False:
            coin_fate = random.randint(1, 2)
            if coin_fate == 1:
                self.even = True
            elif coin_fate == 2:
                self.odd = True



        if self.even == True and self.weighted_coin == False:

            if self.phase == 1:
                self.result = "Heads"
            elif self.phase == 2:
                self.result = "Tails"
            elif self.phase == 3:
                self.result = "Heads"
            elif self.phase == 4:
                self.result = "Tails"
            elif self.phase == 5:
                self.result = "Heads"

        elif self.odd == True and self.weighted_coin == False:
            if self.phase == 1:
                self.result = "Tails"
            elif self.phase == 2:
                self.result = "Heads"
            elif self.phase == 3:
                self.result = "Tails"
            elif self.phase == 4:
                self.result = "Heads"
            elif self.phase == 5:
                self.result = "Tails"

        self.game_state = "results_screen"

    def update(self, state: "GameState"):


        if state.musicOn == True:
            if self.music_on == True:
                self.stop_music()
                # self.initialize_music()
                self.music_on = False


        if self.money < 10:
            self.coinFlipFredDefeated = True



        if state.controller.isQPressed:
            state.currentScreen = state.startScreen
            state.startScreen.start(state)
            return

        controller = state.controller
        controller.update()


        if self.game_state == "welcome_screen":

            self.coin_flip_messages["welcome_message"].update(state)

            if self.money < 1:
               self.game_state = "game_over_screen"

            if state.player.stamina_points < 1:
                self.game_state = "game_over_screen"


            elif state.player.stamina_points <= 6 and state.player.stamina_points > 0:
                self.game_state = "game_over_screen"



            elif state.player.money < 50 and state.player.money > 0:
                self.game_state = "game_over_screen"


            elif state.player.money <= 0:
                self.game_state = "game_over_screen"

            if controller.isUpPressed:
                self.welcome_screen_index = (self.welcome_screen_index - 1) % len(self.welcome_screen_choices)
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.welcome_screen_index = (self.welcome_screen_index + 1) % len(self.welcome_screen_choices)
                controller.isDownPressed = False

            if self.welcome_screen_index == 0 and controller.isTPressed:
                for i in range(0, self.bet, 50):
                    state.player.stamina_points -= 4
                self.game_state = "heads_tails_choose_screen"




                controller.isTPressed = False
            elif self.welcome_screen_index == 1 and controller.isTPressed and self.magic_lock == False:
                self.magic_screen_index = 0
                self.coin_flip_messages["magic_message"].reset()
                self.game_state = "magic_screen"
                controller.isTPressed = False
            elif self.welcome_screen_index == 2 and controller.isTPressed:
                self.coin_flip_messages["bet_message"].reset()
                self.game_state = "bet_screen"

                controller.isTPressed = False

            elif self.welcome_screen_index == 3 and controller.isTPressed and self.lock_down == 0:
                state.currentScreen = state.area2StartScreen
                controller.isTPressed = False


        if self.game_state == "bet_screen":

            self.has_run_money_logic = False
            self.player_choice = ""
            self.message_printed = False
            self.entered_shield_screen = False  # Add this flag

            # self.coin_flip_messages["bet_message"].update(state)
            if not self.coin_flip_messages_initialized:
                # self.initialize_text_boxes()
                self.coin_flip_messages_initialized = True
            self.coin_flip_messages["bet_message"].update(state)
            self.place_bet(state)  # Call the place_bet method to handle bet adjustments
                # Add other game state updates here

        if self.game_state == "heads_tails_choose_screen":
            self.coin_flip_messages["bet_message"].update(state)

            self.coin_flip_messages["heads_tails_message"].update(state)

            if "shield" in state.player.magicinventory and "Magic" not in self.heads_or_tails_Menu:
                self.heads_or_tails_Menu.append("Magic")

            if self.coin_flip_messages["bet_message"].is_finished():
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

        if self.game_state == "magic_screen":
            if "HEADS_FORCE" in state.player.magicinventory and "FORCE" not in self.magic_menu_selector:
                self.magic_menu_selector.insert(1, "FORCE")

            if state.controller.isUpPressed:
                self.magicindex -= 1
                self.menu_movement_sound.play()  # Play the sound effect once

                if self.magicindex < 0:
                    self.magicindex = len(self.magic_menu_selector) - 1  # Wrap around to the last item
                    print(str(self.magicindex))

                # print(self.magic_menu_selector[self.magicindex])  # Print the current menu item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses

            elif state.controller.isDownPressed:
                self.magicindex += 1
                self.menu_movement_sound.play()  # Play the sound effect once

                if self.magicindex >= len(self.magic_menu_selector):
                    self.magicindex = 0  # Wrap around to the first item
                    print(str(self.magicindex))


                # print(self.magic_menu_selector[self.magicindex])  # Print the current menu item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses


        if self.game_state == "flip_screen":
            # print("entering flip screen")


            if not self.flip_screen_initialized:
                # print("Initializing flip timer")
                self.flip_timer = 2500  # Duration for the pause
                self.pause_timer = pygame.time.get_ticks()  # Current time
                self.flip_screen_initialized = True

            # Calculate elapsed time since the flip_screen was entered
            elapsed_time = pygame.time.get_ticks() - self.pause_timer
            # print(f"Elapsed time: {elapsed_time}")

            # if self.coinFlipTedMoney < 10:
            #     self.game_state = "enemy_defeated_screen"

            if elapsed_time >= self.flip_timer:
                # Timer has elapsed, proceed with flipping the coin
                self.flipCoin(state)
                # Reset flip_screen_initialized for next time
                self.flip_screen_initialized = False
                self.pause_timer = 0  # Reset pause timer for the next use
                # Transition to the next state as needed
                # ...
            if elapsed_time >= self.flip_timer:
                # Logic to transition away from flip_screen
                # ...
                self.flip_screen_initialized = False

            self.coin_flip_messages["flip_message"].update(state)
            # if self.coinFlipTedMoney < 10:
            #     self.game_state = "enemy_defeated_screen"


        if self.game_state == "results_screen":
            # if self.coinFlipTedMoney < 10:
            #     self.game_state = "enemy_defeated_screen"

            # Assuming this is part of a class



            if "coin flip glasses" in state.player.items and self.player_choice == self.result:
                # print("Ninejljdfjsldajfjasf;sjf;ladsjf;js;fjsa;ljfl;sajfld;sajf;lsjf;lasjfl;sjf;ljas")

                state.player.money += self.bet + 20
                self.money -= self.bet + 20
                if self.money == -10:
                    self.money = 0
                    state.player.money -= 10
                elif self.money == -20:
                    self.money = 0
                    state.player.money -= 20



            elif self.player_choice == self.result:
                # print("Ninejljdfjsldajfjasf;sjf;ladsjf;js;fjsa;ljfl;sajfld;sajf;lsjf;lasjfl;sjf;ljas")

                state.player.money += self.bet

                self.money -= self.bet

            elif self.player_choice != self.result:
                print("Your choice is : " + self.player_choice)
                print("Your result is :" + self.result)


                # state.player.money -= self.bet
                # self.money += self.bet
                if self.debuff_vanish == True:
                    import random
                    roll = random.randint(1, 100)
                    if roll > 10:
                        state.player.money += self.bet
                        self.money -= self.bet
                        self.game_state = "shield_screen"

            self.has_run_money_logic = True

        self.coin_flip_messages["results_message"].update(state)

        # Construct the result message
        result_message = f"Here you go, the result of your flip: {self.result}"
        # bet_message = f"Bet amount: {self.bet}"

        # Update the messages in the TextBox
        self.coin_flip_messages["results_message"].messages = [result_message]


        # if state.controller.isTPressed:
        #     self.game_state = "play_again_screen"
        #     print(str(self.game_state))

        if self.game_state == "shield_screen":
            # print("sheild time")
            if state.controller.isTPressed:
                self.game_state = "play_again_screen"
                state.controller.isTPressed = False  # Reset the button state

        if self.game_state == "play_again_screen":

            if state.player.money < 1:
                self.game_state = "game_over_no_money"
            elif state.player.stamina_points < 1:
                self.game_state = "game_over_no_stamina"

            if self.money < 10:
                self.coinFlipTedDefeated = True
                self.game_state = "enemy_defeated_screen"

            self.coin_flip_messages["play_again_message"].update(state)
            if not self.message_printed:
                # self.giveExp(state)
                # Set the flag to True after printing the message
                self.message_printed = True

            if state.controller.isUpPressed:
                self.arrow_index -= 1
                if self.arrow_index < 0:
                    self.arrow_index = len(self.yes_or_no_menu) - 1  # Wrap around to the last item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses
            elif state.controller.isDownPressed:
                self.arrow_index += 1
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



        if self.game_state == "hero_desperate_screen":
            if self.coin_flip_messages["hero_desperate_message"].message_index == 3:
                self.hero_desperate_counter = True

                self.game_state = "bet_screen"

        if self.game_state == "enemy_defeated_screen":
            if self.coin_flip_messages["enemy_defeated_message"].message_index == 3:
                self.enemy_defeated_counter = True
                self.coinFlipTedDefeated = True
                state.currentScreen = state.gamblingAreaScreen
                state.gamblingAreaScreen.start(state)


        controller = state.controller
        controller.update()

    ########################we want up and down arrows on bet. have arrow disapear when an item is not in use






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

        if state.player.money < 100:
            text_color = (255, 0, 0)  # Red color
        else:
            text_color = (255, 255, 255)  # White color

        state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True, text_color), (37, 250))

        # state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True,
        #                               (255, 255, 255)), (37, 250))
        if state.player.stamina_points < 20:
            text_color = (255, 0, 0)  # Red color
        else:
            text_color = (255, 255, 255)  # White color

        state.DISPLAY.blit(
            self.font.render(f"HP: {state.player.stamina_points}", True,
                             text_color), (37, 210))

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

        state.DISPLAY.blit(self.font.render(f"Money: {self.money}", True,
                                            (255, 255, 255)), (37, 70))

        if self.debuff_counter == 0:
            state.DISPLAY.blit(self.font.render(f"Status: normal", True,
                                                (255, 255, 255)), (37, 110))
        elif self.debuff_counter > 0:
            state.DISPLAY.blit(self.font.render(f"unlucky: {self.debuff_counter}  ", True,
                                                (255, 255, 255)), (37, 110))


        black_box_height = 130
        black_box_width = 740
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
            if not self.coin_flip_messages_initialized:
                # self.initialize_text_boxes()
                self.coin_flip_messages_initialized = True
            self.coin_flip_messages["welcome_message"].draw(state)

            if self.money < 1:
                self.coin_flip_messages["you_win"].draw(state)

            if state.player.stamina_points < 1:
                self.coin_flip_messages["game_over_no_stamina_message"].draw(state)

            elif state.player.money <= 0:
                self.coin_flip_messages["game_over_no_money_message"].draw(state)

            elif state.player.stamina_points <= 10 and state.player.stamina_points > 0:
                self.coin_flip_messages["game_over_low_stamina_message"].draw(state)

            elif state.player.money < 50 and state.player.money > 0:
                self.coin_flip_messages["game_over_low_money_message"].draw(state)

            black_box_height = 221 - 50  # Adjust height
            black_box_width = 200 - 10  # Adjust width to match the left box
            border_width = 5
            start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
            start_y_right_box = 240  # Adjust vertical alignment

            # Create the black box
            black_box = pygame.Surface((black_box_width, black_box_height))
            black_box.fill((0, 0, 0))

            # Create a white border
            white_border = pygame.Surface(
                (black_box_width + 2 * border_width, black_box_height + 2 * border_width)
            )
            white_border.fill((255, 255, 255))
            white_border.blit(black_box, (border_width, border_width))

            # Determine the position of the white-bordered box
            black_box_x = start_x_right_box - border_width
            black_box_y = start_y_right_box - border_width

            # Blit the white-bordered box onto the display
            state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

            # Draw the menu options
            for idx, choice in enumerate(self.welcome_screen_choices):
                y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, (255, 255, 255)),
                    (start_x_right_box + 60, y_position + 15)
                )
            # if "Focus" not in state.player.magicinventory:
            #     self.magic_lock = True
            #     self.welcome_screen_choices[1] = "Locked"

            if self.welcome_screen_index == 0:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 12)
                )
            elif self.welcome_screen_index == 1:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 52)
                )
            elif self.welcome_screen_index == 2:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 92)
                )
            elif self.welcome_screen_index == 3:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 132)
                )

        if self.game_state == "bet_screen":
            # print("Game state is 'bet'")  # Debugging
            # self.coin_flip_messages["bet_message"].update(state)
            self.coin_flip_messages["bet_message"].draw(state)
            state.DISPLAY.blit(self.font.render(f"Your Current bet:{self.bet}", True,
                                                (255, 255, 255)), (45, 550))

            state.DISPLAY.blit(self.font.render(f"v", True, (255, 255, 255)),
                               (312, 555))
            state.DISPLAY.blit(self.font.render(f"^", True, (255, 255, 255)),
                               (312, 545))



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
            if "shield" in state.player.magicinventory and self.debuff_counter == 0:
                state.DISPLAY.blit(self.font.render(f"Magic ", True, (255, 255, 255)), (text_x, text_y_yes + 80))
            elif self.debuff_counter > 0:
                state.DISPLAY.blit(self.font.render(f"Locked ", True, (255, 255, 255)), (text_x, text_y_yes + 80))

            arrow_x = text_x + 20 - 40  # Adjust the arrow position to the left of the text
            arrow_y = text_y_yes + self.headstailsindex * 40  # Adjust based on the item's height
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
                if self.headstailsindex == 0:
                    self.player_choice = "heads"
                    self.game_state = "flip_screen"
                    state.controller.isTPressed = False  # Reset the button state

                elif self.headstailsindex == 1:
                    self.player_choice = "tails"
                    self.game_state = "flip_screen"
                    state.controller.isTPressed = False  # Reset the button state

                else:
                    if self.debuff_counter == 0:
                        self.player_choice = "magic"
                        self.game_state = "magic_screen"
                        state.controller.isTPressed = False  # Reset the button state
                    elif self.debuff_counter > 0:
                        print("stay here")

        if self.game_state == "magic_screen":
            self.coin_flip_messages["magic_message"].update(state)
            self.coin_flip_messages["magic_message"].draw(state)

            if self.magicindex == 0:
                self.coin_flip_messages["magic_description_shield"].update(state)
                self.coin_flip_messages["magic_description_shield"].draw(state)
            elif self.magicindex == 1:
                self.coin_flip_messages["magic_description_force"].update(state)
                self.coin_flip_messages["magic_description_force"].draw(state)
            elif self.magicindex == 2:
                self.coin_flip_messages["magic_description_back"].update(state)
                self.coin_flip_messages["magic_description_back"].draw(state)

            # Define new_box_x

            black_box_height = 221 - 50  # Adjust height
            black_box_width = 200 - 10  # Adjust width to match the left box
            border_width = 5
            start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
            start_y_right_box = 240  # Adjust vertical alignment

            # Create the black box
            black_box = pygame.Surface((black_box_width, black_box_height))
            black_box.fill((0, 0, 0))

            # Create a white border
            white_border = pygame.Surface(
                (black_box_width + 2 * border_width, black_box_height + 2 * border_width)
            )
            white_border.fill((255, 255, 255))
            white_border.blit(black_box, (border_width, border_width))

            # Determine the position of the white-bordered box
            black_box_x = start_x_right_box - border_width
            black_box_y = start_y_right_box - border_width

            # Blit the white-bordered box onto the display
            state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

            # Draw the menu options
            for idx, choice in enumerate(self.magic_menu_selector):
                y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, (255, 255, 255)),
                    (start_x_right_box + 60, y_position + 15)
                )

            if self.magicindex == 0:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 12)
                )
            elif self.magicindex == 1:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 52)
                )
            elif self.magicindex == 2:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 92)
                )



            if state.controller.isTPressed:
                if self.magicindex == 0 and state.player.focus_points > 0:


                    self.spell_sound.play()  # Play the sound effect once

                    self.debuff_vanish = True
                    self.debuff_counter += 3
                    state.player.focus_points -= 10
                    state.controller.isTPressed = False  # Reset the button state
                    self.game_state = "welcome_screen"

                elif self.magicindex == 1 and state.player.focus_points > 0:


                    self.spell_sound.play()  # Play the sound effect once

                    self.weighted_coin = True
                    self.debuff_counter += 1
                    state.player.focus_points -= 10
                    state.controller.isTPressed = False  # Reset the button state
                    self.game_state = "welcome_screen"



                elif self.magicindex == 2:
                    print(str(self.magic_menu_selector[1]))
                    self.game_state = "welcome_screen"
                    state.controller.isTPressed = False  # Reset the button state


        if self.game_state == "flip_screen":
            self.coin_flip_messages["flip_message"].update(state)
            self.coin_flip_messages["flip_message"].draw(state)

        # if self.game_state == "results_screen":
        #     self.coin_flip_messages["results_message"].update(state)
        #     self.coin_flip_messages["results_message"].draw(state)
        if self.game_state == "results_screen":
            print("your results are in :  " + str(self.result))
            self.coin_flip_messages["results_message"].update(state)
            self.coin_flip_messages["results_message"].draw(state)

            # Display the image based on self.result
            image_to_display = self.heads_image if self.result == "heads" else self.tails_image
            image_rect = image_to_display.get_rect()
            image_rect.center = (state.DISPLAY.get_width() // 2, state.DISPLAY.get_height() // 2)
            state.DISPLAY.blit(image_to_display, image_rect)
            state.DISPLAY.blit(self.font.render(f"The coin landed on :{self.result}", True,
                                                (255, 255, 255)), (70, 460))

            state.DISPLAY.blit(self.font.render(f"You gained: {self.exp_gain} experience points", True,
                                                (255, 255, 255)), (70, 510))

            # Call the update method for the results_message TextBox
            self.coin_flip_messages["results_message"].update(state)

            # Now, draw the results_message TextBox
            self.coin_flip_messages["results_message"].draw(state)

            if state.controller.isTPressed:
                self.game_state = "play_again_screen"
                state.controller.isTPressed = False  # Reset the button state

        if self.game_state == "shield_screen":
            if not self.entered_shield_screen:
                # Randomly select one of the shield messages
                selected_message_key = random.choice(["shield_message1", "shield_message2", "shield_message3"])
                self.selected_shield_message = self.coin_flip_messages[selected_message_key]

                # Set the flag to True to avoid repeating this in the current state
                self.entered_shield_screen = True
                # state.player.money += self.bet
                # self.money -= self.bet

            # Update and draw the selected TextBox
            self.selected_shield_message.update(state)
            self.selected_shield_message.draw(state)
        else:
            # Reset the flag when leaving the state to enable a new random message next time
            self.entered_shield_screen = False

        if self.game_state == "play_again_screen":
            ## this shows the coin
            # image_to_display = self.heads_image if self.result == "heads" else self.tails_image
            # image_rect = image_to_display.get_rect()
            # image_rect.center = (state.DISPLAY.get_width() // 2, state.DISPLAY.get_height() // 2)
            # state.DISPLAY.blit(image_to_display, image_rect)

            if self.coinFlipFredDefeated == False:
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
                if self.arrow_index == 0:

                    if self.debuff_counter > 0:
                        self.debuff_counter -= 1

                        if self.debuff_counter == 0:
                            self.debuff_vanish = False

                    state.controller.isTPressed = False  # Reset the button state

                    if state.player.stamina_points < 2 or state.player.money < 10:
                        self.game_state = "game_over_screen"

                    elif state.player.stamina_points > 1 or state.player.money > 9:
                        self.game_state = "bet_screen"


                else:
                    self.arrow_index = 0
                    self.game_state ="bet_screen"
                    self.music_on = True
                    self.debuff_vanish = False
                    self.debuff_counter = 0

                    state.currentScreen = state.gamblingAreaScreen
                    state.gamblingAreaScreen.start(state)




        if self.game_state == "enemy_desperate_screen":
            print("enemy is veyr desperate now")
            self.coin_flip_messages["enemy_desperate_message"].update(state)
            self.coin_flip_messages["enemy_desperate_message"].draw(state)

        if self.game_state == "hero_desperate_screen":
            print("hero is most desperate now")
            self.coin_flip_messages["hero_desperate_message"].update(state)
            self.coin_flip_messages["hero_desperate_message"].draw(state)

        if self.game_state == "enemy_defeated_screen":
            # print("you won the game")
            self.coin_flip_messages["enemy_defeated_message"].update(state)
            self.coin_flip_messages["enemy_defeated_message"].draw(state)


        if self.game_state == "game_over_no_money":

            self.coin_flip_messages["game_over_no_money"].update(state)
            self.coin_flip_messages["game_over_no_money"].draw(state)
            if self.coin_flip_messages["game_over_no_money"].is_finished():
                if state.controller.isTPressed:
                    state.currentScreen = state.gameOverScreen
                    state.gameOverScreen.start(state)

        if self.game_state == "game_over_no_stamina":
            self.coin_flip_messages["game_over_no_stamina"].update(state)
            self.coin_flip_messages["game_over_no_stamina"].draw(state)
            if self.coin_flip_messages["game_over_no_stamina"].is_finished():
                if state.controller.isTPressed:
                    state.player.money -= 100
                    if state.player.money < 1:
                        state.currentScreen = state.gameOverScreen
                        state.gameOverScreen.start(state)
                    else:
                        self.game_state = "welcome_screen"

                        state.player.canMove = True
                        state.start_area_to_rest_area_entry_point = True

                        state.currentScreen = state.restScreen
                        state.restScreen.start(state)
                        state.player.stamina_points = 1

        pygame.display.flip()












