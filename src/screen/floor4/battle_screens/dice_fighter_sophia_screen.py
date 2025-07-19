import random

import pygame

from constants import WHITE, BLACK
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic



class DiceFighterSophiaScreen(GambleScreen):
    def __init__(self, screenName: str = "Coin FLip") -> None:
        super().__init__(screenName)
        self.dice_sprite_sheet: pygame.Surface = pygame.image.load("./assets/images/dice45.png")

        self.bet: int = 100
        self.bet_index: int = 2
        self.bet_stepper: int = 50
        self.dealer_name: str = "Sophia"
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        self.game_state: str = self.WELCOME_SCREEN
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.attack_screen_choices: list[str] = ["Attack"]
        self.defense_screen_choices: list[str] = ["Defense"]
        self.point_screen_choices: list[str] = ["Point R"]
        self.init_screen_choices: list[str] = ["Roll"]
        self.magic_menu_selector: list[str] = []
        self.menu_movement_sound = pygame.mixer.Sound("./assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)
        self.spell_sound = pygame.mixer.Sound("./assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.welcome_to_play_screen_index: int = 0
        self.welcome_to_magic_screen_index: int = 1
        self.welcome_to_gambling_area_screen_index: int = 2
        self.magic_lock: bool = False
        self.initiative_roll_index: int = 0
        self.initiative_roll_blow_option: int = 0
        self.player_win_init:bool = False
        self.enemy_win_init:bool = False
        self.player_point_roll:int = 0
        self.enemy_point_roll:int = 0
        self.player_triple_roll: bool = False
        self.enemy_triple_roll: bool = False
        self.point_break: int = 0
        self.stamina_points: int = 300
        self.inflict_damage: int = 75
        self.sophia_money= 1000
        self.init_screen_index: int = 0
        self.index_stepper: int = 1
        self.blow_stamina_drain: int = 10
        self.blow_init_dice: bool = False
        self.enemy_attack_roll_1: int = 0
        self.enemy_attack_roll_2: int = 0
        self.enemy_attack_roll_3: int = 0
        self.player_defense_roll: int = 0
        self.player_attack_roll_1: int = 0
        self.player_attack_roll_2: int = 0
        self.player_attack_roll_3: int = 0
        self.enemy_defense_roll: int = 0
        self.player_init_roll_1: int = 0
        self.player_init_roll_2: int = 0
        self.player_init_roll_3: int = 0
        self.player_init_roll_total: int = 0
        self.enemy_init_roll_1: int = 0
        self.enemy_init_roll_2: int = 0
        self.enemy_init_roll_3: int = 0
        self.enemy_init_roll_total: int = 0
        self.player_point_roll_1: int = 0
        self.player_point_roll_2: int = 0
        self.player_point_roll_3: int = 0
        self.player_point_roll_total: int = 0
        self.enemy_point_roll_1: int = 0
        self.enemy_point_roll_2: int = 0
        self.enemy_point_roll_3: int = 0
        self.enemy_point_roll_total: int = 0
        self.point_screen_index = 0
        self.player_win_point: bool = False
        self.enemy_win_point: bool = False
        self.battle_screen_index: int = 0
        self.debuff_bad_luck: int = 0
        self.magic_screen_index: int = 0
        self.buff_rolls_of_fate: int = 0
        self.sophia_magic_points: int = 2
        self.buff_lucky_smile: int = 0
        self.spirit_bonus: int = 0
        self.magic_bonus: int = 0

        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "Sophia: I follow the path of the agile warrior, prepare yourself for my 1000 cuts technique.."
            ]),

            self.PLAYER_WIN_MESSAGE: MessageBox([
                "You won the match niciiiiiiiice!!!"
            ]),
            self.ENEMY_WIN_MESSAGE: MessageBox([
                "You lost the toss."
            ]),
            self.INIT_MESSAGE: MessageBox([
                "Time to roll for init."
            ]),
            self.POST_INIT_MESSAGE: MessageBox([
                "Time to roll for init."
            ]),

            self.POINT_ROLL_MESSAGE: MessageBox([
                "ROLL to set the point"
            ]),

            self.POST_POINT_ROLL_MESSAGE: MessageBox([
                "POST ROLL to set the point"
            ]),
            self.ENEMY_ATTACK_MESSAGE: MessageBox([
                "enemy attacks"
            ]),
            self.PLAYER_ATTACK_MESSAGE: MessageBox([
                "PLayer attacks"
            ]),
            self.PLAYER_DEFENSE_MESSAGE: MessageBox([
                "PLayer DEFENSE ROLL"
            ]),
            self.ENEMY_DEFENSE_MESSAGE: MessageBox([
                "ENEMY DEFENSSE ROLL"
            ]),
            self.BET_MESSAGE: MessageBox([
                "Min bet of 50, max of 200. Press up and down keys to increase/decrease bet. Press B to go back."
            ]),

            self.MAGIC_MENU_BAD_LUCK_DESCRIPTION: MessageBox([
                "give the enemy bad luck on attack rolls."
            ]),
            self.MAGIC_MENU_BACK_DESCRIPTION: MessageBox([
                "go back to previous menu"
            ]),
            self.SOPHIA_CASTING_SPELL_MESSAGE: MessageBox([
                f"Winds of fate, dictate who lives and who falls off the cliff...Rolls of fate(enemy defense rolls are now stronger with a +1 if below 6)"
            ]),

        }

    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    MAGIC_MENU_BAD_LUCK_DESCRIPTION: str = "magic_menu_bad_luck_description"

    PLAYER_DEFENSE_MESSAGE: str = "player_defense_message"
    ENEMY_DEFENSE_MESSAGE: str = "enemy_defense_message"
    ENEMY_ATTACK_MESSAGE: str = "enemy_attack_message"
    PLAYER_ATTACK_MESSAGE: str = "player_attack_message"
    PLAYER_WIN_MESSAGE: str = "player_win_message"
    ENEMY_WIN_MESSAGE: str = "enemy_win_message"
    INIT_MESSAGE: str = "init_message"
    POST_INIT_MESSAGE: str = "post_init_message"
    POINT_ROLL_MESSAGE: str = "point_roll_message"
    POST_POINT_ROLL_MESSAGE: str = "post_point_roll_message"
    SOPHIA_CASTING_SPELL_MESSAGE: str = "sophia casting spell message"

    BACK: str = "Back"
    BET_MESSAGE: str = "bet_message"

    RESULTS_SCREEN: str = "results_screen"
    PLAYER_WIN_SCREEN: str = "player_win_screen"
    ENEMY_WIN_SCREEN: str = "enemy_win_screen"
    INITIATIVE_SCREEN:str = "initiative_screen"
    BATTLE_SCREEN: str = "battle_screen"
    POINT_SET_SCREEN:str = "point_set_screen"
    ATTACK_PHASE_SCREEN: str = "attack_phase_screen"
    DEFENSE_PHASE_SCREEN: str = "defense_phase_screen"
    PLAYER_DEALS_DAMAGE_SCREEN: str = "player_deals_damage_screen"
    ENEMY_DEALS_DAMAGE_SCREEN: str = "enemy_deals_damage_screen"
    POST_INIT_SCREEN: str = "post_init_screen"
    PLAYER_ATTACK_SCREEN: str = "player_attack_screen"
    ENEMY_ATTACK_SCREEN: str = "enemy_attack_screen"
    PLAYER_DEFENSE_SCREEN: str = "player_defense_screen"
    ENEMY_DEFENSE_SCREEN: str = "enemy_defense_screen"
    POST_POINT_SET_SCREEN: str = "post_point_set_screen"
    SOPHIA_CASTING_SPELL_SCREEN: str = "sophia casting a spell screen"

    def start(self, state: 'GameState'):
        self.spirit_bonus: int = state.player.spirit
        self.magic_bonus: int = state.player.mind
    def restart_dice_fighter_game(self):
        self.player_win_init: bool = False
        self.enemy_win_init: bool = False
        self.player_point_roll: int = 0
        self.enemy_point_roll: int = 0
        self.player_triple_roll: bool = False
        self.enemy_triple_roll: bool = False
        self.point_break: int = 0
        self.blow_init_dice = False
        self.player_win_point = False
        self.enemy_win_point = False
        self.player_init_roll_total = 0
        self.enemy_init_roll_total = 0
        self.magic_lock = False
        self.welcome_screen_index = 0
        self.magic_screen_index = 0
        self.buff_rolls_of_fate = 0

    def restart_dice_fighter_round(self, state: 'GameState'):
        self.player_win_init: bool = False
        self.enemy_win_init: bool = False
        self.player_triple_roll: bool = False
        self.enemy_triple_roll: bool = False
        self.player_point_roll: int = 0
        self.enemy_point_roll: int = 0
        self.point_break: int = 0
        self.blow_init_dice = False
        self.player_win_point = False
        self.enemy_win_point = False
        self.player_init_roll_total = 0
        self.enemy_init_roll_total = 0
        if self.debuff_bad_luck > 0:
            self.debuff_bad_luck -= 1
        if self.debuff_bad_luck == 0:
            self.magic_lock = False
        elif self.debuff_bad_luck > 0:
            self.magic_lock = True
        if self.buff_rolls_of_fate > 0:
            self.buff_rolls_of_fate -= 1
        if self.buff_lucky_smile > 0:
            self.buff_lucky_smile -= 1
            if self.buff_lucky_smile == 0:
                state.player.luck -= 3


    def update(self, state):
        super().update(state)
        controller = state.controller
        controller.update()
        state.player.update(state)


        if self.sophia_money <= 0:
            state.currentScreen = state.area4RestScreen
            state.area4RestScreen.start(state)
            Events.add_level_four_event_to_player(state.player, Events.DICE_FIGHTER_SOPHIA_DEFEATED)

        if self.game_state == self.WELCOME_SCREEN:
            self.update_welcome_screen_logic_dice_fighter(controller, state)
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
        elif self.game_state == self.SOPHIA_CASTING_SPELL_SCREEN:
            self.battle_messages[self.SOPHIA_CASTING_SPELL_MESSAGE].update(state)
            self.update_sophia_casting_spell_helper(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].update(state)
            self.update_bet_screen_helper(state, controller)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu_selection_box(controller, state)
        elif self.game_state == self.INITIATIVE_SCREEN:
            self.update_init_helper(controller, state)
        elif self.game_state == self.POST_INIT_SCREEN:
            self.update_post_init_helper(controller, state)
        elif self.game_state == self.POINT_SET_SCREEN:
            self.battle_messages[self.POINT_ROLL_MESSAGE].update(state)
            self.update_point_set_screen_logic_dice_fighter(controller)
        elif self.game_state == self.POST_POINT_SET_SCREEN:
            self.update_post_point_set_helper(controller, state)
        elif self.game_state == self.PLAYER_ATTACK_SCREEN:
            self.update_battle_screen_helper(controller)
            self.battle_messages[self.PLAYER_ATTACK_MESSAGE].update(state)
            self.update_player_attack_helper(state, controller)
        elif self.game_state == self.ENEMY_ATTACK_SCREEN:
            self.update_enemy_attack_helper(controller, state)
        elif self.game_state == self.PLAYER_DEFENSE_SCREEN:
            self.battle_messages[self.PLAYER_DEFENSE_MESSAGE].update(state)
            self.update_battle_screen_helper(controller)
            self.update_player_defense_helper(state, controller)
        elif self.game_state == self.ENEMY_DEFENSE_SCREEN:
            self.battle_messages[self.ENEMY_DEFENSE_MESSAGE].update(state)
            self.update_battle_screen_helper(controller)
            self.update_enemy_defense_helper(state, controller)
        elif self.game_state == self.PLAYER_WIN_SCREEN:
            self.update_player_win_helper(state)
        elif self.game_state == self.ENEMY_WIN_SCREEN:
            self.restart_dice_fighter_round(state)
            self.update_enemy_win_helper(state)

    def draw(self, state):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)
        self.draw_box_info(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.battle_messages[self.WELCOME_MESSAGE].draw(state)
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info_dice_fighter(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].draw(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box(state)
        elif self.game_state == self.INITIATIVE_SCREEN:
            self.battle_messages[self.INIT_MESSAGE].draw(state)
            self.draw_menu_selection_box(state)
            self.draw_init_screen_box_info(state)
            self.draw_display_dice_init_roll(state,
                                        self.player_init_roll_1, self.player_init_roll_2, self.player_init_roll_3,
                                        self.enemy_init_roll_1, self.enemy_init_roll_2, self.enemy_init_roll_3)
        elif self.game_state == self.POST_INIT_SCREEN:
            self.battle_messages[self.POST_INIT_MESSAGE].draw(state)
            self.draw_display_dice_init_roll(state,
                                        self.player_init_roll_1, self.player_init_roll_2, self.player_init_roll_3,
                                        self.enemy_init_roll_1, self.enemy_init_roll_2, self.enemy_init_roll_3)
        elif self.game_state == self.POINT_SET_SCREEN:
            self.battle_messages[self.POINT_ROLL_MESSAGE].draw(state)
            self.draw_menu_selection_box(state)
            self.draw_point_screen_box_info_dice_fighter(state)
            self.draw_display_dice_point_roll(state,
                                          self.player_attack_roll_1, self.player_attack_roll_2, self.player_attack_roll_3,
                                          self.enemy_attack_roll_1, self.enemy_attack_roll_2, self.enemy_attack_roll_3)
        elif self.game_state == self.POST_POINT_SET_SCREEN:
            self.battle_messages[self.POST_POINT_ROLL_MESSAGE].draw(state)
            self.draw_display_dice_point_roll(state,
                                         self.player_attack_roll_1, self.player_attack_roll_2, self.player_attack_roll_3,
                                         self.enemy_attack_roll_1, self.enemy_attack_roll_2, self.enemy_attack_roll_3)
        elif self.game_state == self.PLAYER_ATTACK_SCREEN:
            self.battle_messages[self.PLAYER_ATTACK_MESSAGE].draw(state)
            self.draw_menu_selection_box(state)
            self.draw_battle_screen_box_info(state)
            self.draw_display_defense_dice(state,
                                      self.enemy_attack_roll_1, self.enemy_attack_roll_2, self.enemy_attack_roll_3,
                                      self.enemy_defense_roll,
                                      self.player_attack_roll_1, self.player_attack_roll_2, self.player_attack_roll_3,
                                      self.player_defense_roll)
        elif self.game_state == self.ENEMY_ATTACK_SCREEN:
            self.battle_messages[self.ENEMY_ATTACK_MESSAGE].draw(state)
            self.draw_menu_selection_box(state)
            self.draw_battle_screen_box_info(state)
            self.draw_display_defense_dice(state,
                                      self.enemy_attack_roll_1, self.enemy_attack_roll_2, self.enemy_attack_roll_3,
                                      self.enemy_defense_roll,
                                      self.player_attack_roll_1, self.player_attack_roll_2, self.player_attack_roll_3,
                                      self.player_defense_roll)
        elif self.game_state == self.PLAYER_DEFENSE_SCREEN:
            self.battle_messages[self.PLAYER_DEFENSE_MESSAGE].draw(state)
            self.draw_menu_selection_box(state)
            self.draw_battle_screen_box_info(state)
            self.draw_display_defense_dice(state,
                                      self.enemy_attack_roll_1, self.enemy_attack_roll_2, self.enemy_attack_roll_3,
                                      self.enemy_defense_roll,
                                      self.player_attack_roll_1, self.player_attack_roll_2, self.player_attack_roll_3,
                                      self.player_defense_roll)
        elif self.game_state == self.ENEMY_DEFENSE_SCREEN:
            self.battle_messages[self.ENEMY_DEFENSE_MESSAGE].draw(state)
            self.draw_menu_selection_box(state)
            self.draw_battle_screen_box_info(state)
            self.draw_display_defense_dice(state,
                                      self.enemy_attack_roll_1, self.enemy_attack_roll_2, self.enemy_attack_roll_3,
                                      self.enemy_defense_roll,
                                      self.player_attack_roll_1, self.player_attack_roll_2, self.player_attack_roll_3,
                                      self.player_defense_roll)
        elif self.game_state == self.PLAYER_WIN_SCREEN:
            self.battle_messages[self.PLAYER_WIN_MESSAGE].draw(state)  # elif self.game_state == self.PLAYER_LOSE_SCREEN:
            self.draw_display_defense_dice(state,
                                      self.enemy_attack_roll_1, self.enemy_attack_roll_2, self.enemy_attack_roll_3,
                                      self.enemy_defense_roll,
                                      self.player_attack_roll_1, self.player_attack_roll_2, self.player_attack_roll_3,
                                      self.player_defense_roll)
        elif self.game_state == self.ENEMY_WIN_SCREEN:
            self.battle_messages[self.ENEMY_WIN_MESSAGE].draw(state)
            self.draw_display_defense_dice(state,
                                      self.enemy_attack_roll_1, self.enemy_attack_roll_2, self.enemy_attack_roll_3,
                                      self.enemy_defense_roll,
                                      self.player_attack_roll_1, self.player_attack_roll_2, self.player_attack_roll_3,
                                      self.player_defense_roll)
        pygame.display.flip()

    def update_enemy_win_helper(self, state):
        self.battle_messages[self.ENEMY_WIN_MESSAGE].update(state)  # elif self.game_state == self.PLAYER_LOSE_SCREEN:
        if state.controller.confirm_button and self.battle_messages[self.ENEMY_WIN_MESSAGE].current_message_finished():
            if self.buff_rolls_of_fate == 0:
                state.player.money -= self.bet
                self.sophia_money+= self.bet
                self.restart_dice_fighter_round(state)
                self.game_state = self.WELCOME_SCREEN
            elif self.buff_rolls_of_fate > 0:
                state.player.stamina_points += self.bet // 3
                state.player.money -= self.bet * 3
                self.sophia_money+= self.bet * 3
                self.restart_dice_fighter_round(state)
                self.game_state = self.WELCOME_SCREEN

    def update_player_win_helper(self, state):
        self.battle_messages[self.PLAYER_WIN_MESSAGE].update(state)  # elif self.game_state == self.PLAYER_LOSE_SCREEN:
        if state.controller.confirm_button and self.battle_messages[self.PLAYER_WIN_MESSAGE].current_message_finished():
            state.player.money += self.bet
            self.sophia_money-= self.bet
            self.restart_dice_fighter_round(state)
            self.game_state = self.WELCOME_SCREEN

    def update_enemy_defense_helper(self, state, controller):
        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            print(self.game_state)

            self.enemy_defense_roll = random.randint(1, 6)
            print(self.enemy_defense_roll)

            if self.enemy_defense_roll == self.point_break:
                print("we have LOST the game!!!!!!!!!!")
                self.game_state = self.ENEMY_WIN_SCREEN

                # self.game_state = self.ENEMY_DEALS_DAMAGE_SCREEN
            else:
                if self.player_attack_roll_1 == self.player_attack_roll_2 and self.player_attack_roll_1 != self.player_attack_roll_3 and self.player_attack_roll_1 >= self.point_break:
                    self.point_break = self.player_attack_roll_1
                    print("Player's break point is: " + str(self.point_break))
                    self.game_state = self.PLAYER_DEFENSE_SCREEN
                    return
                elif self.player_attack_roll_1 == self.player_attack_roll_3 and self.player_attack_roll_1 != self.player_attack_roll_2 and self.player_attack_roll_1 >= self.point_break:
                    self.point_break = self.player_attack_roll_1
                    print("Player's break point is: " + str(self.point_break))
                    self.game_state = self.PLAYER_DEFENSE_SCREEN
                    return
                elif self.player_attack_roll_2 == self.player_attack_roll_3 and self.player_attack_roll_2 != self.player_attack_roll_1 and self.player_attack_roll_2 >= self.point_break:
                    self.point_break = self.player_attack_roll_2
                    print("Player's break point is: " + str(self.point_break))
                    self.game_state = self.PLAYER_DEFENSE_SCREEN
                    return
                else:
                    if self.buff_rolls_of_fate > 0:
                        if self.enemy_defense_roll < 6:
                            self.enemy_defense_roll += 1
                            if self.enemy_defense_roll == self.point_break:
                                self.game_state = self.ENEMY_WIN_SCREEN
                        else:
                            self.game_state = self.PLAYER_ATTACK_SCREEN
                    else:
                        self.game_state = self.PLAYER_ATTACK_SCREEN

    def update_player_defense_helper(self, state, controller):

        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            print(self.game_state)
            self.player_defense_roll = random.randint(1, 6)
            print(self.player_defense_roll)
            if self.player_defense_roll == self.point_break:
                print("we have won the game!!!!!!!!!!")
                # self.stamina_points -= self.inflict_damage
                self.game_state = self.PLAYER_WIN_SCREEN
            else:
                if self.enemy_attack_roll_1 == self.enemy_attack_roll_2 and self.enemy_attack_roll_1 != self.enemy_attack_roll_3 and self.enemy_attack_roll_1 >= self.point_break:
                    self.point_break = self.enemy_attack_roll_1
                    print("Enemy's break point is: " + str(self.point_break))
                    self.game_state = self.ENEMY_DEFENSE_SCREEN
                    return
                elif self.enemy_attack_roll_1 == self.enemy_attack_roll_3 and self.enemy_attack_roll_1 != self.enemy_attack_roll_2 and self.enemy_attack_roll_1 >= self.point_break:
                    self.point_break = self.enemy_attack_roll_1
                    print("Enemy's break point is: " + str(self.point_break))
                    self.game_state = self.ENEMY_DEFENSE_SCREEN
                    return
                elif self.enemy_attack_roll_2 == self.enemy_attack_roll_3 and self.enemy_attack_roll_2 != self.enemy_attack_roll_1 and self.enemy_attack_roll_2 >= self.point_break:
                    self.point_break = self.enemy_attack_roll_2
                    print("Enemy's break point is: " + str(self.point_break))
                    self.game_state = self.ENEMY_DEFENSE_SCREEN
                    return
                else:
                    self.game_state = self.ENEMY_ATTACK_SCREEN

    def update_enemy_attack_helper(self, controller, state):

        self.battle_messages[self.ENEMY_ATTACK_MESSAGE].update(state)

        self.update_battle_screen_helper(controller)

        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False

            self.enemy_attack_roll_1: int = random.randint(1, 6)
            self.enemy_attack_roll_2: int = random.randint(1, 6)
            self.enemy_attack_roll_3: int = random.randint(1, 6)

            if self.point_break > 1 and self.debuff_bad_luck > 0:
                unlucky_attack = random.randint(1, 100)
                unlucky_attack += self.spirit_bonus

                if unlucky_attack > self.LEVEL_4_PERCENTAGE_CHANCE:
                    self.enemy_attack_roll_1 = 1
                if unlucky_attack > self.LEVEL_4_PERCENTAGE_CHANCE + 10:
                    self.enemy_attack_roll_2 = 1

            if self.enemy_attack_roll_1 == self.enemy_attack_roll_2 and self.enemy_attack_roll_1 == self.enemy_attack_roll_3 and self.enemy_attack_roll_1 >= self.point_break:
                # self.game_state = self.ENEMY_DEALS_DAMAGE_SCREEN
                self.game_state = self.ENEMY_WIN_SCREEN
                pass
            elif self.enemy_attack_roll_1 == self.enemy_attack_roll_2 and self.enemy_attack_roll_1 != self.enemy_attack_roll_3 and self.enemy_attack_roll_1 >= self.point_break:
                self.point_break = self.enemy_attack_roll_1
                print("Enemy's break point is: " + str(self.point_break))
                self.game_state = self.PLAYER_ATTACK_SCREEN
            elif self.enemy_attack_roll_1 == self.enemy_attack_roll_3 and self.enemy_attack_roll_1 != self.enemy_attack_roll_2 and self.enemy_attack_roll_1 >= self.point_break:
                self.point_break = self.enemy_attack_roll_1
                print("Enemy's break point is: " + str(self.point_break))
                self.game_state = self.PLAYER_ATTACK_SCREEN

                return
            elif self.enemy_attack_roll_2 == self.enemy_attack_roll_3 and self.enemy_attack_roll_2 != self.enemy_attack_roll_1 and self.enemy_attack_roll_2 >= self.point_break:
                self.point_break = self.enemy_attack_roll_2
                print("Enemy's break point is: " + str(self.point_break))
                self.game_state = self.PLAYER_ATTACK_SCREEN
                return
            else:
                self.game_state = self.PLAYER_DEFENSE_SCREEN

    def update_player_attack_helper(self, state, controller):
        lucky_attack: int = random.randint(1, 100)
        lucky_attack += state.player.luck * 10

        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False

            self.player_attack_roll_1: int = random.randint(1, 6)
            self.player_attack_roll_2: int = random.randint(1, 6)
            self.player_attack_roll_3: int = random.randint(1, 6)

            if lucky_attack > 85:
                if self.player_attack_roll_1 < 5:
                    self.player_attack_roll_1: int = self.point_break + 1
            if lucky_attack > 95:
                if self.player_attack_roll_2 < 5:
                    self.player_attack_roll_2: int = self.point_break + 1

            if self.player_attack_roll_1 == self.player_attack_roll_2 and self.player_attack_roll_1 == self.player_attack_roll_3 and self.player_attack_roll_1 >= self.point_break:
                # self.game_state = self.PLAYER_DEALS_DAMAGE_SCREEN
                # self.stamina_points -= self.inflict_damage
                self.game_state = self.PLAYER_WIN_SCREEN

                pass
            elif self.player_attack_roll_1 == self.player_attack_roll_2 and self.player_attack_roll_1 != self.player_attack_roll_3 and self.player_attack_roll_1 >= self.point_break:
                self.point_break = self.player_attack_roll_1
                print("Player's break point is: " + str(self.point_break))
                self.game_state = self.ENEMY_ATTACK_SCREEN
            elif self.player_attack_roll_1 == self.player_attack_roll_3 and self.player_attack_roll_1 != self.player_attack_roll_2 and self.player_attack_roll_1 >= self.point_break:
                self.point_break = self.player_attack_roll_1
                print("Player's break point is: " + str(self.point_break))
                self.game_state = self.ENEMY_ATTACK_SCREEN
                return
            elif self.player_attack_roll_2 == self.player_attack_roll_3 and self.player_attack_roll_2 != self.player_attack_roll_1 and self.player_attack_roll_2 >= self.point_break:
                self.point_break = self.player_attack_roll_2
                print("Player's break point is: " + str(self.point_break))
                self.game_state = self.ENEMY_ATTACK_SCREEN
                return
            else:
                self.game_state = self.ENEMY_DEFENSE_SCREEN

    def update_post_point_set_helper(self, controller, state):
        if self.player_win_point == True:
            self.battle_messages[self.POST_POINT_ROLL_MESSAGE].messages = [f"You won the point and is set at{self.point_break}! YOu have the advantage"]
        elif self.enemy_win_point == True:
            self.battle_messages[self.POST_POINT_ROLL_MESSAGE].messages = [f"ENEMY WON the point and is set at{self.point_break}! ENemy has the advantage"]
        self.battle_messages[self.POST_POINT_ROLL_MESSAGE].update(state)
        if self.battle_messages[self.POST_POINT_ROLL_MESSAGE].is_finished() and controller.isTPressed == True or controller.isAPressedSwitch == True:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            if self.player_win_point == True:
                self.game_state = self.ENEMY_ATTACK_SCREEN
            else:
                self.game_state = self.PLAYER_ATTACK_SCREEN

    def update_post_init_helper(self, controller, state):
        if self.player_init_roll_total > self.enemy_init_roll_total:
            self.battle_messages[self.POST_INIT_MESSAGE].messages = [f"You WON the init.You  rolled a {self.player_init_roll_total} and enemy rolled a {self.enemy_init_roll_total}"]
        else:
            self.battle_messages[self.POST_INIT_MESSAGE].messages = [f"ENEMY won the init. YOu rolled a {self.player_init_roll_total} and enemy rolled a {self.enemy_init_roll_total}"]
        self.battle_messages[self.POST_INIT_MESSAGE].update(state)
        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False

            self.game_state = self.POINT_SET_SCREEN

    def update_init_helper(self, controller, state: 'GameState'):
        if Equipment.CRAPS_WRIST_WATCH.value in state.player.equipped_items:
            if len(self.init_screen_choices) > 1:
                self.init_screen_choices[1] = "Blow"
            else:
                self.init_screen_choices.append("Blow")
        else:
            if len(self.init_screen_choices) > 1:
                self.init_screen_choices[1] = "LOCKED"
            else:
                self.init_screen_choices.append("LOCKED")
        self.battle_messages[self.INIT_MESSAGE].update(state)
        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.init_screen_index = (self.init_screen_index + self.index_stepper) % len(self.init_screen_choices)
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False
            self.init_screen_index = (self.init_screen_index - self.index_stepper) % len(self.init_screen_choices)
        if (controller.isTPressed or controller.isAPressedSwitch) and self.init_screen_index == 0 and self.player_init_roll_total == 0:
            controller.setTPressed = False
            controller.isAPressedSwitch = False
            print("Hi")
            self.initiative_screen_logic(state)
        elif (controller.isTPressed or controller.isAPressedSwitch) and self.init_screen_index == 1 and self.blow_init_dice == False:
            controller.setTPressed = False
            controller.isAPressedSwitch = False
            print("Ya")

            self.blow_init_dice = True
            state.player.stamina_points -= self.blow_stamina_drain
        if self.enemy_win_init == True or self.player_win_init == True:
            if state.controller.isTPressed or state.controller.isAPressedSwitch:
                self.game_state = self.POST_INIT_SCREEN
                state.controller.isTPressed = False
                state.controller.isAPressedSwitch = False


    def update_sophia_casting_spell_helper(self, state):
        if state.controller.confirm_button:
            self.sophia_magic_points -= 1
            self.debuff_spirit_drain = 5
            self.game_state = self.WELCOME_SCREEN

    def update_bet_screen_helper(self, state, controller):

        if controller.isBPressed or controller.isBPressedSwitch:
            controller.isBPressed = False
            controller.isBPressedSwitch = False
            self.game_state = self.WELCOME_SCREEN
        min_bet = 50
        max_bet = 200

        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet += min_bet
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False

            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet -= min_bet

        if self.bet <= min_bet:
            self.bet = min_bet
        elif self.bet >= max_bet:
            self.bet = max_bet

    def update_magic_menu_selection_box(self, controller, state):
        if Magic.BAD_LUCK.value in state.player.magicinventory and Magic.BAD_LUCK.value not in self.magic_menu_selector:
            self.magic_menu_selector.insert(0, Magic.BAD_LUCK.value)

        if Magic.GOOD_LUCK.value in state.player.magicinventory and Magic.GOOD_LUCK.value not in self.magic_menu_selector:
            self.magic_menu_selector.insert(1, Magic.GOOD_LUCK.value)

        if self.magic_menu_selector[self.magic_screen_index] == Magic.BAD_LUCK.value:
            self.battle_messages[self.MAGIC_MENU_BAD_LUCK_DESCRIPTION].update(state)

            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()

        elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)

            self.battle_messages[self.MAGIC_MENU_BAD_LUCK_DESCRIPTION].reset()

        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index - self.index_stepper) % len(self.magic_menu_selector)
            # print(f"Current Magic Menu Selector: {self.magic_menu_selector[self.magic_screen_index]}")
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index + self.index_stepper) % len(self.magic_menu_selector)
            # print(f"Current Magic Menu Selector: {self.magic_menu_selector[self.magic_screen_index]}")

        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            if self.magic_menu_selector[self.magic_screen_index] == Magic.BAD_LUCK.value and state.player.focus_points >= 50:
                state.player.focus_points -= 50
                self.debuff_bad_luck = 10
                print(f"Shield debuff: {self.debuff_bad_luck}")
                self.spell_sound.play()  # Play the sound effect once
                self.magic_lock = True
                self.game_state = self.WELCOME_SCREEN

            if self.magic_menu_selector[self.magic_screen_index] == Magic.GOOD_LUCK.value and state.player.focus_points >= 50:
                state.player.focus_points -= 50
                self.buff_lucky_smile = 5
                state.player.luck += 3

                self.spell_sound.play()  # Play the sound effect once
                self.magic_lock = True
                self.game_state = self.WELCOME_SCREEN

            elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
                self.game_state = self.WELCOME_SCREEN

    def update_battle_screen_helper(self, controller):
        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()
            self.battle_screen_index = (self.battle_screen_index - self.index_stepper) % len(self.battle_screen_choices)
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False
            self.menu_movement_sound.play()
            self.battle_screen_index = (self.battle_screen_index + self.index_stepper) % len(self.battle_screen_choices)

    def initiative_screen_logic(self, state):
        self.player_init_roll_1: int = random.randint(1, 6)
        self.player_init_roll_2: int = random.randint(1, 6)
        self.player_init_roll_3: int = random.randint(1, 6)
        self.player_init_roll_total: int = self.player_init_roll_1 + self.player_init_roll_2 + self.player_init_roll_3
        self.enemy_init_roll_1: int = random.randint(1, 6)
        self.enemy_init_roll_2: int = random.randint(1, 6)
        self.enemy_init_roll_3: int = random.randint(1, 6)
        self.enemy_init_roll_total: int = self.enemy_init_roll_1 + self.enemy_init_roll_2 + self.enemy_init_roll_3
        blow_init_modifier = 6
        print("player init roll is :" + str(self.player_init_roll_total))
        print("enemy init roll is :" + str(self.enemy_init_roll_total))



        if self.blow_init_dice == True:
            print(str(self.blow_init_dice) + "this is the blow int bonus")
            if self.player_init_roll_total <= 9:
                if self.player_init_roll_1 < 3:
                    self.player_init_roll_1 = 4
                if self.player_init_roll_2  < 3:
                    self.player_init_roll_2 = 4
                if self.player_init_roll_3 < 3:
                    self.player_init_roll_3 = 4
                print("player NEW init roll is :" + str(self.player_init_roll_total))

        # blow command takes 10 stamina
        if self.player_init_roll_total > self.enemy_init_roll_total:
            self.player_win_init = True
            print("Ok good duck")

        elif self.player_init_roll_total < self.enemy_init_roll_total:
            print("Ok bad quak")
            self.enemy_win_init = True


        else:
            print("am ai here? i better not be")
            self.player_init_roll_total: int = 0
            self.enemy_init_roll_total: int = 0
            self.initiative_screen_logic(state)

    def update_point_set_screen_logic_dice_fighter(self, controller):
        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            if self.player_win_init == True:
                self.player_attack_roll_1: int = random.randint(1, 6)
                self.player_attack_roll_2: int = random.randint(1, 6)
                self.player_attack_roll_3: int = random.randint(1, 6)
                self.player_point_roll_total: int = self.player_attack_roll_1 + self.player_attack_roll_2 + self.player_attack_roll_3

                print("Player point roll 1: " + str(self.player_attack_roll_1))
                print("Player point roll 2: " + str(self.player_attack_roll_2))
                print("Player point roll 3: " + str(self.player_attack_roll_3))
                print("Player point roll total is : " + str(self.player_point_roll_total))
                if self.player_attack_roll_1 == self.player_attack_roll_2 and self.player_attack_roll_1 == self.player_attack_roll_3:
                    self.game_state = self.PLAYER_DEALS_DAMAGE_SCREEN
                    print("You got a triple you win")
                    return
                if self.player_attack_roll_1 == self.player_attack_roll_2 and self.player_attack_roll_1 != self.player_attack_roll_3:
                    self.point_break = self.player_attack_roll_1
                    print("Your break point is: " + str(self.point_break))
                    self.player_win_point = True
                    self.game_state = self.POST_POINT_SET_SCREEN

                    return
                elif self.player_attack_roll_1 == self.player_attack_roll_3 and self.player_attack_roll_1 != self.player_attack_roll_2:
                    self.point_break = self.player_attack_roll_1
                    self.player_win_point = True
                    self.game_state = self.POST_POINT_SET_SCREEN

                    print("Your break point is: " + str(self.point_break))
                    return

                elif self.player_attack_roll_2 == self.player_attack_roll_3 and self.player_attack_roll_2 != self.player_attack_roll_1:
                    self.point_break = self.player_attack_roll_2
                    self.player_win_point = True
                    self.game_state = self.POST_POINT_SET_SCREEN

                    print("Your break point is: " + str(self.point_break))

                    return

                else:
                    self.player_win_init = False
                    self.enemy_win_init = True
            elif self.enemy_win_init == True:
                self.enemy_attack_roll_1: int = random.randint(1, 6)
                self.enemy_attack_roll_2: int = random.randint(1, 6)
                self.enemy_attack_roll_3: int = random.randint(1, 6)
                self.enemy_attack_roll_total: int = self.enemy_attack_roll_1 + self.enemy_attack_roll_2 + self.enemy_attack_roll_3
                self.enemy_attack_roll = self.enemy_attack_roll_total
                if self.enemy_attack_roll_1 == self.enemy_attack_roll_2 and self.enemy_attack_roll_1 == self.enemy_attack_roll_3:
                    self.game_state = self.ENEMY_DEALS_DAMAGE_SCREEN
                    return
                if self.enemy_attack_roll_1 == self.enemy_attack_roll_2 and self.enemy_attack_roll_1 != self.enemy_attack_roll_3:
                    self.point_break = self.enemy_attack_roll_1
                    self.enemy_win_point = True
                    self.game_state = self.POST_POINT_SET_SCREEN
                    return
                elif self.enemy_attack_roll_1 == self.enemy_attack_roll_3 and self.enemy_attack_roll_1 != self.enemy_attack_roll_2:
                    self.point_break = self.enemy_attack_roll_1
                    self.enemy_win_point = True
                    self.game_state = self.POST_POINT_SET_SCREEN
                    return
                elif self.enemy_attack_roll_2 == self.enemy_attack_roll_3 and self.enemy_attack_roll_2 != self.enemy_attack_roll_1:
                    self.point_break = self.enemy_attack_roll_2
                    self.enemy_win_point = True
                    self.game_state = self.POST_POINT_SET_SCREEN
                    return
                else:
                    self.player_win_init = True
                    self.enemy_win_init = False

            if self.point_break == 0:
                if controller.isTPressed or controller.isAPressedSwitch:
                    controller.isTPressed = False
                    controller.isAPressedSwitch = False
                    self.update_point_set_screen_logic_dice_fighter(controller)

    def update_welcome_screen_logic_dice_fighter(self, controller, state):
        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False

            if self.welcome_screen_index == self.welcome_to_play_screen_index:
                self.game_state = self.INITIATIVE_SCREEN
            elif self.welcome_screen_index == self.welcome_to_magic_screen_index and self.magic_lock == False:
                self.game_state = self.MAGIC_MENU_SCREEN
            elif self.welcome_screen_index == self.bet_index:
                state.controller.isAPressedSwitch = False
                state.controller.isTPressed = False

                self.game_state = self.BET_SCREEN
            elif self.welcome_screen_index == 3:
                self.restart_dice_fighter_game()
                state.currentScreen = state.area3RestScreen
                state.area3RestScreen.start(state)



    def draw_welcome_screen_box_info_dice_fighter(self, state: 'GameState'):
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
            y_position = start_y_right_box + idx * spacing_between_choices  # Adjust spacing between choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )



        if self.BACK not in self.magic_menu_selector:
            self.magic_menu_selector.append(self.BACK)

        if self.magic_lock == True:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif self.magic_lock == False:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if self.welcome_screen_index == self.welcome_to_play_screen_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_play)
            )
        elif self.welcome_screen_index == self.welcome_to_magic_screen_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_magic)
            )
        elif self.welcome_screen_index == self.welcome_to_gambling_area_screen_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_bet)
            )
        elif self.welcome_screen_index == 3:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_quit)
            )

    def draw_point_screen_box_info_dice_fighter(self, state):
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

        for idx, choice in enumerate(self.point_screen_choices):
            y_position = start_y_right_box + idx * spacing_between_choices  # Adjust spacing between choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        if self.point_screen_index == 0:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_play)
            )
        elif self.point_screen_index == 1:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_magic)
            )

    def draw_battle_screen_box_info(self, state: 'GameState'):
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
        if self.game_state == self.PLAYER_ATTACK_SCREEN or self.game_state == self.ENEMY_ATTACK_SCREEN:
            for idx, choice in enumerate(self.attack_screen_choices):
                y_position = start_y_right_box + idx * spacing_between_choices  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, WHITE),
                    (start_x_right_box + text_x_offset, y_position + text_y_offset)
                )
        else:
            for idx, choice in enumerate(self.defense_screen_choices):
                y_position = start_y_right_box + idx * spacing_between_choices  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, WHITE),
                    (start_x_right_box + text_x_offset, y_position + text_y_offset)
                )

        if self.battle_screen_index == 0:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_play)
            )


    def draw_init_screen_box_info(self, state: 'GameState'):
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

        for idx, choice in enumerate(self.init_screen_choices):
            y_position = start_y_right_box + idx * spacing_between_choices  # Adjust spacing between choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )


        if self.init_screen_index == 0:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_play)
            )
        elif self.init_screen_index == 1:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_magic)
            )



    def draw_display_defense_dice(self, state: "GameState",
                             enemy_attack_roll_1: int, enemy_attack_roll_2: int, enemy_attack_roll_3: int,
                             enemy_defense_roll: int,
                             player_attack_roll_1: int, player_attack_roll_2: int, player_attack_roll_3: int,
                             player_defense_roll: int) -> None:
        dice_x_start_position = 250  # Starting position for dice display
        dice_y_position_enemy = -40  # Y-position for enemy dice (top of the screen)
        dice_y_position_player = 80  # Y-position for player dice (bottom of the screen)
        dice_x_gap = 120  # Gap between dice
        dice_faces = [
            pygame.Rect(50, 0, 133, 200),  # Dice face 1
            pygame.Rect(210, 0, 133, 200),  # Dice face 2
            pygame.Rect(370, 0, 133, 200),  # Dice face 3
            pygame.Rect(545, 0, 133, 200),  # Dice face 4
            pygame.Rect(710, 0, 133, 200),  # Dice face 5
            pygame.Rect(880, 0, 133, 200)  # Dice face 6
        ]

        # Enemy attack dice
        enemy_attack_rect1 = dice_faces[enemy_attack_roll_1 - 1]
        cropped_enemy_attack1 = self.dice_sprite_sheet.subsurface(enemy_attack_rect1)

        enemy_attack_rect2 = dice_faces[enemy_attack_roll_2 - 1]
        cropped_enemy_attack2 = self.dice_sprite_sheet.subsurface(enemy_attack_rect2)

        enemy_attack_rect3 = dice_faces[enemy_attack_roll_3 - 1]
        cropped_enemy_attack3 = self.dice_sprite_sheet.subsurface(enemy_attack_rect3)

        # Blit enemy attack dice onto the display (top)
        state.DISPLAY.blit(cropped_enemy_attack1, (dice_x_start_position, dice_y_position_enemy))
        state.DISPLAY.blit(cropped_enemy_attack2, (dice_x_start_position + dice_x_gap, dice_y_position_enemy))
        state.DISPLAY.blit(cropped_enemy_attack3, (dice_x_start_position + dice_x_gap * 2, dice_y_position_enemy))

        # Enemy defense dice
        enemy_defense_rect = dice_faces[enemy_defense_roll - 1]
        cropped_enemy_defense = self.dice_sprite_sheet.subsurface(enemy_defense_rect)

        # Blit enemy defense dice onto the display (top)
        state.DISPLAY.blit(cropped_enemy_defense, (dice_x_start_position + 50 + dice_x_gap * 3, dice_y_position_enemy))

        # Player attack dice
        player_attack_rect1 = dice_faces[player_attack_roll_1 - 1]
        cropped_player_attack1 = self.dice_sprite_sheet.subsurface(player_attack_rect1)

        player_attack_rect2 = dice_faces[player_attack_roll_2 - 1]
        cropped_player_attack2 = self.dice_sprite_sheet.subsurface(player_attack_rect2)

        player_attack_rect3 = dice_faces[player_attack_roll_3 - 1]
        cropped_player_attack3 = self.dice_sprite_sheet.subsurface(player_attack_rect3)

        # Blit player attack dice onto the display (bottom)
        state.DISPLAY.blit(cropped_player_attack1, (dice_x_start_position, dice_y_position_player))
        state.DISPLAY.blit(cropped_player_attack2, (dice_x_start_position + dice_x_gap, dice_y_position_player))
        state.DISPLAY.blit(cropped_player_attack3, (dice_x_start_position + dice_x_gap * 2, dice_y_position_player))

        # Player defense dice
        player_defense_rect = dice_faces[player_defense_roll - 1]
        cropped_player_defense = self.dice_sprite_sheet.subsurface(player_defense_rect)

        # Blit player defense dice onto the display (bottom)
        state.DISPLAY.blit(cropped_player_defense, (dice_x_start_position + 50 + dice_x_gap * 3, dice_y_position_player))

    def draw_display_dice_point_roll(self, state: "GameState",
                                 player_attack_roll_1: int, player_attack_roll_2: int, player_attack_roll_3: int,
                                 enemy_attack_roll_1: int, enemy_attack_roll_2: int, enemy_attack_roll_3: int) -> None:
        dice_x_start_position = 235
        dice_y_position = -10
        dice_x_gap = 120  # Gap between dice

        dice_faces = [
            pygame.Rect(50, 0, 133, 200),  # Dice face 1
            pygame.Rect(210, 0, 133, 200),  # Dice face 2
            pygame.Rect(370, 0, 133, 200),  # Dice face 3
            pygame.Rect(545, 0, 133, 200),  # Dice face 4
            pygame.Rect(710, 0, 133, 200),  # Dice face 5
            pygame.Rect(880, 0, 133, 200)  # Dice face 6
        ]

        # Enemy dice rolls (swap these with player position)
        enemy_dice_rect1 = dice_faces[enemy_attack_roll_1 - 1]
        enemy_dice_rect2 = dice_faces[enemy_attack_roll_2 - 1]
        enemy_dice_rect3 = dice_faces[enemy_attack_roll_3 - 1]

        cropped_enemy_dice1 = self.dice_sprite_sheet.subsurface(enemy_dice_rect1)
        cropped_enemy_dice2 = self.dice_sprite_sheet.subsurface(enemy_dice_rect2)
        cropped_enemy_dice3 = self.dice_sprite_sheet.subsurface(enemy_dice_rect3)

        state.DISPLAY.blit(cropped_enemy_dice1, (dice_x_start_position, dice_y_position))  # Enemy dice in player position
        state.DISPLAY.blit(cropped_enemy_dice2, (dice_x_start_position + dice_x_gap, dice_y_position))  # Second enemy dice
        state.DISPLAY.blit(cropped_enemy_dice3, (dice_x_start_position + 2 * dice_x_gap, dice_y_position))  # Third enemy dice

        # Player dice rolls (swap these with enemy position)
        player_dice_rect1 = dice_faces[player_attack_roll_1 - 1]
        player_dice_rect2 = dice_faces[player_attack_roll_2 - 1]
        player_dice_rect3 = dice_faces[player_attack_roll_3 - 1]

        cropped_player_dice1 = self.dice_sprite_sheet.subsurface(player_dice_rect1)
        cropped_player_dice2 = self.dice_sprite_sheet.subsurface(player_dice_rect2)
        cropped_player_dice3 = self.dice_sprite_sheet.subsurface(player_dice_rect3)

        # Adjust y-position for player dice (swap to enemy y-position)
        player_dice_y_position = dice_y_position + 200  # Assuming 200px below original player position

        state.DISPLAY.blit(cropped_player_dice1, (dice_x_start_position, player_dice_y_position))  # Player dice in enemy position
        state.DISPLAY.blit(cropped_player_dice2, (dice_x_start_position + dice_x_gap, player_dice_y_position))  # Second player dice
        state.DISPLAY.blit(cropped_player_dice3, (dice_x_start_position + 2 * dice_x_gap, player_dice_y_position))  # Third player dice

    def draw_box_info(self, state: 'GameState'):
        player_enemy_box_info_x_position = 37
        player_enemy_box_info_x_position_score = 28
        score_y_position = 150
        enemy_name_y_position = 33
        phase_y_position = 108
        choice_y_position = 148
        enemy_money_y_position = 70
        enemy_status_y_position = 110
        bet_y_position = 370
        player_money_y_position = 250
        hero_name_y_position = 205
        hero_stamina_y_position = 290
        hero_focus_y_position = 330
        score_header = "Score"



        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}", True, WHITE), (player_enemy_box_info_x_position, enemy_money_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE), (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE), (player_enemy_box_info_x_position, player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE), (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE), (player_enemy_box_info_x_position, hero_focus_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.HERO_HEADER}", True, WHITE), (player_enemy_box_info_x_position, hero_name_y_position))

    def draw_display_dice_init_roll(self, state: "GameState",
                                   player_init_roll_1: int, player_init_roll_2: int, player_init_roll_3: int,
                                   enemy_init_roll_1: int, enemy_init_roll_2: int, enemy_init_roll_3: int) -> None:
            dice_x_start_position = 235  # Starting x-position for player dice
            dice_y_position = -10  # y-position for player dice
            dice_x_gap = 120  # Gap between dice

            dice_faces = [
                pygame.Rect(50, 0, 133, 200),  # Dice face 1
                pygame.Rect(210, 0, 133, 200),  # Dice face 2
                pygame.Rect(370, 0, 133, 200),  # Dice face 3
                pygame.Rect(545, 0, 133, 200),  # Dice face 4
                pygame.Rect(710, 0, 133, 200),  # Dice face 5
                pygame.Rect(880, 0, 133, 200)  # Dice face 6
            ]

            # Player dice rolls
            enemy_dice_rect1 = dice_faces[enemy_init_roll_1 - 1]
            enemy_dice_rect2 = dice_faces[enemy_init_roll_2 - 1]
            enemy_dice_rect3 = dice_faces[enemy_init_roll_3 - 1]

            cropped_enemy_dice1 = self.dice_sprite_sheet.subsurface(enemy_dice_rect1)
            cropped_enemy_dice2 = self.dice_sprite_sheet.subsurface(enemy_dice_rect2)
            cropped_enemy_dice3 = self.dice_sprite_sheet.subsurface(enemy_dice_rect3)

            state.DISPLAY.blit(cropped_enemy_dice1, (dice_x_start_position, dice_y_position))  # First dice position
            state.DISPLAY.blit(cropped_enemy_dice2, (dice_x_start_position + dice_x_gap, dice_y_position))  # Second dice position
            state.DISPLAY.blit(cropped_enemy_dice3, (dice_x_start_position + 2 * dice_x_gap, dice_y_position))  # Third dice position

            # Enemy dice rolls
            player_dice_rect1 = dice_faces[player_init_roll_1 - 1]
            player_dice_rect2 = dice_faces[player_init_roll_2 - 1]
            player_dice_rect3 = dice_faces[player_init_roll_3 - 1]

            cropped_player_dice1 = self.dice_sprite_sheet.subsurface(player_dice_rect1)
            cropped_player_dice2 = self.dice_sprite_sheet.subsurface(player_dice_rect2)
            cropped_player_dice3 = self.dice_sprite_sheet.subsurface(player_dice_rect3)

            # Adjust y-position for enemy dice
            enemy_dice_y_position = dice_y_position + 200  # Assuming 200px below player dice

            state.DISPLAY.blit(cropped_player_dice1, (dice_x_start_position, enemy_dice_y_position))  # First dice position
            state.DISPLAY.blit(cropped_player_dice2, (dice_x_start_position + dice_x_gap, enemy_dice_y_position))  # Second dice position
            state.DISPLAY.blit(cropped_player_dice3, (dice_x_start_position + 2 * dice_x_gap, enemy_dice_y_position))  # Third dice position




    def draw_magic_menu_selection_box(self, state):
        if self.magic_menu_selector[self.magic_screen_index] == Magic.BAD_LUCK.value:
            self.battle_messages[self.MAGIC_MENU_BAD_LUCK_DESCRIPTION].draw(state)
        elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)

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

        for idx, choice in enumerate(self.magic_menu_selector):
            y_position = start_y_right_box + idx * choice_spacing  # Use the defined spacing variable
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        # Draw the arrow at the current magic screen index position
        arrow_y_position = start_y_right_box + (self.magic_screen_index * choice_spacing) + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_position)  # Use the arrow offsets
        )



    # test before delte bottom
    # def display_attack_dice(self, state: "GameState",
    #                         player_attack_roll_1: int, player_attack_roll_2: int, player_attack_roll_3: int,
    #                         player_defense_roll: int,
    #                         enemy_attack_roll_1: int, enemy_attack_roll_2: int, enemy_attack_roll_3: int,
    #                         enemy_defense_roll: int) -> None:
    #     dice_x_start_position = 300  # Starting position for dice display
    #     dice_y_position = 50  # Y-position for attack dice (adjust as necessary)
    #     dice_x_gap = 120  # Gap between dice
    #     dice_faces = [
    #         pygame.Rect(50, 0, 133, 200),  # Dice face 1
    #         pygame.Rect(210, 0, 133, 200),  # Dice face 2
    #         pygame.Rect(370, 0, 133, 200),  # Dice face 3
    #         pygame.Rect(545, 0, 133, 200),  # Dice face 4
    #         pygame.Rect(710, 0, 133, 200),  # Dice face 5
    #         pygame.Rect(880, 0, 133, 200)  # Dice face 6
    #     ]
    #
    #     # Crop and blit player attack dice
    #     attack_rect1 = dice_faces[player_attack_roll_1 - 1]
    #     cropped_attack1 = self.dice_sprite_sheet.subsurface(attack_rect1)
    #
    #     attack_rect2 = dice_faces[player_attack_roll_2 - 1]
    #     cropped_attack2 = self.dice_sprite_sheet.subsurface(attack_rect2)
    #
    #     attack_rect3 = dice_faces[player_attack_roll_3 - 1]
    #     cropped_attack3 = self.dice_sprite_sheet.subsurface(attack_rect3)
    #
    #     # Blit player attack dice onto the display
    #     state.DISPLAY.blit(cropped_attack1, (dice_x_start_position, dice_y_position))
    #     state.DISPLAY.blit(cropped_attack2, (dice_x_start_position + dice_x_gap, dice_y_position))
    #     state.DISPLAY.blit(cropped_attack3, (dice_x_start_position + dice_x_gap * 2, dice_y_position))
    #
    #     # Blit player defense dice below attack dice
    #     player_defense_y_position = dice_y_position + 150
    #     player_defense_rect = dice_faces[player_defense_roll - 1]
    #     cropped_player_defense = self.dice_sprite_sheet.subsurface(player_defense_rect)
    #     state.DISPLAY.blit(cropped_player_defense, (dice_x_start_position, player_defense_y_position))
    #
    #     # Blit enemy attack dice above player's attack dice
    #     enemy_y_position = dice_y_position - 150
    #     enemy_attack_rect1 = dice_faces[enemy_attack_roll_1 - 1]
    #     cropped_enemy_attack1 = self.dice_sprite_sheet.subsurface(enemy_attack_rect1)
    #     state.DISPLAY.blit(cropped_enemy_attack1, (dice_x_start_position, enemy_y_position))
    #
    #     enemy_attack_rect2 = dice_faces[enemy_attack_roll_2 - 1]
    #     cropped_enemy_attack2 = self.dice_sprite_sheet.subsurface(enemy_attack_rect2)
    #     state.DISPLAY.blit(cropped_enemy_attack2, (dice_x_start_position + dice_x_gap, enemy_y_position))
    #
    #     enemy_attack_rect3 = dice_faces[enemy_attack_roll_3 - 1]
    #     cropped_enemy_attack3 = self.dice_sprite_sheet.subsurface(enemy_attack_rect3)
    #     state.DISPLAY.blit(cropped_enemy_attack3, (dice_x_start_position + dice_x_gap * 2, enemy_y_position))
    #
    #     # Blit enemy defense dice below the enemy attack dice
    #     enemy_defense_y_position = enemy_y_position + 150
    #     enemy_defense_rect = dice_faces[enemy_defense_roll - 1]
    #     cropped_enemy_defense = self.dice_sprite_sheet.subsurface(enemy_defense_rect)
    #     state.DISPLAY.blit(cropped_enemy_defense, (dice_x_start_position, enemy_defense_y_position))
