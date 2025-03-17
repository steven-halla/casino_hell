import random

import pygame

from constants import WHITE, BLACK, RED
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.coin_flip_constants import CoinFlipConstants
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic


class CoinFlipDexterScreen(GambleScreen):
    # this class has an error with T key so far black jack is only class not affected

    # our money is not in balance let me correct that:
    # Greediest of all the pigs of filth, share your horde with the poor and down trodden of the world...money balancer
    # money balancer effects: Draw player loses self.bet, win player wins self.bet // 1/2 loss player loses self.bet * 2
    def __init__(self, screenName: str = "Coin FLip") -> None:
        super().__init__(screenName)
        self.bet:int = 100
        self.dealer_name: str = "Dexter"
        self.initial_coin_image_position = (300, 250)  # Initial position for the coin
        self.timer_start = None
        self.coin_bottom = False
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        self.sprite_sheet = pygame.image.load("./assets/images/coin_flipping_alpha.png").convert_alpha()
        self.game_state: str = self.WELCOME_SCREEN
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.heads_or_tails_menu: list[str] = ["Heads", "Tails", "Back"]
        self.magic_menu_selector: list[str] = [Magic.SHIELD.value]
        self.welcome_screen_index: int = 0
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.phase: int = 1
        self.flip_coin_index: int = 0
        self.magic_index: int = 1
        self.bet_index: int = 2
        self.shield_debuff_inactive = 0
        self.quit_index: int = 3
        self.headstailsindex: int = 0
        self.image_to_display = ""
        self.heads_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/heads.png")
        self.tails_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/tails.png")

        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)
        self.weighted_coin: bool = False  # this is our magic spell heads force
        self.balance_modifier: int = 0
        self.player_choice = ""
        self.coin_landed = CoinFlipConstants.HEADS.value
        self.dexter_bankrupt: int = 0
        self.magic_lock = False
        self.low_stamina_drain: int = 10
        self.index_stepper: int = 1
        self.magic_screen_index: int = 0
        self.shield_cost: int = 30
        self.shield_debuff = 0
        self.heads_force_cost = 50
        self.heads_force_active = False
        self.coin_bottom = False
        self.exp_gain_high = 1
        self.exp_gain_low = 1
        self.result_anchor = False
        self.timer_start = None  # Initialize the timer variable

        self.money: int = 200  # Add this line


        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "I follow the path of Yin and Yang. Balance is the only true way to play coin flip."
            ]),

            self.BET_MESSAGE: MessageBox([
                "Min bet of 50, max of 200. Press up and down keys to increase/decrease bet. Press B to go back."
            ]),
            self.MAGIC_MENU_SHIELD_DESCRIPTION: MessageBox([
                "The animals of hell are on your side. Defends against bad flips."
            ]),
            self.MAGIC_MENU_FORCE_DESCRIPTION: MessageBox([
                "Using physics you can get the coin to land on heads every time."
            ]),
            self.MAGIC_MENU_BACK_DESCRIPTION: MessageBox([
                "go back to previous menu"
            ]),
            self.COIN_FLIP_MESSAGE: MessageBox([
                "Coin is flipping oh boy I wonder where it will land?"
            ]),
            self.CHOOSE_SIDE_MESSAGE: MessageBox([
                "Pick Heads or Tails."
            ]),
            self.PLAYER_WIN_MESSAGE: MessageBox([
                "You won the toss!!!"
            ]),
            self.PLAYER_LOSE_MESSAGE: MessageBox([
                "You lost the toss."
            ]),
            self.PLAYER_DRAW_MESSAGE: MessageBox([
                f"The Birdy of Hell snatched the coin, it's a DRAW! You win 0 gold and win {self.exp_gain_low} experience points"
            ]),
            self.LEVEL_UP_MESSAGE: MessageBox([
                f"You leveld up!"
            ]),
            self.ANIMAL_DEFENSE_MESSAGE: MessageBox([
                f"A lucky bird swooped in to help you out of a jam!"
            ]),
        }

    # dont draw the coin if its a draw, or maybe draw a bird or animal in its place that "stole/ate
    # the coin.

    COIN_FLIP_SCREEN: str = "coin_flip_screen"
    BACK: str = "Back"
    RESULTS_SCREEN: str = "results_screen"
    CHOOSE_SIDE_SCREEN: str = "choose_side_screen"
    PLAYER_WIN_SCREEN: str = "player_win_screen"
    PLAYER_LOSE_SCREEN: str = "player_lose_screen"
    PLAYER_DRAW_SCREEN: str = "player_draw_screen"

    LEVEL_UP_MESSAGE: str = "level_up_message"


    ANIMAL_DEFENSE_MESSAGE: str = "animal defense message"
    PLAYER_WIN_MESSAGE: str = "player_win_message"
    CHOOSE_SIDE_MESSAGE: str = "choose_side_message"
    PLAYER_LOSE_MESSAGE: str = "player_lose_message"
    PLAYER_DRAW_MESSAGE: str = "player_draw_message"
    COIN_FLIP_MESSAGE: str = "coin_flip_message"
    MAGIC_MENU_FORCE_DESCRIPTION: str = "magic_menu_force_description"
    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    MAGIC_MENU_SHIELD_DESCRIPTION: str = "magic_menu_shield_description"
    BET_MESSAGE: str = "bet_message"
    PLAYER_WIN_ACTION_MESSAGE: str = "player_win_action_message"
    ENEMY_WIN_ACTION_MESSAGE: str = "enemy_win_action_message"
    PLAYER_ENEMY_DRAW_ACTION_MESSAGE: str = "player_enemy_draw_action_message"

    def start(self, state: 'GameState'):
        pass

    def reset_coin_flip_game(self):
        self.battle_messages[self.WELCOME_MESSAGE].reset()
        self.battle_messages[self.COIN_FLIP_MESSAGE].reset()

        self.phase = 1
        self.balance_modifier: int = 0
        self.welcome_screen_index = 0
        self.shield_debuff = 0
        self.heads_force_active = False
        self.coin_bottom = False
        self.result_anchor = False
        self.timer_start = None  # Initialize the timer variable

        self.image_to_display = ""
        self.player_choice = ""
        # self.coin_image_position = (300, 400)  # Reset to the initial value at the start of the round
        self.weighted_coin = False

    def reset_round(self):
        self.battle_messages[self.WELCOME_MESSAGE].reset()

        self.weighted_coin = False
        self.heads_force_active = False
        # self.coin_image_position = (300, 400)  # Reset to the initial value at the start of the round

        self.coin_bottom = False
        self.result_anchor = False
        self.image_to_display = ""
        self.player_choice = ""
        self.timer_start = None  # Initialize the timer variable

        self.phase += 1
        if self.phase > 5:
            self.phase = 1
        if self.phase == 1:
            self.balance_modifier = 0
        if self.shield_debuff > 0:
            self.shield_debuff -= 1
        if self.shield_debuff == 0 and self.weighted_coin == False:
            self.magic_lock = False

    def update(self, state):

        super().update(state)
        controller = state.controller
        controller.update()
        state.player.update(state)
        if self.money <= self.dexter_bankrupt:
            state.currentScreen = state.area3RestScreen
            state.area3RestScreen.start(state)
            Events.add_level_three_event_to_player(state.player, Events.COIN_FLIP_DEXTER_DEFEATED)


        if self.game_state == self.WELCOME_SCREEN:
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
            self.battle_messages[self.BET_MESSAGE].reset()
            self.update_welcome_screen_logic(controller, state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].update(state)
            self.bet_screen_helper(state, controller)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu_selection_box(controller, state)
        elif self.game_state == self.CHOOSE_SIDE_SCREEN:
            self.update_choose_side_logic(controller, state)
        elif self.game_state == self.COIN_FLIP_SCREEN:
            self.battle_messages[self.COIN_FLIP_MESSAGE].update(state)
            self.result_anchor = True
            if self.coin_bottom == True:
                self.game_state = self.RESULTS_SCREEN
        elif self.game_state == self.RESULTS_SCREEN:
            if self.result_anchor == True:
                self.update_flip_coin(controller)
            if controller.isTPressed or controller.isAPressedSwitch:
                controller.isTPressed = False
                controller.isAPressedSwitch = False
                if self.heads_force_active == True:
                    self.coin_landed = CoinFlipConstants.HEADS.value
                if self.player_choice == CoinFlipConstants.HEADS.value and self.heads_force_active == True:
                    self.game_state = self.PLAYER_WIN_SCREEN

                if self.coin_landed == self.player_choice:
                    self.game_state = self.PLAYER_WIN_SCREEN
                elif self.coin_landed != self.player_choice and self.shield_debuff > 0:

                    self.game_state = self.PLAYER_DRAW_SCREEN
                elif self.coin_landed != self.player_choice:
                    self.game_state = self.PLAYER_LOSE_SCREEN

        elif self.game_state == self.PLAYER_WIN_SCREEN:
            self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"You WIN! You WIN {self.bet}:"
                                                                      f" money and gain {self.exp_gain_high}:  "
                                                                      f" experience points!"]
            self.battle_messages[self.PLAYER_WIN_MESSAGE].update(state)

            if controller.isTPressed or controller.isAPressedSwitch:
                controller.isTPressed = False
                controller.isAPressedSwitch = False
                self.reset_round()

                state.player.exp += self.exp_gain_high
                state.player.money += self.bet
                self.money -= self.bet
                perception_bonus = 0  # Initialize perception bonus

                if Equipment.COIN_FLIP_GLASSES.value in state.player.equipped_items:
                    perception_bonus = 0  # Initialize perception bonus

                    for bonus in range(state.player.perception):  # Loop for each perception point
                        perception_bonus += 10  # Add +10 for each perception point

                    # Ensure enemy money doesn't go below 0
                    if self.money < 0:
                        self.money = 0

                    # Player should only receive what is actually available
                    amount_to_gain = min(perception_bonus, self.money)  # Only take what's available
                    state.player.money += amount_to_gain

                    # Deduct from enemy money
                    self.money -= amount_to_gain


                self.game_state = self.WELCOME_SCREEN
        elif self.game_state == self.PLAYER_LOSE_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_MESSAGE].messages = [f"You Lose! You Lose {self.bet}:"
                                                                       f" money and gain {self.exp_gain_low}:   "
                                                                       f"experience points!"]
            self.battle_messages[self.PLAYER_LOSE_MESSAGE].update(state)
            if controller.isTPressed or controller.isAPressedSwitch:
                controller.isTPressed = False
                controller.isAPressedSwitch = False
                self.reset_round()
                state.player.exp += self.exp_gain_low
                state.player.money -= self.bet
                self.money += self.bet
                self.game_state = self.WELCOME_SCREEN
        elif self.game_state == self.PLAYER_DRAW_SCREEN:
            self.battle_messages[self.PLAYER_DRAW_MESSAGE].update(state)

            if controller.isTPressed or controller.isAPressedSwitch:
                controller.isTPressed = False
                controller.isAPressedSwitch = False
                self.reset_round()

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
                    self.reset_coin_flip_game()
                    state.player.money -= 100
                    # state.currentScreen = state.area3RestScreen
                    # state.area3RestScreen.start(state)

    def draw(self, state: 'GameState'):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)
        self.draw_box_info(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.battle_messages[self.WELCOME_MESSAGE].draw(state)
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].draw(state)

        elif self.game_state == self.CHOOSE_SIDE_SCREEN:
            self.draw_choose_side_logic(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box(state)
        elif self.game_state == self.COIN_FLIP_SCREEN:

            self.battle_messages[self.COIN_FLIP_MESSAGE].draw(state)

            self.draw_flip_coin(state)
        elif self.game_state == self.RESULTS_SCREEN:
            self.draw_results_screen_logic(state)
        elif self.game_state == self.PLAYER_WIN_SCREEN:
            self.battle_messages[self.PLAYER_WIN_MESSAGE].draw(state)
            self.draw_results_screen_logic(state)
        elif self.game_state == self.PLAYER_LOSE_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_MESSAGE].draw(state)

            self.draw_results_screen_logic(state)

        elif self.game_state == self.PLAYER_DRAW_SCREEN:
            self.battle_messages[self.PLAYER_DRAW_MESSAGE].draw(state)

            self.draw_results_screen_logic(state)

        elif self.game_state == self.GAME_OVER_SCREEN:
            no_money_game_over = 0
            no_stamina_game_over = 0
            if state.player.money <= no_money_game_over:
                state.DISPLAY.blit(self.font.render(f"You ran out of money and are now a prisoner of hell", True, WHITE), (self.blit_message_x, self.blit_message_y))
            elif state.player.stamina_points <= no_stamina_game_over:
                state.DISPLAY.blit(self.font.render(f"You ran out of stamina , you lose -100 gold", True, WHITE), (self.blit_message_x, self.blit_message_y))

        pygame.display.flip()


    def update_choose_side_logic(self, controller, state):
        self.battle_messages[self.CHOOSE_SIDE_MESSAGE].update(state)

        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()
            self.headstailsindex = (self.headstailsindex - self.index_stepper) % len(self.heads_or_tails_menu)
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False
            self.menu_movement_sound.play()
            self.headstailsindex = (self.headstailsindex + self.index_stepper) % len(self.heads_or_tails_menu)

        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            if self.headstailsindex == 0:
                self.player_choice = CoinFlipConstants.HEADS.value
                self.game_state = self.COIN_FLIP_SCREEN
            elif self.headstailsindex == 1:
                self.player_choice = CoinFlipConstants.TAILS.value
                self.game_state = self.COIN_FLIP_SCREEN

            elif self.headstailsindex == 2:
                self.headstailsindex = 0
                self.game_state = self.WELCOME_SCREEN

    def draw_choose_side_logic(self, state):
        self.battle_messages[self.CHOOSE_SIDE_MESSAGE].draw(state)

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

        for idx, choice in enumerate(self.heads_or_tails_menu):
            y_position = start_y_right_box + idx * choice_spacing  # Use the defined spacing variable
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        # Draw the arrow at the current magic screen index position
        arrow_y_position = start_y_right_box + (self.headstailsindex * choice_spacing) + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_position)  # Use the arrow offsets
        )

    def draw_results_screen_logic(self, state):
        self.image_to_display = (
            self.heads_image
            if self.coin_landed == CoinFlipConstants.HEADS.value
            else self.tails_image
        )

        if self.heads_force_active == True:
            self.image_to_display = self.heads_image

        image_rect = self.image_to_display.get_rect()
        image_rect.center = (state.DISPLAY.get_width() // 2, state.DISPLAY.get_height() // 2)
        state.DISPLAY.blit(self.image_to_display, image_rect)

    def update_magic_menu_selection_box(self, controller, state):
        if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value:
            self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].update(state)

            self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()
        elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value:
            self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].update(state)

            self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()
        elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)

            self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].reset()

        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index - self.index_stepper) % len(self.magic_menu_selector)
            # print(f"Current Magic Menu Selector: {self.magic_menu_selector[self.magic_screen_index]}")
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index + self.index_stepper) % len(self.magic_menu_selector)
            # print(f"Current Magic Menu Selector: {self.magic_menu_selector[self.magic_screen_index]}")

        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value and state.player.focus_points >= self.shield_cost:
                state.player.focus_points -= self.shield_cost
                self.shield_debuff = 3
                print(f"Shield debuff: {self.shield_debuff}")
                self.spell_sound.play()  # Play the sound effect once
                self.magic_lock = True
                self.game_state = self.WELCOME_SCREEN
            elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value and state.player.focus_points >= self.heads_force_cost:
                state.player.focus_points -= self.heads_force_cost
                self.heads_force_active = True
                self.spell_sound.play()  # Play the sound effect once
                self.magic_lock = True
                self.game_state = self.WELCOME_SCREEN
            elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
                self.game_state = self.WELCOME_SCREEN



    def draw_magic_menu_selection_box(self, state):
        if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value:
            self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].draw(state)


        elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value:
            self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].draw(state)


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

    def update_welcome_screen_logic(self, controller, state):
        # print("493")
        # self.game_state = self.CHOOSE_SIDE_SCREEN

        # if state.controller.isTPressed:
        #     print("497")
        #
        #     state.controller.isTPressed = False
        # print("497")

        if self.welcome_screen_index == self.flip_coin_index and controller.isAPressedSwitch :
            state.controller.isAPressedSwitch = False

            state.player.stamina_points -= self.low_stamina_drain
            self.game_state = self.CHOOSE_SIDE_SCREEN
        elif self.welcome_screen_index == self.magic_index and self.magic_lock == False and controller.isAPressedSwitch :
            state.controller.isAPressedSwitch = False

            self.game_state = self.MAGIC_MENU_SCREEN
        elif self.welcome_screen_index == self.bet_index and controller.isAPressedSwitch :
            state.controller.isAPressedSwitch = False

            self.game_state = self.BET_SCREEN
        elif self.welcome_screen_index == self.quit_index and controller.isAPressedSwitch :
            state.controller.isAPressedSwitch = False
            self.reset_coin_flip_game()

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
        arrow_y_coordinate_padding_bet = 92
        arrow_y_coordinate_padding_quit = 132

        for idx, choice in enumerate(self.welcome_screen_choices):
            y_position = start_y_right_box + idx * spacing_between_choices  # Adjust spacing between choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        if Magic.HEADS_FORCE.value not in state.player.magicinventory and Magic.SHIELD.value not in state.player.magicinventory:
            self.magic_lock = True
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif Magic.HEADS_FORCE.value in state.player.magicinventory or Magic.SHIELD.value in state.player.magicinventory:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if Magic.HEADS_FORCE.value in state.player.magicinventory and Magic.HEADS_FORCE.value not in self.magic_menu_selector:
            self.magic_menu_selector.append(Magic.HEADS_FORCE.value)
        if Magic.SHIELD.value in state.player.magicinventory and Magic.SHIELD.value not in self.magic_menu_selector:
            self.magic_menu_selector.append(Magic.SHIELD.value)

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
        elif self.welcome_screen_index == self.welcome_screen_bet_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_bet)
            )
        elif self.welcome_screen_index == self.welcome_screen_quit_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_quit)
            )

    def draw_flip_coin(self, state: 'GameState'):
        # List of predefined x-positions for each coin in the sprite sheet
        x_positions = [85, 235, 380, 525, 670, 815, 960, 1108, 1250, 1394]
        y_position = 110  # Fixed y-coordinate for all coins in the sprite sheet
        width, height = 170, 190  # Size of each coin in the sprite sheet

        # Parameters for the animation
        time_interval = 50  # Time interval in milliseconds for changing images
        fall_speed = 4.5  # Fall speed in pixels per time interval
        max_height = 250  # Maximum height the coin goes up (in pixels)
        drop_height = 175  # Maximum height the coin falls down (in pixels)

        # Start timer if not started
        if self.timer_start is None:
            self.timer_start = pygame.time.get_ticks()

        # Determine which coin to display based on time
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.timer_start
        current_coin_index = (elapsed_time // time_interval) % len(x_positions)

        # Define the rectangle for the current coin in the sprite sheet
        subsurface_rect = pygame.Rect(x_positions[current_coin_index], y_position, width, height)

        # Get the subsurface from the sprite sheet
        sprite = self.sprite_sheet.subsurface(subsurface_rect)

        # Calculate the y position as the coin falls (first upwards, then downwards)
        cycle_time = (2 * max_height // fall_speed) + (2 * drop_height // fall_speed)
        cycle_position = (elapsed_time // time_interval) % cycle_time

        if cycle_position < (max_height // fall_speed):
            # Moving upwards (decreasing y value)
            fall_distance = fall_speed * cycle_position
            coin_image_position = (self.initial_coin_image_position[0], self.initial_coin_image_position[1] - fall_distance)

        elif cycle_position < (max_height // fall_speed) + (drop_height // fall_speed):
            # Moving downwards (increasing y value)
            fall_distance = fall_speed * (cycle_position - (max_height // fall_speed))
            coin_image_position = (self.initial_coin_image_position[0], self.initial_coin_image_position[1] - max_height + fall_distance)

        else:
            # Reaching the bottom and stopping
            fall_distance = fall_speed * (cycle_position - (max_height // fall_speed) - (drop_height // fall_speed))
            coin_image_position = (self.initial_coin_image_position[0], self.initial_coin_image_position[1] - max_height + drop_height - fall_distance)

        # If the animation has reached the end of the cycle, reset for the next iteration
        if elapsed_time >= 4000:  # Check if 4 seconds have passed
            # Reset for next iteration
            self.timer_start = None
            self.coin_bottom = True
            self.initial_coin_image_position = (300, 250)  # Reset initial position

        # Blit (draw) the subsurface (the selected coin) onto the display surface
        state.DISPLAY.blit(sprite, coin_image_position)

    def update_flip_coin(self, controller):


        if self.weighted_coin == True:
            self.balance_modifier += 25
            self.coin_landed = CoinFlipConstants.HEADS.value
        coin_fate = random.randint(1, 100) + self.balance_modifier
        if coin_fate >= 51:
            self.balance_modifier -= 15
            if coin_fate >= 100:
                self.balance_modifier -= 20
            self.coin_landed = CoinFlipConstants.HEADS.value
        elif coin_fate <= 50:
            self.balance_modifier += 15
            if coin_fate <= 0:
                self.balance_modifier += 5
            self.coin_landed = CoinFlipConstants.TAILS.value
        print("Your coin fate is: " + str(coin_fate))
        print("Your blanace modifer is: " + str(self.balance_modifier))



        self.result_anchor = False


    def bet_screen_helper(self,state,  controller):


        if controller.isBPressed or controller.isBPressedSwitch:
            controller.isBPressed = False
            controller.isBPressedSwitch = False
            self.game_state = self.WELCOME_SCREEN
        min_bet = 50
        if Equipment.COIN_FLIP_GLOVES.value in state.player.equipped_items:
            max_bet = 400
        else:
            max_bet = 200

        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet += min_bet
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False

            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet -= min_bet



        if self.bet <= min_bet:
            self.bet = min_bet
        elif self.bet >= max_bet:
            self.bet = max_bet
        print(max_bet)



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

        if self.heads_force_active == True:
            state.DISPLAY.blit(self.font.render(f"Force: 1", True, RED), (player_enemy_box_info_x_position, enemy_name_y_position))
        elif self.shield_debuff == self.shield_debuff_inactive:
            state.DISPLAY.blit(self.font.render(self.dealer_name, True, WHITE), (player_enemy_box_info_x_position, enemy_name_y_position))
        elif self.shield_debuff > self.shield_debuff_inactive:
            state.DISPLAY.blit(self.font.render(f"Shield: {self.shield_debuff}", True, RED), (player_enemy_box_info_x_position, enemy_name_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}", True, WHITE), (player_enemy_box_info_x_position, enemy_money_y_position))
        state.DISPLAY.blit(self.font.render(f" Phase: {self.phase}", True, WHITE), (player_enemy_box_info_x_position - 7, phase_y_position))
        state.DISPLAY.blit(self.font.render(f" Choice: {self.player_choice}", True, WHITE), (player_enemy_box_info_x_position - 7, choice_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE), (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE), (player_enemy_box_info_x_position, player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE), (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE), (player_enemy_box_info_x_position, hero_focus_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.HERO_HEADER}", True, WHITE), (player_enemy_box_info_x_position, hero_name_y_position))








