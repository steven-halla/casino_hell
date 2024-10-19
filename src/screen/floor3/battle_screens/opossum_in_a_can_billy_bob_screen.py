import pygame

from constants import WHITE
from entity.gui.screen.gamble_screen import GambleScreen
from game_constants.magic import Magic


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
        self.magic_lock:bool = False
        self.welcome_screen_choices: list[str] = ["Play", "Magic",  "Quit"]
        self.magic_menu_selector: list[str] = []





    PICK_SCREEN = "pick_screen"

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

    def draw(self, state):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)

        if self.game_state == self.WELCOME_SCREEN:

            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)

            # self.battle_messages[self.WELCOME_MESSAGE].draw(state)

        pygame.display.flip()

    def update_welcome_screen_logic(self, controller, state):
        if controller.isTPressed:
            controller.isTPressed = False

            if self.welcome_screen_index == self.pick_index:
                self.game_state = self.PICK_SCREEN
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




