import random
from typing import Optional
import pygame

from entity.gui.screen.battle_screen import BattleScreen
from entity.gui.textbox.text_box import TextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic
from globalclasses.money_balancer import MoneyBalancer
from screen.examples.screen import Screen
from screen.floor2.map_screens.area_2_start_screen import Area2StartScreen

# maybe we can have craps be more about saving people? that would be a fun mission
# poison dice  is -1 to all dice rolls , this makes it less likely to get a 7 on come out




# for boss if you roll a snake eyes add + 1 to power meter speed. Triple bet loss on 2 3 12 but triple bet win on 7.

# need to set money stat to 1500 for player as a seperate stat
class CrapsBossScreen(BattleScreen):
    def __init__(self, screenName: str = "Casino Slots Screen") -> None:
        super().__init__(screenName)
        self.game_state: str = "welcome_screen"
        self.sprite_sheet = pygame.image.load("./assets/images/dice45.png")

        self.dice_roll_1 = 0
        self.dice_roll_2 = 0
        self.dice_roll_3 = 0
        self.power_meter_index: int = 0  # Example initial power level
        self.come_out_roll_total = 0
        self.point_roll_total = 0

        # self.point_phase_target = self.dice_roll_1 + self.dice_roll_2

        self.battle_messages: dict[str, TextBox] = {
            "welcome_message": TextBox(
                ["It's too bad you didn't take this serious enough."],
                (65, 460, 700, 130),
                36,
                500
            ),

            "bet_message": TextBox(
                ["Time to take a crap with some craps"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "come_out_roll_message": TextBox(
                ["This is your come out roll"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "come_out_roll_message_unlucky_7": TextBox(
                ["This is come out roll message unlucky 7"],
                (65, 460, 700, 130),
                36,
                500
            ),
            "come_out_roll_message_lucky_7": TextBox(
                ["This is come out roll message lucky 7"],
                (65, 460, 700, 130),
                36,
                500
            ),
            "point_phase_message": TextBox(
                [f"Your point phase is here"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "point_phase_result_message": TextBox(
                [f"Your point phase result messaage is here"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "magic_message": TextBox(
                ["Save it for when its needed most."],
                (65, 460, 700, 130),
                36,
                500
            ),

            "power_meter_message": TextBox(
                ["Save it for when its needed most."],
                (65, 460, 700, 130),
                36,
                500
            ),

            "hand_cramp_message": TextBox(
                ["Jack: Potential hero of legend, corrupted with eternal fear. Fall, falter, and succumb to internal failure...Hands of despair", "Hero: My hands...something is wrong, their cramping up bad.",
                 "Sir Leopold: That bastard just cursed you,your come out roll meter is not only sped up but the margin of success is lower.",
                 "Hero:  He's not the only one that can use magic, time to turn this around. I'm going to bankrupt you Jack."],
                (65, 460, 700, 130),
                36,
                500
            ),

            "game_over_no_stamina_message": TextBox(
                ["Hero: Crap I can't...keep...going...(You ran out of stamina)", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "game_over_no_money_message": TextBox(
                ["You ran out of money, game over, enjoy eternity in chicken nugget  hell", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "game_over_low_stamina_message": TextBox(
                ["Hero: I'm too tired to keep gambling i need to rest", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "game_over_low_money_message": TextBox(
                ["I don't have enough money to keep playing time to leave", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "you_win": TextBox(
                ["Rib Demon: well looks like I lost...", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "you_lose_seven_message": TextBox(
                [f"You rolled a 7 you lose. You win 25 exp and lose {self.bet}"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "you_win_matching_message": TextBox(
                [f"You matched  You win 50 exp and win {self.bet}"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "you_lose_come_out_roll_message": TextBox(
                [f"You rolled a {self.point_roll_total}  and lose. You win 50 exp and lose {self.bet}", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "you_win_come_out_roll_message": TextBox(
                [f"You rolled a 7 and win. You win 50 exp and win {self.bet}", ""],
                (65, 460, 700, 130),
                36,
                500
            ),
            "level_up": TextBox(
                [
                    "Betty: wow you beat me in coin flip, bummer!"
                ],
                (65, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),

        }

        self.come_out_roll_choices: list[str] = ["Roll"]
        self.point_roll_choices: list[str] = ["Play", "Bet"]
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.magic_screen_choices: list[str] = ["CRAPS_LUCKY_7", "Back"]
        self.bet_screen_choices: list[str] = ["Back"]

        self.welcome_screen_index: int = 0
        self.magic_screen_index: int = 0
        self.come_out_roll_index: int = 0
        self.point_roll_index: int = 0
        self.point_bet_index: int = 0
        self.magic_magnet = 0
        self.bet = 75

        self.money_balancer = MoneyBalancer(self.money)

        self.game_over_message = []  # Initialize game_over_message

        self.lucky_seven = False
        self.magic_lock = False
        self.extra_dice = 5
        self.poison = 1
        self.poison_meter_speed = 1

        self.lucky_message_switch = False

        self.power_meter_speed = 2.4
        self.power_meter_goal = 85
        self.player_poison_penalty = False

        self.point_phase_win = False
        self.unlucky_message_switch = False

        self.reset_flag = True
        self.come_out_roll_message_flag = True
        self.lucky_seven_flag = False
        self.unlucky_seven_flag = False

        self.lucky_seven_buff_counter = 0
        self.money: int = 1500  # Add this line




    def game_reset(self, state: "GameState"):

        self.come_out_roll_message_flag = True
        self.lucky_seven_flag = False
        self.unlucky_seven_flag = False

        self.battle_messages["come_out_roll_message"].reset()
        self.battle_messages["come_out_roll_message_unlucky_7"].reset()
        self.battle_messages["come_out_roll_message_lucky_7"].reset()
        self.battle_messages["point_phase_message"].reset()
        self.battle_messages["point_phase_result_message"].reset()
        self.battle_messages["you_lose_come_out_roll_message"].reset()
        self.battle_messages["you_win_come_out_roll_message"].reset()

        self.power_meter_speed = 2.4
        self.power_meter_index = 0

        self.bet = 75
        self.point_phase_win = False

        self.welcome_screen_index = 0
        self.magic_screen_index = 0
        self.come_out_roll_index = 0
        self.point_roll_index = 0
        # we can also reset messages here too as needed
        self.lucky_seven = False
        self.dice_roll_2 = 0
        self.dice_roll_1 = 0
        self.point_roll_total = 0
        self.lucky_message_switch = False
        self.point_roll_total = 0
        self.come_out_roll_total = 0



        if self.lucky_seven_buff_counter > 0:
            self.lucky_seven_buff_counter -= 1
            print("Lucky buff" + str(self.lucky_seven_buff_counter))





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

    def update(self, state: "GameState") -> None:
        if self.lucky_seven_buff_counter > 0:
            self.magic_lock = True
        elif self.lucky_seven_buff_counter == 0:
            self.magic_lock = False

        if self.money <= 0:
            Events.add_event_to_player(state.player, Events.BLACK_JACK_BLACK_MACK_DEFEATED)

        # self.lucky_seven = state.player.luck * 2
        pygame.mixer.music.stop()
        if state.controller.isQPressed:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

        controller = state.controller
        controller.update()



        if self.game_state == "welcome_screen":
            if state.player.leveling_up == True:
                self.game_state = "level_up_screen"

            self.battle_messages["welcome_message"].update(state)

            if self.money < 1:
               self.game_state = "game_over_screen"

            if state.player.stamina_points < 1:
                self.game_state = "game_over_screen"


            elif state.player.stamina_points <= 6 and state.player.stamina_points > 0:
                self.game_state = "game_over_screen"



            elif state.player.money < 50 and state.player.money > 0:
                self.game_state = "game_over_screen"


            elif state.player.money <= 0:
                self.game_state = "game_over_screen"

            if controller.isUpPressed:
                self.welcome_screen_index = (self.welcome_screen_index - 1) % len(self.welcome_screen_choices)
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.welcome_screen_index = (self.welcome_screen_index + 1) % len(self.welcome_screen_choices)
                controller.isDownPressed = False

            if self.welcome_screen_index == 0 and controller.isTPressed:
                self.game_state = "power_meter_screen"
                self.display_dice(state, self.dice_roll_1, self.dice_roll_2)  # Call the method to display the dice roll

                state.player.stamina_points -= 4

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
                self.welcome_screen_index = 0
                state.currentScreen = state.area2GamblingScreen
                state.area2GamblingScreen.start(state)
                controller.isTPressed = False

        elif self.game_state == "level_up_screen":
            self.handle_level_up(state, state.controller)

        elif self.game_state == "bet_screen":
            # print(self.game_state)
            if controller.isUpPressed:
                self.bet += 25
                # print(self.game_state)

                if self.bet >= 75:
                    self.bet = 75
                controller.isUpPressed = False

            if controller.isDownPressed:
                self.bet -= 25
                if self.bet <= 50:
                    self.bet = 50
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
                self.magic_screen_index = (self.magic_screen_index - 1) % len(self.magic_screen_choices)
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.magic_screen_index = (self.magic_screen_index + 1) % len(self.magic_screen_choices)
                controller.isDownPressed = False
            if self.magic_screen_index == 0 and controller.isTPressed:
                self.lucky_seven_buff_counter = 10
                self.magic_lock = True
                controller.isTPressed = False
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
                if self.power_meter_index >= 80:
                    self.lucky_seven = True
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

                                self.dice_roll_1 = 5
                                self.dice_roll_2 = 5
                                self.come_out_roll_total = 10
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

                    if unlucky_two_roll >= 55:
                        self.dice_roll_1 = 1
                        self.dice_roll_2 = 1
                        self.come_out_roll_total = 2

                        print("line 562")
                        self.game_state = "you_lose_come_out_roll_screen"

                    elif unlucky_two_roll < 55:
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
                                state.player.money += self.bet
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
                self.point_roll_index = (self.point_roll_index - 1) % len(self.point_roll_choices)
                print(str(self.point_roll_index))
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.point_roll_index = (self.point_roll_index + 1) % len(self.point_roll_choices)
                controller.isDownPressed = False
            if self.point_roll_index == 0 and controller.isTPressed:
                state.player.stamina_points -= 2
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

                    print("hey hey hey")
                    print("Your dice rolls are:")
                    print(self.dice_roll_3)




                    if self.point_roll_total == 7:
                        self.dice_roll_2 = original_dice
                        self.point_roll_total = self.dice_roll_1 + self.dice_roll_2
                        print("your come out  roll total is: " + str(self.come_out_roll_total) + f"and your roll is {self.point_roll_total}")

                    # self.dice_roll_1 = random.randint(1, 6)
                    # self.dice_roll_2 = random.randint(1, 6)
                    # self.point_roll_total = self.dice_roll_1 + self.dice_roll_2


                if self.point_roll_total == 7:
                    print("you rolled 7 line 625")
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
                state.player.money -= self.bet
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
                state.player.money += self.bet
                self.money -= self.bet
                state.player.exp += 25
                self.game_state = "welcome_screen"
                self.game_reset(state)











        elif self.game_state == "point_bet_screen":
            if controller.isUpPressed:
                self.bet += 25
                if self.bet > 150:
                    self.bet = 150
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
                state.player.money -= self.bet
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
                state.player.money -= self.bet
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
                state.player.money += self.bet
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
                state.player.money -= self.bet
                self.money += self.bet
                self.point_roll_total = 0
                self.game_reset(state)

                self.game_state = "welcome_screen"
                controller.isTPressed = False


        elif self.game_state == "roll_match_win_screen":
            self.battle_messages["you_win_matching_message"].update(state)

            if controller.isTPressed:
                state.player.money += self.bet
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



            elif state.player.stamina_points <= 6 and state.player.stamina_points > 0:
                self.battle_messages["game_over_low_stamina_message"].update(state)



            elif state.player.money < 50 and state.player.money > 0:
                self.battle_messages["game_over_low_money_message"].update(state)



            elif state.player.money <= 0:
                self.battle_messages["game_over_no_money_message"].update(state)





    def draw(self, state: "GameState") -> None:
        state.DISPLAY.fill((0, 0, 51))
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)


        self.draw_bottom_black_box(state)


        if self.game_state == "welcome_screen":
            self.battle_messages["welcome_message"].draw(state)

            if self.money < 1:
                self.battle_messages["you_win"].draw(state)

            if state.player.stamina_points < 1:
                self.battle_messages["game_over_no_stamina_message"].draw(state)

            elif state.player.money <= 0:
                self.battle_messages["game_over_no_money_message"].draw(state)

            elif state.player.stamina_points <= 10 and state.player.stamina_points > 0:
                self.battle_messages["game_over_low_stamina_message"].draw(state)

            elif state.player.money < 50 and state.player.money > 0:
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

            if self.magic_lock == True:
                self.welcome_screen_choices[1] = "Locked"

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
                    state.currentScreen = state.area2GamglingScreen
                    state.area2GamglingScreen.start(state)


            elif state.player.money < 50 and state.player.money > 0:
                self.battle_messages["game_over_low_money_message"].draw(state)

                if self.battle_messages["game_over_low_money_message"].message_index == 1:
                    state.currentScreen = state.area2RestScreen
                    state.area2RestScreen.start(state)

            elif state.player.money <= 0:
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
            print("drawing point bet")

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