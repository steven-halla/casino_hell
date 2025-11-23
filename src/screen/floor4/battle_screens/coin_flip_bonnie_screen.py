import random
import math
import os
import pygame

from constants import WHITE, BLACK, RED
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.coin_flip_constants import CoinFlipConstants
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic
from game_constants.player_magic.coin_flip_magic import CoinFlipMagic


class CoinFlipBonnieScreen(GambleScreen):
# have all coin flips be a 1-100 but if its 100% then set the value to 100
    def __init__(self, screenName: str = "Coin FLip") -> None:
        super().__init__(screenName)
        self.bet:int = 100
        self.dealer_name: str = "Bonnie"
        self.initial_coin_image_position: tuple[int, int] = (300, 250)
        self.timer_start:bool = None
        self.coin_bottom:bool = False
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        self.sprite_sheet = pygame.image.load("./assets/images/coin_flipping_alpha.png").convert_alpha()
        self.game_state: str = self.WELCOME_SCREEN
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.heads_or_tails_menu: list[str] = ["Heads", "Tails", "Back"]
        self.magic_menu_selector: list[str] = []
        self.welcome_screen_index: int = 0
        self.spell_sound = pygame.mixer.Sound("./assets/music/spell_sound.mp3")
        self.spell_sound.set_volume(0.3)
        self.phase: int = 1
        self.flip_coin_index: int = 0
        self.magic_index: int = 1
        self.bet_index: int = 2
        self.shield_debuff_inactive = 0
        self.quit_index: int = 3
        self.headstailsindex: int = 0
        self.image_to_display:str = ""
        self.heads_image = pygame.image.load(os.path.join("./assets/images/heads.png"))
        self.tails_image = pygame.image.load(os.path.join(("./assets/images/tails.png")))
        self.menu_movement_sound = pygame.mixer.Sound("./assets/music/1BItemMenuItng.wav")
        self.menu_movement_sound.set_volume(0.2)
        self.player_choice:str = ""
        self.coin_landed:str = CoinFlipConstants.HEADS.value
        self.double_coin_landed:str = CoinFlipConstants.HEADS.value
        self.bonnie_bankrupt: int = 0
        self.magic_lock = False
        self.low_stamina_drain: int = 10
        self.index_stepper: int = 1
        self.magic_screen_index: int = 0
        self.shield_cost: int = 30
        self.shield_debuff: int = 0
        self.heads_force_cost: int = 50
        self.heads_force_active: bool = False
        self.exp_gain_high: int = 1
        self.exp_gain_low: int = 1
        self.result_anchor: bool = False
        self.money: int = 999
        self.bonnie_magic_points: int = 2
        self.debuff_double_flip: int = 0
        self.even: bool = False
        self.odd: bool = False
        self.tri = False
        self.double_flip_chance: int = 0
        self.spirit_bonus: int = 0
        self.magic_bonus: int = 0


        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "Bonnie: It's been a while since I last had a decent challenge."
            ]),
            self.BET_MESSAGE: MessageBox([
                "Min bet of 50, max of 200. Press up and down keys to increase/decrease bet. Press B to go back."
            ]),
            self.MAGIC_MENU_SHIELD_DESCRIPTION: MessageBox([
                "The animals of hell are on your side. Defends against bad flips."
            ]),
            self.MAGIC_MENU_FORCE_DESCRIPTION: MessageBox([
                "Using physics you can get the coin to land on heads every time."
            ]),
            self.MAGIC_MENU_BACK_DESCRIPTION: MessageBox([
                "go back to previous menu"
            ]),
            self.COIN_FLIP_MESSAGE: MessageBox([
                "Coin is flipping oh boy I wonder where it will land?"
            ]),
            self.CHOOSE_SIDE_MESSAGE: MessageBox([
                "Pick Heads or Tails."
            ]),
            self.PLAYER_WIN_MESSAGE: MessageBox([
                "You won the toss!!!"
            ]),
            self.PLAYER_LOSE_MESSAGE: MessageBox([
                "You lost the toss."
            ]),
            self.PLAYER_DRAW_MESSAGE: MessageBox([
                f"The Birdy of Hell snatched the coin, it's a DRAW! You win 0 gold and win {self.exp_gain_low} experience points"
            ]),
            self.LEVEL_UP_MESSAGE: MessageBox([
                f"You leveld up!"
            ]),
            self.ANIMAL_DEFENSE_MESSAGE: MessageBox([
                f"A lucky bird swooped in to help you out of a jam!"
            ]),
            # if player gets first flip, then we flip one more time.
            #  Heads force only works for first flip not 2nd
            self.BONNIE_CASTING_SPELL_MESSAGE: MessageBox([
                f"Gods of darkness and strife,accept this unholy sacrifice and  increase my power times 2...double flip!Ï"
            ]),
        }

    # dont draw the coin if its a draw, or maybe draw a bird or animal in its place that "stole/ate
    # the coin.

    # maybe give extra EXP for luck stat , higher luck higher % to get extra exp , money

    COIN_FLIP_SCREEN: str = "coin_flip_screen"
    BACK: str = "Back"
    RESULTS_SCREEN: str = "results_screen"
    CHOOSE_SIDE_SCREEN: str = "choose_side_screen"
    PLAYER_WIN_SCREEN: str = "player_win_screen"
    PLAYER_LOSE_SCREEN: str = "player_lose_screen"
    PLAYER_DRAW_SCREEN: str = "player_draw_screen"
    BONNIE_CASTING_SPELL_SCREEN: str = "BONNIE_CASTING_SPELL_SCREEN"
    LEVEL_UP_MESSAGE: str = "level_up_message"
    ANIMAL_DEFENSE_MESSAGE: str = "animal defense message"
    PLAYER_WIN_MESSAGE: str = "player_win_message"
    CHOOSE_SIDE_MESSAGE: str = "choose_side_message"
    PLAYER_LOSE_MESSAGE: str = "player_lose_message"
    PLAYER_DRAW_MESSAGE: str = "player_draw_message"
    COIN_FLIP_MESSAGE: str = "coin_flip_message"
    MAGIC_MENU_FORCE_DESCRIPTION: str = "magic_menu_force_description"
    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    MAGIC_MENU_SHIELD_DESCRIPTION: str = "magic_menu_shield_description"
    BET_MESSAGE: str = "bet_message"
    PLAYER_WIN_ACTION_MESSAGE: str = "player_win_action_message"
    ENEMY_WIN_ACTION_MESSAGE: str = "enemy_win_action_message"
    PLAYER_ENEMY_DRAW_ACTION_MESSAGE: str = "player_enemy_draw_action_message"
    BONNIE_CASTING_SPELL_MESSAGE: str= "BONNIE_CASTING_SPELL_MESSAGE"

    def start(self, state: 'GameState'):

        self.reset_coin_flip_game()


        self.welcome_screen_index = 0
        self.coinflip_magic = CoinFlipMagic(state)


        self.luck_bonus: int = state.player.luck

        if Magic.HEADS_FORCE.value in state.player.magicinventory and Magic.HEADS_FORCE.value not in self.magic_menu_selector:
            self.magic_menu_selector.append(Magic.HEADS_FORCE.value)

        if Magic.SHIELD.value in state.player.magicinventory and Magic.SHIELD.value not in self.magic_menu_selector:
            self.magic_menu_selector.append(Magic.SHIELD.value)

        if self.BACK not in self.magic_menu_selector:
            self.magic_menu_selector.append(self.BACK)

    def reset_coin_flip_game(self):
        self.battle_messages[self.WELCOME_MESSAGE].reset()
        self.battle_messages[self.COIN_FLIP_MESSAGE].reset()
        self.phase = 1
        self.welcome_screen_index = 0
        self.shield_debuff = 0
        self.heads_force_active = False
        self.coin_bottom = False
        self.result_anchor = False
        self.timer_start = None
        self.image_to_display = ""
        self.player_choice = ""
        self.bonnie_magic_points = 2

    def reset_round(self):
        self.battle_messages[self.WELCOME_MESSAGE].reset()
        self.heads_force_active = False
        self.coin_bottom = False
        self.result_anchor = False
        self.image_to_display = ""
        self.player_choice = ""
        self.timer_start = None
        self.phase += 1
        if self.phase > 5:
            self.phase = 1
        if self.shield_debuff > 0:
            self.shield_debuff -= 1
        if self.shield_debuff == 0 and self.heads_force_active == False:
            self.magic_lock = False
        if self.debuff_double_flip > 0:
            self.debuff_double_flip -= 1
        self.double_flip_chance += 3
        double_flip_randomizer = random.randint(1, 100) + self.double_flip_chance

        if double_flip_randomizer > 90 and self.bonnie_magic_points > 0 and self.debuff_double_flip == 0:
            self.game_state = self.BONNIE_CASTING_SPELL_SCREEN
            self.double_flip_chance = 0


    def update(self, state):
        super().update(state)
        controller = state.controller
        controller.update()
        state.player.update(state)
        if self.money <= self.bonnie_bankrupt:
            state.currentScreen = state.area4GamblingScreen
            state.area4GamblingScreen.start(state)
            Events.add_level_four_event_to_player(state.player, Events.COIN_FLIP_BONNIE_DEFEATED)

        # switch statement
        # match self.game_state:
        #     case self.WELCOME_SCREEN:
        #         self.battle_messages[self.WELCOME_MESSAGE].update(state)
        #         self.battle_messages[self.BET_MESSAGE].reset()
        #         self.update_welcome_screen_logic(controller, state)
        #
        #     case self.BONNIE_CASTING_SPELL_SCREEN:
        #         self.battle_messages[self.BONNIE_CASTING_SPELL_MESSAGE].update(state)
        #         self.update_bonnies_casting_spell_screen_helper(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
            self.battle_messages[self.BET_MESSAGE].reset()
            self.update_welcome_screen_logic(controller, state)
        elif self.game_state == self.BONNIE_CASTING_SPELL_SCREEN:
            self.battle_messages[self.BONNIE_CASTING_SPELL_MESSAGE].update(state)
            self.update_bonnies_casting_spell_screen_helper(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].update(state)
            self.update_bet_screen_helper(state, controller)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu_selection_box(controller, state)
        elif self.game_state == self.CHOOSE_SIDE_SCREEN:
            self.update_choose_side_logic(controller, state)
        elif self.game_state == self.COIN_FLIP_SCREEN:
            self.battle_messages[self.COIN_FLIP_MESSAGE].update(state)
            self.update_coin_flip_screen_helper(state)
        elif self.game_state == self.RESULTS_SCREEN:
            if self.result_anchor == True:
                if self.debuff_double_flip == 0:
                    self.update_flip_coin()
                else:
                    self.update_double_flip_coin()
            if controller.confirm_button:
                self.update_flip_coin_logic_helper(controller)
        elif self.game_state == self.PLAYER_WIN_SCREEN:
            self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"You WIN! You WIN {self.bet}:"
                                                                      f" money and gain {self.exp_gain_high}:  "
                                                                      f" experience points!"]
            self.battle_messages[self.PLAYER_WIN_MESSAGE].update(state)
            if controller.confirm_button:
                self.update_player_win_screen_helper(state)
        elif self.game_state == self.PLAYER_LOSE_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_MESSAGE].messages = [f"You Lose! You Lose {self.bet}:"
                                                                       f" money and gain {self.exp_gain_low}:   "
                                                                       f"experience points!"]
            self.battle_messages[self.PLAYER_LOSE_MESSAGE].update(state)
            if controller.confirm_button:
                self.update_player_lose_message_helper(state)
        elif self.game_state == self.PLAYER_DRAW_SCREEN:
            self.battle_messages[self.PLAYER_DRAW_MESSAGE].update(state)
            if controller.confirm_button:
                self.update_player_draw_screen_helper()
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.game_over_screen_level_4(state, controller)

    def draw(self, state: 'GameState'):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)
        self.draw_box_info(state)

        if self.game_state == self.BONNIE_CASTING_SPELL_SCREEN:
            self.battle_messages[self.BONNIE_CASTING_SPELL_MESSAGE].draw(state)
        elif self.game_state == self.WELCOME_SCREEN:
            self.battle_messages[self.WELCOME_MESSAGE].draw(state)
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].draw(state)
        elif self.game_state == self.CHOOSE_SIDE_SCREEN:
            self.draw_choose_side_logic(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box(state)
        elif self.game_state == self.COIN_FLIP_SCREEN:
            self.battle_messages[self.COIN_FLIP_MESSAGE].draw(state)
            if self.debuff_double_flip == 0:
                self.draw_flip_coin(state)
            else:
                self.draw_double_flip(state)
        elif self.game_state == self.RESULTS_SCREEN:
            self.draw_coin_results_single_or_double_flip(state)
        elif self.game_state == self.PLAYER_WIN_SCREEN:
            self.battle_messages[self.PLAYER_WIN_MESSAGE].draw(state)
            self.draw_coin_results_single_or_double_flip(state)
        elif self.game_state == self.PLAYER_LOSE_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_MESSAGE].draw(state)
            self.draw_coin_results_single_or_double_flip(state)
        elif self.game_state == self.PLAYER_DRAW_SCREEN:
            self.battle_messages[self.PLAYER_DRAW_MESSAGE].draw(state)
            self.draw_coin_results_single_or_double_flip(state)
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.draw_game_over_screen_helper(state)
        pygame.display.flip()


    def update_choose_side_logic(self, controller, state):
        self.battle_messages[self.CHOOSE_SIDE_MESSAGE].update(state)
        if controller.up_button:
            self.menu_movement_sound.play()
            self.headstailsindex = (self.headstailsindex - self.index_stepper) % len(self.heads_or_tails_menu)
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False
            self.menu_movement_sound.play()
            self.headstailsindex = (self.headstailsindex + self.index_stepper) % len(self.heads_or_tails_menu)
        if controller.confirm_button:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            if self.headstailsindex == 0:
                self.player_choice = CoinFlipConstants.HEADS.value
                self.game_state = self.COIN_FLIP_SCREEN
            elif self.headstailsindex == 1:
                self.player_choice = CoinFlipConstants.TAILS.value
                self.game_state = self.COIN_FLIP_SCREEN
            elif self.headstailsindex == 2:
                self.headstailsindex = 0
                self.game_state = self.WELCOME_SCREEN


    def update_magic_menu_selection_box(self, controller, state):
        if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value:
            self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].update(state)
            self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()
        elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value:
            self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].update(state)
            self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()
        elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)
            self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].reset()
        if controller.up_button:
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index - self.index_stepper) % len(self.magic_menu_selector)
        elif controller.down_button:
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index + self.index_stepper) % len(self.magic_menu_selector)

        if controller.confirm_button:
            if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value and state.player.focus_points >= self.shield_cost:
                self.shield_debuff = self.coinflip_magic.cast_shield()
                self.spell_sound.play()
                self.magic_lock = True
                self.game_state = self.WELCOME_SCREEN
            elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value and state.player.focus_points >= self.coinflip_magic.HEADS_FORCE_COST:
                state.player.focus_points -= self.coinflip_magic.HEADS_FORCE_COST
                self.heads_force_active = True
                self.spell_sound.play()
                self.magic_lock = True
                self.game_state = self.WELCOME_SCREEN
            elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
                self.game_state = self.WELCOME_SCREEN

    def update_welcome_screen_logic(self, controller, state):
        if self.welcome_screen_index == self.flip_coin_index and controller.confirm_button:
            state.player.stamina_points -= self.low_stamina_drain
            self.game_state = self.CHOOSE_SIDE_SCREEN
        elif self.welcome_screen_index == self.magic_index and self.magic_lock == False and controller.confirm_button:
            self.game_state = self.MAGIC_MENU_SCREEN
        elif self.welcome_screen_index == self.bet_index and controller.confirm_button :
            self.game_state = self.BET_SCREEN
        elif self.welcome_screen_index == self.quit_index and controller.confirm_button:
            self.reset_coin_flip_game()
            state.currentScreen = state.area4GamblingScreen
            state.area4GamblingScreen.start(state)

    def update_flip_coin_logic_helper(self,controller):
        # if self.heads_force_active == True:
        #     self.coin_landed = CoinFlipConstants.HEADS.value
        #
        # if self.player_choice == CoinFlipConstants.HEADS.value and self.heads_force_active == True:
        #     self.game_state = self.PLAYER_WIN_SCREEN

        if self.heads_force_active == True:
            # heads_force_modifer = self.magic_bonus
            # self.heads_force_randomizer = random.randint(1, 100) + heads_force_modifer

            # print("Heads force is: " + str(self.heads_force_randomizer))

            if self.coinflip_magic.HEADS_FORCE_SUCCESS_CHANCE > self.coinflip_magic.HEADS_FORCE_ENEMY_DEFENSE:
                self.coin_landed = CoinFlipConstants.HEADS.value
                self.game_state = self.PLAYER_WIN_SCREEN
                return
            else:
                self.heads_force_active = False
                self.coin_landed = CoinFlipConstants.TAILS.value
                self.game_state = self.PLAYER_LOSE_SCREEN
                return

        if self.debuff_double_flip == 0:
            if self.coin_landed == self.player_choice:
                self.game_state = self.PLAYER_WIN_SCREEN
            elif self.coin_landed != self.player_choice and self.shield_debuff > 0:
                next_state = self.coinflip_magic.shield_outcome(
                    self.coin_landed,
                    self.player_choice,
                    self.shield_debuff,
                    self.magic_bonus
                )
                self.game_state = getattr(self, next_state)
                return
            else:
                self.game_state = self.PLAYER_LOSE_SCREEN
        else:
            if self.coin_landed == self.player_choice and self.double_coin_landed == self.player_choice:
                self.game_state = self.PLAYER_WIN_SCREEN
            elif (self.coin_landed != self.player_choice or self.double_coin_landed != self.player_choice) and self.shield_debuff > 0:
                self.game_state = self.PLAYER_DRAW_SCREEN
            elif self.coin_landed != self.player_choice or self.double_coin_landed != self.player_choice:
                self.game_state = self.PLAYER_LOSE_SCREEN


    def update_double_flip_coin(self):
        # Coin 1 (uses phase-based logic)
        if self.heads_force_active:
            self.coin_landed = CoinFlipConstants.HEADS.value
        else:
            if not self.even and not self.odd and not self.tri:
                coin_fate = random.randint(1, 3)
                print("Coin 1 fate:", coin_fate)
                if coin_fate == 1:
                    self.even = True
                elif coin_fate == 2:
                    self.odd = True
                elif coin_fate == 3:
                    self.tri = True

            if self.even:
                if self.phase in [1, 2, 5]:
                    self.coin_landed = CoinFlipConstants.HEADS.value
                elif self.phase in [3, 4]:
                    self.coin_landed = CoinFlipConstants.TAILS.value

            elif self.odd:
                if self.phase in [1, 2, 3, 5]:
                    self.coin_landed = CoinFlipConstants.TAILS.value
                elif self.phase == 4:
                    self.coin_landed = CoinFlipConstants.HEADS.value

            elif self.tri:
                if self.phase in [1, 3, 4]:
                    self.coin_landed = CoinFlipConstants.HEADS.value
                elif self.phase in [2, 5]:
                    self.coin_landed = CoinFlipConstants.TAILS.value

        # Coin 2 (simple 50/50) → assign to double_coin_landed
        self.double_coin_landed = random.choice([
            CoinFlipConstants.HEADS.value,
            CoinFlipConstants.TAILS.value
        ])

        self.result_anchor = False

    def update_double_flip_coin(self):
        # Coin 1 (uses phase-based logic)
        if self.heads_force_active:
            self.coin_landed = CoinFlipConstants.HEADS.value
        else:
            if not self.even and not self.odd and not self.tri:
                coin_fate = random.randint(1, 3)
                print("Coin 1 fate:", coin_fate)
                if coin_fate == 1:
                    self.even = True
                elif coin_fate == 2:
                    self.odd = True
                elif coin_fate == 3:
                    self.tri = True

            if self.even:
                if self.phase in [1, 2, 5]:
                    self.coin_landed = CoinFlipConstants.HEADS.value
                elif self.phase in [3, 4]:
                    self.coin_landed = CoinFlipConstants.TAILS.value

            elif self.odd:
                if self.phase in [1, 2, 3, 5]:
                    self.coin_landed = CoinFlipConstants.TAILS.value
                elif self.phase == 4:
                    self.coin_landed = CoinFlipConstants.HEADS.value

            elif self.tri:
                if self.phase in [1, 3, 4]:
                    self.coin_landed = CoinFlipConstants.HEADS.value
                elif self.phase in [2, 5]:
                    self.coin_landed = CoinFlipConstants.TAILS.value

        # Coin 2 (simple 50/50) → assign to double_coin_landed
        self.double_coin_landed = random.choice([
            CoinFlipConstants.HEADS.value,
            CoinFlipConstants.TAILS.value
        ])

        self.result_anchor = False

    def update_player_draw_screen_helper(self, state):
        state.player.exp += self.exp_gain_low

        self.game_state = self.WELCOME_SCREEN
        self.reset_round()



    def update_flip_coin(self):
        if self.heads_force_active == True:
            self.result = CoinFlipConstants.HEADS.value
            #
        if self.even == False and self.odd == False and self.tri == False:
            coin_fate = random.randint(1, 3)
            print("YOur coin fate" + str(coin_fate))
            if coin_fate == 1:
                self.even = True
            elif coin_fate == 2:
                self.odd = True
            elif coin_fate == 3:
                self.tri = True

        if self.even == True and self.heads_force_active == False:
            if self.phase == 1:
                self.coin_landed = CoinFlipConstants.HEADS.value
            elif self.phase == 2:
                self.coin_landed = CoinFlipConstants.HEADS.value
            elif self.phase == 3:
                self.coin_landed = CoinFlipConstants.TAILS.value
            elif self.phase == 4:
                self.coin_landed = CoinFlipConstants.TAILS.value
            elif self.phase == 5:
                self.coin_landed = CoinFlipConstants.HEADS.value

        elif self.odd == True and self.heads_force_active == False:
            if self.phase == 1:
                self.coin_landed = CoinFlipConstants.TAILS.value
            elif self.phase == 2:
                self.coin_landed = CoinFlipConstants.TAILS.value
            elif self.phase == 3:
                self.coin_landed = CoinFlipConstants.TAILS.value
            elif self.phase == 4:
                self.coin_landed = CoinFlipConstants.HEADS.value
            elif self.phase == 5:
                self.coin_landed = CoinFlipConstants.TAILS.value

        elif self.tri == True and self.heads_force_active == False:
            if self.phase == 1:
                self.coin_landed = CoinFlipConstants.HEADS.value
            elif self.phase == 2:
                self.coin_landed = CoinFlipConstants.TAILS.value
            elif self.phase == 3:
                self.coin_landed = CoinFlipConstants.HEADS.value
            elif self.phase == 4:
                self.coin_landed = CoinFlipConstants.HEADS.value
            elif self.phase == 5:
                self.coin_landed = CoinFlipConstants.TAILS.value

        self.result_anchor = False

    def update_bet_screen_helper(self,state,  controller):
        if controller.action_and_cancel_button:
            controller.isBPressed = False
            controller.isBPressedSwitch = False
            self.game_state = self.WELCOME_SCREEN
        min_bet = 50
        if Equipment.COIN_FLIP_GLOVES.value in state.player.equipped_items:
            max_bet = 200 + (self.spirit_bonus * 40)
        else:
            max_bet = 200
        if controller.up_button:
            self.menu_movement_sound.play()
            self.bet += min_bet
        elif controller.down_button:
            self.menu_movement_sound.play()
            self.bet -= min_bet
        if self.bet <= min_bet:
            self.bet = min_bet
        elif self.bet >= max_bet:
            self.bet = max_bet

    def update_bonnies_casting_spell_screen_helper(self, state: 'GameState'):
        if state.controller.confirm_button:
            self.bonnie_magic_points -= 1
            self.debuff_double_flip += 10
            self.game_state = self.WELCOME_SCREEN

    def update_coin_flip_screen_helper(self, state: 'GameState'):
        self.result_anchor = True
        if self.coin_bottom == True:
            self.game_state = self.RESULTS_SCREEN

    def update_player_win_screen_helper(self, state: 'GameState'):
        state.player.exp += self.exp_gain_high
        state.player.money += self.bet
        self.money -= self.bet
        self.game_state = self.WELCOME_SCREEN
        self.reset_round()


        if Equipment.COIN_FLIP_GLASSES.value in state.player.equipped_items:

            if self.money < 0:
                self.money = 0
            total_gain = self.bet + (self.spirit_bonus * 20)
            state.player.money += total_gain
            self.money -= total_gain
            self.game_state = self.WELCOME_SCREEN
    def update_player_lose_message_helper(self, state: 'GameState'):
        state.player.exp += self.exp_gain_low
        state.player.money -= self.bet
        self.money += self.bet
        self.game_state = self.WELCOME_SCREEN
        self.reset_round()



    def game_over_screen_level_4(self, state: 'GameState', controller):
        no_money_game_over = 0
        no_stamina_game_over = 0
        if state.player.money <= no_money_game_over:
            if controller.confirm_button:
                state.currentScreen = state.gameOverScreen
                state.gameOverScreen.start(state)
        elif state.player.stamina_points <= no_stamina_game_over:
            if controller.confirm_button:
                self.reset_coin_flip_game()
                state.player.money -= 100
                state.currentScreen = state.area4GamblingScreen
                state.area4GamblingScreen.start(state)

    def draw_game_over_screen_helper(self, state: 'Gamestate'):
        no_money_game_over = 0
        no_stamina_game_over = 0
        if state.player.money <= no_money_game_over:
            state.DISPLAY.blit(self.font.render(f"You ran out of money and are now a prisoner of hell", True, WHITE), (self.blit_message_x, self.blit_message_y))
        elif state.player.stamina_points <= no_stamina_game_over:
            state.DISPLAY.blit(self.font.render(f"You ran out of stamina , you lose -100 gold", True, WHITE), (self.blit_message_x, self.blit_message_y))


    def draw_coin_results_single_or_double_flip(self, state: 'GameState'):
        if self.debuff_double_flip == 0:
            self.draw_results_screen_logic(state)
        else:
            self.draw_double_flip_results_screen_logic(state)

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
        arrow_y_coordinate_padding_bet = 92
        arrow_y_coordinate_padding_quit = 132

        for idx, choice in enumerate(self.welcome_screen_choices):
            y_position = start_y_right_box + idx * spacing_between_choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        if Magic.HEADS_FORCE.value not in state.player.magicinventory and Magic.SHIELD.value not in state.player.magicinventory:
            self.magic_lock = True
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif Magic.HEADS_FORCE.value in state.player.magicinventory or Magic.SHIELD.value in state.player.magicinventory:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if Magic.HEADS_FORCE.value in state.player.magicinventory and Magic.HEADS_FORCE.value not in self.magic_menu_selector:
            self.magic_menu_selector.append(Magic.HEADS_FORCE.value)

        if Magic.SHIELD.value in state.player.magicinventory and Magic.SHIELD.value not in self.magic_menu_selector:
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
        elif self.welcome_screen_index == self.welcome_screen_bet_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_bet)
            )
        elif self.welcome_screen_index == self.welcome_screen_quit_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_quit)
            )

    def draw_double_flip(self, state: 'GameState'):
        x_positions = [85, 235, 380, 525, 670, 815, 960, 1108, 1250, 1394]
        y_position = 110
        width, height = 170, 190
        time_interval = 50
        fall_speed = 4.5
        max_height = 250
        drop_height = 175
        coin_spacing = 200  # Distance between the two coins on X axis

        if self.timer_start is None:
            self.timer_start = pygame.time.get_ticks()

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.timer_start
        current_coin_index = (elapsed_time // time_interval) % len(x_positions)
        subsurface_rect = pygame.Rect(x_positions[current_coin_index], y_position, width, height)
        sprite = self.sprite_sheet.subsurface(subsurface_rect)

        cycle_time = (2 * max_height // fall_speed) + (2 * drop_height // fall_speed)
        cycle_position = (elapsed_time // time_interval) % cycle_time

        if cycle_position < (max_height // fall_speed):
            fall_distance = fall_speed * cycle_position
            y_position = self.initial_coin_image_position[1] - fall_distance
        elif cycle_position < (max_height // fall_speed) + (drop_height // fall_speed):
            fall_distance = fall_speed * (cycle_position - (max_height // fall_speed))
            y_position = self.initial_coin_image_position[1] - max_height + fall_distance
        else:
            fall_distance = fall_speed * (cycle_position - (max_height // fall_speed) - (drop_height // fall_speed))
            y_position = self.initial_coin_image_position[1] - max_height + drop_height - fall_distance

        if elapsed_time >= 4000:
            self.timer_start = None
            self.coin_bottom = True
            self.initial_coin_image_position = (300, 250)

        x1 = self.initial_coin_image_position[0]
        x2 = x1 + coin_spacing
        state.DISPLAY.blit(sprite, (x1, y_position))
        state.DISPLAY.blit(sprite, (x2, y_position))

    def draw_flip_coin(self, state: 'GameState'):
        x_positions = [85, 235, 380, 525, 670, 815, 960, 1108, 1250, 1394]
        y_position = 110
        width, height = 170, 190
        time_interval = 50
        fall_speed = 4.5
        max_height = 250
        drop_height = 175

        if self.timer_start is None:
            self.timer_start = pygame.time.get_ticks()

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.timer_start
        current_coin_index = (elapsed_time // time_interval) % len(x_positions)
        subsurface_rect = pygame.Rect(x_positions[current_coin_index], y_position, width, height)
        sprite = self.sprite_sheet.subsurface(subsurface_rect)
        cycle_time = (2 * max_height // fall_speed) + (2 * drop_height // fall_speed)
        cycle_position = (elapsed_time // time_interval) % cycle_time

        if cycle_position < (max_height // fall_speed):
            fall_distance = fall_speed * cycle_position
            coin_image_position = (self.initial_coin_image_position[0], self.initial_coin_image_position[1] - fall_distance)

        elif cycle_position < (max_height // fall_speed) + (drop_height // fall_speed):
            fall_distance = fall_speed * (cycle_position - (max_height // fall_speed))
            coin_image_position = (self.initial_coin_image_position[0], self.initial_coin_image_position[1] - max_height + fall_distance)
        else:
            fall_distance = fall_speed * (cycle_position - (max_height // fall_speed) - (drop_height // fall_speed))
            coin_image_position = (self.initial_coin_image_position[0], self.initial_coin_image_position[1] - max_height + drop_height - fall_distance)

        if elapsed_time >= 4000:
            self.timer_start = None
            self.coin_bottom = True
            self.initial_coin_image_position = (300, 250)

        state.DISPLAY.blit(sprite, coin_image_position)

    def draw_choose_side_logic(self, state):
        self.battle_messages[self.CHOOSE_SIDE_MESSAGE].draw(state)
        choice_spacing = 40
        text_x_offset = 60
        text_y_offset = 15
        arrow_x_offset = 12
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

        for idx, choice in enumerate(self.heads_or_tails_menu):
            y_position = start_y_right_box + idx * choice_spacing
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        arrow_y_position = start_y_right_box + (self.headstailsindex * choice_spacing) + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_position)
        )

    def draw_double_flip_results_screen_logic(self, state):
        # Determine images based on coin results
        image1 = self.heads_image if self.coin_landed == CoinFlipConstants.HEADS.value else self.tails_image
        image2 = self.heads_image if self.double_coin_landed == CoinFlipConstants.HEADS.value else self.tails_image

        if self.heads_force_active:
            image1 = self.heads_image  # force override for coin 1

        # Center Y position and coin 1 X center
        screen_center_x = state.DISPLAY.get_width() // 2
        screen_center_y = state.DISPLAY.get_height() // 2
        coin_spacing = 200

        # Coin 1 placement
        image1_rect = image1.get_rect()
        image1_rect.center = (screen_center_x - coin_spacing // 2, screen_center_y)

        # Coin 2 placement (200px to the right of Coin 1)
        image2_rect = image2.get_rect()
        image2_rect.center = (screen_center_x + coin_spacing // 2, screen_center_y)

        # Draw both coins
        state.DISPLAY.blit(image1, image1_rect)
        state.DISPLAY.blit(image2, image2_rect)

    def draw_results_screen_logic(self, state):
        self.image_to_display = (
            self.heads_image
            if self.coin_landed == CoinFlipConstants.HEADS.value
            else self.tails_image
        )

        if self.heads_force_active == True:
            self.image_to_display = self.heads_image

        image_rect = self.image_to_display.get_rect()
        image_rect.center = (state.DISPLAY.get_width() // 2, state.DISPLAY.get_height() // 2)
        state.DISPLAY.blit(self.image_to_display, image_rect)
    def draw_magic_menu_selection_box(self, state):
        if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value:
            self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].draw(state)
        elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value:
            self.battle_messages[self.MAGIC_MENU_FORCE_DESCRIPTION].draw(state)
        elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)

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

        for idx, choice in enumerate(self.magic_menu_selector):
            y_position = start_y_right_box + idx * choice_spacing
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        arrow_y_position = start_y_right_box + (self.magic_screen_index * choice_spacing) + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_position)
        )

    def draw_box_info(self, state: 'GameState'):
        player_enemy_box_info_x_position = 37
        enemy_name_y_position = 33
        phase_y_position = 108
        choice_y_position = 148
        enemy_money_y_position = 70
        bet_y_position = 370
        player_money_y_position = 250
        hero_name_y_position = 205
        hero_stamina_y_position = 290
        hero_focus_y_position = 330

        if self.heads_force_active == True:
            state.DISPLAY.blit(self.font.render(f"Force: 1", True, RED), (player_enemy_box_info_x_position, enemy_name_y_position))
        elif self.shield_debuff == self.shield_debuff_inactive:
            state.DISPLAY.blit(self.font.render(self.dealer_name, True, WHITE), (player_enemy_box_info_x_position, enemy_name_y_position))
        elif self.shield_debuff > self.shield_debuff_inactive:
            state.DISPLAY.blit(self.font.render(f"Shield: {self.shield_debuff}", True, RED), (player_enemy_box_info_x_position, enemy_name_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}", True, WHITE), (player_enemy_box_info_x_position, enemy_money_y_position))
        state.DISPLAY.blit(self.font.render(f" Phase: {self.phase}", True, WHITE), (player_enemy_box_info_x_position - 7, phase_y_position))
        state.DISPLAY.blit(self.font.render(f" Choice: {self.player_choice}", True, WHITE), (player_enemy_box_info_x_position - 7, choice_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE), (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE), (player_enemy_box_info_x_position, player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE), (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE), (player_enemy_box_info_x_position, hero_focus_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HERO_HEADER}", True, WHITE), (player_enemy_box_info_x_position, hero_name_y_position))
