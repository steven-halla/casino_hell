import random
from typing import List

import pygame

from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen


#
#
#
#   ON LOSS OR IF ALL EMPTY BUT LOSE, LOCK OUT GRAB UNTIL PLAYER HITS RESHUFFLE
#

## PRESS B TO GET OUT FOR OPTIONS

class OpossumInACanNellyScreen(Screen):
    def __init__(self):
        super().__init__("Opossum in a can screen")
        self.third_message_display = ""
        self.desperate = False
        self.debuff_keen_perception = False
        # we can set this as a variable that can get toggled on and off depending on who you are playing aginst
        self.nellyOpossumMoney = 500
        self.opossumBite = False
        self.nellyOpossumIsDefeated = False
        self.opossum_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 36)
        self.player_score = 0
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.opossum_index = 0
        self.five_hundred_points = False
        self.magic_menu_selector_index = 0
        self.game_state = "welcome_opposum"
        self.winner_or_looser: List[str] = ["win", "win",
                                            "win", "win", "lose",
                                            "lucky_star",
                                            "X3_star", "win",
                                    ]

        self.opossumInACanMessages = {
            "welcome_message": TextBox(
                ["Nelly here, good luck to you", "Welcome to Opossum in a can !", "No take backs on your bet, I had to set up the cans after all", ""],
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
                ["Would you like to play again or leave? "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "rapid_opossum_message": TextBox(
                ["Oh no you got bite!!! Wrong Trash can!!!! ", ""],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "opossum_defeated_message": TextBox(
                ["WEll since you beat me I have a super secret item just for you hero take it!! ", "you open the treash can and get bit by a rapid opossom;)", "Ooops I didn't meanto do that, oh well i'll be seeing you soon enjoy your humanity while it loast opossum-kun", ""],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "real_opossum_defeated_message": TextBox(
                ["Stupid Doctor and her shots, hate her I want her to be a opossum soooooo badly ", "",
    ],
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
            "lose_message": TextBox(
                ["something poppped out!!! ", "oh no you just got bit...you better go see a doctor you feel sick", "chompy", ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),

            "immune_lose_message": TextBox(
                ["chompy" , ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),

            "tally_message": TextBox(
                [ "", "" ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "game_over_no_money": TextBox(
                ["Oh yes your out of money OH GOD YES I CANT WAIT TO SEE WHAT THE DEMONS DO TO YOU.. "

                 ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "game_over_no_stamina": TextBox(
                ["Hero: someone, I can't....focus....blacking out..(-100 golds) "

                 ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),

            "less_than_150_money": TextBox(
                ["Chomp",
                 "Nelly: I'm sorry but you dont' have enough money to keep playing, do come back.! ", "",

                 ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "magic_description_reveal": TextBox(
                [
                    "reveal: Your perception is increased. You can now detect subtle shakings of the trash cans. 1 can is X3 star, the other is 1 of 2 rabid opossums"
                ],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "magic_description_back": TextBox(
                [
                    "back: go back to previous menu"
                ],
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
        self.initialized_message = False  # Add this line to initialize the flag
        self.trash_sprite_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/PC Computer - The Sims - Galvanized Trash Can (2).png").convert_alpha()
        self.hand_sprite_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/GameCube - Mario Party 4 - Character Hands (1).png").convert_alpha()
        self.game_state = "welcome_screen"

        self.box_color = (255, 0, 0)  # Initially red

        self.rabiesStaminaChecker = False

        self.has_opossum_insurance = True

        self.choices = ["Grab", "Magic", "Quit"]
        self.choices_index = 0

        self.bet_or_flee = ["bet", "flee"]
        self.bet_or_flee_index = 0
        self.menu_selector = ["grab", "magic", "tally"]


        self.magic_menu_selector = ["Back"]
        self.magic_menu_index = 0



        self.play_again_or_quit = ["Play Again", "Quit"]

        self.play_again_or_quit_index = 0

        self.bluff_activated = 0
        self.bottom_message = ""
        self.opossum_rader = False

        self.luck_activated = 0
        self.total_winnings = 0

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

        self.tally_money_once = True

        self.talley_checker = False

        self.music_file = "/Users/stevenhalla/code/casino_hell/assets/music/opossum_in_a_can_screen.mp3"
        self.music_volume = 0.5  # Adjust as needed
        # self.initialize_music()
        self.music_on = True


        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)

##### what if I try to set a timer so we don't skip?
    ### or maybe something has to be set to false like the T press?


###        self.initialized_message = False  # Add this line to initialize the flag
#### so I think the above will solve the provlem with messags just getting barfed i"ll hav to see another day
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

    def initializeGarbageCans(self):
        # Randomly shuffle the winner_or_looser list
        shuffled_items = random.sample(self.winner_or_looser, len(self.winner_or_looser))

        # Assign shuffled items to each can
        self.can1, self.can2, self.can3, self.can4, self.can5, self.can6, self.can7, self.can8 = shuffled_items

        # Check if any cans are empty and fill them recursively
        for i in range(1, 9):
            can_attribute = getattr(self, f"can{i}")
            if can_attribute == "":
                # If a can is empty, assign a random item from the list to it
                setattr(self, f"can{i}", random.choice([item for item in self.winner_or_looser if item != ""]))
                # Check if any cans are still empty after filling
                if "" in [getattr(self, f"can{j}") for j in range(1, 9)]:
                    self.initializeGarbageCans()
                    break

        # Print the contents of each can
        for i in range(1, 9):
            print(f"Can {i} contains: {getattr(self, f'can{i}')}")


    # def initializeGarbageCans(self):
    #
    #
    #     # Randomly shuffle the winner_or_looser list
    #     # print("yabbba dabbbba dooooooooooo")
    #     shuffled_items = random.sample(self.winner_or_looser, len(self.winner_or_looser))
    #
    #     # Assign a shuffled item to each can and print the content
    #     self.can1 = shuffled_items[0]
    #     # print("Can 1 contains:", self.can1)
    #
    #     self.can2 = shuffled_items[1]
    #     # print("Can 2 contains:", self.can2)
    #
    #     self.can3 = shuffled_items[2]
    #     # print("Can 3 contains:", self.can3)
    #
    #     self.can4 = shuffled_items[3]
    #     # print("Can 4 contains:", self.can4)
    #
    #     self.can5 = shuffled_items[4]
    #     # print("Can 5 contains:", self.can5)
    #
    #     self.can6 = shuffled_items[5]
    #     # print("Can 6 contains:", self.can6)
    #
    #     self.can7 = shuffled_items[6]
    #     # print("Can 7 contains:", self.can7)
    #
    #     self.can8 = shuffled_items[7]
    #     # print("Can 8 contains:", self.can8)


    def refresh(self):
        self.bet = 20
        self.has_opossum_insurance = True
        self.insurance = 200
        self.total_winnings = 0
        self.tally_money_once = True
        self.player_score = 0
        self.talley_checker = False
        self.debuff_keen_perception = False


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
            self.debuff_keen_perception = False

            self.player_score = 0
            if state.player.rabiesImmunity == True:
                if "opossum repellent" in state.player.items:
                    state.player.stamina_points -= 25
                elif "opossum repellent" not in state.player.items:
                    state.player.stamina_points -= 50


                self.refresh()
                self.initializeGarbageCans()
                self.game_state = "immune_lose_screen"


            elif state.player.rabiesImmunity == False:
                self.opossumBite = True
                self.refresh()
                # self.initializeGarbageCans()
                self.initializeGarbageCans()
                self.game_state = "lose_screen"







        # Remove the item from the can (set it to an empty string)
        setattr(self, selected_can_attribute, "")

    def update(self, state: "GameState"):

        if self.music_on == True:
            self.stop_music()
            # self.initialize_music()
            self.music_on = False

        if self.player_score >= 300:
            # print("you got a opossum")
            state.gamblingAreaScreen.five_hundred_opossums = True
        if self.player_score >= 300:
            self.five_hundred_points = True
        if self.fill_cans == True:
            self.initializeGarbageCans()
            self.fill_cans = False
            state.player.money -= 150



        if state.controller.isQPressed:
            # Transition to the main screen
            self.music_on = True

            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

        if "shake" in state.player.magicinventory and "shake" not in self.magic_menu_selector:
            self.magic_menu_selector.append("shake")
            return



        if self.game_state == "tally_screen":
            if self.player_score >= 600 and self.talley_checker == False:

                # state.player.stamina_points -= 10
                print("Your before  total exp is: " + str(state.player.exp))
                state.player.exp += 300
                print("you gained: " + str(300) + "exp")
                print("Your after total exp is: " + str(state.player.exp))
                self.talley_checker = True
                return

            elif self.player_score >= 300 and self.talley_checker == False:

                # state.player.stamina_points -= 5

                print("Your before  total exp is: " + str(state.player.exp))

                state.player.exp += 200
                print("you gained: " + str(200) + "exp")
                print("Your after total exp is: " + str(state.player.exp))
                self.talley_checker = True

                return

            elif self.player_score >= 20 and self.talley_checker == False:
                # state.player.stamina_points -= 3

                print("Your before  total exp is: " + str(state.player.exp))

                state.player.exp += 100
                print("you gained: " + str(100) + "exp")
                print("Your after total exp is: " + str(state.player.exp))
                self.talley_checker = True

                return
            # print("tally ho")
            if self.nellyOpossumMoney < 0:
                self.nellyOpossumMoney = 0
                self.nellyOpossumIsDefeated = True



            while self.tally_money_once == True:
                if self.player_score <= self.nellyOpossumMoney:
                    print("your winnings are before" + str(self.total_winnings))

                    # self.total_winnings = self.player_score
                    # self.nellyOpossumMoney -= self.player_score
                    # print("yo")
                    self.total_winnings = self.player_score
                    state.player.money += self.player_score
                    self.nellyOpossumMoney -= self.player_score


                elif self.player_score > self.nellyOpossumMoney:
                    print("your winnings are" + str(self.total_winnings))
                    print("your nellly monies  are" + str(self.nellyOpossumMoney))
                    self.total_winnings = self.nellyOpossumMoney
                    state.player.money += self.total_winnings
                    self.nellyOpossumMoney = 0

                self.tally_money_once = False


            self.opossumInACanMessages["tally_message"].update(state)


            if self.nellyOpossumMoney < 1 and state.player.rabiesImmunity == False and self.opossumInACanMessages["tally_message"].message_index == 1:
                self.nellyOpossumIsDefeated = True
                self.game_state = "opossum_defeated_screen"

            elif self.nellyOpossumMoney < 1 and state.player.rabiesImmunity == True and self.opossumInACanMessages["tally_message"].message_index == 1:
                # print("Nelly opposum money is at: " + str(self.nellyOpossumMoney))
                self.nellyOpossumIsDefeated = True
                self.game_state = "real_opossum_defeated_screen"

            elif self.opossumInACanMessages["tally_message"].message_index == 1:
                if state.player.money < 150:
                    print("Hi")
                    self.game_state = "no_money_you_leave"
                else:
                    print("Ni")
                    self.game_state = "play_again_or_leave_screen"


        if self.game_state == "no_money_you_leave":
            print("Hi")
            self.opossumInACanMessages["less_than_150_money"].update(state)
            if self.opossumInACanMessages["less_than_150_money"].is_finished():
                state.currentScreen = state.gamblingAreaScreen
                state.gamblingAreaScreen.start(state)

        if self.game_state == "welcome_screen":
            self.opossumInACanMessages["welcome_message"].update(state)

            if self.opossumInACanMessages["welcome_message"].message_index == 3:

                self.game_state = "menu_screen"

        if self.game_state == "menu_screen":
            if "shake" in self.magic_menu_selector:
                if state.controller.isUpPressed:
                    self.opossum_index -= 1
                    self.menu_movement_sound.play()  # Play the sound effect once

                    if self.opossum_index < 0:
                        self.opossum_index = len(self.menu_selector) - 1  # Wrap around to the last item
                        print(str(self.opossum_index))

                    # print(self.magic_menu_selector[self.magicindex])  # Print the current menu item
                    pygame.time.delay(200)  # Add a small delay to avoid rapid button presses

                elif state.controller.isDownPressed:
                    self.opossum_index += 1
                    self.menu_movement_sound.play()  # Play the sound effect once

                    if self.opossum_index >= len(self.menu_selector):
                        self.opossum_index = 0  # Wrap around to the first item
                        print(str(self.opossum_index))

                    # print(self.magic_menu_selector[self.magicindex])  # Print the current menu item
                    pygame.time.delay(200)  # Add a small delay to avoid rapid button presses

            elif "shake" not in self.magic_menu_selector:
                if state.controller.isUpPressed:
                    self.opossum_index -= 2
                    self.menu_movement_sound.play()  # Play the sound effect once

                    if self.opossum_index < 0:
                        self.opossum_index = len(self.menu_selector) - 1  # Wrap around to the last item
                        # print(str(self.opossum_index))

                    # print(self.magic_menu_selector[self.magicindex])  # Print the current menu item
                    pygame.time.delay(200)  # Add a small delay to avoid rapid button presses

                elif state.controller.isDownPressed:
                    self.opossum_index += 2
                    self.menu_movement_sound.play()  # Play the sound effect once

                    if self.opossum_index >= len(self.menu_selector):
                        self.opossum_index = 0  # Wrap around to the first item
                        # print(str(self.opossum_index))

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
                self.menu_movement_sound.play()  # Play the sound effect once

                # Print the current green box index and its content
                current_can_content = getattr(self, f'can{self.green_box_index + 1}')
                print(f"Current green box index: {self.green_box_index}, Content: {current_can_content}")

                # Reset the key pressed time
                state.controller.keyPressedTimes[pygame.K_RIGHT] = pygame.time.get_ticks()

            # Check for 'T' key press
            if state.controller.isTPressed:
                print(self.game_state)

                # Call the function to reveal the selected box content
                state.controller.isPressed = False

                self.reveal_selected_box_content(state)

            self.opossumInACanMessages["pick_message"].update(state)



        if self.game_state == "immune_lose_screen":
            if self.talley_checker == False:
                state.player.exp += 100
                self.talley_checker = True
            # self.opossumInACanMessages["immune_lose_message"].message_index = 0
            self.opossumInACanMessages["immune_lose_message"].update(state)

            if state.player.money < 1:
                self.game_state = "game_over_no_money"

            elif state.player.stamina_points < 1:
                self.game_state = "game_over_no_stamina"
                # state.currentScreen = state.gamblingAreaScreen
                # state.gamblingAreaScreen.start(state)

            elif state.player.money < 150:

                print("Leave")

                self.game_state = "no_money_you_leave"
            elif state.player.stamina_points > 0:

                if state.controller.isTPressed == True:
                    state.controller.isTPressed = False
                    # self.game_state = "play_again_or_leave_screen"
                    # self.opossumInACanMessages["immune_lose_message"].reset()

        if self.game_state == "lose_screen":
            if state.player.money < 1:
                self.game_state = "game_over_no_money"
            # print(str(self.opossumInACanMessages["lose_message"].message_index))
            if self.talley_checker == False:
                state.player.exp += 100
                self.talley_checker = True
                return

            # Reset the message index every time you enter the lose_screen
            if not self.initialized_message:
                self.opossumInACanMessages["lose_message"].message_index = 0
                self.initialized_message = True  # Set the flag to True to avoid resetting again

            # Print the current message index for debugging
            # print(f"Current 'lose_message' index: {self.opossumInACanMessages['lose_message'].message_index}")

            # Update the lose message after resetting the index
            self.opossumInACanMessages["lose_message"].update(state)

            # while self.rabiesStaminaChecker == False:
            #     state.player.stamina_points -= 10
            #     self.rabiesStaminaChecker = True






            # Perform actions based on the message_index
            if self.opossumInACanMessages["lose_message"].message_index == 2:
                state.player.hasRabies = True

                self.initializeGarbageCans()
                self.initialized_message = False

                if state.player.hasRabies == True and state.player.rabiesImmunity == False:
                    state.player.stamina_points = 1
                    self.music_on = True

                    state.currentScreen = state.gamblingAreaScreen
                    state.gamblingAreaScreen.start(state)

                self.game_state = "play_again_or_leave_screen"

            # Reset the flag when you leave the lose_screen state to ensure the message will be reset next time you enter

        if self.game_state == "magic_menu_screen":
            if state.controller.isUpPressed:
                self.magic_menu_opossum_index -= 1
                self.menu_movement_sound.play()  # Play the sound effect once

                if self.magic_menu_opossum_index < 0:
                    self.magic_menu_opossum_index = len(self.magic_menu_selector) - 1  # Wrap around to the last item
                    # print(str(self.magic_menu_opossum_index))

                # print(self.magic_menu_selector[self.magicindex])  # Print the current menu item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses

            elif state.controller.isDownPressed:
                self.magic_menu_opossum_index += 1
                self.menu_movement_sound.play()  # Play the sound effect once

                if self.magic_menu_opossum_index >= len(self.magic_menu_selector):
                    self.magic_menu_opossum_index = 0  # Wrap around to the first item
                    # print(str(self.magic_menu_opossum_index))

                # print(self.magic_menu_selector[self.magicindex])  # Print the current menu item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses




        if self.game_state == "play_again_or_leave_screen":
            self.refresh()
            self.rabiesStaminaChecker = False

            self.opossumInACanMessages["play_again_or_leave_message"].update(state)

            if state.controller.isUpPressed:
                self.play_again_or_quit_index -= 1
                if self.play_again_or_quit_index < 0:
                    self.play_again_or_quit_index = len(self.play_again_or_quit) - 1  # Wrap around to the last item
                pygame.time.delay(200)  # Add a small delay to avoid rapid button presses
            elif state.controller.isDownPressed:
                self.play_again_or_quit_index += 1
                if self.play_again_or_quit_index >= len(self.play_again_or_quit):
                    self.play_again_or_quit_index = 0  # Wrap around to the first item
                pygame.time.delay(200)

            if state.controller.isTPressed:
                if self.play_again_or_quit_index == 0:
                    state.controller.isTPressed = False  # Reset the button state
                    self.debuff_keen_perception = False

                    self.opossumInACanMessages["tally_message"].message_index = 0
                    # print("The oppoin in a can index talley message is at a:" + str(self.opossumInACanMessages["tally_message"].message_index))
                    state.player.money -= 150
                    self.nellyOpossumMoney += 150
                    self.initializeGarbageCans()
                    self.game_state = "menu_screen"


                elif self.play_again_or_quit_index == 1:
                    self.music_on = True
                    self.debuff_keen_perception = False

                    state.currentScreen = state.gamblingAreaScreen
                    state.gamblingAreaScreen.start(state)


        if self.game_state == "opossum_defeated_screen":
            self.opossumBite = True
            state.player.hasRabies = True

            self.opossumInACanMessages["opossum_defeated_message"].update(state)
            if self.opossumInACanMessages["opossum_defeated_message"].message_index == 3:
                # Change the game state to "bet"
                self.music_on = True

                state.currentScreen = state.gamblingAreaScreen
                state.gamblingAreaScreen.start(state)

        if self.game_state == "real_opossum_defeated_screen":
            self.opossumBite = True
            self.opossumInACanMessages["real_opossum_defeated_message"].update(state)
            if self.opossumInACanMessages["real_opossum_defeated_message"].message_index == 1:
                # Change the game state to "bet"
                self.music_on = True

                state.currentScreen = state.gamblingAreaScreen
                state.gamblingAreaScreen.start(state)


        if self.game_state == "hero_defeated_stamina_screen":
            self.opossumInACanMessages["hero_defeated_stamina_message"].update(state)
            if self.opossumInACanMessages["hero_defeated_stamina_message"].message_index == 1:
                # Change the game state to "bet"
                self.music_on = True

                state.currentScreen = state.restScreen
                state.restScreen.start(state)
                state.player.stamina_points = 1

        if self.game_state == "hero_defeated_money_screen":
            self.opossumInACanMessages["hero_defeated_money_message"].update(state)
            if self.opossumInACanMessages["hero_defeated_money_message"].message_index == 1:
                # Change the game state to "bet"
                self.music_on = True

                state.currentScreen = state.gamblingAreaScreen
                state.gamblingAreaScreen.start(state)




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

        sprite_rect = pygame.Rect(1, 255, 133.5, 211)
        sprite = self.trash_sprite_image.subsurface(sprite_rect)
        # hand_sprite = self.hand_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (156, 156))

        box_size = 64
        margin = 50

        # Initialize flags to track if a "lose" can and "X3_star" can have already been shaken
        shaken_lose = False
        shaken_x3_star = False

        # Calculate positions for the trash cans
        positions = []
        for row in range(2):
            for col in range(4):
                x = col * (box_size + margin) + margin + 222
                y = row * (box_size + margin) + margin + 111
                positions.append((x, y))

                # Determine the content of the current trash can
                current_can_content = getattr(self, f'can{len(positions)}')

                # Apply the shaking effect if debuff is active
                if self.debuff_keen_perception == True:
                    shake_effect = (0, 0)  # Default to no shake

                    # Check and apply shake for "lose" cans
                    if current_can_content == 'lose' and not shaken_lose:
                        shaken_lose = True
                        time_since_last_shake = current_time % shake_interval
                        if time_since_last_shake < shake_duration:
                            shake_effect = random.randint(-2, 2), random.randint(-2, 2)

                    # Check and apply shake for "X3_star" cans
                    elif current_can_content == 'X3_star' and not shaken_x3_star:
                        shaken_x3_star = True
                        time_since_last_shake = current_time % shake_interval
                        if time_since_last_shake < shake_duration:
                            shake_effect = random.randint(-2, 2), random.randint(-2, 2)

                    # Apply the shake effect to the position
                    x += shake_effect[0]
                    y += shake_effect[1]

                # Draw the scaled_sprite (trash can) at each position with potential shake effect
                state.DISPLAY.blit(scaled_sprite, (x, y))
        # hand sprite code
        hand_sprite_rect = pygame.Rect(1, 1, 58.5, 58)  # Update these values as needed
        hand_sprite = self.hand_sprite_image.subsurface(hand_sprite_rect)
        scaled_hand_sprite = pygame.transform.scale(hand_sprite, (33, 33))

        if 0 <= self.green_box_index < len(positions):
            hand_x, hand_y = positions[self.green_box_index]
            hand_y += 82  # 10 pixels below the top-left of the selected trash can
            hand_x += 54  # 10 pixels below the top-left of the selected trash can
            state.DISPLAY.blit(scaled_hand_sprite, (hand_x, hand_y))

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
        if state.player.money < 300:
            text_color = (255, 0, 0)  # Red color
        else:
            text_color = (255, 255, 255)  # White color

        state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True, text_color), (37, 210))

        # state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True,
        #                               (255, 255, 255)), (37, 250))
        if state.player.stamina_points < 51:
            text_color = (255, 0, 0)  # Red color
        else:
            text_color = (255, 255, 255)  # White color

        state.DISPLAY.blit(
            self.font.render(f"HP: {state.player.stamina_points}", True,
                             text_color), (37, 250))

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

        state.DISPLAY.blit(self.font.render(f"Money: {self.nellyOpossumMoney}", True,
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

        if self.game_state == "tally_screen":
            # self.opossumInACanMessages["welcome_message"].update(state)

            self.opossumInACanMessages["tally_message"].draw(state)
            if self.opossumInACanMessages["tally_message"].message_index == 0:
                state.DISPLAY.blit(self.font.render(f"Time to tally you up. Your winnings are::{self.total_winnings}", True,
                                                    (255, 255, 255)), (70, 460))

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
            if "shake" in self.magic_menu_selector:
                if self.debuff_keen_perception == False:
                    state.DISPLAY.blit(self.font.render(f"Magic ", True, (255, 255, 255)), (text_x, text_y_yes + 40))
                elif self.debuff_keen_perception == True:
                    state.DISPLAY.blit(self.font.render("Locked", True, (255, 255, 255)), (text_x, text_y_yes + 40))

            elif "shake" not in self.magic_menu_selector:
                if self.debuff_keen_perception == False:
                    state.DISPLAY.blit(self.font.render(f" ", True, (255, 255, 255)), (text_x, text_y_yes + 40))

            state.DISPLAY.blit(self.font.render(f"tally ", True, (255, 255, 255)), (text_x, text_y_yes + 80))

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
                    # state.player.money += self.player_score
                    # self.nellyOpossumMoney -= self.player_score
                    state.player.exp += self.player_score / 5
                    state.controller.isTPressed = False
                    # self.refresh()
                    self.initializeGarbageCans()
                    self.game_state = "tally_screen"
                # elif self.opossum_index == 3:
                #     state.player.money += self.player_score
                #     self.sallyOpossumMoney -= self.player_score
                #     state.controller.isTPressed = False
                #     state.currentScreen = state.gamblingAreaScreen
                #     state.gamblingAreaScreen.start(state)





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
            if "shake" in self.magic_menu_selector:
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
            text_margin = 44  # Margin from the left edge of the top box for the text

            # Position for the "Magic" text inside the top box
            magic_text_x = new_box_x + text_margin
            magic_text_y = new_box_y + (top_box_height - magic_text.get_height()) // 2  # Vertically center inside the top box

            # Blit the "Magic" text onto the screen
            state.DISPLAY.blit(magic_text, (magic_text_x, magic_text_y))
            print(str(self.debuff_keen_perception))

            if self.magic_menu_opossum_index == 0:
                self.opossumInACanMessages["magic_description_reveal"].update(state)
                self.opossumInACanMessages["magic_description_reveal"].draw(state)
            elif self.magic_menu_opossum_index == 1:
                self.opossumInACanMessages["magic_description_back"].update(state)
                self.opossumInACanMessages["magic_description_back"].draw(state)
            if state.controller.isTPressed:
                if self.magic_menu_opossum_index == 0:
                    self.debuff_keen_perception = True
                    state.player.focus_points -= 10
                    self.spell_sound.play()  # Play the sound effect once
                    self.game_state = "menu_screen"
                    state.controller.isTPressed = False  # Reset the button state

                elif self.magic_menu_opossum_index == 1:
                    state.controller.isTPressed = False  # Reset the button state
                    self.game_state = "menu_screen"

        if self.game_state == "immune_lose_screen":
            # self.opossumInACanMessages["welcome_message"].update(state)
            self.opossumInACanMessages["immune_lose_message"].draw(state)
            # state.DISPLAY.blit(self.font.render(f"Opossum Chomp", True,
            #                                     (255, 255, 255)), (70, 460))
            if state.controller.isTPressed:
                state.controller.isTPressed = False
                self.game_state = "play_again_or_leave_screen"

        if self.game_state == "lose_screen":
            # self.opossumInACanMessages["welcome_message"].update(state)

            self.opossumInACanMessages["lose_message"].draw(state)


        if self.game_state == "play_again_or_leave_screen":
            self.opossumInACanMessages["play_again_or_leave_message"].draw(state)
            self.tally_money_once = True

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
            state.DISPLAY.blit(self.font.render(f"No ", True, (255, 255, 255)), (text_x, text_y_yes + 40))
            arrow_x = text_x + 20 - 40  # Adjust the arrow position to the left of the text
            arrow_y = text_y_yes + self.play_again_or_quit_index * 40  # Adjust based on the item's height
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

        if self.game_state == "opossum_defeated_screen":
            self.opossumInACanMessages["opossum_defeated_message"].draw(state)

        if self.game_state == "real_opossum_defeated_screen":
            self.opossumInACanMessages["real_opossum_defeated_message"].draw(state)


        if self.game_state == "hero_defeated_stamina_screen":

            self.opossumInACanMessages["hero_defeated_stamina_message"].draw(state)

        if self.game_state == "hero_defeated_money_screen":
            self.opossumInACanMessages["hero_defeated_stamina_screen"].draw(state)

        if self.game_state == "no_money_you_leave":
            print("draw me")
            self.opossumInACanMessages["less_than_150_money"].draw(state)

        if self.game_state == "game_over_no_money":

            self.opossumInACanMessages["game_over_no_money"].update(state)
            self.opossumInACanMessages["game_over_no_money"].draw(state)
            if self.opossumInACanMessages["game_over_no_money"].is_finished():
                if state.controller.isTPressed:
                    state.currentScreen = state.gameOverScreen
                    state.gameOverScreen.start(state)

        if self.game_state == "game_over_no_stamina":
            self.opossumInACanMessages["game_over_no_stamina"].update(state)
            self.opossumInACanMessages["game_over_no_stamina"].draw(state)
            if self.opossumInACanMessages["game_over_no_stamina"].is_finished():
                if state.controller.isTPressed:
                    state.player.money -= 100
                    if state.player.money < 1:
                        state.currentScreen = state.gameOverScreen
                        state.gameOverScreen.start(state)
                    else:
                        self.game_state = "welcome_screen"

                        state.player.canMove = True
                        state.currentScreen = state.restScreen
                        state.restScreen.start(state)
                        state.player.stamina_points = 1

        pygame.display.flip()