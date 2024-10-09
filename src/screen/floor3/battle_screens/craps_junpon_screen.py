import pygame
import random

from constants import WHITE, RED, GREEN
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
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
        self.start_time = 0
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)

        self.dice_roll_1: int = 0
        self.dice_roll_2: int = 0
        self.dice_roll_2: int = 0
        self.power_meter_index: int = 0
        self.point_roll_total: int = 0
        self.point_roll_choices: list[str] = ["Play", "Blow",  "Bet"]
        self.magic_screen_choices: list[str] = [Magic.CRAPS_LUCKY_7.value, "Back"]
        self.bet_screen_choices: list[str] = ["Back"]
        self.magic_screen_index: int = 0
        self.point_roll_index: int = 0
        self.point_roll_dice_index: int = 0
        self.roll_dice = True  # Track if dice sound should be played

        self.point_blow_index: int = 1
        self.point_bet_index: int = 2
        self.bet: int = 100
        self.bet_minimum: int = 100
        pygame.mixer.music.stop()
        self.lucky_seven_buff_counter: int = 0
        self.magic_lock: bool = False
        self.lucky_seven_flag = False
        self.is_timer_active = True  # Timer is no longer active
        self.blit_message_x = 65
        self.blit_message_y = 460




        self.triple_dice_cast_cost = 50

        self.lucky_seven_buff_not_active = 0
        self.junpon_bankrupt = 0
        self.player_stamina_low_cost = 5
        self.magic_screen_menu_lucky_seven_index = 0
        self.magic_screen_menu_back_index = 1
        self.lock_down_inactive = 0
        self.power_meter_speed = 2
        self.power_meter_goal = 80
        self.index_stepper = 1
        self.dice_roll = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/dice_rolling.wav")  # Adjust the path as needed
        self.dice_roll.set_volume(0.6)

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
                "Rolls 3 dice instead of 2 during point roll."
            ]),
            self.MAGIC_MENU_BACK_DESCRIPTION: MessageBox([
                "go back to previous menu"
            ]),
            self.POWER_METER_MESSAGE: MessageBox([
                "PRESS P at the correct time"
            ]),
            self.POINT_ROLL_MESSAGE: MessageBox([
                "I'm here to lead the point"
            ]),
            self.PLAYER_WIN_COME_OUT_ROLL_MESSAGE: MessageBox([
                "You rolled a lucky 7 congrats."
            ]),
            # self.PLAYER_LOSE_COME_OUT_ROLL_MESSAGE: MessageBox([
            #     f"You rolled a bad roll"
            # ]),
            self.PLAYER_LOSE_POINT_ROLL_MESSAGE: MessageBox([
                "You rolled a bad roll"  # Placeholder text or initial message
            ]),

            self.PLAYER_LOSE_COME_OUT_ROLL_MESSAGE: MessageBox([
                "You rolled a bad roll"  # Placeholder text or initial message
            ]),


            self.POINT_ROLL_ROLLED_DICE_MESSAGE: MessageBox([
                f"Whoa You rolled a place holder"
            ]),

        }

    POWER_METER_MESSAGE = "power_meter_message"
    MAGIC_MENU_TRIPLE_DICE_DESCRIPTION = "magic_menu_triple_dice_description"
    MAGIC_MENU_BACK_DESCRIPTION = "magic_menu_back_description"
    POINT_ROLL_MESSAGE = "point_roll_message"
    PLAYER_WIN_COME_OUT_ROLL_MESSAGE = "player_win_come_out_roll_message"
    PLAYER_LOSE_COME_OUT_ROLL_MESSAGE = "player_lose_come_out_roll_message"
    PLAYER_WIN_POINT_ROLL_MESSAGE = "player_win_point_roll_message"
    PLAYER_LOSE_POINT_ROLL_MESSAGE = "player_lose_point_roll_message"
    # POINT_ROLL_ROLLING_DICE_MESSAGE = "point_roll_roll_rolling_dice_message"
    POINT_ROLL_ROLLED_DICE_MESSAGE = "point_roll_roll_rolled_dice_message"
    BET_MESSAGE = "bet_message"


    TRIPLE_DICE = "Triple Dice"
    # enemy spell maximize bet, this is active during come out roll

    PLAYER_WIN_COME_OUT_SCREEN = "player_win_come_out_screen"
    PLAYER_LOSE_COME_OUT_SCREEN = "player_lose_come_out_screen"
    BET_SCREEN = "Bet Screen"
    MAGIC_SCREEN = "Magic Screen"
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

        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].update(state)
            self.bet_screen_helper(state)

        elif self.game_state == self.MAGIC_MENU_SCREEN:
            if self.magic_screen_index == 0:
                self.battle_messages[self.MAGIC_MENU_TRIPLE_DICE_DESCRIPTION].update(state)
                self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()

            elif self.magic_screen_index == 1:
                self.battle_messages[self.MAGIC_MENU_TRIPLE_DICE_DESCRIPTION].reset()

                self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)


            if controller.isUpPressed:
                controller.isUpPressed = False

                self.menu_movement_sound.play()
                self.magic_screen_index = (self.magic_screen_index - 1) % len(self.magic_screen_choices)
            elif controller.isDownPressed:
                controller.isDownPressed = False
                self.menu_movement_sound.play()
                self.magic_screen_index = (self.magic_screen_index +1 ) % len(self.magic_screen_choices)

            if controller.isTPressed:
                controller.isTPressed = False
                if self.magic_screen_index == 0 and state.player.focus_points >= self.double_dice_cast_cost:
                    self.lucky_seven_buff_counter = 10
                    self.spell_sound.play()  # Play the sound effect once
                    state.player.focus_points -= self.triple_dice_cast_cost
                    self.magic_lock = True
                    self.game_state = self.WELCOME_SCREEN


        elif self.game_state == self.POWER_METER_SCREEN:
            self.power_meter_screen_helper(state)
            self.battle_messages[self.POWER_METER_MESSAGE].update(state)


        elif self.game_state == self.PLAYER_WIN_COME_OUT_SCREEN:
            if controller.isTPressed:
                controller.isTPressed = False
                self.game_state = self.WELCOME_SCREEN
            self.battle_messages[self.PLAYER_WIN_COME_OUT_ROLL_MESSAGE].update(state)


        elif self.game_state == self.PLAYER_LOSE_COME_OUT_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_COME_OUT_ROLL_MESSAGE].update(state)


        elif self.game_state == self.POINT_ROLL_SCREEN:
            self.point_screen_helper(state)


        elif self.game_state == self.PLAYER_LOSE_POINT_ROLL_SCREEN:
            print("player lose point rollllller")

            if controller.isTPressed:
                controller.isTPressed = False
                self.game_state = self.WELCOME_SCREEN



        elif self.game_state == self.PLAYER_WIN_POINT_ROLL_SCREEN:
            print("player win point rollllller")
            if controller.isTPressed:
                controller.isTPressed = False
                self.game_state = self.WELCOME_SCREEN

        elif self.game_state == self.GAME_OVER_SCREEN:
            no_money_game_over = 0
            no_stamina_game_over = 0
            if state.player.money <= no_money_game_over:
                if controller.isTPressed:
                    controller.isTPressed = False
                    state.currentScreen = state.gameOverScreen
                    state.gameOverScreen.start(state)
            elif state.player.stamina <= no_stamina_game_over:
                if controller.isTPressed:
                    controller.isTPressed = False
                    state.currentScreen = state.area2RestScreen
                    state.area2RestScreen.start(state)

    def draw(self, state: 'GameState'):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)
        self.draw_box_info(state)


        if self.game_state == self.WELCOME_SCREEN:
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)
            self.battle_messages[self.WELCOME_MESSAGE].draw(state)

        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].draw(state)

        elif self.game_state == self.MAGIC_MENU_SCREEN:
            if self.magic_screen_index == 0:
                self.battle_messages[self.MAGIC_MENU_TRIPLE_DICE_DESCRIPTION].draw(state)
            elif self.magic_screen_index == 1:
                self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)

            black_box_height = 221 - 50  # Adjust height
            black_box_width = 200 - 10  # Adjust width to match the left box
            border_width = 5
            start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
            start_y_right_box = 240  # Adjust vertical alignment

            # Create the black box
            black_box = pygame.Surface((black_box_width, black_box_height))
            black_box.fill((0, 0, 0))

            # Create a white border
            white_border = pygame.Surface(
                (black_box_width + 2 * border_width, black_box_height + 2 * border_width)
            )
            white_border.fill((255, 255, 255))
            white_border.blit(black_box, (border_width, border_width))

            # Determine the position of the white-bordered box
            black_box_x = start_x_right_box - border_width
            black_box_y = start_y_right_box - border_width

            # Blit the white-bordered box onto the display
            state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

            # Draw the menu options
            for idx, choice in enumerate(self.magic_screen_choices):
                y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, (255, 255, 255)),
                    (start_x_right_box + 60, y_position + 15)
                )

            if self.magic_screen_index == 0:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 12)
                )
            elif self.magic_screen_index == 1:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 52)
                )


        elif self.game_state == self.POWER_METER_SCREEN:
            self.create_meter(state, self.power_meter_index)
            self.battle_messages[self.POWER_METER_MESSAGE].draw(state)



        elif self.game_state == self.PLAYER_WIN_COME_OUT_SCREEN:
            self.battle_messages[self.PLAYER_WIN_COME_OUT_ROLL_MESSAGE].draw(state)

        elif self.game_state == self.PLAYER_LOSE_COME_OUT_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_POINT_ROLL_MESSAGE].messages = f"You rolled a {self.come_out_roll_total}"

            self.battle_messages[self.PLAYER_LOSE_POINT_ROLL_MESSAGE].draw(state)



        elif self.game_state == self.POINT_ROLL_SCREEN:

            self.draw_menu_selection_box(state)
            self.draw_point_screen_box_info(state)

            # Check if 2 seconds have passed and a dice roll has been made
            if self.is_timer_active == False and self.dice_roll_1 > 0:
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)
                state.DISPLAY.blit(self.font.render(f"You need a {self.come_out_roll_total} and you rolled an: {self.point_roll_total} ", True, WHITE), (self.blit_message_x, self.blit_message_y))
            else:
                state.DISPLAY.blit(self.font.render(f"Rolling the dice ", True, WHITE), (self.blit_message_x, self.blit_message_y))




        elif self.game_state == self.PLAYER_WIN_COME_OUT_SCREEN:
            self.battle_messages[self.PLAYER_WIN_POINT_ROLL_MESSAGE].draw(state)

        elif self.game_state == self.PLAYER_LOSE_COME_OUT_SCREEN:
            self.battle_messages[self.PLAYER_LOSE_POINT_ROLL_MESSAGE].draw(state)



        elif self.game_state == self.PLAYER_LOSE_POINT_ROLL_SCREEN:
            # print("ARE WE IN HERE YET????")
            state.DISPLAY.blit(self.font.render(f"You LOSE! You rolled a: {self.point_roll_total}", True, WHITE), (self.blit_message_x, self.blit_message_y))


        elif self.game_state == self.PLAYER_WIN_POINT_ROLL_SCREEN:
            # print("WE better not fucking be here")
            state.DISPLAY.blit(self.font.render(f"You WIN! Point: {self.point_roll_total} matching come out roll {self.come_out_roll_total}", True, WHITE), (self.blit_message_x, self.blit_message_y))


        elif self.game_state == self.GAME_OVER_SCREEN:
            no_money_game_over = 0
            no_stamina_game_over = 0
            if state.player.money <= no_money_game_over:
                state.DISPLAY.blit(self.font.render(f"You ran out of money and are now a prisoner of hell", True, WHITE), (self.blit_message_x, self.blit_message_y))
            elif state.player.stamina <= no_stamina_game_over:
                state.DISPLAY.blit(self.font.render(f"You ran out of stamina , you lose -100 gold", True, WHITE), (self.blit_message_x, self.blit_message_y))
        pygame.display.flip()


    def bet_screen_helper(self, state):
        controller = state.controller
        player_at_come_out_roll_phase = 0
        player_at_point_phase = 0

        if self.point_roll_total == player_at_come_out_roll_phase:

            if controller.isUpPressed:
                controller.isUPPressed = False
                self.menu_movement_sound.play()  # Play the sound effect once
                self.bet += 25

                if self.point_roll_total == 0:
                    if self.bet >= 75:
                        self.bet = 75
            if controller.isDownPressed:
                controller.isDownPressed = False
                self.bet -= 25

                self.menu_movement_sound.play()  # Play the sound effect once
                if self.bet <= 25:
                    self.bet = 25

            if controller.isBPressed:
                controller.isBPressed = False
                self.game_state = self.WELCOME_SCREEN

        elif self.point_roll_total > player_at_point_phase:

            if controller.isUpPressed:
                controller.isUPPressed = False
                self.menu_movement_sound.play()  # Play the sound effect once
                self.bet += 25

                if self.point_roll_total == 0:
                    if self.bet >= 200:
                        self.bet = 200
            if controller.isDownPressed:
                controller.isDownPressed = False
                self.bet -= 25

                self.menu_movement_sound.play()  # Play the sound effect once
                if self.bet <= 25:
                    self.bet = 25

            if controller.isBPressed:
                controller.isBPressed = False
                self.game_state = self.POINT_ROLL_SCREEN

    def point_screen_helper(self, state):
        controller = state.controller
        controller.update()
        print("YOur point roll is : " + str(self.point_roll_total))
        if controller.isTPressed and not self.is_timer_active:
            controller.isTPressed = False

            if self.point_roll_index == self.point_roll_dice_index:
                # Set the start time once when the button is pressed
                self.start_time = pygame.time.get_ticks()  # Set start time
                self.is_timer_active = True  # Activate the timer (so the button can't be pressed again immediately)
                # self.battle_messages[self.POINT_ROLL_ROLLING_DI

                # Call the method to check if 2 seconds have passed
                if self.is_timer_active and self.rolling_dice_timer():
                    # After 2 seconds, roll the dice
                    self.dice_roll_1 = random.randint(1, 6)
                    print("Dice roll of 1 is: " + str(self.dice_roll_1))
                    self.dice_roll_2 = random.randint(1, 6)
                    print("Dice roll of 2 is: " + str(self.dice_roll_2))
                    self.point_roll_total = self.dice_roll_1 + self.dice_roll_2
                    self.is_timer_active = False
                    print("Timer ended, dice rolled.")

                    # Check for a roll of 7 first, which is a losing condition
                    if self.point_roll_total == 7:
                        print("The point roll is 7, you better see this")
                        self.game_state = self.PLAYER_LOSE_POINT_ROLL_SCREEN
                        return  # Exit here to ensure no further checks occur

                    elif self.point_roll_total == self.come_out_roll_total:
                        self.game_state = self.PLAYER_WIN_POINT_ROLL_SCREEN
                        return  # Exit here to ensure no further checks occur


                elif self.point_roll_index == self.point_blow_index:
                    print("blowing on the dice for good luck")
                elif self.point_roll_index == self.point_bet_index:
                    print("time to make a bet")

                if controller.isUpPressed and self.is_timer_active == False:
                    self.menu_movement_sound.play()  # Play the sound effect once

                    self.point_roll_index = (self.point_roll_index - self.index_stepper) % len(self.point_roll_choices)
                    print(str(self.point_roll_index))
                    controller.isUpPressed = False
                elif controller.isDownPressed and self.is_timer_active == False:
                    self.menu_movement_sound.play()  # Play the sound effect once
                    self.point_roll_index = (self.point_roll_index + self.index_stepper) % len(self.point_roll_choices)
                    controller.isDownPressed = False

            elif self.game_state == self.PLAYER_WIN_COME_OUT_SCREEN:
                self.battle_messages[self.PLAYER_WIN_POINT_ROLL_MESSAGE].update(state)

            elif self.game_state == self.PLAYER_LOSE_COME_OUT_SCREEN:
                # Update the existing message in the battle_messages dictionary

                # Then call the update method to reflect changes
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
                self.game_state = self.BET_SCREEN

            elif self.welcome_screen_index == self.welcome_screen_quit_index and self.lock_down == self.lock_down_inactive:
                self.reset_craps_game(state)
                # state.current_player = state.area3GamblingScreen
                # state.area3GamblingScreen.start(state)

    def draw_point_screen_box_info(self, state: 'GameState'):
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

        for idx, choice in enumerate(self.point_roll_choices):
            y_position = start_y_right_box + idx * spacing_between_choices  # Adjust spacing between choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        if self.point_roll_index == self.point_roll_dice_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_play)
            )
        elif self.point_roll_index == self.point_blow_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_magic)
            )
        elif self.point_roll_index == self.point_bet_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box + arrow_y_coordinate_padding_bet)
            )

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

    def draw_box_info(self, state: 'GameState'):

        player_enemy_box_info_x_position = 37
        enemy_name_y_position = 33
        enemy_money_y_position = 70
        enemy_status_y_position = 110
        bet_y_position = 370
        player_money_y_position = 250
        hero_name_y_position = 205
        hero_stamina_y_position = 290
        hero_focus_y_position = 330


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

    def rolling_dice_timer(self) -> bool:
        """Returns True if 2 seconds have passed since start_time, otherwise False."""
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 1000 and self.roll_dice == True:
            self.dice_roll.play()
            self.roll_dice = False

        if current_time - self.start_time >= 2000:
            self.is_timer_active = False  # Timer is no longer active after 2 seconds
            self.roll_dice = True
            return True  # 2 seconds have passed
        return False  # Timer is still running


    def display_dice(self, state: "GameState", dice_roll_1: int, dice_roll_2: int) -> None:

        # Define the rectangles for each dice face
        dice_faces = [
            pygame.Rect(50, 0, 133, 200),  # Dice face 1=
            pygame.Rect(210, 0, 133, 200),  # Dice face 2
            pygame.Rect(370, 0, 133, 200),  # Dice face 3
            pygame.Rect(545, 0, 133, 200),  # Dice face 4
            pygame.Rect(710, 0, 133, 200),  # Dice face
            pygame.Rect(880, 0, 133, 200)  # Dice face 6p
        ]

        # Get the rectangles for the rolled dice
        dice_rect1 = dice_faces[dice_roll_1 - 1]
        cropped_dice1 = self.sprite_sheet.subsurface(dice_rect1)  # Crop the first dice image

        dice_rect2 = dice_faces[dice_roll_2 - 1]
        cropped_dice2 = self.sprite_sheet.subsurface(dice_rect2)  # Crop the second dice image




        # Blit the cropped dice images onto the display with a 30-pixel gap
        state.DISPLAY.blit(cropped_dice1, (300, 0))  # Adjusted y-coordinate for the first dice
        state.DISPLAY.blit(cropped_dice2, (420, 0))  # Placed the second dice 150 pixels to the right


    # Usage:
    # Call this method within your update method or any other place in your code where you need to show the dice roll result
    # Example:
    # self.display_dice(state, self.dice_roll_1)







#Charge: hold A button and rock d pad left and right
# Release right after last d pad button press
# this is for point roll
# the longer you wait the more of a bonus you get
# this is to get rid of times that you can roll 12 rolls
# this move requires stamina to use