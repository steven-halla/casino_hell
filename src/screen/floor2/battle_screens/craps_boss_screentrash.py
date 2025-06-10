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

class CrapsBossScreen(GambleScreen):
    def __init__(self, screenName: str = "Craps") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.sprite_sheet: pygame.Surface = pygame.image.load("./assets/images/dice45.png")
        self.come_out_roll_total: int = 0
        self.dealer_name: str = "Happy"
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
        self.magic_screen_choices: list[str] = []
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
        self.debuff_weighted_dice: int = 0
        self.debuff_counter: int = 3
        self.greed_meter: int = 0
        self.greed_bank: bool = False
        self.hungry_dice_increased_chance:int = 0
        self.level_up_message_initialized = False


        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "Happy: This is the welcome screen"
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
            self.HAPPY_CASTING_SPELL_MESSAGE: MessageBox([
                f"Starving animals of eternal hunger, casts your misery upon the unworthy...weighted dice(all dice totals -1)"
            ]),
            self.LEVEL_UP_MESSAGE: MessageBox([
                f"You leveld up!"
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
    HAPPY_CASTING_SPELL_MESSAGE: str = "HAPPY_CASTING_SPELL_MESSAGE"
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
    HAPPY_CASTING_SPELL_SCREEN: str = "junpon_cating_spell_screen"
    BACK = "back"




    def create_meter(self, state: "GameState", power: int) -> None:
        meter_width = 300  # Three times wider
        meter_height = 30
        max_power = 100

        # Calculate the width of the filled portion of the meter
        filled_width = int((power / max_power) * meter_width)

        # Draw the background of the meter (empty portion)
        meter_bg_rect = pygame.Rect(250, 50, meter_width, meter_height)  # Position: (250, 50)
        pygame.draw.rect(state.DISPLAY, (255, 0, 0), meter_bg_rect)  # Red background

        # Draw the filled portion of the meter
        meter_fill_rect = pygame.Rect(250, 50, filled_width, meter_height)  # Position: (250, 50)
        pygame.draw.rect(state.DISPLAY, (0, 255, 0), meter_fill_rect)  # Green filled portion

        # Draw the border of the meter
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), meter_bg_rect, 2)  # White border

        # Draw the goal indicator line



        goal_position = int((self.power_meter_goal / max_power) * meter_width) + 250  # Adjust position to start from 250

        if self.poison_meter_speed > 0 and self.player_poison_penalty == True:
            self.power_meter_goal += 10
            goal_position += 10
            self.power_meter_speed += .5
            self.player_poison_penalty = False
        pygame.draw.line(state.DISPLAY, (255, 255, 255), (goal_position, 50), (goal_position, 80), 5)  # Thick white line
        # print(f"Power Meter Goal: {self.power_meter_goal}, Goal Position: {goal_position}, Power Meter Speed: {self.power_meter_speed}, Player Poison Penalty: {self.player_poison_penalty}")



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

    def stop_music(self):
        pygame.mixer.music.stop()
    def initialize_music(self):
        # Initialize the mixer
        pygame.mixer.init()

        # Load the music file
        pygame.mixer.music.load(self.music_file)

        # Set the volume for the music (0.0 to 1.0)
        pygame.mixer.music.set_volume(self.music_volume)

        # Play the music, -1 means the music will loop indefinitely
        pygame.mixer.music.play(-1)

    def update(self, state: "GameState") -> None:
        if self.bet > self.money:
            self.bet = self.money

        if state.musicOn == True:
            if self.music_on == True:
                self.stop_music()
                self.initialize_music()
                self.music_on = False

        # print(self.gam)
        if self.lucky_seven_buff_counter > 0:
            self.magic_lock = True
        elif self.lucky_seven_buff_counter == 0:
            self.magic_lock = False

        if self.money <= 0:
            self.lucky_seven_buff_counter = 0




        # self.lucky_seven = state.player.luck * 2
        # pygame.mixer.music.stop()
        if state.controller.isQPressed:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

        controller = state.controller
        controller.update()

        if self.intro == True:
            self.game_state = "intro_screen"

        if self.game_state == "intro_screen":
            self.battle_messages["hand_cramp_message"].update(state)
            if self.battle_messages["hand_cramp_message"].message_index == 1 and self.spell_effect == True:
                self.spell_sound.play()  # Play the sound effect once
                print("dm;lsfjlsadf;jdsa;f;ldsjfsafj;sad")
                self.spell_effect = False


            if self.battle_messages["hand_cramp_message"].message_index == len(self.battle_messages["hand_cramp_message"].messages) - 1:
                print("yaw")
                self.game_state = "welcome_screen"
                self.intro = False

        if self.game_state == "welcome_screen":






            if state.player.leveling_up == True:
                self.game_state = "level_up_screen"

            self.battle_messages["welcome_message"].update(state)

            if self.money < 1:
               self.lucky_seven_buff_counter = 0
               self.game_state = "game_over_screen"

            if state.player.stamina_points < 1:
                self.lucky_seven_buff_counter = 0

                self.game_state = "game_over_screen"






            elif self.player_money < 25 and self.player_money > 0:
                self.game_state = "game_over_screen"


            elif self.player_money <= 0:
                self.game_state = "game_over_screen"

            if controller.isUpPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.welcome_screen_index = (self.welcome_screen_index - 1) % len(self.welcome_screen_choices)
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.welcome_screen_index = (self.welcome_screen_index + 1) % len(self.welcome_screen_choices)
                controller.isDownPressed = False
                self.menu_movement_sound.play()  # Play the sound effect once

            if self.welcome_screen_index == 0 and controller.isTPressed:
                self.game_state = "power_meter_screen"
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)  # Call the method to display the dice roll

                state.player.stamina_points -= self.stamina_drain

                controller.isTPressed = False
            elif self.welcome_screen_index == 1 and controller.isTPressed and self.magic_lock == False:
                self.magic_screen_index = 0
                self.battle_messages["magic_message"].reset()
                self.game_state = "magic_screen"
                controller.isTPressed = False

            elif self.welcome_screen_index == 2 and controller.isTPressed:
                self.battle_messages["bet_message"].reset()
                self.game_state = "bet_screen"

                controller.isTPressed = False

            elif self.welcome_screen_index == 3 and controller.isTPressed and self.lock_down == 0:
                print("no way you running away ")

        elif self.game_state == "level_up_screen":
            self.handle_level_up(state, state.controller)

        elif self.game_state == "bet_screen":
            # print(self.game_state)
            if controller.isUpPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.bet += 25
                # print(self.game_state)

                if self.bet >= 50:
                    self.bet = 50
                controller.isUpPressed = False

            if controller.isDownPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.bet -= 25
                if self.bet <= 25:
                    self.bet = 25
                controller.isDownPressed = False

            if controller.isTPressed:
                self.game_state = "welcome_screen"
                controller.isTPressed = False




        elif self.game_state == "magic_screen":
            if self.magic_screen_index == 0:
                self.battle_messages["magic_message"].messages = [f"Rerolls 2nd dice under favorable circumstances during point phase. 10 turns."]
            elif self.magic_screen_index == 1:
                self.battle_messages["magic_message"].messages = [f"Go back to main menu."]
            self.battle_messages["magic_message"].update(state)
            if controller.isUpPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.magic_screen_index = (self.magic_screen_index - 1) % len(self.magic_screen_choices)
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.magic_screen_index = (self.magic_screen_index + 1) % len(self.magic_screen_choices)
                controller.isDownPressed = False
            if self.magic_screen_index == 0 and controller.isTPressed and state.player.focus_points >= self.double_dice_cast_cost:
                self.lucky_seven_buff_counter = 10
                state.player.focus_points -= self.double_dice_cast_cost
                self.magic_lock = True
                controller.isTPressed = False
                self.spell_sound.play()  # Play the sound effect once

                self.game_state = "welcome_screen"

            elif self.magic_screen_index == 1 and controller.isTPressed:
                self.battle_messages["magic_message"].update(state)
                self.magic_lock = True
                self.game_state = "welcome_screen"
                controller.isTPressed = False

        if self.game_state == "power_meter_screen":

            self.power_meter_index += self.power_meter_speed
            if self.power_meter_index >= 100:
                self.power_meter_index = 0

            if controller.isPPressed:
                self.power_meter_speed = 0
                self.power_meter_index = self.power_meter_index
                controller.isPPressed = False
                if self.power_meter_index >= 85:
                    self.successful_power_strike_sound_effect.play()  # Play the sound effect once

                    self.lucky_seven = True
                elif self.power_meter_index < 85:
                    self.failed_power_strike_sound_effect.play()  # Play the sound effect once

                print("Your meter is:" + str(self.power_meter_index))
                print("-----------------------------------------------------------------------------")
                self.game_state = "come_out_roll_screen"
            self.battle_messages["power_meter_message"].update(state)



        if self.game_state == "come_out_roll_screen":
            # print("Your message index is: " + str(self.battle_messages["come_out_roll_message"].message_index))

            # self.battle_messages["you_win_come_out_roll_message"].reset()


            self.battle_messages["come_out_roll_message"].update(state)
            # if self.come_out_roll_index == 0 and self.lucky_message_switch == False:
            #     self.battle_messages["come_out_roll_message"].messages = [f"Roll the dice"]
            # elif self.come_out_roll_index == 1:
            #     self.battle_messages["come_out_roll_message"].messages = [f"Go back to main menu."]

            if self.come_out_roll_message_flag == True:
                self.battle_messages["come_out_roll_message"].messages = [
                    f"Hti Roll to roll the bones...",


                ]


            if self.come_out_roll_index == 0 and controller.isTPressed:
                self.come_out_roll_message_flag = False
                controller.isTPressed = False

                self.battle_messages["come_out_roll_message"].update(state)
                if self.lucky_seven == True:

                    lucky_player_bonus = state.player.luck
                    lucky_7_roll = random.randint(1, 100) + (lucky_player_bonus * 2)
                    print(f"Your lucky roll is: " + str(lucky_7_roll))
                    if lucky_7_roll >= 85:
                        self.unlucky_seven_flag = True

                        print("505 come out roll total 7")
                        self.game_state = "you_win_come_out_roll_screen"

                    elif lucky_7_roll < 85:
                        self.battle_messages["come_out_roll_message_unlucky_7"].update(state)

                        print("482 lucky roll below 80")

                        self.dice_roll_1 = random.randint(1, 6)
                        self.dice_roll_2 = random.randint(1, 6)
                        print("485")
                        self.come_out_roll_total = self.dice_roll_1 + self.dice_roll_2

                        if self.come_out_roll_total == 2:
                            self.dice_roll_1 = 1
                            self.dice_roll_1 = 1
                            self.game_state = "you_lose_come_out_roll_screen"


                        elif self.come_out_roll_total == 3:

                            if Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value not in state.player.equipped_items:
                                self.dice_roll_1 = 1
                                self.dice_roll_1 = 2
                                self.game_state = "you_lose_come_out_roll_screen"
                            else:
                                print("you guarded against a loss******************************************---------------------------------------------------------------")

                                self.dice_roll_1 = 3
                                self.dice_roll_2 = 5
                                self.come_out_roll_total = 8
                                self.game_state = "point_phase_screen"

                        elif self.come_out_roll_total == 12:
                            self.dice_roll_1 = 6
                            self.dice_roll_1 = 6
                            self.game_state = "you_lose_come_out_roll_screen"


                        elif self.come_out_roll_total == 7:
                            self.unlucky_seven_flag = True

                            print("505 come out roll total 7")
                            self.game_state = "you_win_come_out_roll_screen"

                        else:
                            print("line 527")

                            self.game_state = "point_phase_screen"




                elif self.lucky_seven == False:
                    unlucky_two_roll = random.randint(1, 100)
                    print("unlucky two roll is: " + str(unlucky_two_roll))
                    if Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value in state.player.equipped_items:
                        unlucky_two_roll -= 10
                    print("unlucky two roll is: " + str(unlucky_two_roll))

                    if unlucky_two_roll >= 60:
                        self.dice_roll_1 = 1
                        self.dice_roll_2 = 1
                        self.come_out_roll_total = 2

                        print("line 562")
                        self.game_state = "you_lose_come_out_roll_screen"

                    elif unlucky_two_roll < 60:
                        self.dice_roll_1 = random.randint(1, 6)
                        self.dice_roll_2 = random.randint(1, 6)
                        print("line 568")
                        self.come_out_roll_total = self.dice_roll_1 + self.dice_roll_2
                        print("come out roll total: " + str(self.come_out_roll_total))
                        if self.come_out_roll_total == 2:
                            self.dice_roll_1 = 1
                            self.dice_roll_2 = 1
                            self.game_state = "you_lose_come_out_roll_screen"

                        elif self.come_out_roll_total == 3:

                            if Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value not in state.player.equipped_items:
                                self.dice_roll_1 = 1
                                self.dice_roll_1 = 2
                                self.game_state = "you_lose_come_out_roll_screen"
                            else:
                                print("you guarded against a loss***********************************************----------------------------------------------------")

                                self.dice_roll_1 = 3
                                self.dice_roll_2 = 3
                                self.come_out_roll_total = 6

                                self.game_state = "point_phase_screen"

                        elif self.come_out_roll_total == 12:
                            self.dice_roll_1 = 6
                            self.dice_roll_2 = 6
                            self.game_state = "you_lose_come_out_roll_screen"


                        elif self.come_out_roll_total == 7:



                            self.lucky_message_switch = True
                            self.dice_roll_1 = 1
                            self.dice_roll_2 = 6
                            self.display_dice(state, self.dice_roll_1, self.dice_roll_2)
                            print("Dice roll 1: ", self.dice_roll_1)
                            print("Dice roll 2: ", self.dice_roll_2)
                            self.game_state = "you_win_come_out_roll_screen"







                            # Check if the current message is finished and if the current message index is 2
                            if self.battle_messages["come_out_roll_message_unlucky_7"].message_index == 2:
                                print("469 ---------------")
                                self.player_money += self.bet
                                state.player.exp += 50
                                self.game_state = "welcome_screen"
                                self.battle_messages["come_out_roll_message"].reset()

                                self.game_reset(state)



                        else:
                            print("625")

                            self.game_state = "point_phase_screen"



                controller.isTPressed = False
                print("Dice roll 1 -----------: ", self.dice_roll_1)
                print("Dice roll 2 -----------: ", self.dice_roll_2)
                self.battle_messages["come_out_roll_message"].update(state)

        if self.game_state == "point_phase_screen":
            if self.money < 1:
                self.game_state = "game_over_screen"

            if state.player.stamina_points < 1:
                self.game_state = "game_over_screen"


            elif state.player.stamina_points <= 2 and state.player.stamina_points > 0:
                self.game_state = "game_over_screen"

            # print("point phase target" + str(point_phase_target))

            self.battle_messages["point_phase_message"].messages = [f"Your roll target is {self.come_out_roll_total} and your current roll is {self.point_roll_total}"]

            self.battle_messages["point_phase_message"].update(state)

            if controller.isUpPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.point_roll_index = (self.point_roll_index - 1) % len(self.point_roll_choices)
                print(str(self.point_roll_index))
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.point_roll_index = (self.point_roll_index + 1) % len(self.point_roll_choices)
                controller.isDownPressed = False
            if self.point_roll_index == 0 and controller.isTPressed:
                state.player.stamina_points -= self.stamina_drain
                # self.come_out_roll total is what i need to match
                # self.point_roll_total = random.randint(1, 6)

                self.dice_roll_1 = random.randint(1, 6)
                self.dice_roll_2 = random.randint(1, 6)


                self.point_roll_total = self.dice_roll_1 + self.dice_roll_2


                if self.lucky_seven_buff_counter > 0 and self.point_roll_total != self.come_out_roll_total and self.point_roll_total != 7:
                    self.dice_roll_3 = random.randint(1, 6)
                    original_dice = self.dice_roll_2

                    self.dice_roll_2 = self.dice_roll_3
                    self.point_roll_total = self.dice_roll_1 + self.dice_roll_2

                    print("Dice roll 2")
                    print(original_dice)

                    print("Your dice roll 3 are:")
                    print(self.dice_roll_3)




                    if self.point_roll_total == 7:
                        self.dice_roll_2 = original_dice
                        self.point_roll_total = self.dice_roll_1 + self.dice_roll_2
                        print("your come out  roll total is: " + str(self.come_out_roll_total) + f"and your roll is {self.point_roll_total}")

                    # self.dice_roll_1 = random.randint(1, 6)
                    # self.dice_roll_2 = random.randint(1, 6)
                    # self.point_roll_total = self.dice_roll_1 + self.dice_roll_2


                if self.point_roll_total == 7:
                    print("you rolled 7 line 835")
                    self.game_state = "roll_seven_lose_screen"


                elif self.point_roll_total == self.come_out_roll_total:
                    self.game_state = "roll_match_win_screen"

            elif self.point_roll_index == 1 and controller.isTPressed:
                self.game_state = "point_bet_screen"
                controller.isTPressed = False
            controller.isTPressed = False


        elif self.game_state == "you_lose_come_out_roll_screen":
            if self.dice_roll_1 > 0:  # Check if a dice roll has been made
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)

            self.battle_messages["you_lose_come_out_roll_message"].messages = [
                f"roll  of {self.come_out_roll_total} you lose sorry",
                f"You gain 10 exp and lose {self.bet} coins"

            ]
            self.battle_messages["you_lose_come_out_roll_message"].update(state)
            if self.battle_messages["you_lose_come_out_roll_message"].message_index == 1:
                self.player_money -= self.bet
                self.money += self.bet
                state.player.exp += 15
                self.game_state = "welcome_screen"
                self.game_reset(state)


        elif self.game_state == "you_win_come_out_roll_screen":
            self.dice_roll_1 = 1
            self.dice_roll_2 = 6
            if self.dice_roll_1 > 0:  # Check if a dice roll has been made
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)

            self.battle_messages["you_win_come_out_roll_message"].update(state)
            # print("643 should follow")
            if self.battle_messages["you_win_come_out_roll_message"].message_index == 1:
                self.player_money += self.bet
                self.money -= self.bet
                state.player.exp += 25
                self.game_state = "welcome_screen"
                self.game_reset(state)











        elif self.game_state == "point_bet_screen":
            if controller.isUpPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.bet += 25
                if self.bet > 125:
                    self.bet = 125
                controller.isUpPressed = False

            elif controller.isDownPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.bet -= 25
                if self.bet < 25:
                    self.bet = 25
                controller.isDownPressed = False

            if self.point_bet_index == 0 and controller.isTPressed:
                self.game_state = "point_phase_screen"
                controller.isTPressed = False


        elif self.game_state == "roll_seven_lose_screen":
            self.battle_messages["you_lose_seven_message"].update(state)

            if controller.isTPressed:
                self.player_money -= self.bet
                self.money += self.bet
                self.point_roll_total = 0
                self.game_reset(state)

                self.game_state = "welcome_screen"
                controller.isTPressed = False


        elif self.game_state == "you_lose_come_out_roll_screen":
            print("Your come out roll is: " + str(self.come_out_roll_total))
            if self.dice_roll_1 > 0:  # Check if a dice roll has been made
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)


            self.battle_messages["you_lose_come_out_roll_message"].messages = [
                f"roll  of {self.come_out_roll_total} you lose sorry",
                f"You gain 10 exp and lose {self.bet} coins"

            ]
            self.battle_messages["you_lose_come_out_roll_message"].update(state)
            print("629 should follow")
            if self.battle_messages["you_lose_come_out_roll_message"].message_index == 1:
                self.player_money -= self.bet
                self.money += self.bet
                state.player.exp += 15
                self.game_state = "welcome_screen"
                self.game_reset(state)


        elif self.game_state == "you_win_come_out_roll_screen":
            self.dice_roll_1 = 1
            self.dice_roll_2 = 6
            if self.dice_roll_1 > 0:  # Check if a dice roll has been made
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)

            self.battle_messages["you_win_come_out_roll_message"].update(state)
            # print("643 should follow")
            if self.battle_messages["you_win_come_out_roll_message"].message_index == 1:
                self.player_money += self.bet
                self.money -= self.bet
                state.player.exp += 15
                self.game_state = "welcome_screen"
                self.game_reset(state)











        elif self.game_state == "point_bet_screen":
            if controller.isUpPressed:
                self.bet += 25
                if self.bet > 200:
                    self.bet = 200
                controller.isUpPressed = False

            elif controller.isDownPressed:

                self.bet -= 25
                if self.bet < 50:
                    self.bet = 50
                controller.isDownPressed = False

            if self.point_bet_index == 0 and controller.isTPressed:
                self.game_state = "point_phase_screen"
                controller.isTPressed = False


        elif self.game_state == "roll_seven_lose_screen":
            self.battle_messages["you_lose_seven_message"].update(state)

            if controller.isTPressed:
                self.player_money -= self.bet
                self.money += self.bet
                self.point_roll_total = 0
                self.game_reset(state)

                self.game_state = "welcome_screen"
                controller.isTPressed = False


        elif self.game_state == "roll_match_win_screen":
            self.battle_messages["you_win_matching_message"].update(state)

            if controller.isTPressed:
                self.player_money += self.bet
                self.money -= self.bet
                self.point_roll_total = 0
                self.game_reset(state)

                self.game_state = "welcome_screen"
                controller.isTPressed = False


        elif self.game_state == "game_over_screen":
            if self.money < 1:
                self.battle_messages["you_win"].update(state)


            if state.player.stamina_points < 1:
                self.battle_messages["game_over_no_stamina_message"].update(state)



            # elif state.player.stamina_points <= 6 and state.player.stamina_points > 0:
            #     self.battle_messages["game_over_low_stamina_message"].update(state)



            elif self.player_money < 25 and self.player_money > 0:
                self.battle_messages["game_over_low_money_message"].update(state)



            elif self.player_money <= 0:
                self.battle_messages["game_over_no_money_message"].update(state)





    def draw(self, state: "GameState") -> None:
        state.DISPLAY.fill((0, 0, 51))
        black_box = pygame.Surface((200 - 10, 180 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 235))

        black_box = pygame.Surface((200 - 10, 45 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 195))

        state.DISPLAY.blit(self.font.render(f"Money: {self.money}", True, (255, 255, 255)), (37, 250))
        state.DISPLAY.blit(self.font.render(f"HP: {state.player.stamina_points}", True, (255, 255, 255)), (37, 290))
        state.DISPLAY.blit(self.font.render(f"MP: {state.player.focus_points}", True, (255, 255, 255)), (37, 330))
        if self.lock_down < 1:
            state.DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)), (37, 205))
        elif self.lock_down > 0:
            state.DISPLAY.blit(self.font.render(f"Locked Down:{self.lock_down}", True, (255, 0, 0)), (37, 205))

        self.draw_enemy_info_box(state)


        self.draw_bottom_black_box(state)

        if self.game_state == "intro_screen":
            self.battle_messages["hand_cramp_message"].draw(state)

        if self.game_state == "welcome_screen":



            self.battle_messages["welcome_message"].draw(state)

            if self.money < 1:
                self.battle_messages["you_win"].draw(state)

            if state.player.stamina_points < 1:
                self.battle_messages["game_over_no_stamina_message"].draw(state)

            elif self.player_money <= 0:
                self.battle_messages["game_over_no_money_message"].draw(state)

            elif state.player.stamina_points <= 10 and state.player.stamina_points > 0:
                self.battle_messages["game_over_low_stamina_message"].draw(state)

            elif self.player_money < 50 and self.player_money > 0:
                self.battle_messages["game_over_low_money_message"].draw(state)

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
            for idx, choice in enumerate(self.welcome_screen_choices):
                y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, (255, 255, 255)),
                    (start_x_right_box + 60, y_position + 15)
                )
            if Magic.CRAPS_LUCKY_7.value not in state.player.magicinventory:
                self.magic_lock = True
                self.welcome_screen_choices[1] = "Locked"

            elif Magic.CRAPS_LUCKY_7.value in state.player.magicinventory:
                self.welcome_screen_choices[1] = "Magic"


            if self.magic_lock == True:
                self.welcome_screen_choices[1] = "Locked"

            self.welcome_screen_choices[3] = "Locked"



            if self.welcome_screen_index == 0:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 12)
                )
            elif self.welcome_screen_index == 1:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 52)
                )
            elif self.welcome_screen_index == 2:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 92)
                )
            elif self.welcome_screen_index == 3:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 132)
                )

        elif self.game_state == "game_over_screen":
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

            if self.money < 1:
                self.battle_messages["you_win"].draw(state)

                if self.battle_messages["you_win"].message_index == 1:
                    state.currentScreen = state.area2GamglingScreen
                    state.area2GamglingScreen.start(state)

            if state.player.stamina_points < 1:
                self.battle_messages["game_over_no_stamina_message"].draw(state)

                if self.battle_messages["game_over_no_stamina_message"].message_index == 1:
                    state.currentScreen = state.area2RestScreen
                    state.area2RestScreen.start(state)
            elif state.player.stamina_points <= 10 and state.player.stamina_points > 0:
                self.battle_messages["game_over_low_stamina_message"].draw(state)

                if self.battle_messages["game_over_low_stamina_message"].message_index == 1:
                    state.currentScreen = state.area2GamblingScreen
                    state.area2GamblingScreen.start(state)


            elif self.player_money < 50 and self.player_money > 0:
                self.battle_messages["game_over_low_money_message"].draw(state)

                if self.battle_messages["game_over_low_money_message"].message_index == 1:
                    state.currentScreen = state.area2RestScreen
                    state.area2RestScreen.start(state)

            elif self.player_money <= 0:
                self.battle_messages["game_over_no_money_message"].draw(state)

                if self.battle_messages["game_over_no_money_message"].message_index == 1:
                    state.currentScreen = state.area2RestScreen
                    state.area2RestScreen.start(state)

        elif self.game_state == "level_up_screen":
            self.draw_level_up(state)

        elif self.game_state == "bet_screen":
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
            for idx, choice in enumerate(self.bet_screen_choices):
                y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, (255, 255, 255)),
                    (start_x_right_box + 60, y_position + 15)
                )
            if self.point_bet_index == 0:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 12)
                )




        elif self.game_state == "magic_screen":
            self.battle_messages["magic_message"].draw(state)

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

        elif self.game_state == "bet_screen":

            self.battle_messages["bet_message"].draw(state)

        elif self.game_state == "power_meter_screen":
            self.create_meter(state, self.power_meter_index)
            self.battle_messages["power_meter_message"].draw(state)







        elif self.game_state == "come_out_roll_screen":
            if self.dice_roll_1 > 0:  # Check if a dice roll has been made

                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)


            if self.lucky_seven_flag == True:
                self.battle_messages["come_out_roll_message_lucky_7"].draw(state)
            elif self.unlucky_seven_flag == True:
                print("drawing line 1169")

                self.battle_messages["come_out_roll_message_unlucky_7"].draw(state)
            else:
                self.battle_messages["come_out_roll_message"].draw(state)

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
            for idx, choice in enumerate(self.come_out_roll_choices):
                y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, (255, 255, 255)),
                    (start_x_right_box + 60, y_position + 15)
                )

            if self.come_out_roll_index == 0:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 12)
                )
            elif self.come_out_roll_index == 1:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 52)
                )

        elif self.game_state == "point_bet_screen":

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
            for idx, choice in enumerate(self.bet_screen_choices):
                y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, (255, 255, 255)),
                    (start_x_right_box + 60, y_position + 15)
                )
            if self.point_bet_index == 0:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 12)
                )

        elif self.game_state == "point_phase_screen":

            if state.player.stamina_points < 1:
                self.battle_messages["game_over_no_stamina_message"].draw(state)
            if self.dice_roll_1 > 0:  # Check if a dice roll has been made
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)
            self.battle_messages["point_phase_message"].draw(state)

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
            for idx, choice in enumerate(self.point_roll_choices):
                y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
                state.DISPLAY.blit(
                    self.font.render(choice, True, (255, 255, 255)),
                    (start_x_right_box + 60, y_position + 15)
                )

            if self.point_roll_index == 0:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 12)
                )
            elif self.point_roll_index == 1:
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, start_y_right_box + 52)
                )

        elif self.game_state == "roll_seven_lose_screen":
            if self.dice_roll_1 > 0:  # Check if a dice roll has been made
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)
            self.battle_messages["you_lose_seven_message"].draw(state)

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


        elif self.game_state == "roll_match_win_screen":
            if self.dice_roll_1 > 0:  # Check if a dice roll has been made
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)
            self.battle_messages["you_win_matching_message"].draw(state)

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

        elif self.game_state == "you_lose_come_out_roll_screen":
            if self.dice_roll_1 > 0:  # Check if a dice roll has been made
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)

            self.battle_messages["you_lose_come_out_roll_message"].draw(state)

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



        elif self.game_state == "you_win_come_out_roll_screen":
            if self.dice_roll_1 > 0:  # Check if a dice roll has been made
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)

            self.battle_messages["you_win_come_out_roll_message"].draw(state)

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


        pygame.display.flip()
