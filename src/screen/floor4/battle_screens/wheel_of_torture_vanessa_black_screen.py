import math
from typing import List

from pygame import surface
from typeguard import typechecked

from constants import BLACK, RED, PURPLE, GREEN, WHITE
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
        self.enemy_token_position: int = 15
        self.player_token_position: int = 15


        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_SCREEN: MessageBox([
                "Vanessea Black: this is the welcome screen"
            ]),
            self.BET_MESSAGE: MessageBox([
                "Min bet of 50, max of 200. Press up and down keys to increase/decrease bet. Press B to Exit."
            ]),
        }

    BET_MESSAGE: str = "bet_message"
    SPIN_WHEEL_SCREEN: str = "spin wheel screen"

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
            if state.controller.confirm_button:
                self.update_roll_dice_player()
            elif state.controller.action_and_cancel_button:
                self.update_roll_dice_dealer()
        elif self.game_state == self.SPIN_WHEEL_SCREEN:
            pass

    def draw(self, state):
        super().draw(state)
        if self.game_state == self.WELCOME_SCREEN:
            self.draw_board(state)
            self.draw_enemy_token(state)
            self.draw_player_token(state)
        elif self.game_state == self.SPIN_WHEEL_SCREEN:
            self.draw_wheel(state)
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
        self.player_position += self.move_player
        if self.player_position > 29:
            self.player_position = 29  # cap at last square


    @typechecked
    def update_roll_dice_dealer(self) -> None:
        self.move_dealer = random.randint(1, 6)
        self.enemy_position += self.move_dealer
        if self.enemy_position > 29:
            self.enemy_position = 29

#_-----------------------------------draw methods go below

    @typechecked
    def draw_player_token(self, state) -> None:
        """Draws the player's token (PURPLE) based on their current board position."""
        token_size: int = 10
        padding_inside_square: int = 5
        x_start: int = 50
        y_start: int = 100
        x_padding: int = 70
        y_padding: int = 100
        squares_per_row: int = 10

        # Calculate row and column based on player_position
        row: int = self.player_position // squares_per_row
        col: int = self.player_position % squares_per_row

        token_x: int = x_start + col * x_padding + padding_inside_square
        token_y: int = y_start + row * y_padding + padding_inside_square

        pygame.draw.rect(state.DISPLAY, PURPLE, (token_x, token_y, token_size, token_size))

    @typechecked
    def draw_enemy_token(self, state) -> None:
        """Draws the enemy's token (GREEN) in square 1."""
        token_size: int = 10
        padding_inside_square: int = 5
        x_start: int = 65
        y_start: int = 125
        x_padding: int = 70
        y_padding: int = 100
        squares_per_row: int = 10

        row: int = self.enemy_position // squares_per_row
        col: int = self.enemy_position % squares_per_row

        token_x: int = x_start + col * x_padding + padding_inside_square
        token_y: int = y_start + row * y_padding + padding_inside_square

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

    @typechecked
    def draw_wheel(self, state) -> None:
        # in hell there is no slow down of wheel is stops aburptly
        center_x: int = 400
        center_y: int = 300
        radius: int = 150
        num_slices: int = 20
        spin_speed: float = 1.01
        max_frames: int = 180  # 3 seconds at 60 FPS

        if not hasattr(self, "_wheel_angle"):
            self._wheel_angle = 0.0
        if not hasattr(self, "_wheel_frame_count"):
            self._wheel_frame_count = 0
        if not hasattr(self, "_is_spinning"):
            self._is_spinning = False

        if state.controller.confirm_button and not self._is_spinning:
            self._is_spinning = True
            self._wheel_angle = 0.0
            self._wheel_frame_count = 0

        if self._is_spinning:
            self._wheel_angle += spin_speed
            self._wheel_frame_count += 1
            if self._wheel_frame_count >= max_frames:
                self._is_spinning = False

        # Draw green wheel
        pygame.draw.circle(state.DISPLAY, GREEN, (center_x, center_y), radius)

        # Draw white slices
        for i in range(num_slices):
            angle = (2 * math.pi / num_slices) * i + self._wheel_angle
            end_x = int(center_x + radius * math.cos(angle))
            end_y = int(center_y + radius * math.sin(angle))
            pygame.draw.line(state.DISPLAY, WHITE, (center_x, center_y), (end_x, end_y), 2)

    # @typechecked
    # def draw_wheel(self, state) -> None:
    #     """Draws a 300x300 green wheel with 20 white pie slice divisions."""
    #     center_x: int = 400  # You can position this wherever you want
    #     center_y: int = 300
    #     radius: int = 150
    #     num_slices: int = 20
    #
    #     # Draw the green circle
    #     pygame.draw.circle(state.DISPLAY, GREEN, (center_x, center_y), radius)
    #
    #     # Draw the white lines for pie slices
    #     for i in range(num_slices):
    #         angle: float = (2 * math.pi / num_slices) * i
    #         end_x: int = int(center_x + radius * math.cos(angle))
    #         end_y: int = int(center_y + radius * math.sin(angle))
    #         pygame.draw.line(state.DISPLAY, WHITE, (center_x, center_y), (end_x, end_y), 2)
    #
    #     if state.controller.confirm_button:
    #         spin wheel











