from typing import List

from pygame import surface
from typeguard import typechecked

from constants import BLACK, RED, PURPLE, GREEN
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from entity.npc.npc import Npc
import pygame
from game_constants.events import Events
import random




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
        self.move_player: int = 0
        self.move_dealer: int = 0
        self.player_position: int = 0
        self.enemy_position: int = 0
        self.board_squares: List[str] = []


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
            self.draw_enemy_token(state)
            self.draw_player_token(state)
        pygame.display.flip()

#============================================update methods go below

    @typechecked
    def update_square_effects(self) -> None:
        current_player_square = self.board_squares[self.player_position]
        current_enemy_square = self.board_squares[self.enemy_position]

    @typechecked
    def update_board(self) -> None:
        """Initializes the board as a list of 30 squares."""
        self.board_squares: list = [None] * 30


    @typechecked
    def update_roll_dice_player(self) -> None:
        self.move_player = random.randint(1, 6)


    @typechecked
    def update_roll_dice_dealer(self) -> None:
        self.move_dealer = random.randint(1, 6)




#_-----------------------------------draw methods go below

    @typechecked
    def draw_player_token(self, state) -> None:
        """Draws the player's token (PURPLE) in square 1."""
        token_size: int = 15
        x_start: int = 50
        y_position: int = 100
        padding_inside_square: int = 5

        token_x: int = x_start + padding_inside_square
        token_y: int = y_position + padding_inside_square

        pygame.draw.rect(state.DISPLAY, PURPLE, (token_x, token_y, token_size, token_size))

    @typechecked
    def draw_enemy_token(self, state) -> None:
        """Draws the enemy's token (GREEN) in square 1."""
        token_size: int = 15
        x_start: int = 45
        y_position: int = 95
        padding_inside_square: int = 35  # shifts token lower-right in the square

        token_x: int = x_start + padding_inside_square
        token_y: int = y_position + padding_inside_square

        pygame.draw.rect(state.DISPLAY, GREEN, (token_x, token_y, token_size, token_size))

    @typechecked
    def draw_board(self, state) -> None:
        x_start = 50
        y_position = 100
        y_position_2 = 200
        y_position_3 = 300
        box_height: int = 50
        box_width: int = 50
        border_thickness: int = 2
        x_padding: int = 70


        for i in range(10):
            x_position = x_start + i * x_padding
            pygame.draw.rect(state.DISPLAY, RED, (x_position, y_position, box_height, box_width), border_thickness)

        for i in range(10):
            x_position = x_start + i * x_padding
            pygame.draw.rect(state.DISPLAY, RED, (x_position, y_position_2, box_height, box_width), border_thickness)

        for i in range(10):
            x_position = x_start + i * x_padding
            pygame.draw.rect(state.DISPLAY, RED, (x_position, y_position_3, box_height, box_width), border_thickness)













