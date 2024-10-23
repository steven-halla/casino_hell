import random

import pygame

from constants import WHITE
from entity.gui.screen.gamble_screen import GambleScreen
from game_constants.magic import Magic


class DiceFighterSirSiegfried(GambleScreen):
    def __init__(self, screenName: str = "Coin FLip") -> None:
        super().__init__(screenName)
        self.bet = 100
        self.bet_stepper = 50
        self.dealer_name: str = "Sir Siegfried"
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        self.game_state: str = self.WELCOME_SCREEN
        self.welcome_screen_choices: list[str] = ["Play", "Magic",  "Quit"]
        self.magic_menu_selector: list[str] = []
        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.welcome_to_play_screen_index: int = 0
        self.welcome_to_magic_screen_index: int = 1
        self.welcome_to_gambling_area_screen_index: int = 2
        self.magic_lock = False
        self.initiative_roll_index: int = 0
        self.initiative_roll_blow_option: int = 0
        self.player_win_init:bool = False
        self.enemy_win_init:bool = False
        self.player_point_roll:int = 0
        self.enemy_point_roll:int = 0
        self.player_triple_roll: bool = False
        self.enemy_triple_roll: bool = False
        self.point_break: int = 0


    BACK: str = "Back"

    RESULTS_SCREEN: str = "results_screen"
    PLAYER_WIN_SCREEN: str = "player_win_screen"
    PLAYER_LOSE_SCREEN: str = "player_lose_screen"
    INITIATIVE_SCREEN:str = "initiative_screen"
    BATTLE_SCREEN: str = "battle_screen"
    POINT_SET_SCREEN:str = "point_set_screen"
    ATTACK_PHASE_SCREEN: str = "attack_phase_screen"
    DEFENSE_PHASE_SCREEN: str = "defense_phase_screen"
    PLAYER_DEALS_DAMAGE_SCREEN: str = "player_deals_damage_screen"
    ENEMY_DEALS_DAMAGE_SCREEN: str = "enemy_deals_damage_screen"


    def start(self, state: 'GameState'):
        pass
    def restart_dice_fighter_game(self):
        self.player_win_init: bool = False
        self.enemy_win_init: bool = False
        self.player_point_roll: int = 0
        self.enemy_point_roll: int = 0
        self.player_triple_roll: bool = False
        self.enemy_triple_roll: bool = False
        self.point_break: int = 0

    def restart_dice_fighter_round(self):
        self.player_win_init: bool = False
        self.enemy_win_init: bool = False
        self.player_triple_roll: bool = False
        self.enemy_triple_roll: bool = False
        self.player_point_roll: int = 0
        self.enemy_point_roll: int = 0
        self.point_break: int = 0


    def update(self, state):
        super().update(state)
        controller = state.controller
        controller.update()
        state.player.update(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.update_welcome_screen_logic_dice_fighter(controller, state)

        elif self.game_state == self.INITIATIVE_SCREEN:
            self.initiative_screen_logic(state)
        elif self.game_state == self.POINT_SET_SCREEN:
            self.point_set_screen_logic_dice_fighter()
        elif self.game_state == self.ATTACK_PHASE_SCREEN:
            pass
        elif self.game_state == self.DEFENSE_PHASE_SCREEN:
            pass
        elif self.game_state == self.PLAYER_WIN_SCREEN:
            pass
        elif self.game_state == self.PLAYER_LOSE_SCREEN:
            pass
        elif self.game_state == self.PLAYER_DEALS_DAMAGE_SCREEN:
            pass
        elif self.game_state == self.ENEMY_DEALS_DAMAGE_SCREEN:
            pass
        elif self.game_state == self.GAME_OVER_SCREEN:
            pass



    def draw(self, state):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info_dice_fighter(state)


        elif self.game_state == self.INITIATIVE_SCREEN:
            pass
        elif self.game_state == self.POINT_SET_SCREEN:
            pass
        elif self.game_state == self.ATTACK_PHASE_SCREEN:
            pass
        elif self.game_state == self.DEFENSE_PHASE_SCREEN:
            pass
        elif self.game_state == self.PLAYER_WIN_SCREEN:
            pass
        elif self.game_state == self.PLAYER_LOSE_SCREEN:
            pass
        elif self.game_state == self.PLAYER_DEALS_DAMAGE_SCREEN:
            pass
        elif self.game_state == self.ENEMY_DEALS_DAMAGE_SCREEN:
            pass
        elif self.game_state == self.GAME_OVER_SCREEN:
            pass



        pygame.display.flip()

    def initiative_screen_logic(self, state):
        player_init_roll_1: int = random.randint(1, 6)
        player_init_roll_2: int = random.randint(1, 6)
        player_init_roll_3: int = random.randint(1, 6)
        player_init_roll_total: int = player_init_roll_1 + player_init_roll_2 + player_init_roll_3
        enemy_init_roll_1: int = random.randint(1, 6)
        enemy_init_roll_2: int = random.randint(1, 6)
        enemy_init_roll_3: int = random.randint(1, 6)
        enemy_init_roll_total: int = enemy_init_roll_1 + enemy_init_roll_2 + enemy_init_roll_3
        blow_init_modifier = 1 + state.player.luck
        blow_init_dice = False
        print("player init roll is :" + str(player_init_roll_total))
        print("enemy init roll is :" + str(enemy_init_roll_total))

        if blow_init_dice == True:
            if player_init_roll_total >= 16:
                player_init_roll_total += blow_init_modifier
        # blow command takes 10 stamina
        if player_init_roll_total > enemy_init_roll_total:
            self.player_win_init = True
            self.game_state = self.POINT_SET_SCREEN
        elif player_init_roll_total < enemy_init_roll_total:
            self.enemy_win_init = True
            self.game_state = self.POINT_SET_SCREEN
        else:
            self.initiative_screen_logic(state)

    def triple_dice_checker(self):
        pass


    def point_set_screen_logic_dice_fighter(self):
        if self.player_win_init == True:
            player_point_roll_1: int = random.randint(1, 6)
            player_point_roll_2: int = random.randint(1, 6)
            player_point_roll_3: int = random.randint(1, 6)
            player_point_roll_total: int = player_point_roll_1 + player_point_roll_2 + player_point_roll_3

            print("Player point roll 1: " + str(player_point_roll_1))
            print("Player point roll 2: " + str(player_point_roll_2))
            print("Player point roll 3: " + str(player_point_roll_3))
            print("Player point roll total is : " + str(player_point_roll_total))
            if player_point_roll_1 == player_point_roll_2 and player_point_roll_1 == player_point_roll_3:
                self.game_state = self.PLAYER_DEALS_DAMAGE_SCREEN
                print("You got a triple you win")
                return
            if player_point_roll_1 == player_point_roll_2 and player_point_roll_1 != player_point_roll_3:
                self.point_break = player_point_roll_1
                print("Your break point is: " + str(self.point_break))
                self.game_state = self.ATTACK_PHASE_SCREEN
                return
            elif player_point_roll_1 == player_point_roll_3 and player_point_roll_1 != player_point_roll_2:
                self.point_break = player_point_roll_1
                self.game_state = self.ATTACK_PHASE_SCREEN
                print("Your break point is: " + str(self.point_break))

                return

            elif player_point_roll_2 == player_point_roll_3 and player_point_roll_2 != player_point_roll_1:
                self.point_break = player_point_roll_2
                self.game_state = self.ATTACK_PHASE_SCREEN
                print("Your break point is: " + str(self.point_break))

                return

            else:
                self.player_win_init = False
                self.enemy_win_init = True


        elif self.enemy_win_init == True:
            enemy_point_roll_1: int = random.randint(1, 6)
            enemy_point_roll_2: int = random.randint(1, 6)
            enemy_point_roll_3: int = random.randint(1, 6)
            enemy_point_roll_total: int = enemy_point_roll_1 + enemy_point_roll_2 + enemy_point_roll_3
            print("enemy point roll is : " + str(enemy_point_roll_total))
            print("enemy point roll 1: " + str(enemy_point_roll_1))
            print("enemy point roll 2: " + str(enemy_point_roll_2))
            print("enemy point roll 3: " + str(enemy_point_roll_3))
            self.enemy_point_roll = enemy_point_roll_total
            if enemy_point_roll_1 == enemy_point_roll_2 and enemy_point_roll_1 == enemy_point_roll_3:
                print("Eney got  a triple win")
                self.game_state = self.ENEMY_DEALS_DAMAGE_SCREEN
                return
            if enemy_point_roll_1 == enemy_point_roll_2 and enemy_point_roll_1 != enemy_point_roll_3:
                self.point_break = enemy_point_roll_1
                self.game_state = self.DEFENSE_PHASE_SCREEN
                print("Your break point is: " + str(self.point_break))

                return
            elif enemy_point_roll_1 == enemy_point_roll_3 and enemy_point_roll_1 != enemy_point_roll_2:
                self.point_break = enemy_point_roll_1
                self.game_state = self.DEFENSE_PHASE_SCREEN
                print("Your break point is: " + str(self.point_break))

                return
            elif enemy_point_roll_2 == enemy_point_roll_3 and enemy_point_roll_2 != enemy_point_roll_1:
                self.point_break = enemy_point_roll_2
                self.game_state = self.DEFENSE_PHASE_SCREEN
                print("Your break point is: " + str(self.point_break))

                return

            else:
                self.player_win_init = True
                self.enemy_win_init = False

        if self.point_break == 0:
            self.point_set_screen_logic_dice_fighter()

    def update_welcome_screen_logic_dice_fighter(self, controller, state):
        if controller.isTPressed:
            controller.isTPressed = False

            if self.welcome_screen_index == self.welcome_to_play_screen_index:
                self.game_state = self.INITIATIVE_SCREEN
            elif self.welcome_screen_index == self.welcome_to_magic_screen_index and self.magic_lock == False:
                # self.game_state = self.MAGIC_MENU_SCREEN
                print("well work on this later")
            elif self.welcome_screen_index == self.welcome_to_gambling_area_screen_index:
                print("we'll work on this later")



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




