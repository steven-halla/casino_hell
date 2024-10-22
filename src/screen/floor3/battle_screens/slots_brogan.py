import random
from typing import Dict, Tuple, List, Optional

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

        # Create a list of image keys to maintain order






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
        # Create reel surfaces
        self.reel_surfaces: List[pygame.Surface] = []
        for _ in range(3):  # Three reels
            reel_surface = self.create_reel_surface()
            self.reel_surfaces.append(reel_surface)

        # Reel positions to control vertical movement
        self.reel_positions: List[float] = [0.0, 0.0, 0.0]

        # Spinning state
        self.spinning: bool = False
        self.initial_spin_speed: float = 400.0  # Starting spin speed in pixels per second
        self.spin_start_time: Optional[int] = None  # Time when spinning started

        self.last_update_time: int = pygame.time.get_ticks()
        # self.spin_speed_decrement: float = 100.0  # Decrease spin speed by this amount every second

        # Initialize spinning states for each reel
        self.reel_spinning: List[bool] = [False, False, False]  # All reels start not spinning

        # Initialize stop times for each reel
        self.reel_stop_times: List[Optional[int]] = [None, None, None]  # Stop times are not set yet

        # Set the spin speed (assuming a constant speed)
        self.spin_speed: float = 400.0  # Pixels per second

    SPIN_SCREEN: str = "spin_screen"
    RESULT_SCREEN: str = "result_screen"
    BACK: str = "Back"

    def create_reel_surface(self) -> pygame.Surface:
        # Randomize the order of images for the reel
        image_keys = self.slot_image_keys.copy()
        random.shuffle(image_keys)

        # Calculate the total height of the reel surface
        box_width, box_height = 80, 80  # Same as in draw_grid_box
        reel_height = box_height * len(image_keys)

        # Create the reel surface
        reel_surface = pygame.Surface((box_width, reel_height)).convert_alpha()
        reel_surface.fill((0, 0, 0, 0))  # Transparent background

        # Blit each image onto the reel surface
        for idx, key in enumerate(image_keys):
            image = self.slot_images[key]
            resized_image = pygame.transform.scale(image, (box_width, box_height))
            reel_surface.blit(resized_image, (0, idx * box_height))

        return reel_surface

    def start(self, state: 'GameState'):
        pass

    def reset_slots_game(self):
        pass
    def reset_slots_round(self):
        pass

    def update(self, state):
        super().update(state)
        controller = state.controller
        controller.update()
        state.player.update(state)

        # Get current time once at the beginning
        current_time = pygame.time.get_ticks()

        # Handle input to start spinning
        if controller.isTPressed:
            controller.isTPressed = False
            if not any(self.reel_spinning):
                # Start spinning all reels
                self.reel_spinning = [True, True, True]
                current_time = pygame.time.get_ticks()
                self.spin_start_time = current_time  # Record the time when spinning started
                self.last_update_time = current_time  # Reset last update time

                # Set stop times for each reel
                self.reel_stop_times = [
                    current_time + 3000,  # Reel 0 stops after 3 seconds
                    current_time + 4000,  # Reel 1 stops after 4 seconds
                    current_time + 5000  # Reel 2 stops after 5 seconds
                ]

        # Update spin speed
        # if self.spinning:
        #     elapsed_time = (current_time - self.spin_start_time) / 1000.0  # In seconds
        #     # Decrease spin speed over time
        #     self.spin_speed = max(0.0, self.initial_spin_speed - self.spin_speed_decrement * elapsed_time)
        #     if self.spin_speed == 0.0:
        #         self.spinning = False  # Stop spinning when speed reaches zero

        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_update_time) / 1000.0  # Convert milliseconds to seconds
        self.last_update_time = current_time

        # Update reel positions and check for stopping
        for i in range(3):  # For each reel
            if self.reel_spinning[i]:
                # Update the reel's position
                self.reel_positions[i] -= self.spin_speed * delta_time
                reel_height = self.reel_surfaces[i].get_height()
                self.reel_positions[i] %= reel_height

                # Check if it's time to stop this reel
                if current_time >= self.reel_stop_times[i]:
                    self.reel_spinning[i] = False  # Stop the reel

        # Other game state updates...
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
        # Update overall spinning state
        self.spinning = any(self.reel_spinning)

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
        box_width, box_height = 80, 80
        line_thickness = 2
        grid_columns = 3
        images_to_show = 3  # Number of boxes vertically to display

        total_grid_width = box_width * grid_columns + line_thickness * (grid_columns - 1)
        total_grid_height = box_height * images_to_show + line_thickness * (images_to_show - 1)

        start_x = (screen_width - total_grid_width) // 2
        start_y = (screen_height - total_grid_height) // 2

        for i in range(3):  # For each reel
            reel_surface = self.reel_surfaces[i]
            reel_height = reel_surface.get_height()

            # Calculate the area of the reel to display
            reel_y_pos = self.reel_positions[i] % reel_height
            rect = pygame.Rect(0, reel_y_pos, box_width, box_height * images_to_show)

            # If the rect goes beyond the reel height, we need to stitch the images
            if reel_y_pos + box_height * images_to_show > reel_height:
                upper_part_height = reel_height - reel_y_pos
                lower_part_height = (box_height * images_to_show) - upper_part_height

                upper_part = reel_surface.subsurface(pygame.Rect(0, reel_y_pos, box_width, upper_part_height))
                lower_part = reel_surface.subsurface(pygame.Rect(0, 0, box_width, lower_part_height))

                combined_surface = pygame.Surface((box_width, box_height * images_to_show)).convert_alpha()
                combined_surface.blit(upper_part, (0, 0))
                combined_surface.blit(lower_part, (0, upper_part_height))
            else:
                combined_surface = reel_surface.subsurface(rect)

            # Blit the combined surface onto the screen
            box_x = start_x + i * (box_width + line_thickness)
            box_y = start_y

            state.DISPLAY.blit(combined_surface, (box_x, box_y))

            # Draw the white lines around the boxes
            for j in range(images_to_show):
                rect_x = box_x
                rect_y = box_y + j * (box_height + line_thickness)
                pygame.draw.rect(state.DISPLAY, (255, 255, 255), (rect_x, rect_y, box_width, box_height), line_thickness)

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

    def update_reels(self):
        for i in range(3):
            self.reel_positions[i] = (self.reel_positions[i] + 1) % len(self.slot_image_keys)


















