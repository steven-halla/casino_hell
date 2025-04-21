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
        self.player_rolled: bool = False
        self.enemy_rolled: bool = False
        self.confirm_spin: bool = False
        self.enemy_stat_boost: int  = 0
        self.player_dice_roll: int = 0

        self.enemy_dice_roll: int = 0
        self.player_stat_boost: int = 0
        self.used_wheel_indices: set[int] = set()
        self.enemy_position_holder: int = 0
        self.player_position_holder: int = 0
        self.enemy_equipment_lock: bool = False
        self.dice_rolled: bool = False
        self.game_state: str = self.WELCOME_SCREEN
        self.player_money_pile: int = 0
        self.enemy_money_pile: int = 0
        self.player_exp_pile: int = 0
        self.enemy_exp_pile: int = 0
        self.exp_pile: int = 0
        self.delay_start_time = None
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
        self.wheel_lock: bool = False
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
        self.enemy_turn: bool = False
        self.selected_index = 0
        self.sprite_sheet: pygame.Surface = pygame.image.load("./assets/images/dice45.png")
        self.transition_checker: bool = False



        self.player_turn: bool = True


        self.board_squares: list[str] = [

        ]

        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_SCREEN_MESSAGE: MessageBox([
                "Vanessea Black: this is the welcome screen"
            ]),
            self.BET_MESSAGE: MessageBox([
                "Min bet of 50, max of 200. Press up and down keys to increase/decrease bet. Press B to Exit."
            ]),
            self.INIT_SCREEN_MESSAGE: MessageBox([
                "Vanessea Black: Roll the dice lets see who starts first this round. Press confirm button when ready"
            ]),
            self.DRAW_CARD_SCREEN_MESSAGE: MessageBox([
                "Vanessea Black: your draw card message"
            ]),
            self.APPLY_CARD_SCREEN_MESSAGE: MessageBox([
                "Vanessea Black: APPLYING CARD EFFECT"
            ]),
            self.PLAYER_TURN_SCREEN_MESSAGE: MessageBox([
                "Vanessea Black: ITS THE PLAYER TURN"
            ]),
            self.ENEMY_TURN_SCREEN_MESSAGE: MessageBox([
                "Vanessea Black:  ITS THE ENEMY TURN"
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


    SPIN_WHEEL_SCREEN: str = "spin wheel screen"
    DRAW_CARD_SCREEN: str = "draw card screen"
    APPLY_CARD_SCREEN: str = "apply card screen"
    PLAYER_TURN_SCREEN: str = "player turn screen"
    ENEMY_TURN_SCREEN: str = "enemy turn screen"
    INIT_SCREEN: str = "init screen"

    WELCOME_SCREEN_MESSAGE: str = "welcome screen message"
    INIT_SCREEN_MESSAGE: str = "init screen message"
    DRAW_CARD_SCREEN_MESSAGE: str = "draw card screen message"
    APPLY_CARD_SCREEN_MESSAGE: str = "apply card screen message"
    PLAYER_TURN_SCREEN_MESSAGE: str = "player turn screen message"
    ENEMY_TURN_SCREEN_MESSAGE: str = "enemy turn screen message"
    BET_MESSAGE: str = "bet_message"


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
        self.confirm_spin = False
        self.used_wheel_indices.clear()
        self.player_turn = False
        self.enemy_turn = False
        self.player_position = 0
        self.enemy_position = 0

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
        # print(f"🎯 ENEMYT landed on: {self.board_squares[self.enemy_position]}")
        # print(self.CARD_CONSTANT)
        # print("Player roll is " + str(self.player_dice_roll))
        # print("enemy roll is " + str(self.enemy_dice_roll))
        # print(self.game_state)

        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        # if self.money <= self.vanessa_black_bankrupt:
        #     state.currentScreen = state.area4RestScreen
        #     state.area4RestScreen.start(state)
        #     Events.add_level_four_event_to_player(state.player, Events.WHEEL_OF_TORTURE_VANESSA_BLACK_DEFEATED)

        if self.game_state == self.WELCOME_SCREEN:
            self.battle_messages[self.WELCOME_SCREEN_MESSAGE].update(state)

            if self.battle_messages[self.WELCOME_SCREEN_MESSAGE].is_finished() and controller.confirm_button:
                self.game_state = self.INIT_SCREEN

        elif self.game_state == self.INIT_SCREEN:
            self.battle_messages[self.INIT_SCREEN_MESSAGE].update(state)

            if self.battle_messages[self.INIT_SCREEN_MESSAGE].is_finished() and controller.confirm_button:
                self.update_init_screen_helper(state)


        elif self.game_state == self.SPIN_WHEEL_SCREEN:
            if state.controller.confirm_button and self.wheel_lock == False:
                self.update_wheel_result()





        # elif self.game_state == self.PLAYER_TURN_SCREEN:
        #     self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].update(state)
        #
        #     #
        #     # if state.controller.confirm_button:
        #     if self.transition_checker == False:
        #         self.update_roll_dice_player_enemy_roll_phase(state)
        elif self.game_state == self.PLAYER_TURN_SCREEN:
            if not self.player_rolled:
                # self.move_player = random.randint(1, 6)
                self.move_player = 4
                self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].messages = [
                    f"PLAYER rolled a {self.move_player}."
                ]
                self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].reset()
                self.player_rolled = True

            self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].update(state)

            if self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].is_finished() and controller.confirm_button:
                self.update_roll_dice_player_enemy_roll_phase(state)
                self.player_rolled = False  # reset for next time
        elif self.game_state == self.ENEMY_TURN_SCREEN:
            if not self.enemy_rolled:
                self.move_dealer = random.randint(1, 6)
                self.battle_messages[self.ENEMY_TURN_SCREEN_MESSAGE].messages = [
                    f"ENemy rolled a {self.move_dealer}."
                ]
                self.battle_messages[self.ENEMY_TURN_SCREEN_MESSAGE].reset()
                self.enemy_rolled = True

            self.battle_messages[self.ENEMY_TURN_SCREEN_MESSAGE].update(state)

            if self.battle_messages[self.ENEMY_TURN_SCREEN_MESSAGE].is_finished() and controller.confirm_button:
                self.update_roll_dice_player_enemy_roll_phase(state)
                self.enemy_rolled = False  # reset for next time





        elif self.game_state == self.DRAW_CARD_SCREEN:
            if not hasattr(self, "_card_drawn"):
                self.update_draw_card(state)
                drawn_card = self.CARD_CONSTANT.replace("_", " ").title()
                self.battle_messages[self.DRAW_CARD_SCREEN_MESSAGE].messages = [
                    f"You drew the “{drawn_card}” card."
                ]
                self.battle_messages[self.DRAW_CARD_SCREEN_MESSAGE].reset()
                self._card_drawn = True

            self.battle_messages[self.DRAW_CARD_SCREEN_MESSAGE].update(state)

            if self.battle_messages[self.DRAW_CARD_SCREEN_MESSAGE].is_finished() and state.controller.confirm_button:
                self.game_state = self.APPLY_CARD_SCREEN
                del self._card_drawn





        # elif self.game_state == self.DRAW_CARD_SCREEN:
        #     if state.controller.confirm_button:
        #         print("🎬 Calling update_draw_card")
        #         self.update_draw_card(state)
        #
        #     if self.CARD_CONSTANT:
        #         print("➡️ Moving to APPLY_CARD_SCREEN")
        #         self.game_state = self.APPLY_CARD_SCREEN

        elif self.game_state == self.APPLY_CARD_SCREEN:
            if not hasattr(self, "_effect_shown"):
                if self.CARD_CONSTANT in self.card_messages:
                    self.card_messages[self.CARD_CONSTANT].reset()
                self._effect_shown = True

            if self.CARD_CONSTANT in self.card_messages:
                self.card_messages[self.CARD_CONSTANT].update(state)
                if self.card_messages[self.CARD_CONSTANT].is_finished() and state.controller.confirm_button:
                    self.update_card_effects(state)
                    del self._effect_shown

            # if state.controller.confirm_button:
            #     selected_card = self.card_constants[self.index]
            #
            #     if selected_card in self.card_messages:
            #         self.CARD_CONSTANT = selected_card
            #         self.card_messages[selected_card].reset()
            #         print(f"🎯 Wheel selected index: {self.selected_index}")
            #         print(f"🃏 Selected Card: {selected_card}")
            #         for line in self.card_messages[selected_card].messages:
            #             print(f"📜 Message: {line}")
            #         self.card_constants.remove(selected_card)
            #         print(self.CARD_CONSTANT)
            #         self.update_card_effects(state)
            #
            # if self.CARD_CONSTANT in self.card_messages:
            #     self.card_messages[self.CARD_CONSTANT].update(state)








    def draw(self, state):
        super().draw(state)
        self.draw_board(state)
        self.draw_enemy_token(state)
        self.draw_player_token(state)
        if self.game_state == self.WELCOME_SCREEN:
            self.battle_messages[self.WELCOME_SCREEN_MESSAGE].draw(state)


        elif self.game_state == self.INIT_SCREEN:
            self.battle_messages[self.INIT_SCREEN_MESSAGE].draw(state)

            self.draw_display_dice(state, self.player_dice_roll, self.enemy_dice_roll)


        # elif self.game_state == self.SPIN_WHEEL_SCREEN:
        #     self.draw_wheel(state)
        elif self.game_state == self.PLAYER_TURN_SCREEN:
            self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].draw(state)

            self.draw_display_dice(state, self.move_player, 0)


        elif self.game_state == self.ENEMY_TURN_SCREEN:
            self.battle_messages[self.ENEMY_TURN_SCREEN_MESSAGE].draw(state)

            self.draw_display_dice(state, 0, self.move_dealer)


        elif self.game_state == self.SPIN_WHEEL_SCREEN:
            self.draw_wheel(state)  # This updates the wheel's animation
            if self._has_landed:
                # Reset the flag for future spins
                self._has_landed = False
                # Transition to the next game state
                self.game_state = self.DRAW_CARD_SCREEN
        elif self.game_state == self.DRAW_CARD_SCREEN:
            self.battle_messages[self.DRAW_CARD_SCREEN_MESSAGE].draw(state)
        elif self.game_state == self.APPLY_CARD_SCREEN:
            # self.battle_messages[self.APPLY_CARD_SCREEN_MESSAGE].draw(state)
            self.draw_card_message(state)


            # if self.CARD_CONSTANT in self.card_messages:
            #     self.card_messages[self.CARD_CONSTANT].draw(state)


        pygame.display.flip()

#============================================update methods go below

    @typechecked
    def update_wheel_result(self) -> None:
        """Rolls 1–100 and sets the selected slice index based on chance. Returns the selected index."""
        roll: int = random.randint(1, 100)

        # Define index groups
        red_indices = [1, 5, 9, 13, 15, 17]
        sky_blue_index = 7
        purple_indices = [3, 11]
        all_indices = set(range(20))
        used_indices = self.used_wheel_indices

        # Determine available indices for each color
        available_red = [i for i in red_indices if i not in used_indices]
        available_sky_blue = [sky_blue_index] if sky_blue_index not in used_indices else []
        available_purple = [i for i in purple_indices if i not in used_indices]
        available_green = list(all_indices - used_indices - set(red_indices + [sky_blue_index] + purple_indices))

        # Select index based on roll
        if roll <= 30 and available_red:
            self.selected_index = random.choice(available_red)
        elif roll <= 35 and available_sky_blue:
            self.selected_index = sky_blue_index
        elif roll <= 45 and available_purple:
            self.selected_index = random.choice(available_purple)
        elif available_green:
            self.selected_index = random.choice(available_green)
        else:
            # Fallback: select any unused index
            remaining_indices = list(all_indices - used_indices)
            if not remaining_indices:
                print("⚠️ All wheel indices have been used this round.")
                return -1  # Indicate that no selection was made
            self.selected_index = random.choice(remaining_indices)

        # Mark the selected index as used
        self.used_wheel_indices.add(self.selected_index)
        self.confirm_spin = True

        print(f"🎯 Wheel result roll: {roll} → selected_index: {self.selected_index}")
        self.wheel_lock = True

    def update_init_screen_helper(self, state):
        if not self.dice_rolled:
            self.player_dice_roll = random.randint(1, 6)
            self.enemy_dice_roll = random.randint(1, 2)
            self.battle_messages[self.INIT_SCREEN_MESSAGE].messages = [
                f"You rolled a {self.player_dice_roll}, Vanessa rolled a {self.enemy_dice_roll}."
            ]
            self.battle_messages[self.INIT_SCREEN_MESSAGE].reset()
            self.dice_rolled = True

        elif self.battle_messages[self.INIT_SCREEN_MESSAGE].is_finished():
            if self.player_dice_roll > self.enemy_dice_roll:
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
            elif self.enemy_dice_roll > self.player_dice_roll:
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            else:
                self.dice_rolled = False  # Tie: reroll

    @typechecked
    def update_draw_card(self, state) -> None:
        total_cards: int = len(self.card_constants)

        if total_cards == 0:
            print("⚠️ No cards left to draw.")
            return

        self.index: int = self.selected_index % total_cards
        selected_card = self.card_constants[self.index]

        if selected_card not in self.card_messages:
            print(f"❌ Card {selected_card} not found in messages.")
            return

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

        self.wheel_lock = False
        if self.player_turn == True:
            self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].messages = [
                f"PLAYER rolled a {self.move_player}."
            ]
            # self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].update(state)
            print(self.move_player)

            print("Hi")
            self.player_position += self.move_player
            if self.player_position > 29:
                self.player_position = 29
                self.round_reset(state)
                self.game_state = self.WELCOME_SCREEN

            square_type = self.board_squares[self.player_position]
            print(f"🎲 Player rolled: {self.move_player}")
            print(f"🎯 Player landed on square {self.player_position}: {square_type}")
        elif self.enemy_turn == True:
            self.battle_messages[self.ENEMY_TURN_SCREEN_MESSAGE].messages = [
                f"ENEMY rolled a {self.move_dealer}."
            ]
            # self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].update(state)
            print(self.move_dealer)

            print("Hi")
            self.enemy_position += self.move_dealer
            if self.enemy_position > 29:
                self.enemy_position = 29
                self.round_reset(state)
                self.game_state = self.WELCOME_SCREEN
            square_type = self.board_squares[self.enemy_position]
            print(f"🎲 ENEMY rolled: {self.move_player}")
            print(f"🎯 ENEMY landed on square {self.enemy_position}: {square_type}")
        else:
            return  # no valid turn, exit safely

        # ---- Handle square effect ----
        if square_type == self.GOLD_SQUARE:
            if self.player_turn == True:
                self.player_money_pile += 25
                print("💰 Player GOLD_SQUARE: +25 gold!")
                self.game_state = self.ENEMY_TURN_SCREEN
                self.player_turn = False
                self.enemy_turn = True

            elif self.enemy_turn == True:
                self.enemy_money_pile += 25
                print("💰 Enemy GOLD_SQUARE: +25 gold!")
                self.game_state = self.PLAYER_TURN_SCREEN
                self.enemy_turn = False
                self.player_turn = True




        elif square_type == self.EXP_SQUARE:
            if self.player_turn == True:
                self.player_exp_pile += 25
                print("📘 Player EXP_SQUARE: +25 EXP!")
                self.game_state = self.ENEMY_TURN_SCREEN
                self.player_turn = False
                self.enemy_turn = True

            elif self.enemy_turn == True:
                self.enemy_exp_pile += 25
                self.game_state = self.PLAYER_TURN_SCREEN
                self.player_turn = True

                self.enemy_turn = False
                print("📘 Enemy EXP_SQUARE: +25 EXP!")

        elif square_type == self.TRAP_SQUARE:
            if self.player_turn == True:
                state.player.stamina_points -= 25
                state.player.focus_points -= 25
                self.game_state = self.ENEMY_TURN_SCREEN
                self.player_turn = False
                self.enemy_turn = True

                print("💀 Player TRAP_SQUARE: -25 Stamina, -25 Focus!")
            elif self.enemy_turn == True:
                self.enemy_hp -= 2
                self.enemy_mp -= 1
                self.game_state = self.PLAYER_TURN_SCREEN
                self.enemy_turn = False
                self.player_turn = True

                print("💀 Enemy TRAP_SQUARE: -2 HP, -1 MP!")

        elif square_type == self.THIEF_SQUARE:
            if self.player_turn == True:
                self.player_money_pile -= 250
                self.game_state = self.ENEMY_TURN_SCREEN
                self.player_turn = False
                self.enemy_turn = True

                print("🦹 Player THIEF_SQUARE: -250 gold!")
            elif self.enemy_turn == True:
                self.enemy_money_pile -= 250
                self.game_state = self.PLAYER_TURN_SCREEN
                self.enemy_turn = False
                self.player_turn = True

                print("🦹 Enemy THIEF_SQUARE: -250 gold!")

        elif square_type == self.CARD_SQUARE:
            self.game_state = self.DRAW_CARD_SCREEN
            if self.player_turn == True:
                self.game_state = self.SPIN_WHEEL_SCREEN

                print("🃏 Player CARD_SQUARE: Switching to Card Screen!")
            elif self.enemy_turn == True:
                self.game_state = self.SPIN_WHEEL_SCREEN
                self.game_state = self.PLAYER_TURN_SCREEN
                self.enemy_turn = False
                self.player_turn = True


                print("🃏 Enemy CARD_SQUARE: Switching to Card Screen!")

        elif square_type == self.VICTORY_SQUARE:
            if self.player_turn == True:
                self.game_state = self.WELCOME_SCREEN
                self.round_reset(state)

                # self.game_state = self.ENEMY_TURN_SCREEN
                # self.player_turn = False
                print("🏆 Player VICTORY_SQUARE: You win! 🎉")
            elif self.enemy_turn == True:
                self.game_state = self.WELCOME_SCREEN

                self.round_reset(state)

                # self.game_state = self.PLAYER_TURN_SCREEN
                # self.enemy_turn = False
                print("💀 Enemy VICTORY_SQUARE: Enemy wins!")

        # elif square_type == self.EMPTY_SQUARE:
        #     # self.game_state = self.WELCOME_SCREEN
        #
        #     if self.player_turn == True:
        #         print("😶 Player EMPTY_SQUARE: Nothing happens.")
        #     elif self.enemy_turn == True:
        #         print("😶 Enemy EMPTY_SQUARE: Nothing happens.")

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
        max_frames: int = 120  # 2 seconds at 60 FPS

        # Color definitions
        SKY_BLUE = (135, 206, 235)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        PURPLE = (138, 43, 226)
        WHITE = (255, 255, 255)

        # Final color layout
        wheel_colors: list[tuple[int, int, int]] = [
            GREEN, RED, GREEN, PURPLE, GREEN, RED, GREEN, SKY_BLUE, GREEN, RED,
            GREEN, PURPLE, GREEN, RED, GREEN, RED, GREEN, RED, GREEN, GREEN
        ]

        # Initialize wheel state
        if not hasattr(self, "_wheel_angle"):
            self._wheel_angle = 0.0
        if not hasattr(self, "_wheel_frame_count"):
            self._wheel_frame_count = 0
        if not hasattr(self, "_is_spinning"):
            self._is_spinning = False
        if not hasattr(self, "_has_landed"):
            self._has_landed = False

        # Start spinning on confirm
        if self.confirm_spin == True and not self._is_spinning and not self._has_landed:
            self._is_spinning = True
            self._wheel_angle = 0.0
            self._wheel_frame_count = 0
        # Initialize delay_start_time at the beginning of the function
        delay_start_time = None

        if self._is_spinning:
            self._wheel_angle += spin_speed
            self._wheel_frame_count += 1
            if self._wheel_frame_count >= max_frames:
                self._is_spinning = False
                self.delay_start_time = pygame.time.get_ticks()  # Assign current time
        if self.delay_start_time is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.delay_start_time >= 2000:  # 2000 milliseconds = 2 seconds
                self._has_landed = True
                self.delay_start_time = None  # Reset after use
                # Proceed to the next screen or state transition here
        # # Spin phase
        # if self._is_spinning:
        #     self._wheel_angle += spin_speed
        #     self._wheel_frame_count += 1
        #     if self._wheel_frame_count >= max_frames:
        #         self._is_spinning = False
        #         self._has_landed = True
        #
        #         # Calculate final alignment angle
        #         slice_angle = (2 * math.pi) / num_slices
        #         self._wheel_angle = -slice_angle * self.selected_index
        #         print(f"🎯 Final wheel stop on slice: {self.selected_index}")

        # Draw slices
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

        # Draw dividing lines
        for i in range(num_slices):
            angle = (2 * math.pi / num_slices) * i + self._wheel_angle
            end_x = int(center_x + radius * math.cos(angle))
            end_y = int(center_y + radius * math.sin(angle))
            pygame.draw.line(state.DISPLAY, WHITE, (center_x, center_y), (end_x, end_y), 2)

        # Draw arrow
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
        self.confirm_spin = False


    def draw_display_dice(self, state: 'GameState', player_dice_roll: int, enemy_dice_roll: int) -> None:
        player_dice_x_start_position = 50
        player_dice_y_start_position = 300
        enemy_dice_x_start_position = 600
        enemy_dice_y_start_position = 300
        dice_faces = [
            pygame.Rect(50, 0, 133, 200),  # Dice face 1=
            pygame.Rect(210, 0, 133, 200),  # Dice face 2
            pygame.Rect(370, 0, 133, 200),  # Dice face 3
            pygame.Rect(545, 0, 133, 200),  # Dice face 4
            pygame.Rect(710, 0, 133, 200),  # Dice face
            pygame.Rect(880, 0, 133, 200)  # Dice face 6p
        ]

        if self.game_state == self.INIT_SCREEN:
            player_dice_rect = dice_faces[player_dice_roll - 1]
            player_cropped_dice = self.sprite_sheet.subsurface(player_dice_rect)
            state.DISPLAY.blit(player_cropped_dice, (player_dice_x_start_position,player_dice_y_start_position))

            enemy_dice_rect = dice_faces[enemy_dice_roll - 1]
            enemy_cropped_dice = self.sprite_sheet.subsurface(enemy_dice_rect)
            state.DISPLAY.blit(enemy_cropped_dice, (enemy_dice_x_start_position, enemy_dice_y_start_position))
        elif self.game_state == self.PLAYER_TURN_SCREEN:
            player_dice_rect = dice_faces[player_dice_roll - 1]
            player_cropped_dice = self.sprite_sheet.subsurface(player_dice_rect)
            state.DISPLAY.blit(player_cropped_dice, (player_dice_x_start_position, player_dice_y_start_position))
        elif self.game_state == self.ENEMY_TURN_SCREEN:
            enemy_dice_rect = dice_faces[enemy_dice_roll - 1]
            enemy_cropped_dice = self.sprite_sheet.subsurface(enemy_dice_rect)
            state.DISPLAY.blit(enemy_cropped_dice, (enemy_dice_x_start_position, enemy_dice_y_start_position))

    @typechecked
    def update_card_effects(self, state) -> None:
        """Applies the effects of the currently drawn card."""
        index_to_card_constant = {
            0: self.BANKRUPT,
            1: self.EXP_HOLE,
            2: self.MAGIC_LOCK_UP,
            3: self.EQUIPMENT_LOCK_UP,
            4: self.MOVE_BACK_3,
            5: self.MID_POINT_MOVE,
            6: self.EXP_CARD_HALF_UP,
            7: self.GOLD_CARD_HALF_UP,
            8: self.GOLD_CARD_BONUS,
            9: self.EXP_CARD_BONUS,
            10: self.MOVE_3_SQUARES,
            11: self.TASTY_TREAT,
            12: self.MOVE_ENEMY_3,
            13: self.STAT_BOOSTER,
            14: self.FREE_WIN,
            15: self.PLAYER_MOVE_FORWARD,
            16: self.ENEMY_MOVE_BACK,
            17: self.ENEMY_MOVE_BACK_3,
            18: self.SWAP_POSITIONS,
            19: self.SPECIAL_ITEM,
        }
        self.CARD_CONSTANT = index_to_card_constant.get(self.selected_index)
        print(self.CARD_CONSTANT)

        print(self.player_money_pile)
        if self.CARD_CONSTANT == self.BANKRUPT:
            if self.player_turn == True:
                self.player_money_pile = 0
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_money_pile = 0
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.EXP_HOLE:
            if self.player_turn == True:
                self.player_exp_pile = 0
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_exp_pile = 0
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.MAGIC_LOCK_UP:
            if self.player_turn == True:
                self.player_magic_lock = True
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_magic_lock = True
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.EQUIPMENT_LOCK_UP:
            if self.player_turn == True:
                self.player_equipment_lock = True
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_equipment_lock = True
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.MOVE_BACK_3:
            if self.player_turn == True:
                self.player_position -= 3
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_position -= 3
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.MID_POINT_MOVE:
            if self.player_turn == True:
                self.player_position = 15
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_position = 15
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.EXP_CARD_HALF_UP:
            if self.player_turn == True:
                self.player_exp_pile += self.player_exp_pile // 2
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_exp_pile += self.enemy_exp_pile // 2
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.GOLD_CARD_HALF_UP:
            if self.player_turn == True:
                self.player_money_pile += self.player_money_pile // 2
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_money_pile += self.enemy_money_pile // 2
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.EXP_CARD_BONUS:
            if self.player_turn == True:
                self.player_exp_pile += 250
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_exp_pile += 250
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.GOLD_CARD_BONUS:
            if self.player_turn == True:
                self.player_money_pile += 250
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_money_pile += 250
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.MOVE_3_SQUARES:
            if self.player_turn == True:
                self.player_position += 3
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_position += 3
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.TASTY_TREAT:
            if self.player_turn == True:
                # create a fun in player that doesn't allow stam/focus to go above max
                state.player.stamina_points += 100
                state.player.focus_points += 50
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_hp += 4
                self.enemy_mp += 2
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.MOVE_ENEMY_3:
            if self.player_turn == True:
                self.enemy_position += 3
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.player_position += 3
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.STAT_BOOSTER:
            if self.player_turn == True:
                self.player_stat_boost += 1
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_stat_boost += 1
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.FREE_WIN:
            if self.player_turn == True:
                self.player_win_token += 1
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_win_token += 1
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.PLAYER_MOVE_FORWARD:
            if self.player_turn == True:
                self.player_move_boost += 1
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.enemy_move_boost += 1
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.ENEMY_MOVE_BACK:
            if self.player_turn == True:
                self.enemy_move_boost -= 1
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.player_move_boost -= 1
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.ENEMY_MOVE_BACK_3:
            if self.player_turn == True:
                self.enemy_position -= 3
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.player_position -= 3
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.SWAP_POSITIONS:
            self.player_position_holder = self.player_position
            self.enemy_position_holder = self.enemy_position
            self.player_position = self.enemy_position_holder
            self.enemy_position = self.player_position_holder
            if self.player_turn == True:
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
            elif self.enemy_turn == True:
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
        elif self.CARD_CONSTANT == self.SPECIAL_ITEM:
            if self.player_turn == True:
                print("he")
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN

            if self.enemy_turn == True:
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                print("me")

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











