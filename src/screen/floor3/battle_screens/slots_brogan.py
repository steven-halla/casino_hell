from typing import Dict, Tuple, List

import pygame

from constants import WHITE, BLACK
from entity.gui.screen.gamble_screen import GambleScreen
from game_constants.magic import Magic


class SlotsBrogan(GambleScreen):
    def __init__(self, screenName: str = "Slots") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.dealer_name: str = "Brogan"
        self.slot_images_sprite_sheet: pygame.Surface = pygame.image.load("./assets/images/slots_images_trans.png")

        self.spell_sound: pygame.mixer.Sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.magic_screen_choices: list[str] = []
        self.hack_cost = 75
        self.money: int = 1000
        self.slot_hack_active: int = 5
        self.slot_hack_inactive: int = 0


        self.bet_screen_choices: list[str] = ["Back"]
        self.spin_screen_index: int = 0
        self.magic_screen_index: int = 1
        self.bet_screen_index: int = 2
        self.quit_index: int = 3
        self.magic_index = 0
        pygame.mixer.music.stop()
        self.magic_lock: bool = False
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        self.brogan_bankrupt: int = 0
        self.player_stamina_med_cost: int = 5
        self.player_stamina_high_cost: int = 10  # useing higher bet option
        self.lock_down_inactive: int = 0
        self.index_stepper = 1

        self.slot_images: Dict[str, pygame.Surface] = {
            "bomb": self.slot_images_sprite_sheet.subsurface(pygame.Rect(450, 100, 50, 52)),
            "lucky_seven": self.slot_images_sprite_sheet.subsurface(pygame.Rect(300, 30, 60, 60)),
            "dice": self.slot_images_sprite_sheet.subsurface(pygame.Rect(350, 100, 50, 52)),
            "coin": self.slot_images_sprite_sheet.subsurface(pygame.Rect(20, 30, 75, 52)),
            "diamond": self.slot_images_sprite_sheet.subsurface(pygame.Rect(20, 170, 75, 52)),
            "crown": self.slot_images_sprite_sheet.subsurface(pygame.Rect(15, 275, 80, 52)),
            "chest": self.slot_images_sprite_sheet.subsurface(pygame.Rect(300, 275, 75, 58)),
            "cherry": self.slot_images_sprite_sheet.subsurface(pygame.Rect(120, 210, 75, 58)),
            "dice_six": self.slot_images_sprite_sheet.subsurface(pygame.Rect(400, 210, 50, 58)),
            "spin": self.slot_images_sprite_sheet.subsurface(pygame.Rect(40, 110, 52, 58)),
        }

        self.slot_image_keys: List[str] = list(self.slot_images.keys())

        # Initialize your slot positions and values
        self.slot_positions1: List[int] = [-50, 0, 50]
        self.slot_positions2: List[int] = [-50, 0, 50]
        self.slot_positions3: List[int] = [-50, 0, 50]
        self.slot1: List[int] = [0, 0, 0]
        self.slot2: List[int] = [0, 0, 0]
        self.slot3: List[int] = [0, 0, 0]
        self.grid_positions: List[Tuple[int, int]] = []

    SPIN_SCREEN: str = "spin_screen"
    RESULT_SCREEN: str = "result_screen"
    BACK: str = "Back"

    def start(self, state: 'GameState'):
        pass

    def reset_slots_game(self):
        pass
    def reset_slots_round(self):
        pass

    def update(self,  state):
        # print(self.game_state)
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.update_welcome_screen_logic(controller)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu_selection_box(controller, state)

        elif self.game_state == self.BET_SCREEN:
            self.bet_screen_helper(controller)

        elif self.game_state == self.SPIN_SCREEN:
            pass
        elif self.game_state == self.RESULT_SCREEN:
            pass
        elif self.game_state == self.GAME_OVER_SCREEN:
            no_money_game_over = 0
            no_stamina_game_over = 0

            if state.player.money <= no_money_game_over:
                if controller.isTPressed:
                    controller.isTPressed = False
                    state.currentScreen = state.gameOverScreen
                    state.gameOverScreen.start(state)
            elif state.player.stamina_points <= no_stamina_game_over:
                if controller.isTPressed:
                    controller.isTPressed = False
                    self.reset_slots_game()
                    state.player.money -= 100
                    # state.currentScreen = state.area3RestScreen
                    # state.area3RestScreen.start(state)


    def draw(self, state):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)

        self.draw_grid_box(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)



        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box(state)
        elif self.game_state == self.BET_SCREEN:
            pass
        elif self.game_state == self.SPIN_SCREEN:
            pass
        elif self.game_state == self.RESULT_SCREEN:
            pass
        elif self.game_state == self.GAME_OVER_SCREEN:
            no_money_game_over = 0
            no_stamina_game_over = 0
            if state.player.money <= no_money_game_over:
                state.DISPLAY.blit(self.font.render(f"You ran out of money and are now a prisoner of hell", True, WHITE), (self.blit_message_x, self.blit_message_y))
            elif state.player.stamina <= no_stamina_game_over:
                state.DISPLAY.blit(self.font.render(f"You ran out of stamina , you lose -100 gold", True, WHITE), (self.blit_message_x, self.blit_message_y))


        # Set the coordinates for the sprite

        # self.draw_slot_images(state)


        pygame.display.flip()

    def draw_grid_box(self, state: "GameState") -> None:
        screen_width, screen_height = state.DISPLAY.get_size()
        box_width, box_height = 80, 80  # Adjust box size to fit images
        line_thickness = 2
        grid_columns = 3  # 3 columns as per your requirement
        grid_rows = len(self.slot_images)  # 10 rows for each image

        total_grid_width = box_width * grid_columns + line_thickness * (grid_columns - 1)
        total_grid_height = box_height * grid_rows + line_thickness * (grid_rows - 1)

        start_x = (screen_width - total_grid_width) // 2
        start_y = (screen_height - total_grid_height) // 2

        black_color = (0, 0, 0)
        white_color = (255, 255, 255)

        # Iterate over the grid positions
        for row, key in enumerate(self.slot_image_keys):
            for col in range(grid_columns):
                image = self.slot_images[key]
                box_x = start_x + col * (box_width + line_thickness)
                box_y = start_y + row * (box_height + line_thickness)

                # Draw the box
                pygame.draw.rect(state.DISPLAY, black_color, (box_x, box_y, box_width, box_height))

                # Resize the image to fit the box if necessary
                resized_image = pygame.transform.scale(image, (box_width, box_height))

                # Blit the image onto the box
                state.DISPLAY.blit(resized_image, (box_x, box_y))

                # Draw the white lines around the box
                pygame.draw.rect(state.DISPLAY, white_color, (box_x, box_y, box_width, box_height), line_thickness)

        # Draw vertical grid lines
        for j in range(grid_columns + 1):
            x = start_x + j * (box_width + line_thickness) - line_thickness // 2
            x = int(x)
            pygame.draw.line(
                state.DISPLAY,
                white_color,
                (x, start_y),
                (x, start_y + total_grid_height - line_thickness),
                line_thickness
            )

        # Draw horizontal grid lines
        for i in range(grid_rows + 1):
            y = start_y + i * (box_height + line_thickness) - line_thickness // 2
            y = int(y)
            pygame.draw.line(
                state.DISPLAY,
                white_color,
                (start_x, y),
                (start_x + total_grid_width - line_thickness, y),
                line_thickness
            )

    def draw_magic_menu_selection_box(self, state):
        if self.magic_screen_choices[self.magic_screen_index] == Magic.SLOTS_HACK.value:
            # self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].draw(state)
            pass





        elif self.magic_screen_choices[self.magic_screen_index] == self.BACK:
            pass
            # self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)

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

        for idx, choice in enumerate(self.magic_screen_choices):
            y_position = start_y_right_box + idx * choice_spacing  # Use the defined spacing variable
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        # Draw the arrow at the current magic screen index position
        arrow_y_position = start_y_right_box + (self.magic_index * choice_spacing) + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_position)  # Use the arrow offsets
        )

    def update_magic_menu_selection_box(self, controller, state):
        if self.magic_screen_choices[self.magic_index] == Magic.SLOTS_HACK.value:
            pass
            # self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].update(state)
            #
            # self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].reset()
            # self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()

        elif self.magic_screen_choices[self.magic_index] == self.BACK:
            pass
            # self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)
            #
            # self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].reset()
            # self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].reset()

        if controller.isUpPressed:
            controller.isUpPressed = False
            self.menu_movement_sound.play()
            self.magic_index = (self.magic_index - self.index_stepper) % len(self.magic_screen_choices)
            print(f"Current Magic Menu Selector: {self.magic_screen_choices[self.magic_screen_index]}")
        elif controller.isDownPressed:
            controller.isDownPressed = False
            self.menu_movement_sound.play()
            self.magic_index = (self.magic_index + self.index_stepper) % len(self.magic_screen_choices)
            print(f"Current Magic Menu Selector: {self.magic_screen_choices[self.magic_screen_index]}")

        if controller.isTPressed:
            controller.isTPressed = False
            if self.magic_screen_choices[self.magic_index] == Magic.SLOTS_HACK.value and state.player.focus_points >= self.hack_cost:
                print("yes")
                state.player.focus_points -= self.hack_cost
                self.slot_hack_active = 5
                self.spell_sound.play()  # Play the sound effect once
                self.magic_lock = True
                self.game_state = self.WELCOME_SCREEN
                print(self.slot_hack_active)

            elif self.magic_screen_choices[self.magic_index] == self.BACK:
                self.magic_index = 0
                self.game_state = self.WELCOME_SCREEN


    def bet_screen_helper(self, controller):
        if controller.isBPressed:
            controller.isBPressed = False
            self.game_state = self.WELCOME_SCREEN
        min_bet = 50
        bet_step = 25
        max_bet = 100
        if controller.isUpPressed:
            controller.isUpPressed = False
            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet += bet_step
        elif controller.isDownPressed:
            controller.isDownPressed = False

            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet -= bet_step

        if self.bet <= min_bet:
            self.bet = min_bet
        elif self.bet >= max_bet:
            self.bet = max_bet

    def update_welcome_screen_logic(self, controller):
        if controller.isTPressed:
            controller.isTPressed = False
            if self.welcome_screen_index == self.spin_screen_index:
                self.game_state = self.SPIN_SCREEN
            elif self.welcome_screen_index == self.magic_screen_index and self.magic_lock == False:
                self.game_state = self.MAGIC_MENU_SCREEN
            elif self.welcome_screen_index == self.bet_screen_index:
                self.game_state = self.BET_SCREEN
            elif self.welcome_screen_index == self.quit_index:
                print("this will come later")


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

        if Magic.SLOTS_HACK.value not in state.player.magicinventory:
            self.magic_lock = True
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif Magic.SLOTS_HACK.value in state.player.magicinventory:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if Magic.SLOTS_HACK.value in state.player.magicinventory and Magic.SLOTS_HACK.value not in self.magic_screen_choices:
            self.magic_screen_choices.append(Magic.SLOTS_HACK.value)


        if self.BACK not in self.magic_screen_choices:
            self.magic_screen_choices.append(self.BACK)

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

    def draw_slot_images(self, state):
        sprite_data = {
            "bomb": ((10, 20), (450, 100, 50, 52)),
            "lucky_seven": ((100, 20), (300, 30, 60, 60)),
            "dice": ((181, 20), (350, 100, 50, 52)),
            "coin": ((240, 20), (20, 30, 75, 52)),
            "diamond": ((320, 20), (20, 170, 75, 52)),
            "crown": ((400, 20), (15, 275, 80, 52)),
            "chest": ((500, 20), (300, 275, 75, 58)),
            "cherry": ((20, 80), (120, 210, 75, 58)),
            "dice_6": ((120, 80), (400, 210, 50, 58)),
            "spin": ((200, 80), (40, 110, 52, 58)),
        }

        # Loop through the dictionary and blit each sprite
        for name, (blit_coords, sprite_rect) in sprite_data.items():
            sprite = self.slot_images_sprite_sheet.subsurface(pygame.Rect(*sprite_rect))
            state.DISPLAY.blit(sprite, blit_coords)

















