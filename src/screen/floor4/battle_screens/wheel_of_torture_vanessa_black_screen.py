from pygame import surface

from constants import BLACK, RED
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from entity.npc.npc import Npc
import pygame
from game_constants.events import Events




class WheelOfTortureVanessaBlackScreen(GambleScreen):
    def __init__(self, screenName: str = "wheel of torturett"):
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.money_pile: int = 0
        self.exp_pile: int = 0
        self.money: int = 2000
        self.vanessa_black_bankrupt: int = 0
        self.magic_lock: bool = False
        self.dealer_name: str = "vanessa black"
        self.magic_screen_choices: list[str] = ["back"]
        self.magic_menu_index: int = 0
        self.spirit_bonus: int = 0
        self.magic_bonus: int = 0

        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_SCREEN: MessageBox([
                "Vanessea Black: this is the welcome screen"
            ]),
            self.BET_MESSAGE: MessageBox([
                "Min bet of 50, max of 200. Press up and down keys to increase/decrease bet. Press B to Exit."
            ]),
        }

    BET_MESSAGE: str = "bet_message"

    def start(self, state):
        self.spirit_bonus: int = state.player.spirit * 10
        self.magic_bonus: int = state.player.mind * 10

    def round_reset(self):
        self.money_pile = 0
        self.exp_pile = 0

    def update(self, state):
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        if self.money <= self.vanessa_black_bankrupt:
            state.currentScreen = state.area4RestScreen
            state.area4RestScreen.start(state)
            Events.add_level_four_event_to_player(state.player, Events.WHEEL_OF_TORTURE_VANESSA_BLACK_DEFEATED)

        if self.game_state == self.WELCOME_SCREEN:
            pass

    def draw(self, state):
        super().draw(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.draw_board(state)


        pygame.display.flip()

    def draw_board(self, state) -> None:
        """Draws a simple board of 30 black squares from left to right.

        Each square is 30x30 pixels with 20 pixels of padding between them.
        """
        x_start = 30  # Starting x position
        y_position = 100  # Fixed y position for all squares
        y_position_2 = 150  # Fixed y position for all squares
        box_height: int = 30
        box_width: int = 30
        border_thickness: int = 2
        x_padding: int = 50

        for i in range(15):
            x_position = x_start + i * (x_padding)
            pygame.draw.rect(state.DISPLAY, RED, (x_position, y_position, box_height, box_width), border_thickness)

        for i in range(15):
            x_position = x_start + i * (x_padding)
            pygame.draw.rect(state.DISPLAY, RED, (x_position, y_position_2, box_height, box_width), border_thickness)













