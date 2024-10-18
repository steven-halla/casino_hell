import random

import pygame

from constants import WHITE, BLACK
from entity.gui.screen.gamble_screen import GambleScreen
from game_constants.coin_flip_constants import CoinFlipConstants
from game_constants.events import Events
from game_constants.magic import Magic


class CoinFlipDexterScreen(GambleScreen):
    # I believe in the yin yang of coin flip, balance is needed in all things
    # our money is not in balance let me correct that:
    # Greediest of all the pigs of filth, share your horde with the poor and down trodden of the world...money balancer
    def __init__(self, screenName: str = "Coin FLip") -> None:
        super().__init__(screenName)
        self.bet:int = 100
        self.sprite_sheet = pygame.image.load("./assets/images/coin_flipping_alpha.png").convert_alpha()
        self.game_state: str = self.WELCOME_SCREEN
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.heads_or_tails_menu: list[str] = ["Heads", "Tails", "Back"]
        self.magic_menu_selector: list[str] = []
        self.welcome_screen_index: int = 0
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.phase: int = 1
        self.flip_coin_index: int = 0
        self.magic_index: int = 1
        self.bet_index: int = 2
        self.quit_index: int = 3
        self.headstailsindex: int = 0
        self.heads_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/heads.png")
        self.tails_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/tails.png")

        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)
        self.weighted_coin: bool = False  # this is our magic spell heads force
        self.balance_modifier: int = 0
        self.player_choice = CoinFlipConstants.HEADS.value
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
        self.result_anchor = False

    COIN_FLIP_SCREEN: str = "coin_flip_screen"
    BACK: str = "Back"
    RESULTS_SCREEN: str = "results_screen"
    CHOOSE_SIDE_SCREEN: str = "choose_side_screen"


    def reset_coin_flip_game(self):
        self.phase = 1
        self.balance_modifier: int = 0
        self.welcome_screen_index = 0
        self.shield_debuff = 0
        self.heads_force_active = False
        self.coin_bottom = False
        self.result_anchor = False

        self.weighted_coin = False




    def reset_round(self):
        self.weighted_coin = False
        self.heads_force_active = False
        self.coin_bottom = False
        self.result_anchor = False


        self.phase += 1
        if self.phase == 6:
            self.phase = 1
        if self.phase == 1:
            self.balance_modifier = 0
        if self.shield_debuff > 0:
            self.shield_debuff -= 1




    def update(self, state):
        super().update(state)
        controller = state.controller
        controller.update()
        state.player.update(state)
        if self.money <= self.dexter_bankrupt:
            Events.add_event_to_player(state.player, Events.COIN_FLIP_DEXTER_DEFEATED)


        if self.game_state == self.WELCOME_SCREEN:
            self.update_welcome_screen_logic(controller, state)

        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu_selection_box(controller, state)
        elif self.game_state == self.CHOOSE_SIDE_SCREEN:
            self.update_choose_side_logic(controller, state)

        elif self.game_state == self.COIN_FLIP_SCREEN:
            self.result_anchor = True
            if self.coin_bottom == True:
                self.game_state = self.RESULTS_SCREEN
        elif self.game_state == self.RESULTS_SCREEN:
            if controller.isTPressed:
                controller.isTPressed = False
                self.game_state = self.WELCOME_SCREEN
            if self.result_anchor == True:
                self.update_flip_coin()


    def draw(self, state: 'GameState'):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)
        elif self.game_state == self.CHOOSE_SIDE_SCREEN:
            self.draw_choose_side_logic(state)

        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box(state)

        elif self.game_state == self.COIN_FLIP_SCREEN:
            self.draw_flip_coin(state)

        elif self.game_state == self.RESULTS_SCREEN:
            self.draw_results_screen_logic(state)


        pygame.display.flip()

    def update_choose_side_logic(self, controller, state):
        if controller.isUpPressed:
            print(self.headstailsindex)
            controller.isUpPressed = False
            self.menu_movement_sound.play()
            self.headstailsindex = (self.headstailsindex - self.index_stepper) % len(self.heads_or_tails_menu)
        elif controller.isDownPressed:
            controller.isDownPressed = False
            self.menu_movement_sound.play()
            self.headstailsindex = (self.headstailsindex + self.index_stepper) % len(self.heads_or_tails_menu)

        if controller.isTPressed:
            controller.isTPressed = False
            if self.headstailsindex == 0:
                self.player_choice = CoinFlipConstants.HEADS.value
            elif self.headstailsindex == 1:
                self.player_choice = CoinFlipConstants.TAILS.value
            elif self.headstailsindex == 2:
                self.headstailsindex = 0
                self.game_state = self.WELCOME_SCREEN


    def draw_choose_side_logic(self, state):
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
        image_to_display = (
            self.heads_image
            if self.coin_landed == CoinFlipConstants.HEADS.value
            else self.tails_image
        )

        image_rect = image_to_display.get_rect()
        image_rect.center = (state.DISPLAY.get_width() // 2, state.DISPLAY.get_height() // 2)
        state.DISPLAY.blit(image_to_display, image_rect)

    def update_magic_menu_selection_box(self, controller, state):

        if controller.isUpPressed:
            controller.isUpPressed = False
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index - self.index_stepper) % len(self.magic_menu_selector)
            print(f"Current Magic Menu Selector: {self.magic_menu_selector[self.magic_screen_index]}")
        elif controller.isDownPressed:
            controller.isDownPressed = False
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index + self.index_stepper) % len(self.magic_menu_selector)
            print(f"Current Magic Menu Selector: {self.magic_menu_selector[self.magic_screen_index]}")

        if controller.isTPressed:
            controller.isTPressed = False
            if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value and state.player.focus_points >= self.shield_cost:
                state.player.focus_points -= self.shield_cost
                self.shield_debuff = 3
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
        if controller.isTPressed:
            controller.isTPressed = False

            if self.welcome_screen_index == self.flip_coin_index:
                state.player.stamina_points -= self.low_stamina_drain
                self.game_state = self.CHOOSE_SIDE_SCREEN
            elif self.welcome_screen_index == self.magic_index and self.magic_lock == False:
                self.game_state = self.MAGIC_MENU_SCREEN
            elif self.welcome_screen_index == self.bet_index:
                self.game_state = self.BET_SCREEN
            elif self.welcome_screen_index == self.quit_index:
                print("we'll work on this later")


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

        # Fixed position to draw the coin on the screen
        initial_coin_image_position = (300, -80)  # Starting position on the screen for the coin

        # List of predefined x-positions for each coin in the sprite sheet
        x_positions = [85, 235, 380, 525, 670, 815, 960, 1108, 1250, 1394]
        y_position = 110  # Fixed y-coordinate for all coins in the sprite sheet
        width, height = 170, 190  # Size of each coin in the sprite sheet

        # Parameters for the animation
        time_interval = 50  # Time interval in milliseconds for changing images
        fall_speed = 3 # Fall speed in pixels per time interval

        # Determine which coin to display based on time
        current_time = pygame.time.get_ticks()
        current_coin_index = (current_time // time_interval) % len(x_positions)

        # Define the rectangle for the current coin in the sprite sheet
        subsurface_rect = pygame.Rect(x_positions[current_coin_index], y_position, width, height)

        # Get the subsurface from the sprite sheet
        sprite = self.sprite_sheet.subsurface(subsurface_rect)

        # Calculate the y position as the coin falls
        fall_distance = min(fall_speed * (current_time // time_interval), 300)  # Fall up to a maximum of 100 pixels
        coin_image_position = (initial_coin_image_position[0], initial_coin_image_position[1] + fall_distance)

        if fall_distance >= 300:
            print("Coin has reached the bottom of its fall")
            self.coin_bottom = True


        # Blit (draw) the subsurface (the selected coin) onto the display surface at a calculated position
        state.DISPLAY.blit(sprite, coin_image_position)

    def update_flip_coin(self):

        if self.weighted_coin == True:
            self.balance_modifier += 15
            self.coin_landed = CoinFlipConstants.HEADS.value
        coin_fate = random.randint(1, 100) + self.balance_modifier
        if coin_fate >= 51:
            self.balance_modifier += 15
            if self.balance_modifier >= 85:
                self.balance_modifier -= 125
            self.coin_landed = CoinFlipConstants.HEADS.value
        elif coin_fate <= 50:
            self.balance_modifier -= 15
            if self.balance_modifier <= 15:
                self.balance_modifier += 125
            self.coin_landed = CoinFlipConstants.TAILS.value



        self.result_anchor = False
        return








