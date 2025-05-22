import pygame
import random
from constants import WHITE, RED, GREEN, BLACK
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic

from typeguard import typechecked


# an eleven is a win condition for come out roll
# need to animate extra dice

class CrapsWimpletonScreen(GambleScreen):
    def __init__(self, screenName: str = "Craps") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.sprite_sheet: pygame.Surface = pygame.image.load("./assets/images/dice45.png")
        self.come_out_roll_total: int = 0
        self.dealer_name: str = "Naba"
        self.start_time: int = 0
        self.spell_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "./assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.dice_roll_1: int = 0
        self.dice_roll_2: int = 0
        self.dice_roll_2: int = 0
        self.power_meter_index: int = 0
        self.point_roll_total: int = 0
        self.point_roll_choices: list[str] = ["Play", "Blow", "Bet"]
        self.magic_screen_choices: list[str] = [Magic.CRAPS_LUCKY_7.value, Magic.GREED_METER.value,  "Back"]
        self.bet_screen_choices: list[str] = ["Back"]
        self.magic_screen_index: int = 0
        self.triple_dice_index: int = 0
        self.back_index: int = 1
        self.point_roll_index: int = 0
        self.point_roll_dice_index: int = 0
        self.roll_dice: bool = True
        self.point_blow_index: int = 1
        self.point_bet_index: int = 2
        self.bet: int = 75
        self.bet_minimum: int = 75
        pygame.mixer.music.stop()
        self.lucky_seven_buff_counter: int = 0
        self.triple_dice_counter_start_set = 10
        self.magic_lock: bool = False
        self.lucky_seven_flag: bool = False
        self.is_timer_active: bool = False
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        self.lucky_seven: bool = False
        self.triple_dice_cast_cost: int = 50
        self.set_variable_to_zero: int = 0
        self.lucky_seven_buff_not_active: int = 0
        self.naba_bankrupt: int = 0
        self.player_stamina_high_cost: int = 10
        self.player_stamina_med_cost: int = 5
        self.player_stamina_low_cost: int = 2
        self.magic_screen_menu_lucky_seven_index: int = 0
        self.magic_screen_menu_back_index: int = 1
        self.lock_down_inactive: int = 0
        self.power_meter_speed: int = 2
        self.reset_power_meter_to_base: int = 2
        self.power_meter_goal: int = 80
        self.piggy_meter_goal: int = 92
        self.index_stepper: int = 1
        self.counter_stepper: int = 1
        self.blow_counter: int = 0
        self.blow_meter: int = 0
        self.blow_turn: int = 0
        self.last_blow_decrement_time = pygame.time.get_ticks()  # Initialize to current game time
        self.blow_sound_checker: bool = True
        self.blow_timer_start = 0
        self.play_tune: bool = False
        self.blow_meter_ready: pygame.mixer.Sound = pygame.mixer.Sound("./assets/music/blowready.wav")
        self.blow_meter_ready.set_volume(0.6)
        self.dice_roll: pygame.mixer.Sound = pygame.mixer.Sound("./assets/music/dice_rolling.wav")
        self.dice_roll.set_volume(0.6)
        self.failed_power_strike_sound_effect: pygame.mixer.Sound = pygame.mixer.Sound(
            "./assets/music/9FBlockSword.wav")
        self.failed_power_strike_sound_effect.set_volume(0.6)
        self.successful_power_strike_sound_effect: pygame.mixer.Sound = pygame.mixer.Sound(
            "./assets/music/8CRodHit.wav")
        self.successful_power_strike_sound_effect.set_volume(0.6)
        self.wimpleton_magic_points: int = 2
        self.debuff_weighted_dice: int = 0
        self.debuff_counter: int = 3
        self.greed_meter: int = 0
        self.greed_bank: bool = False
        self.hungry_dice_increased_chance:int = 0

        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "This is the welcome screen"
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
            self.PLAYER_LOSE_POINT_ROLL_MESSAGE: MessageBox([
                "mmmm rolled a bad roll"
            ]),
            self.PLAYER_LOSE_COME_OUT_ROLL_MESSAGE: MessageBox([
                "You rolled a bad roll"
            ]),
            self.POINT_ROLL_ROLLED_DICE_MESSAGE: MessageBox([
                f"Whoa You rolled a place holder"
            ]),
            self.BLOW_POINT_ROLL_MESSAGE: MessageBox([
                f"Hold A key and rock d pad"
            ]),
            self.WIMPLETON_CASTING_SPELL_MESSAGE: MessageBox([
                f"Starving animals of eternal hunger, casts your misery upon the unworthy...weighted dice(all dice totals -1)"
            ]),
        }

    POWER_METER_MESSAGE: str = "power_meter_message"
    MAGIC_MENU_TRIPLE_DICE_DESCRIPTION: str = "magic_menu_triple_dice_description"
    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    POINT_ROLL_MESSAGE: str = "point_roll_message"
    PLAYER_WIN_COME_OUT_ROLL_MESSAGE: str = "player_win_come_out_roll_message"
    PLAYER_LOSE_COME_OUT_ROLL_MESSAGE: str = "player_lose_come_out_roll_message"
    PLAYER_WIN_POINT_ROLL_MESSAGE: str = "player_win_point_roll_message"
    PLAYER_LOSE_POINT_ROLL_MESSAGE: str = "player_lose_point_roll_message"
    POINT_ROLL_ROLLED_DICE_MESSAGE: str = "point_roll_roll_rolled_dice_message"
    BLOW_POINT_ROLL_MESSAGE: str = "blow_point_roll_message"
    BET_MESSAGE: str = "bet_message"
    WIMPLETON_CASTING_SPELL_MESSAGE: str = "WIMPLETON_CASTING_SPELL_MESSAGE"
    TRIPLE_DICE: str = "Triple Dice"
    PLAYER_WIN_COME_OUT_SCREEN: str = "player_win_come_out_screen"
    PLAYER_LOSE_COME_OUT_SCREEN: str = "player_lose_come_out_screen"
    BET_SCREEN: str = "Bet Screen"
    MAGIC_SCREEN: str = "Magic Screen"
    POWER_METER_SCREEN: str = "power_meter_screen"
    POINT_ROLL_SCREEN: str = "point_roll_screen"
    PLAYER_WIN_POINT_ROLL_SCREEN: str = "player_win_point_roll_screen"
    PLAYER_LOSE_POINT_ROLL_SCREEN: str = "player_lose_point_roll_screen"
    BLOW_POINT_ROLL_SCREEN: str = "blow_point_roll_screen"
    WIMPLETON_CASTING_SPELL_SCREEN: str = "junpon_cating_spell_screen"

    def start(self, state: 'GameState'):
        self.spirit_bonus: int = state.player.spirit
        self.magic_bonus: int = state.player.mind
        if (Magic.GREED_METER.value in state.player.magicinventory
                and Magic.GREED_METER.value not in self.magic_screen_choices):
            self.magic_screen_choices.append(Magic.GREED_METER.value)

    def round_reset(self, state: 'GameState'):

        self.bet = self.bet_minimum
        if self.lucky_seven_buff_counter >= self.lucky_seven_buff_not_active:
            self.lucky_seven_buff_counter -= self.counter_stepper
            if self.lucky_seven_buff_counter == self.lucky_seven_buff_not_active:
                self.magic_lock = False
            # put a check here if enemy_spell == 0 set magic lock to False
        self.point_roll_total = self.set_variable_to_zero
        self.come_out_roll_total = self.set_variable_to_zero
        self.dice_roll_1 = self.set_variable_to_zero
        self.dice_roll_2 = self.set_variable_to_zero
        self.dice_roll_3 = self.set_variable_to_zero
        self.power_meter_index = self.set_variable_to_zero
        self.power_meter_speed = self.reset_power_meter_to_base
        self.lucky_seven = True
        self.blow_counter = self.set_variable_to_zero
        self.blow_meter = self.set_variable_to_zero
        self.blow_turn = self.set_variable_to_zero
        self.blow_sound_checker = True
        self.blow_timer_start = 0
        self.debuff_counter = 3
        self.greed_bank = False
        if self.greed_meter > 0:
            self.greed_meter -= 1
            self.magic_lock = True
        if self.greed_meter == 0:
            self.magic_lock = False

        self.hungry_dice_increased_chance += 3

        dice_of_deception_random_chance = random.randint(1, 100) + self.hungry_dice_increased_chance

        if self.debuff_weighted_dice == 0 and self.wimpleton_magic_points > 0 and dice_of_deception_random_chance >= 100:
            self.hungry_dice_increased_chance = 0
            self.game_state = self.WIMPLETON_CASTING_SPELL_SCREEN

    def reset_craps_game(self, state: 'GameState'):
        self.welcome_screen_quit_index = self.welcome_screen_play_index
        self.lucky_seven_buff_counter = self.lucky_seven_buff_not_active
        self.magic_lock = False
        self.bet = self.bet_minimum
        self.lucky_seven = False
        state.player.canMove = True
        self.point_roll_total = self.set_variable_to_zero
        self.come_out_roll_total = self.set_variable_to_zero
        self.dice_roll_1 = self.set_variable_to_zero
        self.dice_roll_2 = self.set_variable_to_zero
        self.dice_roll_3 = self.set_variable_to_zero
        self.power_meter_index = self.set_variable_to_zero
        self.blow_counter = self.set_variable_to_zero
        self.blow_meter = self.set_variable_to_zero
        self.blow_turn = self.set_variable_to_zero
        self.blow_sound_checker = True
        self.blow_timer_start = 0
        self.debuff_counter = 3
        self.wimpleton_magic_points = 2
        self.debuff_weighted_dice = 0
        self.greed_meter: int = 0
        self.greed_bank: bool = False

    def update(self, state: 'GameState'):
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        if self.money <= self.naba_bankrupt:
            Events.add_event_to_player(state.player, Events.CRAPS_NABA_DEFEATED)

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
            self.update_welcome_screen_helper(state)
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
        elif self.game_state == self.WIMPLETON_CASTING_SPELL_SCREEN:
            self.battle_messages[self.WIMPLETON_CASTING_SPELL_MESSAGE].update(state)
            self.update_naba_casting_spell_helper(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].update(state)
            self.update_bet_screen_helper(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu_helper(state)
        elif self.game_state == self.POWER_METER_SCREEN:
            self.update_power_meter_screen_helper(state)
            self.battle_messages[self.POWER_METER_MESSAGE].update(state)
        elif self.game_state == self.PLAYER_WIN_COME_OUT_SCREEN:
            self.update_come_out_roll_helper(state)
            self.battle_messages[self.PLAYER_WIN_COME_OUT_ROLL_MESSAGE].update(state)
        elif self.game_state == self.PLAYER_LOSE_COME_OUT_SCREEN:
            self.update_player_lose_come_out_roll(state)
        elif self.game_state == self.POINT_ROLL_SCREEN:
            self.update_point_screen_helper(state)
        elif self.game_state == self.BLOW_POINT_ROLL_SCREEN:
            self.update_blow_point_roll_helper(state)
        elif self.game_state == self.PLAYER_LOSE_POINT_ROLL_SCREEN:
            self.update_player_lose_point_roll(state)
        elif self.game_state == self.PLAYER_WIN_POINT_ROLL_SCREEN:
            self.update_player_win_point_roll_helper(state)
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.game_over_screen_level_4(state, controller)

    def draw(self, state: 'GameState'):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)
        self.draw_box_info(state)

        if self.game_state == self.WIMPLETON_CASTING_SPELL_SCREEN:
            self.battle_messages[self.WIMPLETON_CASTING_SPELL_MESSAGE].draw(state)
        elif self.game_state == self.WELCOME_SCREEN:
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)
            self.battle_messages[self.WELCOME_MESSAGE].draw(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].draw(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box(state)
            if self.magic_screen_index == 0:
                self.battle_messages[self.MAGIC_MENU_TRIPLE_DICE_DESCRIPTION].draw(state)
            elif self.magic_screen_index == 1:
                self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)
        elif self.game_state == self.POWER_METER_SCREEN:
            self.draw_create_meter(state, self.power_meter_index)
            self.battle_messages[self.POWER_METER_MESSAGE].draw(state)
        elif self.game_state == self.PLAYER_WIN_COME_OUT_SCREEN:
            self.draw_display_dice(state, self.dice_roll_1, self.dice_roll_2)
            self.battle_messages[self.PLAYER_WIN_COME_OUT_ROLL_MESSAGE].draw(state)
        elif self.game_state == self.PLAYER_LOSE_COME_OUT_SCREEN:
            self.draw_display_dice(state, self.dice_roll_1, self.dice_roll_2)
            self.battle_messages[self.PLAYER_LOSE_COME_OUT_ROLL_MESSAGE].draw(state)
        elif self.game_state == self.POINT_ROLL_SCREEN:
            self.draw_menu_selection_box(state)
            self.draw_point_screen_box_info(state)
            if self.is_timer_active == False and self.dice_roll_1 > 0:
                self.draw_display_dice(state, self.dice_roll_1, self.dice_roll_2)
                state.DISPLAY.blit(self.font.render(
                    f"You need a {self.come_out_roll_total} and you rolled an: {self.point_roll_total} ", True, WHITE),
                                   (self.blit_message_x, self.blit_message_y))
            else:
                state.DISPLAY.blit(self.font.render(f"Rolling the dice ", True, WHITE),
                                   (self.blit_message_x, self.blit_message_y))
        elif self.game_state == self.BLOW_POINT_ROLL_SCREEN:
            time_elapsed: int = int((pygame.time.get_ticks() - self.blow_timer_start) / 1000)
            timer_x_pois = 333
            timer_y_pois = 125
            state.DISPLAY.blit(self.font.render(f"TIMER: {time_elapsed}/7  ", True, RED), (timer_x_pois, timer_y_pois))
            if time_elapsed >= 7:
                self.blow_timer_start = pygame.time.get_ticks()
            self.draw_create_blow_meter(state, time_elapsed)
            self.draw_create_blow_meter(state, self.blow_counter)
            self.battle_messages[self.BLOW_POINT_ROLL_MESSAGE].draw(state)
        elif self.game_state == self.PLAYER_WIN_POINT_ROLL_SCREEN:
            self.draw_display_dice(state, self.dice_roll_1, self.dice_roll_2)
            state.DISPLAY.blit(self.font.render(
                f"You WIN! Point: {self.point_roll_total} matching come out roll {self.come_out_roll_total}", True,
                WHITE), (self.blit_message_x, self.blit_message_y))
        elif self.game_state == self.PLAYER_LOSE_POINT_ROLL_SCREEN:
            self.draw_display_dice(state, self.dice_roll_1, self.dice_roll_2)
            state.DISPLAY.blit(self.font.render(f"You LOSE! You rolled a: {self.point_roll_total}", True, WHITE),
                               (self.blit_message_x, self.blit_message_y))
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.draw_game_over_screen_helper(state)
        pygame.display.flip()

    def update_player_win_point_roll_helper(self, state):
        if state.controller.confirm_button:
            self.round_reset(state)
            self.money -= self.bet
            state.player.money += self.bet
            self.game_state = self.WELCOME_SCREEN

    def update_player_lose_point_roll(self, state):
        if state.controller.confirm_button:
            self.round_reset(state)
            self.money += self.bet
            state.player.money -= self.bet
            self.game_state = self.WELCOME_SCREEN

    def update_blow_point_roll_helper(self, state):
        meter_finished = 7
        self.bet = self.bet_minimum
        blow_counter_max = 21
        blow_counter_min_needed = 20
        self.update_handle_dice_rolling_simulation(state.controller)
        if not hasattr(self, 'blow_timer_start'):
            self.blow_timer_start = pygame.time.get_ticks()
        time_elapsed = (pygame.time.get_ticks() - self.blow_timer_start) / 1000
        if time_elapsed >= meter_finished:
            self.dice_roll_1 = 3
            self.dice_roll_2 = 4
            self.point_roll_total = 7
            self.game_state = self.PLAYER_LOSE_POINT_ROLL_SCREEN
            self.blow_timer_start = pygame.time.get_ticks()
        if self.blow_counter >= blow_counter_max:
            self.blow_counter = blow_counter_max
        if (
                state.controller.isTPressed or state.controller.isAPressedSwitch) == False and self.blow_counter >= blow_counter_min_needed:
            self.blow_timer_start = pygame.time.get_ticks()
            self.point_roll_total = self.come_out_roll_total
            self.game_state = self.PLAYER_WIN_POINT_ROLL_SCREEN
        self.battle_messages[self.BLOW_POINT_ROLL_MESSAGE].update(state)

    def update_player_lose_come_out_roll(self, state):
        self.battle_messages[self.PLAYER_LOSE_COME_OUT_ROLL_MESSAGE].messages[0] \
            = f"You rolled a {self.come_out_roll_total}"
        self.battle_messages[self.PLAYER_LOSE_COME_OUT_ROLL_MESSAGE].update(state)
        if state.controller.confirm_button:
            self.round_reset(state)
            state.player.money -= self.bet
            self.money += self.bet
            self.game_state = self.WELCOME_SCREEN

    def update_naba_casting_spell_helper(self, state):
        if state.controller.confirm_button:
            self.wimpleton_magic_points -= 1
            self.debuff_weighted_dice = 5
            self.game_state = self.WELCOME_SCREEN

    def update_come_out_roll_helper(self, state: 'GameState'):
        if state.controller.confirm_button:
            self.round_reset(state)
            if self.greed_bank == False:
                state.player.money += self.bet
                self.money -= self.bet
            if self.greed_bank == True:
                state.player.money += int(self.bet * 1.5)
                self.money -= int(self.bet * 1.5)


            else:
                self.game_state = self.WELCOME_SCREEN

    def update_handle_dice_rolling_simulation(self, controller):
        if controller.confirm_button:
            if (controller.isLeftPressed or controller.isLeftPressedSwitch) and not self.is_left_pressed:
                self.is_left_pressed = True
                self.left_press_time = pygame.time.get_ticks()
                controller.isLeftPressed = False
                controller.isLeftPressedSwitch = False

            elif controller.confirm_button and self.is_left_pressed:
                time_since_left = (pygame.time.get_ticks() - self.left_press_time) / 1000

                if time_since_left <= 0.5:
                    self.is_left_pressed = False
                    controller.isRightPressed = False
                    controller.isRightPressedSwitch = False
                    self.blow_counter += 2
                else:
                    self.is_left_pressed = False

        if not controller.confirm_button:
            self.is_left_pressed = False

        current_time = pygame.time.get_ticks()
        if current_time - self.last_blow_decrement_time >= 2000:
            if self.blow_counter > 0:
                self.blow_counter -= 1
            self.last_blow_decrement_time = current_time

    def update_magic_menu_helper(self, state):

        triple_dice_spell = 0
        back_to_welcome_screen = 1
        if self.magic_screen_index == triple_dice_spell:
            self.battle_messages[self.MAGIC_MENU_TRIPLE_DICE_DESCRIPTION].update(state)
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()
        elif self.magic_screen_index == back_to_welcome_screen:
            self.battle_messages[self.MAGIC_MENU_TRIPLE_DICE_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)
        controller = state.controller

        if controller.up_button:
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index - self.index_stepper) % len(self.magic_screen_choices)
        elif controller.down_button:
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index + self.index_stepper) % len(self.magic_screen_choices)

        if controller.confirm_button:
            selected_choice = self.magic_screen_choices[self.magic_screen_index]

            if selected_choice == Magic.CRAPS_LUCKY_7.value and state.player.focus_points >= self.triple_dice_cast_cost:
                self.lucky_seven_buff_counter = self.triple_dice_counter_start_set
                self.spell_sound.play()
                state.player.focus_points -= self.triple_dice_cast_cost
                self.magic_lock = True
                self.game_state = self.WELCOME_SCREEN

            elif selected_choice == Magic.GREED_METER.value and state.player.focus_points >= 25:
                self.spell_sound.play()
                self.greed_meter = 3
                state.player.focus_points -= 25
                self.magic_lock = True
                self.game_state = self.WELCOME_SCREEN

            elif selected_choice == "Back":
                self.game_state = self.WELCOME_SCREEN

    def update_bet_screen_helper(self, state):
        come_out_point_roll_bet_min = 25
        come_out_roll_bet_max = 75
        point_roll_bet_max = 200
        controller = state.controller
        player_at_come_out_roll_phase = 0
        player_at_point_phase = 0
        is_player_in_come_out_roll = 0

        if self.come_out_roll_total == player_at_come_out_roll_phase:
            if controller.isUpPressed or controller.isUpPressedSwitch:
                controller.isUpPressed = False
                controller.isUpPressedSwitch = False
                self.menu_movement_sound.play()  # Play the sound effect once
                self.bet += come_out_point_roll_bet_min

                if self.point_roll_total == is_player_in_come_out_roll:
                    if self.bet >= come_out_roll_bet_max:
                        self.bet = come_out_roll_bet_max
            if controller.isDownPressed or controller.isDownPressedSwitch:
                controller.isDownPressed = False
                controller.isDownPressedSwitch = False
                self.bet -= come_out_point_roll_bet_min

                self.menu_movement_sound.play()  # Play the sound effect once
                if self.bet <= come_out_point_roll_bet_min:
                    self.bet = come_out_point_roll_bet_min

            if controller.isBPressed or controller.isBPressedSwitch:
                controller.isBPressed = False
                controller.isBPressedSwitch = False
                self.game_state = self.WELCOME_SCREEN

        elif self.come_out_roll_total > player_at_point_phase:

            if controller.isUpPressed or controller.isUpPressedSwitch:
                controller.isUpPressed = False
                controller.isUpPressedSwitch = False
                self.menu_movement_sound.play()  # Play the sound effect once
                self.bet += come_out_point_roll_bet_min

                if self.point_roll_total == player_at_point_phase:
                    if self.bet >= point_roll_bet_max:
                        self.bet = point_roll_bet_max
            if controller.isDownPressed or controller.isDownPressedSwitch:
                controller.isDownPressed = False
                controller.isDownPressedSwitch = False
                self.bet -= come_out_point_roll_bet_min

                self.menu_movement_sound.play()  # Play the sound effect once
                if self.bet <= come_out_point_roll_bet_min:
                    self.bet = come_out_point_roll_bet_min

            if controller.isBPressed or controller.isBPressedSwitch:
                controller.isBPressed = False
                controller.isBPressedSwitch = False
                self.game_state = self.POINT_ROLL_SCREEN

    def game_over_screen_level_4(self, state: 'GameState', controller):
        no_money_game_over = 0
        no_stamina_game_over = 0
        if state.player.money <= no_money_game_over:
            if controller.confirm_button:
                state.currentScreen = state.gameOverScreen
                state.gameOverScreen.start(state)
        elif state.player.stamina_points <= no_stamina_game_over:
            if controller.confirm_button:
                self.reset_craps_game(state)
                state.player.money -= 100
                state.currentScreen = state.area4RestScreen
                state.area4RestScreen.start(state)

    def update_power_meter_screen_helper(self, state):
        controller = state.controller
        controller.update()
        nugget_amulet_buff = 10

        you_lose_unlucky_roll = 60
        self.battle_messages[self.POWER_METER_MESSAGE].update(state)
        erika_nugget_amulet_protection = 4
        power_meter_max = 100
        power_meter_min = 0
        if self.greed_meter == 0:
            power_meter_success = 80
        elif self.greed_meter > 0:
            power_meter_success = self.piggy_meter_goal


        player_lucky_7_come_out_roll_reward = 7


        self.power_meter_index += self.power_meter_speed
        if self.power_meter_index >= power_meter_max:
            self.power_meter_index = power_meter_min

        if controller.action_and_cancel_button:
            self.power_meter_speed = power_meter_min
            self.power_meter_index = self.power_meter_index
            print("Your roll is: " + str(self.power_meter_index))

            if self.greed_meter > 0:
                if self.power_meter_index >= self.piggy_meter_goal:
                    self.greed_bank = True

            if self.power_meter_index >= power_meter_success:
                self.successful_power_strike_sound_effect.play()
                self.lucky_seven = True
            elif self.power_meter_index < power_meter_success:
                self.failed_power_strike_sound_effect.play()
                self.lucky_seven = False
            if self.lucky_seven == False:
                unlucky_two_roll = random.randint(1, 100)
                if Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value in state.player.equipped_items:
                    unlucky_two_roll -= nugget_amulet_buff
                if unlucky_two_roll >= you_lose_unlucky_roll:
                    self.dice_roll_1 = 1
                    self.dice_roll_2 = 1
                    self.come_out_roll_total = 2
                    self.game_state = self.PLAYER_LOSE_COME_OUT_SCREEN
                elif unlucky_two_roll < you_lose_unlucky_roll:
                    self.dice_roll_1 = random.randint(1, 6)
                    if self.debuff_weighted_dice == 0:
                        self.dice_roll_2 = random.randint(1, 6)
                    elif self.debuff_weighted_dice > 0:
                        self.dice_roll_2 = self.dice_roll_1
                    self.come_out_roll_total = self.dice_roll_1 + self.dice_roll_2
                    if self.come_out_roll_total == 2 or self.come_out_roll_total == 12:
                        self.game_state = self.PLAYER_LOSE_COME_OUT_SCREEN
                        return
                    elif self.come_out_roll_total == 7:
                        self.game_state = self.PLAYER_WIN_COME_OUT_SCREEN
                        return
                    elif self.come_out_roll_total == 11:
                        self.game_state = self.PLAYER_WIN_COME_OUT_SCREEN
                        return
                    if Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value in state.player.equipped_items and self.come_out_roll_total == 3:
                        player_advantage = 4
                        self.dice_roll_1 = player_advantage
                        self.dice_roll_2 = player_advantage
                        self.come_out_roll_total = player_advantage + player_advantage
                        self.game_state = self.POINT_ROLL_SCREEN
                        return
                    elif Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value not in state.player.equipped_items and self.come_out_roll_total == 3:
                        self.game_state = self.PLAYER_LOSE_COME_OUT_SCREEN
                        return
                    else:
                        self.game_state = self.POINT_ROLL_SCREEN

            if self.lucky_seven == True:
                lucky_player_bonus = state.player.luck
                luck_roll_success = 85
                luck_multiplier = 2
                lucky_7_roll = random.randint(1, 100) + (lucky_player_bonus * luck_multiplier)
                if lucky_7_roll >= luck_roll_success:
                    self.dice_roll_1 = 1
                    self.dice_roll_2 = 6
                    self.come_out_roll_total = player_lucky_7_come_out_roll_reward
                    self.game_state = self.PLAYER_WIN_COME_OUT_SCREEN
                elif lucky_7_roll < luck_roll_success:
                    self.dice_roll_1 = random.randint(1, 6)
                    if self.debuff_weighted_dice == 0:
                        self.dice_roll_2 = random.randint(1, 6)
                    elif self.debuff_weighted_dice > 0:
                        self.dice_roll_2 = self.dice_roll_1


                    self.come_out_roll_total = self.dice_roll_1 + self.dice_roll_2

                    if self.come_out_roll_total == 2:
                        self.game_state = self.PLAYER_LOSE_COME_OUT_SCREEN
                    elif self.come_out_roll_total == 3:
                        if Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value not in state.player.equipped_items:
                            self.game_state = self.PLAYER_LOSE_COME_OUT_SCREEN
                        else:
                            self.successful_power_strike_sound_effect.play()
                            self.dice_roll_1 = erika_nugget_amulet_protection
                            self.dice_roll_2 = erika_nugget_amulet_protection
                            self.come_out_roll_total = self.dice_roll_1 + self.dice_roll_2
                            self.game_state = self.POINT_ROLL_SCREEN
                    elif self.come_out_roll_total == 12:
                        self.game_state = self.PLAYER_LOSE_COME_OUT_SCREEN
                    elif self.come_out_roll_total == 7:
                        self.unlucky_seven_flag = True
                        self.game_state = self.PLAYER_WIN_COME_OUT_SCREEN
                    else:
                        print("come out roll is : " + str(self.come_out_roll_total))
                        self.game_state = self.POINT_ROLL_SCREEN

    def update_welcome_screen_helper(self, state: "GameState") -> None:
        controller = state.controller
        controller.update()
        self.battle_messages[self.WELCOME_MESSAGE].update(state)
        if state.controller.confirm_button:
            if self.welcome_screen_index == self.welcome_screen_play_index:
                self.game_state = self.POWER_METER_SCREEN
                state.player.stamina_points -= self.player_stamina_med_cost
            elif self.welcome_screen_index == self.welcome_screen_magic_index and self.magic_lock == False \
                    and Magic.CRAPS_LUCKY_7.value in state.player.magicinventory:
                self.magic_screen_index = self.magic_screen_menu_lucky_seven_index
                self.battle_messages[self.MAGIC_MENU_TRIPLE_DICE_DESCRIPTION].reset()
                self.game_state = self.MAGIC_MENU_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_bet_index:
                self.game_state = self.BET_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_quit_index and self.lock_down == self.lock_down_inactive:
                self.reset_craps_game(state)
                state.currentScreen = state.area4RestScreen
                state.area4RestScreen.start(state)

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
        blow_ability_active = 5

        for idx, choice in enumerate(self.point_roll_choices):
            y_position = start_y_right_box + idx * spacing_between_choices  # Adjust spacing between choices

            if idx == 1:
                if self.blow_counter < 5:
                    text_surface = self.font.render(choice, True, RED)
                elif self.blow_turn >= blow_ability_active and Equipment.CRAPS_WRIST_WATCH.value in state.player.equipped_items and not self.blow_sound_checker:
                    text_surface = self.font.render(choice, True, GREEN)
                else:
                    text_surface = self.font.render(choice, True, WHITE)
            else:
                text_surface = self.font.render(choice, True, WHITE)

            state.DISPLAY.blit(text_surface, (start_x_right_box + text_x_offset, y_position + text_y_offset))

        if Equipment.CRAPS_WRIST_WATCH.value not in state.player.equipped_items:
            self.point_roll_choices[1] = "Locked"

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

    def draw_game_over_screen_helper(self, state: 'Gamestate'):
        no_money_game_over = 0
        no_stamina_game_over = 0
        if state.player.money <= no_money_game_over:
            state.DISPLAY.blit(self.font.render(f"You ran out of money and are now a prisoner of hell", True, WHITE),
                               (self.blit_message_x, self.blit_message_y))
        elif state.player.stamina_points <= no_stamina_game_over:
            state.DISPLAY.blit(self.font.render(f"You ran out of stamina , you lose -100 gold", True, WHITE),
                               (self.blit_message_x, self.blit_message_y))

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

        state.DISPLAY.blit(self.font.render(self.dealer_name, True, WHITE),
                           (player_enemy_box_info_x_position, enemy_name_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}", True, WHITE),
                           (player_enemy_box_info_x_position, enemy_money_y_position))
        if self.lucky_seven_buff_counter == self.lucky_seven_buff_not_active:
            state.DISPLAY.blit(self.font.render(f"{self.STATUS_GREEN}", True, WHITE),
                               (player_enemy_box_info_x_position, enemy_status_y_position))
        elif self.lucky_seven_buff_counter > self.lucky_seven_buff_not_active:
            state.DISPLAY.blit(self.font.render(f"{self.TRIPLE_DICE}: {self.lucky_seven_buff_counter} ", True, WHITE),
                               (player_enemy_box_info_x_position, enemy_status_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE),
                           (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE),
                           (player_enemy_box_info_x_position, player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE),
                           (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE),
                           (player_enemy_box_info_x_position, hero_focus_y_position))

        if self.lock_down <= self.lock_down_inactive:
            state.DISPLAY.blit(self.font.render(f"{self.HERO_HEADER}", True, WHITE),
                               (player_enemy_box_info_x_position, hero_name_y_position))
        elif self.lock_down > self.lock_down_inactive:
            state.DISPLAY.blit(self.font.render(f"{self.LOCKED_DOWN_HEADER}:{self.lock_down}", True, RED),
                               (player_enemy_box_info_x_position, hero_name_y_position))

    def draw_create_meter(self, state: "GameState", power: int) -> None:
        meter_width = 300  # Three times wider
        meter_height = 30
        max_power = 100
        white_border_width = 2
        meter_x_position = 250
        meter_y_position = 50
        line_y_start = 50
        line_y_end = 80
        line_thickness = 1
        filled_width = int((power / max_power) * meter_width)

        meter_bg_rect = pygame.Rect(meter_x_position, meter_y_position, meter_width, meter_height)
        pygame.draw.rect(state.DISPLAY, RED, meter_bg_rect)

        meter_fill_rect = pygame.Rect(meter_x_position, meter_y_position, filled_width, meter_height)
        pygame.draw.rect(state.DISPLAY, GREEN, meter_fill_rect)

        pygame.draw.rect(state.DISPLAY, WHITE, meter_bg_rect, white_border_width)
        if self.greed_meter == 0:
            goal_position = int((self.power_meter_goal / max_power) * meter_width) + meter_x_position
        elif self.greed_meter > 0:
            goal_position = int((self.piggy_meter_goal / max_power) * meter_width) + meter_x_position

        pygame.draw.line(state.DISPLAY, WHITE, (goal_position, line_y_start), (goal_position, line_y_end),
                         line_thickness)

    def rolling_dice_timer(self) -> bool:
        current_time = pygame.time.get_ticks()

        if current_time - self.start_time >= 1000 and self.roll_dice == True:
            self.dice_roll.play()
            self.roll_dice = False

        if current_time - self.start_time >= 2000:
            self.is_timer_active = False
            self.roll_dice = True
            return True
        remaining_time = 2000 - (current_time - self.start_time)
        return False  # Timer is still running

    def draw_display_dice(self, state: "GameState", dice_roll_1: int, dice_roll_2: int) -> None:
        dice_x_start_position = 300
        dice_y_position = 0
        dice_x_gap = 120
        dice_faces = [
            pygame.Rect(50, 0, 133, 200),  # Dice face 1=
            pygame.Rect(210, 0, 133, 200),  # Dice face 2
            pygame.Rect(370, 0, 133, 200),  # Dice face 3
            pygame.Rect(545, 0, 133, 200),  # Dice face 4
            pygame.Rect(710, 0, 133, 200),  # Dice face
            pygame.Rect(880, 0, 133, 200)  # Dice face 6p
        ]

        dice_rect1 = dice_faces[dice_roll_1 - 1]
        cropped_dice1 = self.sprite_sheet.subsurface(dice_rect1)  # Crop the first dice image

        dice_rect2 = dice_faces[dice_roll_2 - 1]
        cropped_dice2 = self.sprite_sheet.subsurface(dice_rect2)  # Crop the second dice image

        state.DISPLAY.blit(cropped_dice1, (dice_x_start_position, dice_y_position))  # First dice position
        state.DISPLAY.blit(cropped_dice2, (dice_x_start_position + dice_x_gap, dice_y_position))  # Second dice with gap

    def update_point_screen_helper(self, state):
        controller = state.controller
        controller.update()
        if (controller.isUpPressed or controller.isUpPressedSwitch) and self.is_timer_active == False:
            self.menu_movement_sound.play()  # Play the sound effect once

            self.point_roll_index = (self.point_roll_index - self.index_stepper) % len(self.point_roll_choices)
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
        elif (controller.isDownPressed or controller.isDownPressedSwitch) and self.is_timer_active == False:
            self.menu_movement_sound.play()  # Play the sound effect once
            self.point_roll_index = (self.point_roll_index + self.index_stepper) % len(self.point_roll_choices)
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False

        if (
                controller.isTPressed or controller.isAPressedSwitch) and not self.is_timer_active and self.point_roll_index == 0:
            self.start_time = pygame.time.get_ticks()  # Set start time
            self.is_timer_active = True
            self.blow_turn += 1
            controller.isTPressed = False
            controller.isAPressedSwitch = False

        elif controller.confirm_button and not self.is_timer_active and self.point_roll_index == 1 and self.blow_turn >= 0:
            state.player.stamina_points -= self.player_stamina_high_cost
            self.game_state = self.BLOW_POINT_ROLL_SCREEN


        elif controller.confirm_button and not self.is_timer_active and self.point_roll_index == 2:
            self.game_state = self.BET_SCREEN

        if self.is_timer_active:
            if self.rolling_dice_timer():
                self.dice_roll_1 = random.randint(1, 6)
                self.dice_roll_2 = random.randint(1, 6)

                state.player.stamina_points -= self.player_stamina_low_cost

                self.point_roll_total = self.dice_roll_1 + self.dice_roll_2
                self.is_timer_active = False
                self.start_time = 0

                if self.lucky_seven_buff_counter > 0 and self.point_roll_total != self.come_out_roll_total and self.point_roll_total != 7:
                    self.dice_roll_3 = random.randint(1, 6)
                    original_dice = self.dice_roll_2
                    self.dice_roll_2 = self.dice_roll_3
                    self.point_roll_total = self.dice_roll_1 + self.dice_roll_2
                    if self.point_roll_total == 7:
                        self.dice_roll_2 = original_dice
                        self.point_roll_total = self.dice_roll_1 + self.dice_roll_2

                if self.point_roll_total == 7:
                    self.game_state = self.PLAYER_LOSE_POINT_ROLL_SCREEN
                    return
                elif self.point_roll_total == self.come_out_roll_total:
                    self.game_state = self.PLAYER_WIN_POINT_ROLL_SCREEN
                    return
                else:
                    if self.blow_turn == 0 and self.blow_sound_checker == True:
                        self.blow_sound_checker = False
                        self.blow_meter_ready.play()

    def draw_create_blow_meter(self, state: "GameState", blow_counter: int) -> None:
        meter_width = 300  # Total width of the meter
        meter_height = 30
        max_blow_counter = 20  # 100% equals 20 points (5% per point, so 20 points total for full meter)
        white_border_width = 2
        meter_x_position = 250
        meter_y_position = 50
        line_y_start = 50
        line_y_end = 80
        line_thickness = 5
        filled_width = int((blow_counter / max_blow_counter) * meter_width)
        meter_bg_rect = pygame.Rect(meter_x_position, meter_y_position, meter_width,
                                    meter_height)  # Position: (250, 50)
        pygame.draw.rect(state.DISPLAY, RED, meter_bg_rect)  # Red background
        meter_fill_rect = pygame.Rect(meter_x_position, meter_y_position, filled_width, meter_height)
        pygame.draw.rect(state.DISPLAY, GREEN, meter_fill_rect)  # Green filled portion
        pygame.draw.rect(state.DISPLAY, WHITE, meter_bg_rect, white_border_width)  # White border
        goal_position = int((self.power_meter_goal / max_blow_counter) * meter_width) + meter_x_position
        pygame.draw.line(state.DISPLAY, WHITE, (goal_position, line_y_start), (goal_position, line_y_end),
                         line_thickness)

    def draw_magic_menu_selection_box(self, state):
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

        for idx, choice in enumerate(self.magic_screen_choices):
            y_position = start_y_right_box + idx * choice_spacing  # Use the defined spacing variable
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        arrow_y_offset = self.magic_screen_index * choice_spacing + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, start_y_right_box + arrow_y_offset)
        )

