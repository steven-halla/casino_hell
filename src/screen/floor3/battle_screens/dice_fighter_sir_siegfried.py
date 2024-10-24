import random

import pygame

from constants import WHITE
from entity.gui.screen.gamble_screen import GambleScreen
from game_constants.magic import Magic


class DiceFighterSirSiegfried(GambleScreen):
    def __init__(self, screenName: str = "Coin FLip") -> None:
        super().__init__(screenName)
        self.dice_sprite_sheet: pygame.Surface = pygame.image.load("./assets/images/dice45.png")

        self.bet = 100
        self.bet_stepper = 50
        self.dealer_name: str = "Sir Siegfried"
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        self.game_state: str = self.WELCOME_SCREEN
        self.welcome_screen_choices: list[str] = ["Play", "Magic",  "Quit"]
        self.point_screen_choices: list[str] = ["Point R"]
        self.init_screen_choices: list[str] = ["Roll", "Blow"]
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
        self.stamina_points = 300
        self.inflict_damage = 75
        self.money = 1000
        self.init_screen_index = 0
        self.index_stepper = 1
        self.blow_stamina_drain = 10
        self.blow_init_dice = False
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
    POST_INIT_SCREEN: str = "post_init_screen"


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
        self.blow_init_dice = False


    def restart_dice_fighter_round(self):
        self.player_win_init: bool = False
        self.enemy_win_init: bool = False
        self.player_triple_roll: bool = False
        self.enemy_triple_roll: bool = False
        self.player_point_roll: int = 0
        self.enemy_point_roll: int = 0
        self.point_break: int = 0
        self.blow_init_dice = False

    def update(self, state):
        # print(self.game_state)
        super().update(state)
        controller = state.controller
        controller.update()
        state.player.update(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.update_welcome_screen_logic_dice_fighter(controller, state)
        elif self.game_state == self.INITIATIVE_SCREEN:
            if controller.isUpPressed:
                controller.isUpPressed = False
                self.init_screen_index = (self.init_screen_index + self.index_stepper) % len(self.init_screen_choices)
            elif controller.isDownPressed:
                controller.isDownPressed = False
                self.init_screen_index = (self.init_screen_index - self.index_stepper) % len(self.init_screen_choices)

            if controller.isTPressed and self.init_screen_index == 0 and self.player_init_roll_total == 0:
                controller.setTPressed = False
                self.initiative_screen_logic(state)
            elif controller.isTPressed and self.init_screen_index == 1 and self.blow_init_dice == False :
                controller.setTPressed = False
                self.blow_init_dice = True
                state.player.stamina_points -= self.blow_stamina_drain
        elif self.game_state == self.POST_INIT_SCREEN:
            if controller.isTPressed:
                controller.isTPressed = False
                self.game_state = self.POINT_SET_SCREEN


        elif self.game_state == self.POINT_SET_SCREEN:
            self.point_set_screen_logic_dice_fighter(controller)
        elif self.game_state == self.ATTACK_PHASE_SCREEN:
            self.attack_phase_screen_logic(controller)
        elif self.game_state == self.DEFENSE_PHASE_SCREEN:
            self.defense_phase_screen_logic(controller)
        # elif self.game_state == self.PLAYER_WIN_SCREEN:
        #     pass
        # elif self.game_state == self.PLAYER_LOSE_SCREEN:
        #     pass
        # elif self.game_state == self.PLAYER_DEALS_DAMAGE_SCREEN:
        #     if controller.isTPressed:
        #         controller.setTPressed = False
        #         self.stamina_points -= self.inflict_damage
        #
        # elif self.game_state == self.ENEMY_DEALS_DAMAGE_SCREEN:
        #     if controller.isTPressed:
        #         controller.setTPressed = False
        #         state.player.stamina_points -= self.inflict_damage
        # elif self.game_state == self.GAME_OVER_SCREEN:
        #     pass

    def draw(self, state):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info_dice_fighter(state)


        elif self.game_state == self.INITIATIVE_SCREEN:
            self.draw_menu_selection_box(state)
            self.draw_init_screen_box_info(state)
            self.display_dice_init_roll(state,
                                        self.player_init_roll_1, self.player_init_roll_2, self.player_init_roll_3,
                                        self.enemy_init_roll_1, self.enemy_init_roll_2, self.enemy_init_roll_3)

        elif self.game_state == self.POST_INIT_SCREEN:
            self.display_dice_init_roll(state,
                                        self.player_init_roll_1, self.player_init_roll_2, self.player_init_roll_3,
                                        self.enemy_init_roll_1, self.enemy_init_roll_2, self.enemy_init_roll_3)


        elif self.game_state == self.POINT_SET_SCREEN:
            self.draw_menu_selection_box(state)
            self.draw_point_screen_box_info_dice_fighter(state)

            # Call the function and pass in the appropriate dice roll values
            self.display_dice_point_roll(state,
                                         self.player_point_roll_1, self.player_point_roll_2, self.player_point_roll_3,
                                         self.enemy_point_roll_1, self.enemy_point_roll_2, self.enemy_point_roll_3)
        elif self.game_state == self.ATTACK_PHASE_SCREEN:
            # Call to display the attack dice
            self.display_attack_dice(state, self.player_attack_roll_1, self.player_attack_roll_2, self.player_attack_roll_3, self.enemy_defense_roll)

        elif self.game_state == self.DEFENSE_PHASE_SCREEN:
            # Call to display the defense dice
            self.display_defense_dice(state, self.enemy_attack_roll_1, self.enemy_attack_roll_2, self.enemy_attack_roll_3, self.player_defense_roll)
        #
        # elif self.game_state == self.PLAYER_WIN_SCREEN:
        #     pass
        # elif self.game_state == self.PLAYER_LOSE_SCREEN:
        #     pass
        # elif self.game_state == self.PLAYER_DEALS_DAMAGE_SCREEN:
        #     pass
        # elif self.game_state == self.ENEMY_DEALS_DAMAGE_SCREEN:
        #     pass
        # elif self.game_state == self.GAME_OVER_SCREEN:
        #     pass



        pygame.display.flip()

    def defense_phase_screen_logic(self, controller):
        if controller.isTPressed:
            controller.isTPressed = False
            if self.player_defense_roll == 0:
                self.enemy_attack_roll_1: int = random.randint(1, 6)
                self.enemy_attack_roll_2: int = random.randint(1, 6)
                self.enemy_attack_roll_3: int = random.randint(1, 6)
            if self.enemy_attack_roll_1 == self.enemy_attack_roll_2 and self.enemy_attack_roll_1 == self.enemy_attack_roll_3 and self.enemy_attack_roll_1 >= self.point_break:
                self.game_state = self.ENEMY_DEALS_DAMAGE_SCREEN
                print("Enemy got a triple, enemy wins")
                return
            elif self.enemy_attack_roll_1 == self.enemy_attack_roll_2 and self.enemy_attack_roll_1 != self.enemy_attack_roll_3 and self.enemy_attack_roll_1 >= self.point_break:
                self.point_break = self.enemy_attack_roll_1
                print("Enemy's break point is: " + str(self.point_break))
                self.game_state = self.ATTACK_PHASE_SCREEN
                return
            elif self.enemy_attack_roll_1 == self.enemy_attack_roll_3 and self.enemy_attack_roll_1 != self.enemy_attack_roll_2 and self.enemy_attack_roll_1 >= self.point_break:
                self.point_break = self.enemy_attack_roll_1
                self.game_state = self.ATTACK_PHASE_SCREEN
                print("Enemy's break point is: " + str(self.point_break))
                return
            elif self.enemy_attack_roll_2 == self.enemy_attack_roll_3 and self.enemy_attack_roll_2 != self.enemy_attack_roll_1 and self.enemy_attack_roll_2 >= self.point_break:
                self.point_break = self.enemy_attack_roll_2
                self.game_state = self.ATTACK_PHASE_SCREEN
                print("Enemy's break point is: " + str(self.point_break))
                return

            else:
                self.player_defense_roll: int = random.randint(1, 6)
                print("enemy defense roll is: " + str(self.player_defense_roll))
                print("Piont break is: " + str(self.point_break))

                if self.player_defense_roll == self.point_break:
                    print("player wins")
                else:
                    if controller.isTPressed:
                        controller.isTPressed = False
                        self.player_defense_roll = 0
                        self.defense_phase_screen_logic(controller)

    def attack_phase_screen_logic(self,controller):
        if controller.isTPressed:
            controller.isTPressed = False
            if self.enemy_defense_roll == 0:

                self.player_attack_roll_1: int = random.randint(1, 6)
                self.player_attack_roll_2: int = random.randint(1, 6)
                self.player_attack_roll_3: int = random.randint(1, 6)
            if self.player_attack_roll_1 == self.player_attack_roll_2 and self.player_attack_roll_1 == self.player_attack_roll_3 and self.player_attack_roll_1 >= self.point_break:
                self.game_state = self.PLAYER_DEALS_DAMAGE_SCREEN
                print("You got a triple you win")
                return
            elif self.player_attack_roll_1 == self.player_attack_roll_2 and self.player_attack_roll_1 != self.player_attack_roll_3 and self.player_attack_roll_1 >= self.point_break:
                self.point_break = self.player_attack_roll_1
                print("Your break point is: " + str(self.point_break))
                self.game_state = self.DEFENSE_PHASE_SCREEN
                return
            elif self.player_attack_roll_1 == self.player_attack_roll_3 and self.player_attack_roll_1 != self.player_attack_roll_2:
                self.point_break = self.player_attack_roll_1
                self.game_state = self.DEFENSE_PHASE_SCREEN
                print("Your break point is: " + str(self.point_break))
                return
            elif self.player_attack_roll_2 == self.player_attack_roll_3 and self.player_attack_roll_2 != self.player_attack_roll_1:
                self.point_break = self.player_attack_roll_2
                self.game_state = self.DEFENSE_PHASE_SCREEN
                print("Your break point is: " + str(self.point_break))
                return

            else:
                self.enemy_defense_roll: int = random.randint(1, 6)
                print("enemy defense roll is: " + str(self.enemy_defense_roll))
                print("Piont break is: " + str(self.point_break))

                if self.enemy_defense_roll == self.point_break:
                    print("enemy wins")
                else:
                    if controller.isTPressed:
                        controller.isTPressed = False
                        self.attack_phase_screen_logic(controller)



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
            if self.player_init_roll_total <= 16:
                self.player_init_roll_total += blow_init_modifier
                print("player NEW init roll is :" + str(self.player_init_roll_total))

        # blow command takes 10 stamina
        if self.player_init_roll_total > self.enemy_init_roll_total:
            self.player_win_init = True
            if state.controller.isTPressed:
                state.controller.isTPressed = False
                print("Ok good luck")
                self.game_state = self.POST_INIT_SCREEN
        elif self.player_init_roll_total < self.enemy_init_roll_total:
            print("Ok bad luck")
            if state.controller.isTPressed:
                state.controller.isTPressed = False
                self.enemy_win_init = True
                self.game_state = self.POST_INIT_SCREEN
        else:
            self.player_init_roll_total: int = 0
            self.enemy_init_roll_total: int = 0

            if state.controller.isTPressed:
                state.controller.isTPressed = False
                self.initiative_screen_logic(state)

    def triple_dice_checker(self):
        pass


    def point_set_screen_logic_dice_fighter(self, controller):
        if controller.isTPressed:
            controller.isTPressed = False
            if self.player_win_init == True:
                self.player_point_roll_1: int = random.randint(1, 6)
                self.player_point_roll_2: int = random.randint(1, 6)
                self.player_point_roll_3: int = random.randint(1, 6)
                self.player_point_roll_total: int = self.player_point_roll_1 + self.player_point_roll_2 + self.player_point_roll_3

                print("Player point roll 1: " + str(self.player_point_roll_1))
                print("Player point roll 2: " + str(self.player_point_roll_2))
                print("Player point roll 3: " + str(self.player_point_roll_3))
                print("Player point roll total is : " + str(self.player_point_roll_total))
                if self.player_point_roll_1 == self.player_point_roll_2 and self.player_point_roll_1 == self.player_point_roll_3:
                    self.game_state = self.PLAYER_DEALS_DAMAGE_SCREEN
                    print("You got a triple you win")
                    return
                if self.player_point_roll_1 == self.player_point_roll_2 and self.player_point_roll_1 != self.player_point_roll_3:
                    self.point_break = self.player_point_roll_1
                    print("Your break point is: " + str(self.point_break))
                    self.game_state = self.DEFENSE_PHASE_SCREEN
                    return
                elif self.player_point_roll_1 == self.player_point_roll_3 and self.player_point_roll_1 != self.player_point_roll_2:
                    self.point_break = self.player_point_roll_1
                    self.game_state = self.DEFENSE_PHASE_SCREEN
                    print("Your break point is: " + str(self.point_break))
                    return

                elif self.player_point_roll_2 == self.player_point_roll_3 and self.player_point_roll_2 != self.player_point_roll_1:
                    self.point_break = self.player_point_roll_2
                    self.game_state = self.DEFENSE_PHASE_SCREEN
                    print("Your break point is: " + str(self.point_break))

                    return

                else:
                    self.player_win_init = False
                    self.enemy_win_init = True


            elif self.enemy_win_init == True:
                self.enemy_point_roll_1: int = random.randint(1, 6)
                self.enemy_point_roll_2: int = random.randint(1, 6)
                self.enemy_point_roll_3: int = random.randint(1, 6)
                self.enemy_point_roll_total: int = self.enemy_point_roll_1 + self.enemy_point_roll_2 + self.enemy_point_roll_3
                print("enemy point roll is : " + str(self.enemy_point_roll_total))
                print("enemy point roll 1: " + str(self.enemy_point_roll_1))
                print("enemy point roll 2: " + str(self.enemy_point_roll_2))
                print("enemy point roll 3: " + str(self.enemy_point_roll_3))
                self.enemy_point_roll = self.enemy_point_roll_total
                if self.enemy_point_roll_1 == self.enemy_point_roll_2 and self.enemy_point_roll_1 == self.enemy_point_roll_3:
                    print("Eney got  a triple win")
                    self.game_state = self.ENEMY_DEALS_DAMAGE_SCREEN
                    return
                if self.enemy_point_roll_1 == self.enemy_point_roll_2 and self.enemy_point_roll_1 != self.enemy_point_roll_3:
                    self.point_break = self.enemy_point_roll_1
                    self.game_state = self.ATTACK_PHASE_SCREEN
                    print("Your break point is: " + str(self.point_break))

                    return
                elif self.enemy_point_roll_1 == self.enemy_point_roll_3 and self.enemy_point_roll_1 != self.enemy_point_roll_2:
                    self.point_break = self.enemy_point_roll_1
                    self.game_state = self.ATTACK_PHASE_SCREEN
                    print("Your break point is: " + str(self.point_break))
                    return
                elif self.enemy_point_roll_2 == self.enemy_point_roll_3 and self.enemy_point_roll_2 != self.enemy_point_roll_1:
                    self.point_break = self.enemy_point_roll_2
                    self.game_state = self.ATTACK_PHASE_SCREEN
                    print("Your break point is: " + str(self.point_break))
                    return
                else:
                    self.player_win_init = True
                    self.enemy_win_init = False

            if self.point_break == 0:
                if controller.isTPressed:
                    controller.isTPressed = False
                    self.point_set_screen_logic_dice_fighter(controller)

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


    def display_attack_dice(self, state: "GameState", attack_roll_1: int, attack_roll_2: int, attack_roll_3: int, enemy_defense_roll: int) -> None:
        dice_x_start_position = 300  # Starting position for dice display
        dice_y_position = 50  # Y-position for attack dice (adjust as necessary)
        dice_x_gap = 120  # Gap between dice
        dice_faces = [
            pygame.Rect(50, 0, 133, 200),  # Dice face 1
            pygame.Rect(210, 0, 133, 200),  # Dice face 2
            pygame.Rect(370, 0, 133, 200),  # Dice face 3
            pygame.Rect(545, 0, 133, 200),  # Dice face 4
            pygame.Rect(710, 0, 133, 200),  # Dice face 5
            pygame.Rect(880, 0, 133, 200)  # Dice face 6
        ]

        # Crop and blit the attack dice
        attack_rect1 = dice_faces[attack_roll_1 - 1]
        cropped_attack1 = self.dice_sprite_sheet.subsurface(attack_rect1)

        attack_rect2 = dice_faces[attack_roll_2 - 1]
        cropped_attack2 = self.dice_sprite_sheet.subsurface(attack_rect2)

        attack_rect3 = dice_faces[attack_roll_3 - 1]
        cropped_attack3 = self.dice_sprite_sheet.subsurface(attack_rect3)

        # Blit attack dice onto the display
        state.DISPLAY.blit(cropped_attack1, (dice_x_start_position, dice_y_position))
        state.DISPLAY.blit(cropped_attack2, (dice_x_start_position + dice_x_gap, dice_y_position))
        state.DISPLAY.blit(cropped_attack3, (dice_x_start_position + dice_x_gap * 2, dice_y_position))

        defense_y_position = dice_y_position + 200  # Y-position for defense dice below the attack dice
        defense_rect = dice_faces[enemy_defense_roll - 1]
        cropped_defense = self.dice_sprite_sheet.subsurface(defense_rect)

        # Blit defense dice onto the display
        state.DISPLAY.blit(cropped_defense, (dice_x_start_position, defense_y_position))

    def display_defense_dice(self, state: "GameState", defense_roll_1: int, defense_roll_2: int, defense_roll_3: int, player_defense_roll: int) -> None:
        dice_x_start_position = 300  # Starting position for dice display
        dice_y_position = 250  # Y-position for defense dice (adjust as necessary)
        dice_x_gap = 120  # Gap between dice
        dice_faces = [
            pygame.Rect(50, 0, 133, 200),  # Dice face 1
            pygame.Rect(210, 0, 133, 200),  # Dice face 2
            pygame.Rect(370, 0, 133, 200),  # Dice face 3
            pygame.Rect(545, 0, 133, 200),  # Dice face 4
            pygame.Rect(710, 0, 133, 200),  # Dice face 5
            pygame.Rect(880, 0, 133, 200)  # Dice face 6
        ]

        # Crop and blit the defense dice
        defense_rect1 = dice_faces[defense_roll_1 - 1]
        cropped_defense1 = self.dice_sprite_sheet.subsurface(defense_rect1)

        defense_rect2 = dice_faces[defense_roll_2 - 1]
        cropped_defense2 = self.dice_sprite_sheet.subsurface(defense_rect2)

        defense_rect3 = dice_faces[defense_roll_3 - 1]
        cropped_defense3 = self.dice_sprite_sheet.subsurface(defense_rect3)

        # Blit defense dice onto the display
        state.DISPLAY.blit(cropped_defense1, (dice_x_start_position, dice_y_position))
        state.DISPLAY.blit(cropped_defense2, (dice_x_start_position + dice_x_gap, dice_y_position))
        state.DISPLAY.blit(cropped_defense3, (dice_x_start_position + dice_x_gap * 2, dice_y_position))

        player_defense_y_position = dice_y_position + 150  # Display player's defense dice below regular defense dice
        player_defense_rect = dice_faces[player_defense_roll - 1]
        cropped_player_defense = self.dice_sprite_sheet.subsurface(player_defense_rect)

        # Blit player defense dice onto the display
        state.DISPLAY.blit(cropped_player_defense, (dice_x_start_position, player_defense_y_position))

    def display_dice_point_roll(self, state: "GameState",
                                player_point_roll_1: int, player_point_roll_2: int, player_point_roll_3: int,
                                enemy_point_roll_1: int, enemy_point_roll_2: int, enemy_point_roll_3: int) -> None:
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

        # Player dice rolls
        player_dice_rect1 = dice_faces[player_point_roll_1 - 1]
        player_dice_rect2 = dice_faces[player_point_roll_2 - 1]
        player_dice_rect3 = dice_faces[player_point_roll_3 - 1]

        cropped_player_dice1 = self.dice_sprite_sheet.subsurface(player_dice_rect1)
        cropped_player_dice2 = self.dice_sprite_sheet.subsurface(player_dice_rect2)
        cropped_player_dice3 = self.dice_sprite_sheet.subsurface(player_dice_rect3)

        state.DISPLAY.blit(cropped_player_dice1, (dice_x_start_position, dice_y_position))  # First dice position
        state.DISPLAY.blit(cropped_player_dice2, (dice_x_start_position + dice_x_gap, dice_y_position))  # Second dice position
        state.DISPLAY.blit(cropped_player_dice3, (dice_x_start_position + 2 * dice_x_gap, dice_y_position))  # Third dice position

        # Enemy dice rolls
        enemy_dice_rect1 = dice_faces[enemy_point_roll_1 - 1]
        enemy_dice_rect2 = dice_faces[enemy_point_roll_2 - 1]
        enemy_dice_rect3 = dice_faces[enemy_point_roll_3 - 1]

        cropped_enemy_dice1 = self.dice_sprite_sheet.subsurface(enemy_dice_rect1)
        cropped_enemy_dice2 = self.dice_sprite_sheet.subsurface(enemy_dice_rect2)
        cropped_enemy_dice3 = self.dice_sprite_sheet.subsurface(enemy_dice_rect3)

        # Adjust y-position for enemy dice
        enemy_dice_y_position = dice_y_position + 200  # Assuming 200px below player dice

        state.DISPLAY.blit(cropped_enemy_dice1, (dice_x_start_position, enemy_dice_y_position))  # First dice position
        state.DISPLAY.blit(cropped_enemy_dice2, (dice_x_start_position + dice_x_gap, enemy_dice_y_position))  # Second dice position
        state.DISPLAY.blit(cropped_enemy_dice3, (dice_x_start_position + 2 * dice_x_gap, enemy_dice_y_position))  # Third dice position


    def display_dice_init_roll(self, state: "GameState",
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
            player_dice_rect1 = dice_faces[player_init_roll_1 - 1]
            player_dice_rect2 = dice_faces[player_init_roll_2 - 1]
            player_dice_rect3 = dice_faces[player_init_roll_3 - 1]

            cropped_player_dice1 = self.dice_sprite_sheet.subsurface(player_dice_rect1)
            cropped_player_dice2 = self.dice_sprite_sheet.subsurface(player_dice_rect2)
            cropped_player_dice3 = self.dice_sprite_sheet.subsurface(player_dice_rect3)

            state.DISPLAY.blit(cropped_player_dice1, (dice_x_start_position, dice_y_position))  # First dice position
            state.DISPLAY.blit(cropped_player_dice2, (dice_x_start_position + dice_x_gap, dice_y_position))  # Second dice position
            state.DISPLAY.blit(cropped_player_dice3, (dice_x_start_position + 2 * dice_x_gap, dice_y_position))  # Third dice position

            # Enemy dice rolls
            enemy_dice_rect1 = dice_faces[enemy_init_roll_1 - 1]
            enemy_dice_rect2 = dice_faces[enemy_init_roll_2 - 1]
            enemy_dice_rect3 = dice_faces[enemy_init_roll_3 - 1]

            cropped_enemy_dice1 = self.dice_sprite_sheet.subsurface(enemy_dice_rect1)
            cropped_enemy_dice2 = self.dice_sprite_sheet.subsurface(enemy_dice_rect2)
            cropped_enemy_dice3 = self.dice_sprite_sheet.subsurface(enemy_dice_rect3)

            # Adjust y-position for enemy dice
            enemy_dice_y_position = dice_y_position + 200  # Assuming 200px below player dice

            state.DISPLAY.blit(cropped_enemy_dice1, (dice_x_start_position, enemy_dice_y_position))  # First dice position
            state.DISPLAY.blit(cropped_enemy_dice2, (dice_x_start_position + dice_x_gap, enemy_dice_y_position))  # Second dice position
            state.DISPLAY.blit(cropped_enemy_dice3, (dice_x_start_position + 2 * dice_x_gap, enemy_dice_y_position))  # Third dice position









