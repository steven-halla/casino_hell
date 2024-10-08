import pygame
import random

from constants import WHITE, RED, GREEN
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from entity.gui.textbox.text_box import TextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic


class CrapsJunponScreen(GambleScreen):

    def __init__(self, screenName: str = "Craps") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.sprite_sheet: pygame.Surface = pygame.image.load("./assets/images/dice45.png")
        self.come_out_roll_total: int = 0
        self.dealer_name = "Junpon"

        self.dice_roll_1: int = 0
        self.dice_roll_2: int = 0
        self.dice_roll_2: int = 0
        self.power_meter_index: int = 0
        self.point_roll_total: int = 0
        self.point_roll_choices: list[str] = ["Play", "Bet"]
        self.magic_screen_choices: list[str] = [Magic.CRAPS_LUCKY_7.value, "Back"]
        self.bet_screen_choices: list[str] = ["Back"]
        self.welcome_screen_index: int = 0
        self.magic_screen_index: int = 0
        self.point_roll_index: int = 0
        self.bet: int = 100
        self.bet_minimum: int = 100
        pygame.mixer.music.stop()
        self.lucky_seven_buff_counter: int = 0
        self.magic_lock: bool = False
        self.lucky_seven_flag = False

        self.lucky_seven_buff_not_active = 0
        self.junpon_bankrupt = 0
        self.player_stamina_low_cost = 5
        self.magic_screen_menu_lucky_seven_index = 0
        self.magic_screen_menu_back_index = 1
        self.lock_down_inactive = 0
        self.power_meter_speed = 2
        self.power_meter_goal = 80

        self.failed_power_strike_sound_effect = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/9FBlockSword.wav")  # Adjust the path as needed
        self.failed_power_strike_sound_effect.set_volume(0.6)

        self.successful_power_strike_sound_effect = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/8CRodHit.wav")  # Adjust the path as needed
        self.successful_power_strike_sound_effect.set_volume(0.6)

        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "This is the first message"
            ]),
            self.BET_MESSAGE: MessageBox([
                "Max bet of 75 during Come out Roll. Point Roll Max is 200"
            ]),
            self.MAGIC_MENU_TRIPLE_DICE_DESCRIPTION: MessageBox([
                "description for magic meter"
            ]),
            self.POWER_METER_MESSAGE: MessageBox([
                "PRESS P at the correct time"
            ]),
            self.POINT_ROLL_MESSAGE: MessageBox([
                "I'm here to lead the point"
            ]),
            self.PLAYER_WIN_COME_OUT_ROLL_MESSAGE: MessageBox([
                "You rolled a lucky 7 congrats"
            ]),
            self.PLAYER_LOSE_COME_OUT_ROLL_MESSAGE: MessageBox([
                f"You rolled a bad roll"
            ]),
        }
    POWER_METER_MESSAGE = "power_meter_message"
    MAGIC_MENU_TRIPLE_DICE_DESCRIPTION = "magic_menu_triple_dice_description"
    POINT_ROLL_MESSAGE = "point_roll_message"
    PLAYER_WIN_COME_OUT_ROLL_MESSAGE = "player_win_come_out_roll_message"
    PLAYER_LOSE_COME_OUT_ROLL_MESSAGE = "player_lose_come_out_roll_message"
    PLAYER_WIN_POINT_ROLL_MESSAGE = "player_win_point_roll_message"
    PLAYER_LOSE_POINT_ROLL_MESSAGE = "player_lose_point_roll_message"

    TRIPLE_DICE = "Triple Dice"
    # enemy spell maximize bet, this is active during come out roll

    PLAYER_WIN_COME_OUT_SCREEN = "player_win_come_out_screen"
    PLAYER_LOSE_COME_OUT_SCREEN = "player_lose_come_out_screen"
    POWER_METER_SCREEN = "power_meter_screen"
    POINT_ROLL_SCREEN = "point_roll_screen"
    PLAYER_WIN_POINT_ROLL_SCREEN = "player_win_point_roll_screen"
    PLAYER_LOSE_POINT_ROLL_SCREEN = "player_win_point_roll_screen"


    def start(self, state: 'GameState'):
        pass

    def reset_craps_game(self, state: 'GameState'):
        self.welcome_screen_quit_index = self.welcome_screen_play_index
        self.lucky_seven_buff_counter = self.lucky_seven_buff_not_active
        self.magic_lock = False
        self.bet = self.bet_minimum
        self.lucky_seven = False
        state.player.canMove = True
        self.dice_roll_1 = 0
        self.dice_roll_2 = 0
        self.dice_roll_3 = 0

    def create_meter(self, state: "GameState", power: int) -> None:
        meter_width = 300  # Three times wider
        meter_height = 30
        max_power = 100
        white_border_width = 2
        meter_x_position = 250
        meter_y_position = 50
        line_y_start = 50
        line_y_end = 80
        line_thickness = 5
        # Calculate the width of the filled portion of the meter
        filled_width = int((power / max_power) * meter_width)

        # Draw the background of the meter (empty portion)
        meter_bg_rect = pygame.Rect(meter_x_position, meter_y_position, meter_width, meter_height)  # Position: (250, 50)
        pygame.draw.rect(state.DISPLAY, RED, meter_bg_rect)  # Red background

        # Draw the filled portion of the meter


        meter_fill_rect = pygame.Rect(meter_x_position, meter_y_position, filled_width, meter_height)
        pygame.draw.rect(state.DISPLAY, GREEN, meter_fill_rect)  # Green filled portion

        # Draw the border of the meter
        pygame.draw.rect(state.DISPLAY, WHITE, meter_bg_rect, white_border_width)  # White border

        goal_position = int((self.power_meter_goal / max_power) * meter_width) + meter_x_position  # Adjust position to start from 250


        pygame.draw.line(state.DISPLAY, WHITE, (goal_position, line_y_start), (goal_position, line_y_end), line_thickness)

    def update(self, state: 'GameState'):
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        if self.money <= self.junpon_bankrupt:
            Events.add_event_to_player(state.player, Events.CRAPS_JUNPON_DEFEATED)

        try:
            if self.lucky_seven_buff_counter > self.lucky_seven_buff_not_active:
                self.magic_lock = True
            elif self.lucky_seven_buff_counter == self.lucky_seven_buff_not_active:
                self.magic_lock = False
        except AttributeError:
            print("AttributeError: lucky_seven_buff_counter does not exist")
            self.magic_lock = False
        except TypeError:
            print("TypeError: lucky_seven_buff_counter is not of the expected type")
            self.magic_lock = False

        if self.game_state == self.WELCOME_SCREEN:
            self.welcome_screen_helper(state)
            self.battle_messages[self.WELCOME_MESSAGE].update(state)


        elif self.game_state == self.POWER_METER_SCREEN:
            self.power_meter_screen_helper(state)
            self.battle_messages[self.POWER_METER_MESSAGE].update(state)


        elif self.game_state == self.PLAYER_WIN_COME_OUT_SCREEN:
            print("player wins point roll lucky ducky 7")
            self.battle_messages[self.PLAYER_WIN_COME_OUT_ROLL_MESSAGE].update(state)


        elif self.game_state == self.PLAYER_LOSE_COME_OUT_SCREEN:
            print("player lose come out screen")
            self.battle_messages[self.PLAYER_LOSE_COME_OUT_ROLL_MESSAGE].update(state)


        elif self.game_state == self.POINT_ROLL_SCREEN:
            self.battle_messages[self.POINT_ROLL_MESSAGE].update(state)

        elif self.game_state == self.PLAYER_WIN_COME_OUT_SCREEN:
            self.battle_messages[self.PLAYER_WIN_POINT_ROLL_MESSAGE].update(state)

        elif self.game_state == self.PLAYER_LOSE_COME_OUT_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_POINT_ROLL_MESSAGE].update(state)






    def power_meter_screen_helper(self, state):
        controller = state.controller
        controller.update()

        self.battle_messages[self.POWER_METER_MESSAGE].update(state)

        erika_nugget_amulet_protection = 4
        power_meter_max = 100
        power_meter_min = 0
        power_meter_success = 80
        player_lucky_7_come_out_roll_reward = 7

        self.power_meter_index += self.power_meter_speed
        if self.power_meter_index >= power_meter_max:
            self.power_meter_index = power_meter_min

        if controller.isPPressed:
            self.power_meter_speed = power_meter_min
            self.power_meter_index = self.power_meter_index
            controller.isPPressed = False
            if self.power_meter_index >= power_meter_success:
                self.successful_power_strike_sound_effect.play()
                self.lucky_seven = True
            elif self.power_meter_index < power_meter_success:
                self.failed_power_strike_sound_effect.play()
            if self.lucky_seven == True:
                lucky_player_bonus = state.player.luck
                luck_roll_success = 85
                luck_multiplier = 2
                lucky_7_roll = random.randint(1, 100) + (lucky_player_bonus * luck_multiplier)
                print("Lucky roll 7 is: " + str(lucky_7_roll))
                if lucky_7_roll >= luck_roll_success:
                    print("Lucky Roll of 7")
                    self.dice_roll_1 = 1
                    self.dice_roll_2 = 6
                    self.come_out_roll_total = player_lucky_7_come_out_roll_reward
                    self.game_state = self.PLAYER_WIN_COME_OUT_SCREEN
                elif lucky_7_roll < luck_roll_success:
                    self.dice_roll_1 = random.randint(1, 6)
                    print("Dice roll of 1 is: " + str(self.dice_roll_1))
                    self.dice_roll_2 = random.randint(1, 6)
                    print("Dice roll of 2 is: " + str(self.dice_roll_2))
                    self.come_out_roll_total = self.dice_roll_1 + self.dice_roll_2
                    print("come out roll is : " + str(self.come_out_roll_total))
                    if self.come_out_roll_total == 2:
                        self.game_state = self.PLAYER_LOSE_COME_OUT_SCREEN
                    elif self.come_out_roll_total == 3:
                        if Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value not in state.player.equipped_items:
                            self.game_state =  self.PLAYER_LOSE_COME_OUT_SCREEN
                        else:
                            self.successful_power_strike_sound_effect.play()
                            self.dice_roll_1 = erika_nugget_amulet_protection
                            self.dice_roll_2 = erika_nugget_amulet_protection
                            self.come_out_roll_total = self.dice_roll_1 + self.dice_roll_2
                            self.game_state = "point_phase_screen"
                    elif self.come_out_roll_total == 12:
                        self.game_state = self.PLAYER_LOSE_COME_OUT_SCREEN
                    elif self.come_out_roll_total == 7:
                        self.unlucky_seven_flag = True
                        self.game_state = self.PLAYER_WIN_COME_OUT_SCREEN
                    else:
                        print("come out roll is : " + str(self.come_out_roll_total))
                        self.game_state = self.POINT_ROLL_SCREEN


    def welcome_screen_helper(self, state: "GameState") -> None:
        controller = state.controller
        controller.update()
        self.battle_messages[self.WELCOME_MESSAGE].update(state)
        if state.controller.isTPressed:
            state.controller.isTPressed = False
            if self.welcome_screen_index == self.welcome_screen_play_index:
                self.game_state = self.POWER_METER_SCREEN
                state.player.stamina_points -= self.player_stamina_low_cost

            elif self.welcome_screen_index == self.welcome_screen_magic_index and self.magic_lock == False \
                    and Magic.CRAPS_LUCKY_7.value in state.player.magicinventory:
                self.magic_screen_index = self.magic_screen_menu_lucky_seven_index
                self.battle_messages[self.MAGIC_MENU_TRIPLE_DICE_DESCRIPTION].reset()
                self.game_state = self.MAGIC_MENU_SCREEN

            elif self.welcome_screen_index == self.welcome_screen_bet_index:
                self.game_state = self.BET_MENU_SCREEN

            elif self.welcome_screen_index == self.welcome_screen_quit_index and self.lock_down == self.lock_down_inactive:
                self.reset_craps_game(state)
                # state.current_player = state.area3GamblingScreen
                # state.area3GamblingScreen.start(state)




    def draw_box_info(self, state: 'GameState'):
        arrow_x_coordinate_padding = 12
        arrow_y_coordinate_padding_play = 12
        arrow_y_coordinate_padding_magic = 52
        arrow_y_coordinate_padding_bet = 92
        arrow_y_coordinate_padding_quit = 132
        player_enemy_box_info_x_position = 37
        enemy_name_y_position = 33
        enemy_money_y_position = 70
        enemy_status_y_position = 110
        bet_y_position = 370
        player_money_y_position = 250
        hero_name_y_position = 205
        hero_stamina_y_position = 290
        hero_focus_y_position = 330
        box_width_offset = 10
        horizontal_padding = 25
        vertical_position = 240
        spacing_between_choices = 40
        text_x_offset = 60
        text_y_offset = 15
        black_box_width = 200 - box_width_offset
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - horizontal_padding
        start_y_right_box = vertical_position

        state.DISPLAY.blit(self.font.render(self.dealer_name, True, WHITE), (player_enemy_box_info_x_position, enemy_name_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}", True, WHITE), (player_enemy_box_info_x_position, enemy_money_y_position))
        if self.lucky_seven_buff_counter == self.lucky_seven_buff_not_active:
            state.DISPLAY.blit(self.font.render(f"{self.STATUS_GREEN}", True, WHITE), (player_enemy_box_info_x_position, enemy_status_y_position))
        elif self.lucky_seven_buff_counter > self.lucky_seven_buff_not_active:
            state.DISPLAY.blit(self.font.render(f"{self.TRIPLE_DICE}: {self.lucky_seven_buff_counter} ", True, WHITE), (player_enemy_box_info_x_position, enemy_status_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE), (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE), (player_enemy_box_info_x_position, player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE), (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE), (player_enemy_box_info_x_position, hero_focus_y_position))

        if self.lock_down <= self.lock_down_inactive:
            state.DISPLAY.blit(self.font.render(f"{self.HERO_HEADER}", True, WHITE), (player_enemy_box_info_x_position, hero_name_y_position))
        elif self.lock_down > self.lock_down_inactive:
            state.DISPLAY.blit(self.font.render(f"{self.LOCKED_DOWN_HEADER}:{self.lock_down}", True, RED), (player_enemy_box_info_x_position, hero_name_y_position))

        for idx, choice in enumerate(self.welcome_screen_choices):
            y_position = start_y_right_box + idx * spacing_between_choices  # Adjust spacing between choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        if Magic.CRAPS_LUCKY_7.value not in state.player.magicinventory:
            self.magic_lock = True
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif Magic.CRAPS_LUCKY_7.value in state.player.magicinventory:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

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

    def draw(self, state: 'GameState'):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)
        self.draw_menu_selection_box(state)
        self.draw_box_info(state)




        if self.game_state == self.WELCOME_SCREEN:
            self.battle_messages[self.WELCOME_MESSAGE].draw(state)


        elif self.game_state == self.POWER_METER_SCREEN:
            print("power meter screen")

            self.create_meter(state, self.power_meter_index)
            self.battle_messages[self.POWER_METER_MESSAGE].draw(state)



        elif self.game_state == self.PLAYER_WIN_COME_OUT_SCREEN:
            self.battle_messages[self.PLAYER_WIN_COME_OUT_ROLL_MESSAGE].draw(state)

            print("come out win screen")
            print("Come out roll is lucky 7 I hope: " + str(self.come_out_roll_total))

        elif self.game_state == self.PLAYER_LOSE_COME_OUT_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_COME_OUT_ROLL_MESSAGE].draw(state)

            print("come out lose screen")



        elif self.game_state == self.POINT_ROLL_SCREEN:
            print("point roll screen")
            self.battle_messages[self.POINT_ROLL_MESSAGE].draw(state)

        elif self.game_state == self.PLAYER_WIN_COME_OUT_SCREEN:
            self.battle_messages[self.PLAYER_WIN_POINT_ROLL_MESSAGE].draw(state)

        elif self.game_state == self.PLAYER_LOSE_COME_OUT_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_POINT_ROLL_MESSAGE].draw(state)

        pygame.display.flip()












#Charge: hold A button and rock d pad left and right
# Release right after last d pad button press
# this is for point roll
# the longer you wait the more of a bonus you get
# this is to get rid of times that you can roll 12 rolls
# this move requires stamina to use