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
        self.enemy_stat_boost = None
        self.player_stat_boost = None
        self.enemy_position_holder = None
        self.player_position_holder = None
        self.enemy_equipment_lock: bool= False
        self.game_state: str = self.PLAYER_TURN_SCREEN
        self.player_money_pile: int = 0
        self.enemy_money_pile: int = 0
        self.player_exp_pile: int = 0
        self.enemy_exp_pile: int = 0
        self.exp_pile: int = 0
        self.player_magic_lock: bool = False
        self.enemy_magic_lock: bool = False
        self.player_equipment_lock: bool = False
        self.enemy_equipment_lock: bool = False
        self.enemy_mp: int = 2
        self.enemy_hp: int = 4
        self.player_win_token: int = 0
        self.enemy_win_token: int = 0
        self.player_move_boost: int = 0
        self.enemy_move_boost: int = 0
        self.money: int = 2000
        self.vanessa_black_bankrupt: int = 0
        self.magic_lock: bool = False
        self.equipment_lock: bool = False
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
        self.game_cards: List[str] = []
        self.enemy_token_position: int = 15
        self.player_token_position: int = 15
        self.card_constants: list[str] = []
        self.player_turn: bool = False
        self.enemy_turn: bool = False

        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_SCREEN: MessageBox([
                "Vanessea Black: this is the welcome screen"
            ]),
            self.BET_MESSAGE: MessageBox([
                "Min bet of 50, max of 200. Press up and down keys to increase/decrease bet. Press B to Exit."
            ]),
        }

        # Initialize the card messages dictionary
        self.card_messages: dict[str, MessageBox] = {
            self.EXP_CARD_HALF_UP: MessageBox([
                "1) Increase EXP in pile by 50%"
            ]),
            self.GOLD_CARD_HALF_UP: MessageBox([
                "2) Increase gold in pile by 50%"
            ]),
            self.GOLD_CARD_BONUS: MessageBox([
                "3) Gain 250 gold"
            ]),
            self.EXP_CARD_BONUS: MessageBox([
                "4) Gain 250 EXP"
            ]),
            self.MOVE_3_SQUARES: MessageBox([
                "5) Move up 3 squares (10% board movement)"
            ]),
            self.TASTY_TREAT: MessageBox([
                "6) Gain +100 stamina + 50 focus"
            ]),
            self.FREE_WIN: MessageBox([
                "7) Player v enemy roll : winner gets a free win."
            ]),
            self.PLAYER_MOVE_FORWARD: MessageBox([
                "8) +1 movement for player (rest of round)"
            ]),
            self.ENEMY_MOVE_BACK: MessageBox([
                "9) -1 movement for enemy (rest of round)"
            ]),
            self.ENEMY_MOVE_BACK_3: MessageBox([
                "10) Move enemy back 3 squares (10% board movement)"
            ]),
            self.SWAP_POSITIONS: MessageBox([
                "11) Swap positions with enemy"
            ]),
            self.STAT_BOOSTER: MessageBox([
                "12) +1 to player’s luck, spirit, and magic"
            ]),
            self.SPECIAL_ITEM: MessageBox([
                "13) Gain special item or 1000 gold (enemy loses -1000 gold from player pile)"
            ]),
            self.BANKRUPT: MessageBox([
                "14) Bankrupt – lose all money in pile"
            ]),
            self.EXP_HOLE: MessageBox([
                "15) Bankrupt – lose all EXP in pile"
            ]),
            self.MAGIC_LOCK_UP: MessageBox([
                "16) Magic lock for rest of round"
            ]),
            self.EQUIPMENT_LOCK_UP: MessageBox([
                "17) Disable equipment for rest of round"
            ]),
            self.MOVE_BACK_3: MessageBox([
                "18) Move back 3 squares"
            ]),
            self.MOVE_ENEMY_3: MessageBox([
                "19) Enemy moves forward 3 squares"
            ]),
            self.MID_POINT_MOVE: MessageBox([
                "20) Move to mid point on map"
            ]),
        }


    BET_MESSAGE: str = "bet_message"
    SPIN_WHEEL_SCREEN: str = "spin wheel screen"
    DRAW_CARD_SCREEN: str = "draw card screen"
    PLAYER_TURN_SCREEN: str = "player turn screen"
    ENEMY_TURN_SCREEN: str = "enemy turn screen"

    #squres of game board
    GOLD_SQUARE: str = "gold square"
    EXP_SQUARE: str = "exp square"
    TRAP_SQUARE: str = "trap square"
    VICTORY_SQUARE: str = "victory square"
    THIEF_SQUARE: str = "thief square"
    CARD_SQUARE: str = "card square"



    # the below are for cards
    EXP_CARD_HALF_UP: str = "exp_card_half_up"
    GOLD_CARD_HALF_UP: str = "gold_card_half_up"
    GOLD_CARD_BONUS: str = "gold_card_bonus"
    EXP_CARD_BONUS: str = "exp_card_bonus"
    MOVE_3_SQUARES: str = "move_3_squares"
    TASTY_TREAT: str = "TASTY_TREAT"
    FREE_WIN: str = "free_win"
    PLAYER_MOVE_FORWARD: str = "player_move_forward"
    ENEMY_MOVE_BACK: str = "enemy_move_back"
    ENEMY_MOVE_BACK_3: str = "enemy_move_back_3"
    SWAP_POSITIONS: str = "swap_positions"
    STAT_BOOSTER: str = "stat_booster"
    SPECIAL_ITEM: str = "special_item"
    BANKRUPT: str = "bankrupt"
    EXP_HOLE: str = "exp_hole"
    MAGIC_LOCK_UP: str = "magic_lock_up"
    EQUIPMENT_LOCK_UP: str = "equipment_lock_up"
    MOVE_BACK_3: str = "move_back_3"
    MOVE_ENEMY_3: str = "move_enemy_3"
    MID_POINT_MOVE: str = "mid_point_move"
    CARD_CONSTANT: str = "card_constant"


    def start(self, state):
        #v------TESTING---------v#
        self.player_money_pile = 100
        self.exp_pile = 100

        #^-------TESTING---------^#

        self.spirit_bonus: int = state.player.spirit * 10
        self.magic_bonus: int = state.player.mind * 10
        self.card_constants: list[str] = [
            self.BANKRUPT,
            self.EXP_HOLE,
            self.MAGIC_LOCK_UP,
            self.EQUIPMENT_LOCK_UP,
            self.MOVE_BACK_3,
            self.MID_POINT_MOVE,
            self.EXP_CARD_HALF_UP,
            self.GOLD_CARD_HALF_UP,
            self.GOLD_CARD_BONUS,
            self.EXP_CARD_BONUS,
            self.MOVE_3_SQUARES,
            self.TASTY_TREAT,
            self.MOVE_ENEMY_3,
            self.STAT_BOOSTER,
            self.FREE_WIN,
            self.PLAYER_MOVE_FORWARD,
            self.ENEMY_MOVE_BACK,
            self.ENEMY_MOVE_BACK_3,
            self.SWAP_POSITIONS,
            self.SPECIAL_ITEM,
        ]
        self.game_cards = self.card_constants.copy()
        self.update_board()


    def round_reset(self, state):
        self.player_money_pile = 0
        self.exp_pile = 0
        self.card_constants: list[str] = [
            self.BANKRUPT,
            self.EXP_HOLE,
            self.MAGIC_LOCK_UP,
            self.EQUIPMENT_LOCK_UP,
            self.MOVE_BACK_3,
            self.MID_POINT_MOVE,
            self.EXP_CARD_HALF_UP,
            self.GOLD_CARD_HALF_UP,
            self.GOLD_CARD_BONUS,
            self.EXP_CARD_BONUS,
            self.MOVE_3_SQUARES,
            self.TASTY_TREAT,
            self.MOVE_ENEMY_3,
            self.STAT_BOOSTER,
            self.FREE_WIN,
            self.PLAYER_MOVE_FORWARD,
            self.ENEMY_MOVE_BACK,
            self.ENEMY_MOVE_BACK_3,
            self.SWAP_POSITIONS,
            self.SPECIAL_ITEM,
        ]
        self.update_board()


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

        elif self.game_state == self.SPIN_WHEEL_SCREEN:
            pass
        elif self.game_state == self.PLAYER_TURN_SCREEN:
            if state.controller.confirm_button:
                self.update_roll_dice_player()
            elif state.controller.action_and_cancel_button:
                self.update_roll_dice_dealer()
        elif self.game_state == self.ENEMY_TURN_SCREEN:
            if state.controller.confirm_button:
                self.update_roll_dice_player()
            elif state.controller.action_and_cancel_button:
                self.update_roll_dice_dealer()
        if self.game_state == self.DRAW_CARD_SCREEN:
            if self.CARD_CONSTANT in self.card_messages:
                self.card_messages[self.CARD_CONSTANT].update(state)
                self.update_card_effects(state)
            if state.controller.confirm_button:
                self.update_draw_card(state)



    def draw(self, state):
        super().draw(state)
        self.draw_board(state)
        self.draw_enemy_token(state)
        self.draw_player_token(state)
        if self.game_state == self.WELCOME_SCREEN:
            pass

        elif self.game_state == self.SPIN_WHEEL_SCREEN:
            self.draw_wheel(state)
        elif self.game_state == self.DRAW_CARD_SCREEN:
            self.draw_card_message(state)
        pygame.display.flip()

#============================================update methods go below

    @typechecked
    def update_card_effects(self, state) -> None:
        """Applies the effects of the currently drawn card."""
        print(self.player_money_pile)
        if self.CARD_CONSTANT == self.BANKRUPT:
            if self.player_turn == True:
                self.player_money_pile = 0
            elif self.enemy_turn == True:
                self.enemy_money_pile = 0
        elif self.CARD_CONSTANT == self.EXP_HOLE:
            if self.player_turn == True:
                self.player_exp_pile = 0
            elif self.enemy_turn == True:
                self.enemy_exp_pile = 0
        elif self.CARD_CONSTANT == self.MAGIC_LOCK_UP:
            if self.player_turn == True:
                self.player_magic_lock = True
            elif self.enemy_turn == True:
                self.enemy_magic_lock = True
        elif self.CARD_CONSTANT == self.EQUIPMENT_LOCK_UP:
            if self.player_turn == True:
                self.player_equipment_lock = True
            elif self.enemy_turn == True:
                self.enemy_equipment_lock = True
        elif self.CARD_CONSTANT == self.MOVE_BACK_3:
            if self.player_turn == True:
                self.player_position -= 3
            elif self.enemy_turn == True:
                self.enemy_position -= 3
        elif self.CARD_CONSTANT == self.MID_POINT_MOVE:
            if self.player_turn == True:
                self.player_position = 15
            elif self.enemy_turn == True:
                self.enemy_position = 15
        elif self.CARD_CONSTANT == self.EXP_CARD_HALF_UP:
            if self.player_turn == True:
                self.player_exp_pile += self.player_exp_pile // 2
            elif self.enemy_turn == True:
                self.enemy_exp_pile += self.enemy_exp_pile // 2
        elif self.CARD_CONSTANT == self.GOLD_CARD_HALF_UP:
            if self.player_turn == True:
                self.player_money_pile += self.player_money_pile // 2
            elif self.enemy_turn == True:
                self.enemy_money_pile += self.enemy_money_pile // 2
        elif self.CARD_CONSTANT == self.EXP_CARD_BONUS:
            if self.player_turn == True:
                self.player_exp_pile += 250
            elif self.enemy_turn == True:
                self.enemy_exp_pile += 250
        elif self.CARD_CONSTANT == self.GOLD_CARD_BONUS:
            if self.player_turn == True:
                self.player_money_pile += 250
            elif self.enemy_turn == True:
                self.enemy_money_pile += 250
        elif self.CARD_CONSTANT == self.MOVE_3_SQUARES:
            if self.player_turn == True:
                self.player_position += 3
            elif self.enemy_turn == True:
                self.enemy_position += 3
        elif self.CARD_CONSTANT == self.TASTY_TREAT:
            if self.player_turn == True:
                # create a fun in player that doesn't allow stam/focus to go above max
                state.player.stamina_points += 100
                state.player.focus_points += 50
            elif self.enemy_turn == True:
                self.enemy_hp += 4
                self.enemy_mp += 2
        elif self.CARD_CONSTANT == self.MOVE_ENEMY_3:
            if self.player_turn == True:
                self.enemy_position += 3
            elif self.enemy_turn == True:
                self.player_position += 3
        elif self.CARD_CONSTANT == self.STAT_BOOSTER:
            if self.player_turn == True:
                self.player_stat_boost += 1
            elif self.enemy_turn == True:
                self.enemy_stat_boost += 1
        elif self.CARD_CONSTANT == self.FREE_WIN:
            if self.player_turn == True:
                self.player_win_token += 1
            elif self.enemy_turn == True:
                self.enemy_win_token += 1
        elif self.CARD_CONSTANT == self.PLAYER_MOVE_FORWARD:
            if self.player_turn == True:
                self.player_move_boost += 1
            elif self.enemy_turn == True:
                self.enemy_move_boost += 1
        elif self.CARD_CONSTANT == self.ENEMY_MOVE_BACK:
            if self.player_turn == True:
                self.enemy_move_boost -= 1
            elif self.enemy_turn == True:
                self.player_move_boost -= 1
        elif self.CARD_CONSTANT == self.ENEMY_MOVE_BACK_3:
            if self.player_turn == True:
                self.enemy_position -= 3
            elif self.enemy_turn == True:
                self.player_position -= 3
        elif self.CARD_CONSTANT == self.SWAP_POSITIONS:
            self.player_position_holder = self.player_position
            self.enemy_position_holder = self.enemy_position
            self.player_position = self.enemy_position_holder
            self.enemy_position = self.player_position_holder
        elif self.CARD_CONSTANT == self.SPECIAL_ITEM:
            if self.player_turn == True:
                pass
            elif self.enemy_turn == True:
                pass

    @typechecked
    def update_draw_card(self, state) -> None:
        """Rolls a number from 1–100, maps it to a card, and selects the next available one if needed."""
        roll: int = random.randint(1, 100)
        start_index: int = (roll - 1) // 5
        total_cards: int = len(self.card_constants)

        # Start searching from rolled index, wrapping around if necessary
        for offset in range(total_cards):
            index = (start_index + offset) % total_cards
            selected_card = self.card_constants[index]
            if selected_card in self.card_messages:
                self.CARD_CONSTANT = selected_card
                self.card_messages[selected_card].reset()
                print(f"🎲 Rolled: {roll}")
                print(f"🃏 Selected Card: {selected_card}")
                for line in self.card_messages[selected_card].messages:
                    print(f"📜 Message: {line}")
                self.card_constants.remove(selected_card)
                break

    @typechecked
    def update_square_effects(self) -> None:
        current_player_square = self.board_squares[self.player_position]
        current_enemy_square = self.board_squares[self.enemy_position]

    @typechecked
    def update_board(self) -> None:
        """Creates a 30-square board with exact type counts, no spacing rules."""
        total_squares = 30
        self.board_squares: list[str] = [None] * (total_squares - 1)  # Leave space for victory square

        square_types_with_counts = {
            self.CARD_SQUARE: 6,
            self.GOLD_SQUARE: 10,
            self.EXP_SQUARE: 6,
            self.TRAP_SQUARE: 5,
            self.THIEF_SQUARE: 2,
        }

        all_indexes = list(range(total_squares - 1))
        random.shuffle(all_indexes)
        index_pointer = 0

        for square_type, count in square_types_with_counts.items():
            for _ in range(count):
                idx = all_indexes[index_pointer]
                self.board_squares[idx] = square_type
                index_pointer += 1

        self.board_squares.append(self.VICTORY_SQUARE)

        print("\n=== BOARD SQUARE LAYOUT ===")
        for idx, square in enumerate(self.board_squares):
            print(f"Square {idx + 1:02}: {square}")

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
    def draw_card_message(self,state) -> None:
        """Draws the message box for the currently selected card."""
        if self.CARD_CONSTANT in self.card_messages:
            self.card_messages[self.CARD_CONSTANT].draw(state)




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











