import math
from typing import List
from random import randint

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
        self.game_state: str = self.SPIN_WHEEL_SCREEN
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
        self.selected_index = 0
        self.board_squares: list[str] = [

        ]

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
    EMPTY_SQUARE: str = "empty square"



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
        self.board_squares: list[str] = [
            self.EMPTY_SQUARE,  # 1
            self.EXP_SQUARE,  # 2
            self.TRAP_SQUARE,  # 3
            self.GOLD_SQUARE,  # 4
            self.CARD_SQUARE,  # 5
            self.EXP_SQUARE,  # 6
            self.TRAP_SQUARE,  # 7
            self.GOLD_SQUARE,  # 8
            self.EXP_SQUARE,  # 9
            self.CARD_SQUARE,  # 10
            self.GOLD_SQUARE,  # 11
            self.THIEF_SQUARE,  # 12
            self.EXP_SQUARE,  # 13
            self.GOLD_SQUARE,  # 14
            self.CARD_SQUARE,  # 15
            self.TRAP_SQUARE,  # 16
            self.EXP_SQUARE,  # 17
            self.GOLD_SQUARE,  # 18
            self.TRAP_SQUARE,  # 19
            self.CARD_SQUARE,  # 20
            self.EXP_SQUARE,  # 21
            self.GOLD_SQUARE,  # 22
            self.TRAP_SQUARE,  # 23
            self.THIEF_SQUARE,  # 24
            self.CARD_SQUARE,  # 25
            self.GOLD_SQUARE,  # 26
            self.GOLD_SQUARE,  # 27
            self.GOLD_SQUARE,  # 28
            self.CARD_SQUARE,  # 29
            self.VICTORY_SQUARE  # 30
        ]


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


    def update(self, state):
        # print(f"🎯 Player landed on: {self.board_squares[self.player_position]}")

        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        if self.money <= self.vanessa_black_bankrupt:
            state.currentScreen = state.area4RestScreen
            state.area4RestScreen.start(state)
            Events.add_level_four_event_to_player(state.player, Events.WHEEL_OF_TORTURE_VANESSA_BLACK_DEFEATED)

        if self.game_state == self.WELCOME_SCREEN:
            self.update_welcome_screen_helper()

        elif self.game_state == self.SPIN_WHEEL_SCREEN:
            if state.controller.confirm_button:
                self.update_wheel_result()
        elif self.game_state == self.PLAYER_TURN_SCREEN:
            if state.controller.confirm_button:
                self.update_roll_dice_player_enemy_roll_phase(state)

        elif self.game_state == self.ENEMY_TURN_SCREEN:
            if state.controller.confirm_button:
                self.update_roll_dice_player_enemy_roll_phase()

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
    def update_wheel_result(self) -> int:

        """Rolls 1–100 and sets the selected slice index based on chance. Returns the selected index."""
        roll: int = random.randint(1, 100)

        # RED slices (30%)
        if roll <= 30:
            red_indices = [1, 5, 9, 13, 15, 17]
            self.selected_index = random.choice(red_indices)

        # SKY BLUE slice (5%)
        elif roll <= 35:
            self.selected_index = 7

        # PURPLE slices (10%)
        elif roll <= 45:
            purple_indices = [3, 11]
            self.selected_index = random.choice(purple_indices)

        # GREEN slices (55%)
        else:
            all_indices = set(range(20))
            used = {1, 3, 5, 7, 9, 11, 13, 15, 17}
            green_indices = list(all_indices - used)
            self.selected_index = random.choice(green_indices)

        print(f"🎯 Wheel result roll: {roll} → selected_index: {self.selected_index}")
        return self.selected_index  # <— now always returns an int

    def update_welcome_screen_helper(self):
        while True:
            player_init_roll = random.randint(1, 6)
            enemy_init_roll = random.randint(1, 6)
            print(f"🎲 Player rolled: {player_init_roll}, Enemy rolled: {enemy_init_roll}")

            if player_init_roll > enemy_init_roll:
                self.game_state = self.PLAYER_TURN_SCREEN
                print("🎮 Player goes first!")
                break
            elif enemy_init_roll > player_init_roll:
                self.game_state = self.ENEMY_TURN_SCREEN
                print("👾 Enemy goes first!")
                break
            else:
                print("🔁 Tie! Rerolling...")

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
        """Uses the selected_index from the wheel to choose a card and sets CARD_CONSTANT accordingly."""
        total_cards: int = len(self.card_constants)

        if total_cards == 0:
            print("⚠️ No cards left to draw.")
            return

        index: int = self.selected_index % total_cards
        selected_card = self.card_constants[index]

        if selected_card in self.card_messages:
            self.CARD_CONSTANT = selected_card
            self.card_messages[selected_card].reset()
            print(f"🎯 Wheel selected index: {self.selected_index}")
            print(f"🃏 Selected Card: {selected_card}")
            for line in self.card_messages[selected_card].messages:
                print(f"📜 Message: {line}")
            self.card_constants.remove(selected_card)

    @typechecked
    def update_square_effects(self) -> None:
        current_player_square = self.board_squares[self.player_position]
        current_enemy_square = self.board_squares[self.enemy_position]

    @typechecked
    def update_roll_dice_player_enemy_roll_phase(self, state) -> None:
        if self.player_turn == True:
            self.move_player = random.randint(1, 6)
            self.player_position += self.move_player
            if self.player_position > 29:
                self.player_position = 29
            square_type = self.board_squares[self.player_position]
            print(f"🎲 Player rolled: {self.move_player}")
            print(f"🎯 Player landed on square {self.player_position}: {square_type}")
        elif self.enemy_turn == True:
            self.move_dealer = random.randint(1, 6)
            self.enemy_position += self.move_dealer
            if self.enemy_position > 29:
                self.enemy_position = 29
            square_type = self.board_squares[self.enemy_position]
            print(f"🎲 Enemy rolled: {self.move_dealer}")
            print(f"🎯 Enemy landed on square {self.enemy_position}: {square_type}")
        else:
            return  # no valid turn, exit safely

        # ---- Handle square effect ----
        if square_type == self.GOLD_SQUARE:
            if self.player_turn == True:
                self.player_money_pile += 25
                print("💰 Player GOLD_SQUARE: +25 gold!")
            elif self.enemy_turn == True:
                self.enemy_money_pile += 25
                print("💰 Enemy GOLD_SQUARE: +25 gold!")

        elif square_type == self.EXP_SQUARE:
            if self.player_turn == True:
                self.player_exp_pile += 25
                print("📘 Player EXP_SQUARE: +25 EXP!")
            elif self.enemy_turn == True:
                self.enemy_exp_pile += 25
                print("📘 Enemy EXP_SQUARE: +25 EXP!")

        elif square_type == self.TRAP_SQUARE:
            if self.player_turn == True:
                state.player.stamina_points -= 25
                state.player.focus_points -= 25
                print("💀 Player TRAP_SQUARE: -25 Stamina, -25 Focus!")
            elif self.enemy_turn == True:
                self.enemy_hp -= 2
                self.enemy_mp -= 1
                print("💀 Enemy TRAP_SQUARE: -2 HP, -1 MP!")

        elif square_type == self.THIEF_SQUARE:
            if self.player_turn == True:
                self.player_money_pile -= 250
                print("🦹 Player THIEF_SQUARE: -250 gold!")
            elif self.enemy_turn == True:
                self.enemy_money_pile -= 250
                print("🦹 Enemy THIEF_SQUARE: -250 gold!")

        elif square_type == self.CARD_SQUARE:
            self.game_state = self.DRAW_CARD_SCREEN
            if self.player_turn == True:
                print("🃏 Player CARD_SQUARE: Switching to Card Screen!")
            elif self.enemy_turn == True:
                print("🃏 Enemy CARD_SQUARE: Switching to Card Screen!")

        elif square_type == self.VICTORY_SQUARE:
            if self.player_turn == True:
                print("🏆 Player VICTORY_SQUARE: You win! 🎉")
            elif self.enemy_turn == True:
                print("💀 Enemy VICTORY_SQUARE: Enemy wins!")

        elif square_type == self.EMPTY_SQUARE:
            if self.player_turn == True:
                print("😶 Player EMPTY_SQUARE: Nothing happens.")
            elif self.enemy_turn == True:
                print("😶 Enemy EMPTY_SQUARE: Nothing happens.")

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
        y_start = 100
        box_height: int = 50
        box_width: int = 50
        border_thickness: int = 2
        x_padding: int = 70
        y_padding: int = 100
        squares_per_row: int = 10

        # Color mapping by square type
        color_map = {
            self.GOLD_SQUARE: (255, 165, 0),  # ORANGE
            self.EMPTY_SQUARE: (255, 111, 0),  # ORANGE
            self.EXP_SQUARE: (0, 255, 255),  # CYAN
            self.CARD_SQUARE: (255, 0, 255),  # MAGENTA
            self.TRAP_SQUARE: (255, 105, 180),  # PINK
            self.THIEF_SQUARE: (128, 128, 128),  # GRAY
            self.VICTORY_SQUARE: (50, 205, 50),  # LIME
        }

        for index, square in enumerate(self.board_squares):
            row = index // squares_per_row
            col = index % squares_per_row
            x_position = x_start + col * x_padding
            y_position = y_start + row * y_padding

            color = color_map.get(square, (255, 0, 0))  # Fallback to RED if not found
            pygame.draw.rect(state.DISPLAY, color, (x_position, y_position, box_height, box_width), border_thickness)

    @typechecked
    def draw_wheel(self, state) -> None:
        center_x: int = 400
        center_y: int = 300
        radius: int = 150
        num_slices: int = 20
        spin_speed: float = 0.10
        max_frames: int = 180

        # Internal spin state
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

        # Colors
        SKY_BLUE = (135, 206, 235)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        PURPLE = (138, 43, 226)
        WHITE = (255, 255, 255)

        # Final color layout (green every other slice)
        wheel_colors: list[tuple[int, int, int]] = [
            GREEN,  # 0
            RED,  # 1
            GREEN,  # 2
            PURPLE,  # 3
            GREEN,  # 4
            RED,  # 5
            GREEN,  # 6
            SKY_BLUE,  # 7
            GREEN,  # 8
            RED,  # 9
            GREEN,  # 10
            PURPLE,  # 11
            GREEN,  # 12
            RED,  # 13
            GREEN,  # 14
            RED,  # 15
            GREEN,  # 16
            RED,  # 17
            GREEN,  # 18
            GREEN  # 19 ← filler green
        ]

        # Draw each slice
        for i in range(num_slices):
            angle_start = (2 * math.pi / num_slices) * i + self._wheel_angle
            angle_end = (2 * math.pi / num_slices) * (i + 1) + self._wheel_angle

            point1 = (center_x, center_y)
            point2 = (
                int(center_x + radius * math.cos(angle_start)),
                int(center_y + radius * math.sin(angle_start))
            )
            point3 = (
                int(center_x + radius * math.cos(angle_end)),
                int(center_y + radius * math.sin(angle_end))
            )

            pygame.draw.polygon(state.DISPLAY, wheel_colors[i], [point1, point2, point3])

        # Draw white dividing lines
        for i in range(num_slices):
            angle = (2 * math.pi / num_slices) * i + self._wheel_angle
            end_x = int(center_x + radius * math.cos(angle))
            end_y = int(center_y + radius * math.sin(angle))
            pygame.draw.line(state.DISPLAY, WHITE, (center_x, center_y), (end_x, end_y), 2)

        # Draw top-down arrow
        arrow_width = 20
        arrow_height = 15
        arrow_x = center_x
        arrow_y = center_y - radius - 10

        pygame.draw.polygon(
            state.DISPLAY,
            RED,
            [
                (arrow_x, arrow_y),
                (arrow_x - arrow_width // 2, arrow_y - arrow_height),
                (arrow_x + arrow_width // 2, arrow_y - arrow_height)
            ]
        )
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











