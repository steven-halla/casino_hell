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

from game_constants.equipment import Equipment
from game_constants.events import Events
import random

from game_constants.magic import Magic


class WheelOfTortureVanessaBlackScreen(GambleScreen):
    def __init__(self, screenName: str = "wheel of torturett"):
        super().__init__(screenName)
        self.player_roll_choices: dict[tuple:str] = ["Roll", "Magic"]
        self.enemy_exp_move_modifier:int = 0
        self.player_rolled: bool = False
        self.enemy_rolled: bool = False
        self.confirm_spin: bool = False
        self.enemy_stat_boost: int = 0
        self.player_dice_roll: int = 0
        self.player_roll_dice_index: int = 0
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
        self.enemy_mp: int = 0
        self.enemy_hp: int = 500
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
        self.magic_dice: bool = False
        self.magic_dice_movement: int = 1

        self.player_turn: bool = True

        self.enemy_move_modifier: int = 0
        self.player_move_modifier: int = 0


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
            self.MAGIC_DICE_MESSAGE: MessageBox([
                "Vanessea : Magic dice time"
            ]),


        }



        # Initialize the card messages dictionary
        # Initialize the card messages dictionary in correct order
        self.card_messages: dict[str, MessageBox] = {
            self.BANKRUPT: MessageBox([
                "1) RED  Bankrupt – lose all money in pile"
            ]),
            self.EXP_HOLE: MessageBox([
                "2) RED  EXP BANKED – lose all EXP in pile"
            ]),
            self.MAGIC_LOCK_UP: MessageBox([
                "3) RED  Magic lock for rest of round"
            ]),
            self.EQUIPMENT_LOCK_UP: MessageBox([
                "4) RED Disable equipment for rest of round"
            ]),
            self.MOVE_BACK_3: MessageBox([
                "5) RED Move back 3 squares"
            ]),
            self.EXP_CARD_HALF_UP: MessageBox([
                "6) Increase EXP in pile by 50%"
            ]),
            self.GOLD_CARD_HALF_UP: MessageBox([
                "7) Increase gold in pile by 50%"
            ]),
            self.GOLD_CARD_BONUS: MessageBox([
                "8) Gain 250 gold"
            ]),
            self.EXP_CARD_BONUS: MessageBox([
                "9) Gain 250 EXP"
            ]),
            self.MOVE_3_SQUARES: MessageBox([
                "10) Move up 3 squares (10% board movement)"
            ]),
            self.TASTY_TREAT: MessageBox([
                "11) Gain +100 stamina + 50 focus"
            ]),
            self.MOVE_ENEMY_3: MessageBox([
                "12) RED Enemy moves forward 3 squares"
            ]),
            self.STAT_BOOSTER: MessageBox([
                "13) +1 to player’s luck, spirit, and magic"
            ]),
            self.FREE_WIN: MessageBox([
                "14) Player v enemy roll: winner gets a free win."
            ]),
            self.PLAYER_MOVE_FORWARD: MessageBox([
                "15) +1 movement for player (rest of round)"
            ]),
            self.ENEMY_MOVE_BACK: MessageBox([
                "16) -1 movement for enemy (rest of round)"
            ]),
            self.ENEMY_MOVE_BACK_3: MessageBox([
                "17) Move enemy back 3 squares (10% board movement)"
            ]),
            self.MID_POINT_MOVE: MessageBox([
                "18) Move to mid point on map"
            ]),
            self.SWAP_POSITIONS: MessageBox([
                "19) Swap positions with enemy"
            ]),
            self.SPECIAL_ITEM: MessageBox([
                "20) Gain special item or 1000 gold (enemy loses -1000 gold from player pile)"
            ]),
        }


    SPIN_WHEEL_SCREEN: str = "spin wheel screen"
    MAGIC_DICE_SCREEN: str = "magic dice screen"
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
    MAGIC_DICE_MESSAGE: str = "magic dice message"



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
        self.enemy_money_pile = 100
        # self.exp_pile = 100


        #^-------TESTING---------^#

        self.spirit_bonus: int = state.player.spirit * 10
        self.magic_bonus: int = state.player.mind * 10
        self.card_constants: list[str] = [
            self.BANKRUPT,  # 0
            self.EXP_HOLE,  # 1
            self.MAGIC_LOCK_UP,  # 2
            self.EQUIPMENT_LOCK_UP,  # 3
            self.MOVE_BACK_3,  # 4
            self.EXP_CARD_HALF_UP,  # 5
            self.GOLD_CARD_HALF_UP,  # 6
            self.GOLD_CARD_BONUS,  # 7
            self.EXP_CARD_BONUS,  # 8
            self.MOVE_3_SQUARES,  # 9
            self.TASTY_TREAT,  # 10
            self.MOVE_ENEMY_3,  # 11
            self.STAT_BOOSTER,  # 12
            self.FREE_WIN,  # 13
            self.PLAYER_MOVE_FORWARD,  # 14
            self.ENEMY_MOVE_BACK,  # 15
            self.ENEMY_MOVE_BACK_3,  # 16
            self.MID_POINT_MOVE,  # 17 ✅ moved here
            self.SWAP_POSITIONS,  # 18
            self.SPECIAL_ITEM  # 19
        ]

        self.card_constants: list[str] = [
            self.BANKRUPT,  # 0
            self.EXP_HOLE,  # 1
            self.MAGIC_LOCK_UP,  # 2
            self.EQUIPMENT_LOCK_UP,  # 3
            self.MOVE_BACK_3,  # 4
            self.EXP_CARD_HALF_UP,  # 5
            self.GOLD_CARD_HALF_UP,  # 6
            self.GOLD_CARD_BONUS,  # 7
            self.EXP_CARD_BONUS,  # 8
            self.MOVE_3_SQUARES,  # 9
            self.TASTY_TREAT,  # 10
            self.MOVE_ENEMY_3,  # 11
            self.STAT_BOOSTER,  # 12
            self.FREE_WIN,  # 13
            self.PLAYER_MOVE_FORWARD,  # 14
            self.ENEMY_MOVE_BACK,  # 15
            self.ENEMY_MOVE_BACK_3,  # 16
            self.MID_POINT_MOVE,  # 17
            self.SWAP_POSITIONS,  # 18
            self.SPECIAL_ITEM  # 19
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
        print("Player tokens at:" + str(self.player_win_token))
        print("Enemy tokens at:" + str(self.enemy_win_token))
        print("player money at:" + str(self.player_money_pile))
        print("Enemy money at:" + str(self.enemy_money_pile))
        if self.enemy_exp_pile >= 1000:
            self.enemy_exp_move_modifier += 1
            self.enemy_exp_pile -= 1000

        self.confirm_spin = False
        self.player_magic_lock = False
        self.player_equipment_lock = False
        self.enemy_equipment_lock = False
        self.enemy_magic_lock = False
        self.used_wheel_indices.clear()
        self.player_turn = False
        self.enemy_turn = False
        self.player_position = 0
        self.enemy_position = 0
        self.enemy_move_modifier: int = 0
        self.player_move_modifier: int = 0


        self.card_constants: list[str] = [
            self.BANKRUPT,  # 0
            self.EXP_HOLE,  # 1
            self.MAGIC_LOCK_UP,  # 2
            self.EQUIPMENT_LOCK_UP,  # 3
            self.MOVE_BACK_3,  # 4
            self.EXP_CARD_HALF_UP,  # 5
            self.GOLD_CARD_HALF_UP,  # 6
            self.GOLD_CARD_BONUS,  # 7
            self.EXP_CARD_BONUS,  # 8
            self.MOVE_3_SQUARES,  # 9
            self.TASTY_TREAT,  # 10
            self.MOVE_ENEMY_3,  # 11
            self.STAT_BOOSTER,  # 12
            self.FREE_WIN,  # 13
            self.PLAYER_MOVE_FORWARD,  # 14
            self.ENEMY_MOVE_BACK,  # 15
            self.ENEMY_MOVE_BACK_3,  # 16
            self.MID_POINT_MOVE,  # 17 ✅ moved here
            self.SWAP_POSITIONS,  # 18
            self.SPECIAL_ITEM  # 19
        ]


    def update(self, state):
        # print(f"🎯 Player landed on: {self.board_squares[self.player_position]}")
        # print(f"🎯 ENEMYT landed on: {self.board_squares[self.enemy_position]}")
        # print(self.CARD_CONSTANT)
        # print("Player roll is " + str(self.player_dice_roll))
        # print("enemy roll is " + str(self.enemy_dice_roll))
        # print(self.game_state)
        if self.player_win_token >= 3:
            print("Plyer winss!!!")
        elif self.enemy_win_token >= 3:
            print("ENEMY WINSQWRERFEW######")

        if state.controller.isEPressed:
            print("PLayer money is at: " + str(self.player_money_pile))
            print("Enemy money is at: " + str(self.enemy_money_pile))

        if self.player_money_pile < 0:
            self.player_money_pile = 0
        if self.enemy_money_pile < 0:
            self.enemy_money_pile = 0



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


            # print(self.player_roll_dice_index)


            if controller.up_button:

                self.menu_movement_sound.play()
                # the % modulus  operator keeps our number in the index range
                self.player_roll_dice_index = (self.player_roll_dice_index
                                             - self.move_index_by_1) % len(self.player_roll_choices)
            elif controller.down_button:

                self.menu_movement_sound.play()
                self.player_roll_dice_index = (self.player_roll_dice_index
                                             + self.move_index_by_1) % len(self.player_roll_choices)



            self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].update(state)

            if state.controller.confirm_button:

                if not self.player_rolled:
                    if self.player_roll_dice_index == 0:
                        if not self.magic_dice:
                            self.move_player = random.randint(1, 6) + self.player_move_modifier
                        else:
                            self.move_player = self.magic_dice_movement + self.player_move_modifier

                        self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].messages = [
                            f"PLAYER rolled a {self.move_player}."
                        ]
                        self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].reset()  # important!
                        self.player_rolled = True  # ✅ Now wait one cycle

                    elif self.player_roll_dice_index == 1:
                        self.game_state = self.MAGIC_MENU_SCREEN

                else:
                    self.update_roll_dice_player_enemy_roll_phase(state)
                    self.player_rolled = False

        elif self.game_state == self.MAGIC_MENU_SCREEN:
            print(self.magic_menu_index)
            if controller.up_button:
                self.menu_movement_sound.play()
                self.magic_menu_index = (self.magic_menu_index - self.index_stepper) % len(self.magic_screen_choices)
            elif controller.down_button:
                self.menu_movement_sound.play()
                self.magic_menu_index = (self.magic_menu_index + self.index_stepper) % len(self.magic_screen_choices)
            if state.controller.confirm_button:
                if self.magic_menu_index == 0:
                    self.magic_dice_movement = 1
                    self.magic_dice = True
                    self.game_state = self.MAGIC_DICE_SCREEN
                if self.magic_menu_index == 1:
                    self.game_state = self.PLAYER_TURN_SCREEN

        elif self.game_state == self.MAGIC_DICE_SCREEN:

            self.battle_messages[self.MAGIC_DICE_MESSAGE].messages = [
                f"Press up and down to change values. Dice is set to {self.magic_dice_movement}"
            ]
            self.battle_messages[self.MAGIC_DICE_MESSAGE].update(state)

            if state.controller.up_button:
                self.magic_dice_movement += 1

            if state.controller.down_button:
                self.magic_dice_movement -= 1

            if self.magic_dice_movement < 1:
                self.magic_dice_movement = 1

            if self.magic_dice_movement > 6:
                self.magic_dice_movement = 6

            if state.controller.confirm_button:
                self.game_state = self.PLAYER_TURN_SCREEN





        elif self.game_state == self.ENEMY_TURN_SCREEN:
            self.magic_dice = False
            if not self.enemy_rolled:
                self.move_dealer = random.randint(1, 6) + self.enemy_move_modifier
                # self.move_dealer = 4 + self.enemy_move_modifier
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
        font = pygame.font.SysFont("Arial", 24)

        player_info = [
            f"Player Money: {self.player_money_pile}",
            f"Player EXP: {self.player_exp_pile}",
            f"Player Position: {self.player_position}",
            f"Player Space: {self.board_squares[self.player_position]}"
        ]

        enemy_info = [
            f"Enemy Money: {self.enemy_money_pile}",
            f"Enemy EXP: {self.enemy_exp_pile}",
            f"Enemy Position: {self.enemy_position}",
            f"Enemy Space: {self.board_squares[self.enemy_position]}"
        ]

        # Draw player info (bottom-left)
        for i, text in enumerate(player_info):
            rendered = font.render(text, True, WHITE)
            state.DISPLAY.blit(rendered, (30, 500 + i * 25))

        # Draw enemy info (bottom-left, right under player info)
        for i, text in enumerate(enemy_info):
            rendered = font.render(text, True, WHITE)
            state.DISPLAY.blit(rendered, (400, 500 + i * 25))
        if self.game_state == self.WELCOME_SCREEN:
            self.battle_messages[self.WELCOME_SCREEN_MESSAGE].draw(state)


        elif self.game_state == self.INIT_SCREEN:
            self.battle_messages[self.INIT_SCREEN_MESSAGE].draw(state)

            self.draw_display_dice(state, self.player_dice_roll, self.enemy_dice_roll)


        # elif self.game_state == self.SPIN_WHEEL_SCREEN:
        #     self.draw_wheel(state)
        elif self.game_state == self.PLAYER_TURN_SCREEN:
            self.battle_messages[self.PLAYER_TURN_SCREEN_MESSAGE].draw(state)

            self.draw_player_roll_screen_box_info(state)
            self.draw_player_roll_menu_selection_box(state)

            self.draw_display_dice(state, self.move_player, 0)




        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box(state)







        elif self.game_state == self.MAGIC_DICE_SCREEN:
            self.battle_messages[self.MAGIC_DICE_MESSAGE].draw(state)

        elif self.game_state == self.ENEMY_TURN_SCREEN:
            self.battle_messages[self.ENEMY_TURN_SCREEN_MESSAGE].draw(state)

            self.draw_display_dice(state, 0, self.move_dealer)
        elif self.game_state == self.SPIN_WHEEL_SCREEN:
            self.draw_wheel(state)  # This updates the wheel's animation

            if self._has_landed:
                # Start the pause timer if it hasn't been started yet
                if not hasattr(self, "_pause_timer"):
                    self._pause_timer = pygame.time.get_ticks()

                # Check if 1 second has passed
                elif pygame.time.get_ticks() - self._pause_timer >= 1000:
                    self._has_landed = False  # ✅ Clear after the pause finishes
                    del self._pause_timer
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

    # @typechecked
    # def update_wheel_result(self) -> None:
    #     self.player_exp_pile = 1000
    #     """TEMP TEST: Force MID_POINT_MOVE at index 17 every time."""
    #     self.selected_index = 5 # MID_POINT_MOVE
    #     self.used_wheel_indices.add(5)
    #     self.confirm_spin = True
    #     self.wheel_lock = True
    #     print("🎯 Index 5 = EXP_CARD_HALF_UP")
    #     print(f"🎴 Your CARD_CONSTANT is: {self.CARD_CONSTANT}")
    #     return

    @typechecked
    def update_wheel_result(self) -> None:
        """Rolls 1–100 and sets the selected slice index based on chance. Returns the selected index."""
        roll: int = random.randint(1, 100)

        red_indices = [1, 5, 9, 13, 15, 17]
        # red_indices = [1, 5, 9, 13, 15, 17, 4]
        green_indices = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 19]
        purple_indices = [3, 11]
        sky_blue_index = 7
        all_indices = set(range(20))
        used_indices = self.used_wheel_indices

        # Determine available indices for each color
        available_red = [i for i in red_indices if i not in used_indices]
        available_sky_blue = [sky_blue_index] if sky_blue_index not in used_indices else []
        available_purple = [i for i in purple_indices if i not in used_indices]
        available_green = list(all_indices - used_indices - set(red_indices + [sky_blue_index] + purple_indices))

        # Select index based on roll
        # These rolls trigger exact slices for their color
        red_rolls = [1, 5, 9, 13, 15, 17]
        green_rolls = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        purple_rolls = [3, 11]
        sky_blue_rolls = [7]

        if roll in red_rolls and available_red:
            self.selected_index = random.choice(available_red)
            # print(f"DEBUG RED: roll={roll}, available_red={available_red}")

        elif roll in green_rolls and available_green:
            self.selected_index = random.choice(available_green)
            # print(f"DEBUG GREEN: roll={roll}, available_green={available_green}")

        elif roll in purple_rolls and available_purple:
            self.selected_index = random.choice(available_purple)
            # print(f"DEBUG PURPLE: roll={roll}, available_purple={available_purple}")

        elif roll in sky_blue_rolls and available_sky_blue:
            self.selected_index = sky_blue_index
            # print(f"DEBUG SKY_BLUE: roll={roll}, available_sky_blue={available_sky_blue}")
        else:
            # Fallback: select any unused index
            remaining_indices = list(all_indices - used_indices)
            if not remaining_indices:
                # print("⚠️ All wheel indices have been used this round.")
                return -1  # Indicate that no selection was made
            self.selected_index = random.choice(remaining_indices)

        # Mark the selected index as used
        self.used_wheel_indices.add(self.selected_index)
        self.confirm_spin = True

        # print(f"🎯 Wheel result roll: {roll} → selected_index: {self.selected_index}")
        self.wheel_lock = True

    def update_init_screen_helper(self, state):
        if not self.dice_rolled:
            self.player_dice_roll = random.randint(1, 6)
            # self.enemy_dice_roll = random.randint(1, 6)
            self.enemy_dice_roll = 0
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
            return

        self.CARD_CONSTANT = selected_card
        self.card_messages[selected_card].reset()

        for line in self.card_messages[selected_card].messages:
            print(f"📜 Message: {line}")


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
            # print(self.move_player)
            #
            # print("Hi")
            self.player_position += self.move_player
            if self.player_position > 29:

                if self.player_money_pile >= 1000:
                    print("Player gets the win")
                    self.player_money_pile -= 1000
                    self.player_win_token += 1
                    self.player_position = 29

                elif self.player_money_pile <= 1000:
                    self.player_money_pile += 250
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
            # print(self.move_dealer)

            # print("Hi")
            self.enemy_position += self.move_dealer
            if self.enemy_position > 29:
                if self.enemy_money_pile >= 1000:
                    if Equipment.SIR_LEOPOLDS_RING.value in state.player.equipped_items:
                        self.player_money_pile += 250



                    print("enemy gets the win")
                    self.enemy_money_pile -= 1000
                    self.enemy_win_token += 1
                    self.enemy_position = 29

                elif self.enemy_money_pile <= 1000:
                    if Equipment.SIR_LEOPOLDS_RING.value in state.player.equipped_items:
                        self.player_money_pile += 250
                    self.enemy_money_pile += 250
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
                self.player_money_pile += 250
                print("💰 Player GOLD_SQUARE: +25 gold!")
                self.game_state = self.ENEMY_TURN_SCREEN
                self.player_turn = False
                self.enemy_turn = True

            elif self.enemy_turn == True:
                self.enemy_money_pile += 250
                print("💰 Enemy GOLD_SQUARE: +25 gold!")
                self.game_state = self.PLAYER_TURN_SCREEN
                self.enemy_turn = False
                self.player_turn = True




        elif square_type == self.EXP_SQUARE:
            if self.player_turn == True:
                self.player_exp_pile += 250
                print("📘 Player EXP_SQUARE: +25 EXP!")
                self.game_state = self.ENEMY_TURN_SCREEN
                self.player_turn = False
                self.enemy_turn = True

            elif self.enemy_turn == True:
                self.enemy_exp_pile += 250
                self.game_state = self.PLAYER_TURN_SCREEN
                self.player_turn = True

                self.enemy_turn = False
                print("📘 Enemy EXP_SQUARE: +25 EXP!")

        elif square_type == self.TRAP_SQUARE:
            if self.player_turn == True:
                state.player.stamina_points -= 100
                state.player.focus_points -= 50
                self.game_state = self.ENEMY_TURN_SCREEN
                self.player_turn = False
                self.enemy_turn = True

                print("💀 Player TRAP_SQUARE: -25 Stamina, -25 Focus!")
            elif self.enemy_turn == True:
                self.enemy_hp -= 100
                self.enemy_mp -= 50
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
                # self.game_state = self.PLAYER_TURN_SCREEN
                # self.enemy_turn = False
                # self.player_turn = True


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
        token_size: int = 15
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
        center_x = 400
        center_y = 300
        radius = 150
        num_slices = 20
        spin_speed = 0.10

        # Local wheel colors (no self)
        wheel_colors = [
            (255, 0, 0),  # 0  RED
            (0, 255, 0),  # 1  GREEN
            (0, 0, 255),  # 2  BLUE
            (255, 255, 0),  # 3  YELLOW
            (255, 165, 0),  # 4  ORANGE
            (128, 0, 128),  # 5  PURPLE
            (0, 255, 255),  # 6  CYAN
            (255, 192, 203),  # 7  PINK
            (210, 105, 30),  # 8  CHOCOLATE
            (0, 128, 128),  # 9  TEAL
            (173, 216, 230),  # 10 LIGHT BLUE
            (255, 20, 147),  # 11 DEEP PINK
            (154, 205, 50),  # 12 YELLOW GREEN
            (139, 69, 19),  # 13 SADDLE BROWN
            (0, 100, 0),  # 14 DARK GREEN
            (255, 99, 71),  # 15 TOMATO
            (70, 130, 180),  # 16 STEEL BLUE
            (128, 128, 0),  # 17 OLIVE
            (255, 140, 0),  # 18 DARK ORANGE
            (199, 21, 133)  # 19 MEDIUM VIOLET RED
        ]

        # Initialize internal state
        if not hasattr(self, "_wheel_angle"):
            self._wheel_angle = 0.0
        if not hasattr(self, "_has_landed"):
            self._has_landed = False
        if not hasattr(self, "delay_start_time"):
            self.delay_start_time = None

        # Start spin if needed
        if self.confirm_spin and self.delay_start_time is None and not self._has_landed:
            self.delay_start_time = pygame.time.get_ticks()

        # Spin and snap logic
        if self.delay_start_time is not None and not self._has_landed:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.delay_start_time

            slice_angle = (2 * math.pi) / num_slices
            angle_offset = slice_angle * 0.5  # Adjust as needed
            target_angle = (2 * math.pi) + (-slice_angle * self.selected_index + angle_offset)

            if elapsed < 2000:
                self._wheel_angle += spin_speed
            else:
                self._wheel_angle += spin_speed
                if abs((self._wheel_angle % (2 * math.pi)) - (target_angle % (2 * math.pi))) <= 0.05:
                    self._wheel_angle = target_angle
                    self._has_landed = True
                    self.delay_start_time = None
                    selected_color = wheel_colors[self.selected_index]
                    print(f"🎨 Landed on color: {selected_color} at index {self.selected_index}")

        # Draw pie slices
        slice_angle = (2 * math.pi) / num_slices
        angle_offset = slice_angle * 0.2
        for i in range(num_slices):
            angle_start = slice_angle * i + self._wheel_angle + angle_offset
            angle_end = slice_angle * (i + 1) + self._wheel_angle + angle_offset

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

        # Draw slice dividers
        for i in range(num_slices):
            angle = slice_angle * i + self._wheel_angle + angle_offset
            end_x = int(center_x + radius * math.cos(angle))
            end_y = int(center_y + radius * math.sin(angle))
            pygame.draw.line(state.DISPLAY, (255, 255, 255), (center_x, center_y), (end_x, end_y), 2)

        # Draw arrow
        arrow_x, arrow_y = center_x, center_y - radius - 10
        pygame.draw.polygon(
            state.DISPLAY, (255, 0, 0),
            [
                (arrow_x, arrow_y),
                (arrow_x - 10, arrow_y - 15),
                (arrow_x + 10, arrow_y - 15)
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
            5: self.EXP_CARD_HALF_UP,
            6: self.GOLD_CARD_HALF_UP,
            7: self.GOLD_CARD_BONUS,
            8: self.EXP_CARD_BONUS,
            9: self.MOVE_3_SQUARES,
            10: self.TASTY_TREAT,
            11: self.MOVE_ENEMY_3,
            12: self.STAT_BOOSTER,
            13: self.FREE_WIN,
            14: self.PLAYER_MOVE_FORWARD,
            15: self.ENEMY_MOVE_BACK,
            16: self.ENEMY_MOVE_BACK_3,
            17: self.MID_POINT_MOVE,
            18: self.SWAP_POSITIONS,
            19: self.SPECIAL_ITEM,
        }
        self.CARD_CONSTANT = index_to_card_constant.get(self.selected_index)
        print(self.CARD_CONSTANT)

        print(self.player_money_pile)
        if self.CARD_CONSTANT == self.BANKRUPT:
            if self.player_turn == True:
                print("YOU DREW THE BANKRUP CARD")

                self.player_money_pile = 0
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                return
                # print("Player money is after bankrupted: " + str(self.player_money_pile))
            elif self.enemy_turn == True:
                self.enemy_money_pile = 0
                print("YOU DREW THE BANKRUP CARD")

                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.EXP_HOLE:
            print("YOU REAW THE EXP HOLD CARD")

            if self.player_turn == True:
                self.player_exp_pile = 0
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                # print("Player exp is after " + str(self.player_exp_pile))
                return
            elif self.enemy_turn == True:
                self.enemy_exp_pile = 0
                print("YOU REAW THE EXP HOLD CARD")

                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.MAGIC_LOCK_UP:
            print("You drew magic lock up")
            if self.player_turn == True:
                self.player_magic_lock = True
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                print("Player magic lock up should be True:  " + str(self.player_magic_lock))
                return
            elif self.enemy_turn == True:
                self.enemy_magic_lock = True
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.EQUIPMENT_LOCK_UP:
            print("You drew equp lock up")
            if self.player_turn == True:
                self.player_equipment_lock = True
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                print("Player Equipment lock up should be True:  " + str(self.player_equipment_lock))
                return

            elif self.enemy_turn == True:
                self.enemy_equipment_lock = True
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.MOVE_BACK_3:
            print("You drew move back 3")

            if self.player_turn == True:
                self.player_position -= 3
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.enemy_position -= 3
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.MID_POINT_MOVE:
            print("you drew mid point move")
            if self.player_turn == True:
                print(f"CARD_CONSTANT: {self.CARD_CONSTANT}")
                print(f"MID_POINT_MOVE: {self.MID_POINT_MOVE}")
                print(self.CARD_CONSTANT == self.MID_POINT_MOVE)
                self.player_position = 15
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                print(f"CARD_CONSTANT: {self.CARD_CONSTANT}")
                print(f"MID_POINT_MOVE: {self.MID_POINT_MOVE}")
                print(self.CARD_CONSTANT == self.MID_POINT_MOVE)
                self.enemy_position = 15
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.EXP_CARD_HALF_UP:
            print("You drew exp card half up")
            # print(f"[DEBUG] CARD_CONSTANT at APPLY_CARD_SCREEN: {self.CARD_CONSTANT}")

            if self.player_turn == True:
                self.player_exp_pile += self.player_exp_pile // 2
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                print("fdasfdsafdsfsda   Player exp is after " + str(self.player_exp_pile))
                return

            elif self.enemy_turn == True:
                self.enemy_exp_pile += self.enemy_exp_pile // 2
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.GOLD_CARD_HALF_UP:
            print("You drew gold card half up")
            if self.player_turn == True:
                self.player_money_pile += self.player_money_pile // 2
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.enemy_money_pile += self.enemy_money_pile // 2
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.EXP_CARD_BONUS:
            print("You get the exp card bonus card")
            if self.player_turn == True:
                self.player_exp_pile += 250
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.enemy_exp_pile += 250
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.GOLD_CARD_BONUS:
            print("You get the gold card bonus card")
            if self.player_turn == True:
                self.player_money_pile += 250
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.enemy_money_pile += 250
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.MOVE_3_SQUARES:
            print("You get the move 3 squres card")
            if self.player_turn == True:
                self.player_position += 3
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.enemy_position += 3
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.TASTY_TREAT:
            print("You get the teasty treat card")
            if self.player_turn == True:
                # create a fun in player that doesn't allow stam/focus to go above max
                state.player.stamina_points += 100
                state.player.focus_points += 50
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.enemy_hp += 200
                # self.enemy_mp += 2
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.MOVE_ENEMY_3:
            print("You get the move enemy 3 card")
            if self.player_turn == True:
                self.enemy_position += 3
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.player_position += 3
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.STAT_BOOSTER:
            print("you get the state booster card")

            if self.player_turn == True:
                self.player_stat_boost += 1
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.enemy_stat_boost += 1
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.FREE_WIN:
            print("You get the free win card")
            if self.player_turn == True:
                self.player_win_token += 1
                self.player_turn = False
                self.enemy_turn = True
                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.enemy_win_token += 1
                self.player_turn = True
                self.enemy_turn = False
                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.PLAYER_MOVE_FORWARD:
            print("You get the player move forward card + 1 move entire roun")
            if self.player_turn == True:
                self.player_turn = False
                self.enemy_turn = True
                self.player_move_modifier += 1

                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.player_turn = True
                self.enemy_turn = False
                self.enemy_move_modifier += 1

                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.ENEMY_MOVE_BACK:
            print("You get the enemy move back card enemy moves back  1 entire round")
            if self.player_turn == True:
                self.player_turn = False
                self.enemy_turn = True
                self.enemy_move_modifier -= 1

                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.player_turn = True
                self.enemy_turn = False
                self.player_move_modifier -= 1

                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.ENEMY_MOVE_BACK_3:
            print("you get the nemeyh move back 3 card")
            if self.player_turn == True:

                self.player_turn = False
                self.enemy_turn = True
                self.enemy_position -= 3

                self.game_state = self.ENEMY_TURN_SCREEN
                return
            elif self.enemy_turn == True:
                self.player_turn = True
                self.enemy_turn = False
                self.player_position -= 3

                self.game_state = self.PLAYER_TURN_SCREEN
                return
        elif self.CARD_CONSTANT == self.SWAP_POSITIONS:
            print("You get the swap positions card")
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
            print("You get the special item card")
            if self.player_turn == True:
                print("he")
                self.player_turn = False
                self.enemy_turn = True
                self.player_money_pile += 1000
                self.game_state = self.ENEMY_TURN_SCREEN

                return
            if self.enemy_turn == True:
                self.player_turn = True
                self.enemy_turn = False
                self.enemy_money_pile += 1000

                self.game_state = self.PLAYER_TURN_SCREEN
                return

    # Enemy mid move is not working need to check enemy cards

    def draw_player_roll_menu_selection_box(self, state):
        # if Magic.BLACK_JACK_REDRAW.value in state.player.magicinventory:
        #     if self.magic_menu_index == 0:
        #         self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].draw(state)
        #     elif self.magic_menu_index == 1:
        #         self.battle_messages[self.MAGIC_MENU_REDRAW_DESCRIPTION].draw(state)
        #     elif self.magic_menu_index == 2:
        #         self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)
        # elif Magic.BLACK_JACK_REDRAW.value not in state.player.magicinventory:
        #     if self.magic_menu_index == 0:
        #         self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].draw(state)
        #     elif self.magic_menu_index == 1:
        #         self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)
        choice_spacing = 40
        text_x_offset = 60
        text_y_offset = 15
        arrow_x_offset = 12
        black_box_height = 221 - 50
        black_box_width = 200 - 10
        border_width = 5
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
        start_y_right_box = 240
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
        #
        # if (Magic.DICE_FORCE.value in state.player.magicinventory
        #         and Magic.DICE_FORCE.value not in self.magic_screen_choices):
        #     self.magic_screen_choices.insert(1, Magic.DICE_FORCE.value)

        for idx, choice in enumerate(self.player_roll_choices):
            y_position = start_y_right_box + idx * choice_spacing  # Use dynamic spacing
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        arrow_y_coordinate = start_y_right_box + self.player_roll_dice_index * choice_spacing
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_coordinate + text_y_offset)  # Align arrow with the text
        )

    def draw_magic_menu_selection_box(self, state):
        # if Magic.BLACK_JACK_REDRAW.value in state.player.magicinventory:
        #     if self.magic_menu_index == 0:
        #         self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].draw(state)
        #     elif self.magic_menu_index == 1:
        #         self.battle_messages[self.MAGIC_MENU_REDRAW_DESCRIPTION].draw(state)
        #     elif self.magic_menu_index == 2:
        #         self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)
        # elif Magic.BLACK_JACK_REDRAW.value not in state.player.magicinventory:
        #     if self.magic_menu_index == 0:
        #         self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].draw(state)
        #     elif self.magic_menu_index == 1:
        #         self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)
        choice_spacing = 40
        text_x_offset = 60
        text_y_offset = 15
        arrow_x_offset = 12
        black_box_height = 221 - 50
        black_box_width = 200 - 10
        border_width = 5
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
        start_y_right_box = 240
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

        if (Magic.DICE_FORCE.value in state.player.magicinventory
                and Magic.DICE_FORCE.value not in self.magic_screen_choices):
            self.magic_screen_choices.insert(0, Magic.DICE_FORCE.value)

        for idx, choice in enumerate(self.magic_screen_choices):
            y_position = start_y_right_box + idx * choice_spacing  # Use dynamic spacing
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        arrow_y_coordinate = start_y_right_box + self.magic_menu_index * choice_spacing
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_coordinate + text_y_offset)  # Align arrow with the text
        )

    def draw_player_roll_screen_box_info(self, state: 'GameState'):
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

        for idx, choice in enumerate(self.player_roll_choices):
            y_position = start_y_right_box + idx * spacing_between_choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        # if Magic.REVEAL.value not in state.player.magicinventory:
        #     self.magic_lock = True
        #     self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        # elif Magic.REVEAL.value in state.player.magicinventory:
        #     self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        # if self.magic_lock == True:
        #     self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        # elif self.magic_lock == False:
        #     self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if self.player_roll_dice_index == 0:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box
                 + arrow_y_coordinate_padding_play)
            )
        elif self.player_roll_dice_index == 1:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box
                 + arrow_y_coordinate_padding_magic)
            )
        # elif self.welcome_screen_index == self.welcome_screen_bet_index:
        #     state.DISPLAY.blit(
        #         self.font.render("->", True, WHITE),
        #         (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box
        #          + arrow_y_coordinate_padding_bet)
        #     )
        # elif self.welcome_screen_index == self.welcome_screen_quit_index:
        #     state.DISPLAY.blit(
        #         self.font.render("->", True, WHITE),
        #         (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box
        #          + arrow_y_coordinate_padding_quit)
        #     )











