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
        self.pick_tally_screen_index = 0
        self.magic_lock:bool = False
        self.welcome_screen_choices: list[str] = ["Play", "Magic",  "Quit"]
        self.pick_screen_choices: list[str] = ["Pick", "Tally"]
        self.magic_menu_selector: list[str] = []
        self.index_stepper = 1


    PICK_TALLY_MENU_SCREEN:str = "pick_tally_menu_screen"
    PICK_SCREEN:str = "pick_screen"
    TALLY_SCREEN:str = "tally_screen"

    BACK: str = "Back"


    def start(self, state: 'GameState'):
        pass

    def opossum_game_reset(self):
        pass
    def opossum_round_reset(self):
        pass

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

        pygame.display.flip()

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




