import random
from typing import List

import pygame

from constants import WHITE, BLACK
from entity.gui.screen.gamble_screen import GambleScreen
from game_constants.magic import Magic

# opssoum shuffle - reshuffles the cans


class OpossumInACanBillyBobScreen(GambleScreen):
    def __init__(self, screenName: str = "Opossum in a can Billy Bob") -> None:
        super().__init__(screenName)
        self.bet: int = 100
        self.game_state:str = self.WELCOME_SCREEN
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)
        self.stamina_drain:int = 50
        self.stamina_drain_repellant:int = 25
        self.pick_index:int = 0
        self.magic_index:int = 1
        self.quit_index:int = 2
        self.pick_screen_index = 0
        self.tally_index = 1
        self.debuff_keen_perception:bool = False

        self.pick_tally_screen_index:int = 0
        self.current_box_index:int = 0  # Index of the currently green box

        self.magic_lock:bool = False
        self.welcome_screen_choices: list[str] = ["Play", "Magic",  "Quit"]
        self.pick_screen_choices: list[str] = ["Pick", "Tally"]
        self.magic_menu_selector: list[str] = []
        self.index_stepper = 1
        self.trash_sprite_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/PC Computer - The Sims - Galvanized Trash Can (2).png").convert_alpha()
        self.hand_sprite_image = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/GameCube - Mario Party 4 - Character Hands (1).png").convert_alpha()
        self.winner_or_looser: List[str] = ["win", "win",
                                            "big win", "big win", "lose",
                                            "lucky_star",
                                            "X3_star", "lose",

                                            ]
        self.winner_or_looser_lucky: List[str] = ["win", "win",
                                                  "big win", "big win", "win",
                                                  "lucky_star",
                                                  "X3_star", "win",

                                                  ]
        self.result:str = ""

        self.can1:str = ""
        self.can2:str = ""
        self.can3:str = ""
        self.can4:str = ""
        self.can5:str = ""
        self.can6:str = ""
        self.can7:str = ""
        self.can8:str = ""
        self.shake:bool = False




    PICK_TALLY_MENU_SCREEN:str = "pick_tally_menu_screen"
    PICK_SCREEN:str = "pick_screen"
    TALLY_SCREEN:str = "tally_screen"

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
        self.initializeGarbageCans(state)


    def opossum_round_reset(self, state):
        self.shake = False
        self.initializeGarbageCans(state)


    def update(self, state):
        super().update(state)
        controller = state.controller
        controller.update()
        state.player.update(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.update_welcome_screen_logic(controller, state)
            # self.battle_messages[self.WELCOME_MESSAGE].update(state)
        elif self.game_state == self.PICK_TALLY_MENU_SCREEN:
            self.update_pick_tally_menu_screen_logic(controller)

            # self.battle_messages[self.PICK_MESSAGE].update(state)
        elif self.game_state == self.PICK_SCREEN:
            self.update_pick_screen(controller, state)

        elif self.game_state == self.TALLY_SCREEN:
            pass


    def draw(self, state):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)



        if self.game_state == self.WELCOME_SCREEN:

            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)

            # self.battle_messages[self.WELCOME_MESSAGE].draw(state)

        elif self.game_state == self.PICK_TALLY_MENU_SCREEN:
            self.draw_pick_tally_menu_logic(state)
            # self.battle_messages[self.PICK_MESSAGE].draw(state)

        elif self.game_state == self.PICK_SCREEN:
            self.draw_pick_screen(state)
        elif self.game_state == self.TALLY_SCREEN:
            self.draw_pick_screen(state)

        pygame.display.flip()

    def update_pick_screen(self, controller, state):
        time_since_right_pressed = state.controller.timeSinceKeyPressed(pygame.K_RIGHT)
        time_since_left_pressed = state.controller.timeSinceKeyPressed(pygame.K_LEFT)
        key_press_threshold = 80  # Example threshold, adjust as needed

        if state.controller.isRightPressed and time_since_right_pressed >= key_press_threshold:
            # Initially move to the next box
            self.current_box_index = (self.current_box_index + 1) % 8
            current_can_content = getattr(self, f'can{self.current_box_index + 1}')

            # Continue moving right if the can is empty
            while current_can_content == "":
                self.current_box_index = (self.current_box_index + 1) % 8
                current_can_content = getattr(self, f'can{self.current_box_index + 1}')

            self.menu_movement_sound.play()  # Play the sound effect once for the valid move
            print(f"Current green box index: {self.current_box_index}, Content: {current_can_content}")
            state.controller.keyPressedTimes[pygame.K_RIGHT] = pygame.time.get_ticks()

        elif state.controller.isLeftPressed and time_since_left_pressed >= key_press_threshold:
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

    def draw_pick_screen(self, state):
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
                x = col * (box_size + margin) + margin + 190
                y = row * (box_size + margin) + margin + 50
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
                if current_can_content:
                    state.DISPLAY.blit(scaled_sprite, (x, y))
        # hand sprite code
        hand_sprite_rect = pygame.Rect(1, 1, 58.5, 58)  # Update these values as needed
        hand_sprite = self.hand_sprite_image.subsurface(hand_sprite_rect)
        scaled_hand_sprite = pygame.transform.scale(hand_sprite, (33, 33))

        if 0 <= self.current_box_index < len(positions):
            hand_x, hand_y = positions[self.current_box_index]
            hand_y += 82  # 10 pixels below the top-left of the selected trash can
            hand_x += 54  # 10 pixels below the top-left of the selected trash can
            state.DISPLAY.blit(scaled_hand_sprite, (hand_x, hand_y))

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
        if controller.isTPressed:
            controller.isTPressed = False

            if self.pick_screen_index == self.pick_index:
                self.game_state = self.PICK_SCREEN
            elif self.pick_screen_index == self.tally_index:
                self.game_state = self.TALLY_SCREEN


        if controller.isUpPressed:
            controller.isUpPressed = False
            self.menu_movement_sound.play()
            self.pick_tally_screen_index = (self.pick_tally_screen_index - self.index_stepper) % len(self.pick_screen_choices)
        elif controller.isDownPressed:
            controller.isDownPressed = False
            self.menu_movement_sound.play()
            self.pick_tally_screen_index = (self.pick_tally_screen_index + self.index_stepper) % len(self.pick_screen_choices)


    def update_welcome_screen_logic(self, controller, state):
        if controller.isTPressed:
            controller.isTPressed = False

            if self.welcome_screen_index == self.pick_index:
                self.game_state = self.PICK_TALLY_MENU_SCREEN
            elif self.welcome_screen_index == self.magic_index and self.magic_lock == False:
                self.game_state = self.MAGIC_MENU_SCREEN
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

        elif self.welcome_screen_index == self.quit_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_quit)
            )




