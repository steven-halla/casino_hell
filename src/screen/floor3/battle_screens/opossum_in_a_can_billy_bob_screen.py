import random
from typing import List

import pygame

from constants import WHITE, BLACK, RED
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic

# opssoum shuffle - reshuffles the cans
# opossum guilty shoes- if score is above 750 and you lose , retain 200 points


class OpossumInACanBillyBobScreen(GambleScreen):
    def __init__(self, screenName: str = "Opossum in a can Billy Bob") -> None:
        super().__init__(screenName)
        self.bet: int = 100
        self.dealer_name = "Billy Bob"
        self.billy_bob_bankrupt = 0
        self.game_state:str = self.WELCOME_SCREEN
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)
        self.stamina_drain: int = 50
        self.stamina_drain_repellant: int = 25
        self.pick_index: int = 0
        self.magic_index: int = 1
        self.quit_index: int = 2
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        self.pick_screen_index: int = 0
        self.tally_index:int = 1
        self.debuff_keen_perception: bool = False
        self.player_score: int = 0
        self.pick_tally_screen_index: int = 0
        self.current_box_index: int = 0  # Index of the currently green box
        self.magic_screen_index: int = 0
        self.magic_menu_selector: list[str] = []
        self.shake_cost = 10
        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "My Opossums sure are friendly, they wont bite you. They just wanna nibble."
            ]),

            self.PICK_TALLY_MENU_MESSAGE: MessageBox([
                "Pick to go to trash can selection, tally to end round and turn in points.Score must be higher than 0 to tally."
            ]),


            self.MAGIC_MENU_SHAKE_DESCRIPTION: MessageBox([
                "Shakes the can, reveals 1 opossum and 1 lucky star."
            ]),
            self.PICK_SELECTION_MESSAGE: MessageBox([
                "Shakes the can, reveals 1 opossum and 1 lucky star."
            ]),

            self.MAGIC_MENU_BACK_DESCRIPTION: MessageBox([
                "go back to previous menu"
            ]),

            self.PLAYER_WIN_MESSAGE: MessageBox([
                "You won the toss!!!"
            ]),
            self.PLAYER_LOSE_MESSAGE: MessageBox([
                "You lost the toss."
            ]),

        }


        self.magic_lock: bool = False
        self.welcome_screen_choices: list[str] = ["Play", "Magic",  "Quit"]
        self.pick_screen_choices: list[str] = ["Pick", "Tally"]
        self.index_stepper = 1
        self.positions = []  # Initialize positions list to store trash can positions

        self.trash_sprite_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/PC Computer - The Sims - Galvanized Trash Can (2).png").convert_alpha()
        self.opossum_sprite_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/opossum_redone2.png")
        self.hand_sprite_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/GameCube - Mario Party 4 - Character Hands (1).png").convert_alpha()
        self.winner_or_looser: List[str] = ["win", "med win",
                                            "big win", "high win", "lose",
                                            "lucky_star",
                                            "X3_star", "lose",

                                            ]
        self.winner_or_looser_lucky: List[str] = ["high win", "win",
                                                  "big win", "super win", "med win",
                                                  "lucky_star",
                                                  "X3_star", "lose",

                                                  ]
        self.result: str = ""

        self.can1: str = ""
        self.can2: str = ""
        self.can3: str = ""
        self.can4: str = ""
        self.can5: str = ""
        self.can6: str = ""
        self.can7: str = ""
        self.can8: str = ""
        self.shake: bool = False

        self.win_x, self.win_y = None, None
        self.big_win_x, self.big_win_y = None, None
        self.triple_x, self.triple_y = None, None
        self.lucky_star_x, self.lucky_star_y = None, None
        self.super_win_x, self.super_win_y = None, None
        self.high_win_x, self.high_win_y = None, None
        self.med_win_x, self.med_win_y = None, None
        self.trash_can_x, self.trash_can_y = None, None  # For the opossum image
        self.exp_gain_high = 25
        self.exp_gain_low = 10
        self.exp_gain_medium = 20


    PICK_TALLY_MENU_SCREEN:str = "pick_tally_menu_screen"
    PICK_SCREEN:str = "pick_screen"
    # TALLY_SCREEN:str = "tally_screen"
    PLAYER_LOSE_SCREEN:str = "player_lose_screen"
    PLAYER_WIN_SCREEN:str = "player_win_screen"

    PLAYER_WIN_MESSAGE: str = "player_win_message"
    PLAYER_LOSE_MESSAGE: str = "player_lose_message"
    MAGIC_MENU_SHAKE_DESCRIPTION: str = "magic_menu_force_description"
    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    PICK_TALLY_MENU_MESSAGE: str = "pick_tally_menu_message"
    PICK_SELECTION_MESSAGE: str = "pick_selection_message"


    BACK: str = "Back"


    def initializeGarbageCans(self, state):
        self.trash_can_pick = ""
        self.result = ""
        shuffled_items = random.sample(self.winner_or_looser, len(self.winner_or_looser))
        lucky_draw = random.randint(0, 100)
        print("your lucky draw is: " + str(lucky_draw))

        for luck in range(state.player.luck):
            lucky_draw += 4
        print("your lucky draw is: " + str(lucky_draw))
        if lucky_draw > 90:
            shuffled_items = random.sample(self.winner_or_looser_lucky, len(self.winner_or_looser_lucky))

        self.can1 = shuffled_items[0]

        self.can2 = shuffled_items[1]

        self.can3 = shuffled_items[2]

        self.can4 = shuffled_items[3]

        self.can5 = shuffled_items[4]

        self.can6 = shuffled_items[5]

        self.can7 = shuffled_items[6]

        self.can8 = shuffled_items[7]


    def start(self, state: 'GameState'):
        self.initializeGarbageCans(state)

    def opossum_game_reset(self, state):
        self.shake = False
        self.magic_lock = False
        self.initializeGarbageCans(state)
        self.player_score = 0
        # Reset all win-related positions to None
        # Reset all win-related positions to None
        self.win_x, self.win_y = None, None

        self.big_win_x, self.big_win_y = None, None
        self.triple_x, self.triple_y = None, None
        self.lucky_star_x, self.lucky_star_y = None, None
        self.super_win_x, self.super_win_y = None, None
        self.high_win_x, self.high_win_y = None, None
        self.med_win_x, self.med_win_y = None, None
        self.trash_can_x, self.trash_can_y = None, None  # For the opossum image

    def opossum_round_reset(self, state):
        self.shake = False
        if self.shake == False:
            self.magic_lock = False
        self.initializeGarbageCans(state)
        self.player_score = 0
        # Reset all win-related positions to None
        # Reset all win-related positions to None
        self.win_x, self.win_y = None, None
        self.big_win_x, self.big_win_y = None, None
        self.triple_x, self.triple_y = None, None
        self.lucky_star_x, self.lucky_star_y = None, None
        self.super_win_x, self.super_win_y = None, None
        self.high_win_x, self.high_win_y = None, None
        self.med_win_x, self.med_win_y = None, None
        self.trash_can_x, self.trash_can_y = None, None  # For the opossum image

    def update(self, state):
        if self.money <= self.billy_bob_bankrupt:
            Events.add_event_to_player(state.player, Events.OPOSSUM_IN_A_CAN_BILLY_BOB_DEFEATED)
        super().update(state)
        controller = state.controller
        controller.update()
        state.player.update(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.update_welcome_screen_logic(controller, state)
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
        if self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu_selection_box(controller, state)

        elif self.game_state == self.PICK_TALLY_MENU_SCREEN:


            self.battle_messages[self.PICK_TALLY_MENU_MESSAGE].update(state)

            self.update_pick_tally_menu_screen_logic(controller)

            # self.battle_messages[self.PICK_MESSAGE].update(state)
        elif self.game_state == self.PICK_SCREEN:
            self.update_pick_screen(controller, state)
            self.battle_messages[self.PICK_SELECTION_MESSAGE].update(state)


        elif self.game_state == self.PLAYER_LOSE_SCREEN:
            if Equipment.OPOSSUM_REPELLENT.value in state.player.equipped_items:
                self.battle_messages[self.PLAYER_LOSE_MESSAGE].messages = [f"The repellant scares him off before too much damage is taking. You take 25 damage, and gain {self.exp_gain_high}:   experience points and 0 money."]
            elif Equipment.OPOSSUM_REPELLENT.value not in state.player.equipped_items:
                self.battle_messages[self.PLAYER_LOSE_MESSAGE].messages = [f"The hungry opossum deals 50 damage, you gain {self.exp_gain_high}:   experience points and 0 money."]
            self.battle_messages[self.PLAYER_LOSE_MESSAGE].update(state)

            if controller.isTPressed or controller.isAPressedSwitch:
                controller.isTPressed = False
                controller.isAPressedSwitch = False
                if Equipment.OPOSSUM_REPELLENT.value in state.player.equipped_items:
                    state.player.stamina_points -= self.stamina_drain_repellant
                elif Equipment.OPOSSUM_REPELLENT.value not in state.player.equipped_items:
                    state.player.stamina_points -= self.stamina_drain
                state.player.exp += self.exp_gain_high
                self.opossum_round_reset(state)
                self.game_state = self.WELCOME_SCREEN

        elif self.game_state == self.PLAYER_WIN_SCREEN:
            if self.player_score > self.money:
                self.player_score = self.money
            if self.player_score < 750:
                self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"You WIN! You gain {self.player_score}: money and gain {self.exp_gain_low}:   experience points!"]
            elif self.player_score > 750:
                self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"You WIN! You gain {self.player_score}: money and gain {self.exp_gain_medium}:   experience points!"]

            self.battle_messages[self.PLAYER_WIN_MESSAGE].update(state)
            if controller.isTPressed or controller.isAPressedSwitch:
                if self.player_score < 750:
                    state.player.exp += self.exp_gain_low
                elif self.player_score > 750:
                    state.player.exp += self.exp_gain_medium

                controller.isTPressed = False
                controller.isAPressedSwitch = False

                if self.player_score > self.money:
                    self.player_score = self.money

                state.player.money += self.player_score
                self.money -= self.player_score
                if self.money < 0:
                    self.money = 0
                self.opossum_round_reset(state)

                self.game_state = self.WELCOME_SCREEN
        elif self.game_state == self.GAME_OVER_SCREEN:
            no_money_game_over = 0
            no_stamina_game_over = 0

            if state.player.money <= no_money_game_over:
                if controller.isTPressed or controller.isAPressedSwitch:
                    controller.isTPressed = False
                    controller.isAPressedSwitch = False
                    state.currentScreen = state.gameOverScreen
                    state.gameOverScreen.start(state)
            elif state.player.stamina_points <= no_stamina_game_over:
                if controller.isTPressed or controller.isAPressedSwitch:
                    controller.isTPressed = False
                    controller.isAPressedSwitch = False
                    self.opossum_round_reset(state)
                    state.player.money -= 100
                    # state.currentScreen = state.area3RestScreen
                    # state.area3RestScreen.start(state)


    def draw(self, state):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)
        self.draw_box_info(state)
        self.draw_opossum_sprite_image(state)
        self.draw_win_message(state)
        self.draw_big_win_message(state)
        self.draw_med_win_message(state)
        self.draw_high_win_message(state)
        self.draw_super_win_message(state)
        self.draw_triple_win_message(state)
        self.draw_lucky_star_message(state)



        if self.game_state == self.WELCOME_SCREEN:

            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)

            self.battle_messages[self.WELCOME_MESSAGE].draw(state)

        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box(state)

        elif self.game_state == self.PICK_TALLY_MENU_SCREEN:
            self.draw_pick_tally_menu_logic(state)
            self.battle_messages[self.PICK_TALLY_MENU_MESSAGE].draw(state)

            # self.battle_messages[self.PICK_MESSAGE].draw(state)

        elif self.game_state == self.PICK_SCREEN:
            self.battle_messages[self.PICK_SELECTION_MESSAGE].draw(state)

            self.draw_pick_screen(state)

        elif self.game_state == self.PLAYER_LOSE_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_MESSAGE].draw(state)

        elif self.game_state == self.PLAYER_WIN_SCREEN:
            self.battle_messages[self.PLAYER_WIN_MESSAGE].draw(state)

        elif self.game_state == self.GAME_OVER_SCREEN:
            no_money_game_over = 0
            no_stamina_game_over = 0
            if state.player.money <= no_money_game_over:
                state.DISPLAY.blit(self.font.render(f"You ran out of money and are now a prisoner of hell", True, WHITE), (self.blit_message_x, self.blit_message_y))
            elif state.player.stamina <= no_stamina_game_over:
                state.DISPLAY.blit(self.font.render(f"You ran out of stamina , you lose -100 gold", True, WHITE), (self.blit_message_x, self.blit_message_y))

        pygame.display.flip()

    def draw_magic_menu_selection_box(self, state):
        if self.magic_menu_selector[self.magic_screen_index] == Magic.SHAKE.value:
            self.battle_messages[self.MAGIC_MENU_SHAKE_DESCRIPTION].draw(state)
        #
        #
        # elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value:
        #     self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].draw(state)
        #
        #
        elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)


        choice_spacing = 40
        text_x_offset = 60
        text_y_offset = 15
        arrow_x_offset = 12
        arrow_y_offset_triple_dice = 12
        arrow_y_offset_back = 52
        black_box_height = 221 - 50  # Adjust height
        black_box_width = 200 - 10  # Adjust width to match the left box
        border_width = 5
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
        start_y_right_box = 240  # Adjust vertical alignment

        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill(BLACK)

        white_border = pygame.Surface(
            (black_box_width + 2 * border_width, black_box_height + 2 * border_width)
        )
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))

        black_box_x = start_x_right_box - border_width
        black_box_y = start_y_right_box - border_width

        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

        for idx, choice in enumerate(self.magic_menu_selector):
            y_position = start_y_right_box + idx * choice_spacing  # Use the defined spacing variable
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        # Draw the arrow at the current magic screen index position
        arrow_y_position = start_y_right_box + (self.magic_screen_index * choice_spacing) + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_position)  # Use the arrow offsets
        )

    def update_magic_menu_selection_box(self, controller, state):
        if self.magic_menu_selector[self.magic_screen_index] == Magic.SHAKE.value:
            self.battle_messages[self.MAGIC_MENU_SHAKE_DESCRIPTION].update(state)
            #
            # self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()
        elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
            self.battle_messages[self.MAGIC_MENU_SHAKE_DESCRIPTION].reset()
            #
            # self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)
        # elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
        #     self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)
        #
        #     self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].reset()
        #     self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].reset()

        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index - self.index_stepper) % len(self.magic_menu_selector)
            print(f"Current Magic Menu Selector: {self.magic_menu_selector[self.magic_screen_index]}")
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index + self.index_stepper) % len(self.magic_menu_selector)
            print(f"Current Magic Menu Selector: {self.magic_menu_selector[self.magic_screen_index]}")

        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            if self.magic_menu_selector[self.magic_screen_index] == Magic.SHAKE.value and state.player.focus_points >= self.shake_cost:
                state.player.focus_points -= self.shake_cost
                self.debuff_keen_perception = True
                self.spell_sound.play()  # Play the sound effect once
                self.magic_lock = True
                self.game_state = self.WELCOME_SCREEN

            elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
                self.game_state = self.WELCOME_SCREEN

    def update_pick_screen(self, controller, state):
        if controller.isBPressed or controller.isBPressedSwitch:
            controller.isBPressed = False
            controller.isBPressedSwitch = False
            self.game_state = self.PICK_TALLY_MENU_SCREEN
        time_since_right_pressed = state.controller.timeSinceKeyPressed(pygame.K_RIGHT)
        time_since_left_pressed = state.controller.timeSinceKeyPressed(pygame.K_LEFT)
        key_press_threshold = 80  # Example threshold, adjust as needed
        current_can_content = ""

        if (state.controller.isRightPressed or state.controller.isRightPressedSwitch) and time_since_right_pressed >= key_press_threshold:
            # Initially move to the next box

            self.current_box_index = (self.current_box_index + 1) % 8
            current_can_content = getattr(self, f'can{self.current_box_index + 1}')

            # Continue moving right if the can is empty
            while current_can_content == "":
                self.current_box_index = (self.current_box_index + 1) % 8
                current_can_content = getattr(self, f'can{self.current_box_index + 1}')

            self.menu_movement_sound.play()  # Play the sound effect once for the valid move
            print(f"Current full box index: {self.current_box_index}, Content: {current_can_content}")
            state.controller.keyPressedTimes[pygame.K_RIGHT] = pygame.time.get_ticks()

        elif (state.controller.isLeftPressed or state.controller.isLeftPressedSwitch) and time_since_left_pressed >= key_press_threshold:
            # Initially move to the previous box
            self.current_box_index = (self.current_box_index - 1 + 8) % 8  # Adding 8 before modulo for negative index handling
            current_can_content = getattr(self, f'can{self.current_box_index + 1}')

            # Continue moving left if the can is empty
            while current_can_content == "":
                self.current_box_index = (self.current_box_index - 1 + 8) % 8  # Ensure the index wraps correctly
                current_can_content = getattr(self, f'can{self.current_box_index + 1}')

            self.menu_movement_sound.play()  # Play the sound effect once for the valid move
            print(f"Current green box index: {self.current_box_index}, Content: {current_can_content}")
            state.controller.keyPressedTimes[pygame.K_LEFT] = pygame.time.get_ticks()

            # Check for 'T' key press
        if state.controller.isTPressed or state.controller.isAPressedSwitch:
            print(";fdsjfds;lafjsaf;lj")
            # print(self.game_state)

            # Call the function to reveal the selected box content
            state.controller.isTPressed = False
            state.controller.isAPressedSwitch = False

            self.reveal_selected_box_content(state)

    def reveal_selected_box_content(self, state):
        selected_can_attribute = f'can{self.current_box_index + 1}'
        selected_box_content = getattr(self, selected_can_attribute)
        # print(f"Selected box content: {selected_box_content}")

        if selected_box_content == "win":
            self.trash_can_pick = "win"
            self.player_score += 60
            self.result = "+60"
            self.win_x, self.win_y = self.positions[self.current_box_index]  # Store the position
            # Reset or do not set the win coordinates for other outcomes

        if selected_box_content == "med win":
            self.trash_can_pick = "med win"
            self.player_score += 70
            self.result = "+70"
            self.med_win_x, self.med_win_y = self.positions[self.current_box_index]  # Store the position
            # Reset or do not set the win coordinates for other outcomes

        if selected_box_content == "high win":
            self.trash_can_pick = "med win"
            self.player_score += 80
            self.result = "+80"
            self.high_win_x, self.high_win_y = self.positions[self.current_box_index]  # Store the position
            # Reset or do not set the win coordinates for other outcomes

        if selected_box_content == "super win":
            self.trash_can_pick = "super win"
            self.player_score += 100
            self.result = "+100"
            self.super_win_x, self.super_win_y = self.positions[self.current_box_index]  # Store the position
            # Reset or do not set the win coordinates for other outcomes


        if selected_box_content == "big win":
            self.trash_can_pick = "win"
            self.player_score += 120
            self.result = "+120"
            self.big_win_x, self.big_win_y = self.positions[self.current_box_index]  # Store the position

        if selected_box_content == "X3_star":
            self.trash_can_pick = "X3_star"
            self.result = "X3"

            self.player_score *= 3
            self.triple_x, self.triple_y = self.positions[self.current_box_index]  # Store the position


        if selected_box_content == "lucky_star":
            self.trash_can_pick = "lucky_star"
            self.player_score += 250
            self.result = "+250"
            self.lucky_star_x, self.lucky_star_y = self.positions[self.current_box_index]  # Store the position


        if selected_box_content == "lose":
            self.result = "lose"

            self.trash_can_pick = "lose"
            self.debuff_keen_perception = False
            self.player_score = 0

            self.trash_can_x, self.trash_can_y = self.positions[self.current_box_index]
            self.game_state = self.PLAYER_LOSE_SCREEN
            print(self.game_state)


            # self.opossum_round_reset(state)
            # self.game_state = self.PLAYER_LOSE_SCREEN

        # Remove the item from the can (set it to an empty string)
        setattr(self, selected_can_attribute, "")

    def draw_triple_win_message(self, state):
        if self.triple_x is not None and self.triple_y is not None:
            font = pygame.font.Font(None, 50)
            triple_win_message = font.render("*3", True, WHITE)
            state.DISPLAY.blit(triple_win_message, (self.triple_x + 59, self.triple_y + 28))

    def draw_super_win_message(self, state):
        if self.super_win_x is not None and self.super_win_y is not None:
            font = pygame.font.Font(None, 50)
            super_win_message = font.render("+100", True, WHITE)
            state.DISPLAY.blit(super_win_message, (self.super_win_x + 33, self.super_win_y + 28))

    def draw_high_win_message(self, state):
        if self.high_win_x is not None and self.high_win_y is not None:
            font = pygame.font.Font(None, 50)
            high_win_message = font.render("+80", True, WHITE)
            state.DISPLAY.blit(high_win_message, (self.high_win_x + 43, self.high_win_y + 28))

    def draw_med_win_message(self, state):
        if self.med_win_x is not None and self.med_win_y is not None:
            font = pygame.font.Font(None, 50)
            med_win_message = font.render("+70", True, WHITE)
            state.DISPLAY.blit(med_win_message, (self.med_win_x + 43, self.med_win_y + 28))

    def draw_big_win_message(self, state):
        if self.big_win_x is not None and self.big_win_y is not None:
            font = pygame.font.Font(None, 50)
            big_win_message = font.render("+120", True, WHITE)
            state.DISPLAY.blit(big_win_message, (self.big_win_x + 33, self.big_win_y + 28))

    def draw_win_message(self, state):
        if self.win_x is not None and self.win_y is not None:
            font = pygame.font.Font(None, 50)
            win_message = font.render("+60", True, WHITE)
            state.DISPLAY.blit(win_message, (self.win_x + 44, self.win_y + 28))

    def draw_lucky_star_message(self, state):
        if self.lucky_star_x is not None and self.lucky_star_y is not None:
            font = pygame.font.Font(None, 50)
            lucky_star_message = font.render("+250", True, WHITE)
            state.DISPLAY.blit(lucky_star_message, (self.lucky_star_x + 33, self.lucky_star_y + 28))


    def draw_opossum_sprite_image(self, state):
        if self.result == "lose" and hasattr(self, 'trash_can_x') and hasattr(self, 'trash_can_y'):
            sprite_rect = pygame.Rect(1, 145, 48, 44)
            opossum_sprite = self.opossum_sprite_image.subsurface(sprite_rect)
            scaled_opossum_sprite = pygame.transform.scale(opossum_sprite, (99, 99))
            state.DISPLAY.blit(scaled_opossum_sprite, (self.trash_can_x + 30, self.trash_can_y - 30))

    def draw_pick_screen(self, state):
        # self.result = "lose"
        #
        # self.trash_can_pick = "lose"


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
        self.positions = []  # Recalculate the positions every time the screen is drawn
        for row in range(2):
            for col in range(4):
                if len(self.positions) < 8:  # Ensure only 8 positions are created
                    x = col * (box_size + margin) + margin + 190
                    y = row * (box_size + margin) + margin + 50
                    self.positions.append((x, y))

                # Determine the content of the current trash can
                # Determine the content of the current trash can
                current_can_content = getattr(self, f'can{len(self.positions)}')
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
                if current_can_content:
                    state.DISPLAY.blit(scaled_sprite, (x, y))
        # hand sprite code
        hand_sprite_rect = pygame.Rect(1, 1, 58.5, 58)  # Update these values as needed
        hand_sprite = self.hand_sprite_image.subsurface(hand_sprite_rect)
        scaled_hand_sprite = pygame.transform.scale(hand_sprite, (33, 33))

        if 0 <= self.current_box_index < len(self.positions):
            hand_x, hand_y = self.positions[self.current_box_index]
            hand_y += 82  # 10 pixels below the top-left of the selected trash can
            hand_x += 54  # 10 pixels below the top-left of the selected trash can
            state.DISPLAY.blit(scaled_hand_sprite, (hand_x, hand_y))
            # print(f"Selected trash can position: x = {hand_x}, y = {hand_y}")



    def draw_pick_tally_menu_logic(self, state):
        # self.battle_messages[self.CHOOSE_SIDE_MESSAGE].draw(state)

        choice_spacing = 40
        text_x_offset = 60
        text_y_offset = 15
        arrow_x_offset = 12
        arrow_y_offset_triple_dice = 12
        arrow_y_offset_back = 52
        black_box_height = 221 - 50  # Adjust height
        black_box_width = 200 - 10  # Adjust width to match the left box
        border_width = 5
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
        start_y_right_box = 240  # Adjust vertical alignment

        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill(BLACK)

        white_border = pygame.Surface(
            (black_box_width + 2 * border_width, black_box_height + 2 * border_width)
        )
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))

        black_box_x = start_x_right_box - border_width
        black_box_y = start_y_right_box - border_width

        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

        for idx, choice in enumerate(self.pick_screen_choices):
            y_position = start_y_right_box + idx * choice_spacing  # Use the defined spacing variable
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        # Draw the arrow at the current magic screen index position
        arrow_y_position = start_y_right_box + (self.pick_tally_screen_index * choice_spacing) + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_position)  # Use the arrow offsets
        )

    def update_pick_tally_menu_screen_logic(self, controller):
        if controller.isTPressed or controller.isAPressedSwitch:
            print(";fdjfl;jsalfjsafjsf;ljsa")
            print(self.pick_screen_index)
            controller.isTPressed = False
            controller.isAPressedSwitch = False

            if self.pick_tally_screen_index == self.pick_index:
                self.game_state = self.PICK_SCREEN
            elif self.pick_tally_screen_index == self.tally_index and self.player_score > 0:
                self.game_state = self.PLAYER_WIN_SCREEN

        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()
            self.pick_tally_screen_index = (self.pick_tally_screen_index - self.index_stepper) % len(self.pick_screen_choices)
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False
            self.menu_movement_sound.play()
            self.pick_tally_screen_index = (self.pick_tally_screen_index + self.index_stepper) % len(self.pick_screen_choices)


    def update_welcome_screen_logic(self, controller, state):
        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            if self.welcome_screen_index == self.pick_index:
                self.game_state = self.PICK_TALLY_MENU_SCREEN
            elif self.welcome_screen_index == self.magic_index and self.magic_lock == False:
                self.game_state = self.MAGIC_MENU_SCREEN
            elif self.welcome_screen_index == self.quit_index:
                state.currentScreen = state.area3RestScreen
                state.area3RestScreen.start(state)

    def draw_welcome_screen_box_info(self, state: 'GameState'):
        box_width_offset = 10
        horizontal_padding = 25
        vertical_position = 240
        spacing_between_choices = 40
        text_x_offset = 60
        text_y_offset = 15
        black_box_width = 200 - box_width_offset
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - horizontal_padding
        start_y_right_box = vertical_position
        arrow_x_coordinate_padding = 12
        arrow_y_coordinate_padding_play = 12
        arrow_y_coordinate_padding_magic = 52

        arrow_y_coordinate_padding_quit = 92

        for idx, choice in enumerate(self.welcome_screen_choices):
            y_position = start_y_right_box + idx * spacing_between_choices  # Adjust spacing between choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        if Magic.SHAKE.value not in state.player.magicinventory:
            self.magic_lock = True
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif Magic.SHAKE.value in state.player.magicinventory:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if Magic.SHAKE.value in state.player.magicinventory and Magic.SHAKE.value not in self.magic_menu_selector:
            self.magic_menu_selector.append(Magic.SHAKE.value)

        if self.BACK not in self.magic_menu_selector:
            self.magic_menu_selector.append(self.BACK)

        if self.magic_lock == True:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif self.magic_lock == False:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if self.welcome_screen_index == self.welcome_screen_play_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_play)
            )
        elif self.welcome_screen_index == self.welcome_screen_magic_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_magic)
            )

        elif self.welcome_screen_index == self.quit_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_quit)
            )

    def draw_box_info(self, state: 'GameState'):
        player_enemy_box_info_x_position = 37
        player_enemy_box_info_x_position_score = 28
        score_y_position = 150
        enemy_name_y_position = 33
        phase_y_position = 108
        choice_y_position = 148
        enemy_money_y_position = 70
        enemy_status_y_position = 110
        bet_y_position = 370
        player_money_y_position = 250
        hero_name_y_position = 205
        hero_stamina_y_position = 290
        hero_focus_y_position = 330
        score_header = "Score"

        if self.debuff_keen_perception == True:
            state.DISPLAY.blit(self.font.render(f"Shake: 1", True, RED), (player_enemy_box_info_x_position, enemy_name_y_position))
        elif self.debuff_keen_perception == False:
            state.DISPLAY.blit(self.font.render(self.dealer_name, True, WHITE), (player_enemy_box_info_x_position, enemy_name_y_position))


        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}", True, WHITE), (player_enemy_box_info_x_position, enemy_money_y_position))
        state.DISPLAY.blit(self.font.render(f" Score: {self.player_score}", True, WHITE), (player_enemy_box_info_x_position - 7, choice_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE), (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE), (player_enemy_box_info_x_position, player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE), (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE), (player_enemy_box_info_x_position, hero_focus_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.HERO_HEADER}", True, WHITE), (player_enemy_box_info_x_position, hero_name_y_position))






