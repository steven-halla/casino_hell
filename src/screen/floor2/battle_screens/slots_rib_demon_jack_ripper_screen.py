import pygame
import random
from entity.gui.screen.battle_screen import BattleScreen
from entity.gui.textbox.text_box import TextBox
from game_constants.events import Events
from game_constants.magic import Magic
from globalclasses.exp_gain import ExpGain
from globalclasses.game_over import GameOver
from globalclasses.money_balancer import MoneyBalancer
from screen.examples.screen import Screen
from screen.floor2.map_screens.area_2_gambling_screen import Area2GamblingScreen
from screen.floor2.map_screens.area_2_start_screen import Area2StartScreen



class SlotsRippaSnappaScreen(BattleScreen):
    def __init__(self) -> None:
        super().__init__("Casino Slots Screen")

        self.game_over = GameOver()  # Initialize GameOver


        self.three_zeros: bool = False
        self.three_ones: bool  = False
        self.three_twos: bool  = False
        self.three_threes: bool  = False
        self.three_fours: bool  = False
        self.three_fives: bool  = False
        self.three_sixes: bool  = False
        self.three_sevens: bool  = False
        self.three_eights: bool  = False
        self.three_nines: bool  = False
        self.secret_item = False

        self.lock_down: int = 0




        self.no_matches = True

        self.resolve_penalty = False

        self.slot1: list[int] = [0, 0, 0]
        self.slot2: list[int] = [0, 0, 0]
        self.slot3: list[int] = [0, 0, 0]
        self.slot_positions1: list[int] = [-50, 0, 50]
        self.slot_positions2: list[int] = [-50, 0, 50]
        self.slot_positions3: list[int] = [-50, 0, 50]
        self.last_update_time: int = pygame.time.get_ticks()
        self.spin_delay: int = 44
        self.spinning: bool = False
        self.stopping: bool = False
        self.stop_start_time: int = 0
        self.stopping_first: bool = False
        self.stopping_second: bool = False
        self.magic_lock = False


        self.exp_gain = ExpGain()  # Initialize ExpGain without specifying experience points



        self.magic_screen_choices: list[str] = [ "Back"]
        self.welcome_screen_index: int = 0
        self.magic_screen_index: int = 0

        #maybe replace Bet with Rules?
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.level_screen_stats: list[str] = ["Body", "Mind", "Spirit", "Perception", "Luck"]
        self.level_up_stat_increase_index: int = 0

        self.go_to_results: bool = False

        self.new_font: pygame.font.Font = pygame.font.Font(None, 36)
        self.game_state: str = "welcome_screen"
        self.bet: int = 50
        self.money: int = 1000
        self.font: pygame.font.Font = pygame.font.Font(None, 36)
        self.battle_messages: dict[str, TextBox] = {
            "welcome_message": TextBox(
                [""],
                (65, 460, 700, 130),
                36,
                500
            ),
            "spin_message": TextBox(
                ["Press the A key to start the spin."],
                (65, 460, 700, 130),
                36,
                500
            ),
            "magic_message": TextBox(
                ["Casts a spell"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "bet_message": TextBox(
                ["Min Bet of 50, Bet of 60 increases chances for super secret item!"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "results_message": TextBox(
                ["Your spinssss is {0} {1} {2}", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "game_over_no_stamina_message": TextBox(
                ["Hero: Crap I can't...keep...going...(You ran out of stamina", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

            "game_over_no_money_message": TextBox(
                ["You ran out of money game over, enjoy eternity in rib demon hell", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

        "game_over_low_stamina_message": TextBox(
                ["Hero: I'm too tired to keep gambling i need to rest)", ""],
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

            "level_up": TextBox(
                [f"Grats you levels up. ", "", "", "", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

        }

        self.hide_numbers: bool = True

        self.money_balancer = MoneyBalancer(self.money)
        self.game_over = GameOver()  # Initialize GameOver

        self.game_over_message = []  # Initialize game_over_message

        self.slot_hack = 0
        self.rib_demon_attack_damage = 50
        self.lucky_strike = 0
        self.hack_cast_cost = 50

        self.spell_sound = pygame.mixer.Sound("./assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)

        self.menu_movement_sound = pygame.mixer.Sound("./assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)

        # self.music_file = "./assets/music/coin_flip_screen.mp3"
        # self.music_volume = 0.5  # Adjust as needed
        # self.initialize_music()
        self.music_on = True

        self.music_file = "./assets/music/slots_music.mp3"
        self.music_volume = 0.5  # Adjust as needed
        pygame.mixer.music.stop()

    def start(self, state: 'GameState') -> None:
        self.initialize_music()

    def print_current_slots(self) -> None:
        visible_slots = [self.slot1[0], self.slot2[0], self.slot3[0]]

    def generate_numbers(self, state) -> None:
        # Generate the first slot number based on a 1-100 range
        generated_values1 = [random.randint(1, 100) for _ in range(3)]
        print(f"Generated values for slot1: {generated_values1}")

        # Map the generated values to slot numbers 0-9
        def map_to_slot_number(value: int) -> int:
            if self.lock_down == 0 and self.lucky_strike == 0 and self.bet < 60:
                print("self.lockdown == 0 and self.luck_strike == 0 and self.bet < 60")
                slot_mapping = {
                            range(1, 7): 0,  # lose a rib
                            range(7, 15): 1,  # lost 50 extra coins from your state.player.money
                            range(15, 27): 2,  # unlucky spin cannot exit out of game + 10% to lose a rib -rib lock status
                            range(27, 42): 3,  # add 100 coins
                            range(42, 54): 4,  # gain 10 hp 10 mp 100 coins
                            range(54, 66): 5,  # gain 20 hp 20 mp 125 coins
                            range(66, 76): 6,  # add 200 coins
                            range(76, 85): 7,  # lucky spin better % for jackpot
                            range(85, 95): 8,  # get special item or 50 coins
                            range(95, 101): 9,  # jackpot
                }

            elif self.lock_down > 0 and self.lucky_strike == 0:
                print("elif self.lock_down > 0 and self.lucky_strike == 0:")
                slot_mapping = {
                    range(1, 19): 0,  # lose a rib
                    range(19, 24): 1,  # lost 50 extra coins from your state.player.money
                    range(24, 33): 2,  # unlucky spin cannot exit out of game + 10% to lose a rib -rib lock status
                    range(33, 51): 3,  # add 100 coins
                    range(51, 62): 4,  # gain 10 hp 10 mp 100 coins
                    range(62, 101): 5,  # gain 20 hp 20 mp 125 coins

                }

            elif self.lucky_strike == 0 and self.bet > 50:
                print("Lucky strike == 0 and self.bet > 50")
                slot_mapping = {
                    range(1, 7): 0,  # lose a rib
                    range(7, 15): 1,  # lost 50 extra coins from your state.player.money
                    range(15, 27): 2,  # unlucky spin cannot exit out of game + 10% to lose a rib -rib lock status
                    range(27, 42): 3,  # add 100 coins
                    range(42, 54): 4,  # gain 10 hp 10 mp 100 coins
                    range(53, 60): 5,  # gain 20 hp 20 mp 125 coins
                    range(60, 67): 6,  # add 200 coins
                    range(67, 76): 7,  # lucky spin better % for jackpot
                    range(76, 92): 8,  # get special item or 50 coins
                    range(92, 101): 9,  # jackpot
                }





            elif self.lucky_strike > 0 and self.bet > 50:
                print("elif self.lucky_strike > 0 and self.bet > 50:")
                slot_mapping = {

                    range(1, 30): 3,  # add 100 coins
                    range(30, 40): 4,  # gain 10 hp 10 mp 100 coins
                    range(40, 50): 5,  # gain 20 hp 20 mp 125 coins
                    range(50, 55): 6,  # add 200 coins
                    range(55, 85): 8,  # get special item or 50 coins
                    range(85, 101): 9,  # jackpot
                }

            elif self.lucky_strike > 0:
                print("elif self.lucky_strike > 0:")
                slot_mapping = {

                    range(1, 30): 3,  # add 100 coins
                    range(30, 40): 4,  # gain 10 hp 10 mp 100 coins
                    range(40, 50): 5,  # gain 20 hp 20 mp 125 coins
                    range(50, 60): 6,  # add 200 coins
                    range(60, 85): 8,  # get special item or 50 coins
                    range(85, 101): 9,  # jackpot
                }

            else:
                print("else default just in case")
                slot_mapping = {
                    range(1, 7): 0,  # lose a rib
                    range(7, 15): 1,  # lost 50 extra coins from your state.player.money
                    range(15, 24): 2,  # unlucky spin cannot exit out of game + 10% to lose a rib -rib lock status
                    range(24, 42): 3,  # add 100 coins
                    range(42, 54): 4,  # gain 10 hp 10 mp 100 coins
                    range(54, 66): 5,  # gain 20 hp 20 mp 125 coins
                    range(66, 76): 6,  # add 200 coins
                    range(76, 85): 7,  # lucky spin better % for jackpot
                    range(85, 95): 8,  # get special item or 50 coins
                    range(95, 101): 9,  # jackpot
                }

            # for key in slot_mapping:
            #     print(f"Range {key}: {slot_mapping[key]}")

            for key in slot_mapping:
                if value in key:
                    return slot_mapping[key]
            return 0  # Default value in case something goes wrong

        self.slot1 = [map_to_slot_number(value) for value in generated_values1]

        generated_value2 = random.randint(1, 100)
        if self.lock_down > 0:
            if self.slot1[0] <= 2:
                generated_value2 += 20
                print(generated_value2)
        print(generated_value2)
        # Assuming generated_value2 is defined earlier in your code
        for luck in range(state.player.luck):
            if self.slot1[0] > 2:
                generated_value2 += 2
                print(generated_value2)


        if generated_value2 >= 40:  # 50% chance to match slot1
            self.slot2[0] = self.slot1[0]
        else:
            self.slot2[0] = map_to_slot_number(generated_value2)

        # Generate the third slot number based on a 1-100 roll
        generated_value3 = random.randint(1, 100)
        if self.lock_down > 0:
            if self.slot1[0] <= 2:
                generated_value3 += 20
                print(generated_value3)
        print(generated_value3)

        for luck in range(state.player.luck):
            if self.slot1[0] > 2:
                generated_value3 += 2
                print(generated_value3)


        # print(f"Generated value for slot3 position 0: {generated_value3}")
        if generated_value3 >= 60:  # 75% chance to match slot1
            self.slot3[0] = self.slot1[0]
        else:
            self.slot3[0] = map_to_slot_number(generated_value3)
        # for testing
        # self.slot1[0] = 8
        # self.slot2[0] = 8
        # self.slot3[0] = 8




            # Check if all three slots are 0 and print "hi zeros"
        if self.slot1[0] == 0 and self.slot2[0] == 0 and self.slot3[0] == 0:
            print("hi zeros")
            self.three_zeros = True
            self.no_matches = False

        if self.slot1[0] == 1 and self.slot2[0] == 1 and self.slot3[0] == 1:
            print("hi ones")
            self.three_ones = True
            self.no_matches = False


        if self.slot1[0] == 2 and self.slot2[0] == 2 and self.slot3[0] == 2:
            print("hi twos")
            self.three_twos = True
            self.no_matches = False


        if self.slot1[0] == 3 and self.slot2[0] == 3 and self.slot3[0] == 3:
            print("hi threes")
            self.three_threes = True
            self.no_matches = False


        if self.slot1[0] == 4 and self.slot2[0] == 4 and self.slot3[0] == 4:
            print("hi fours")
            self.three_fours = True
            self.no_matches = False


        if self.slot1[0] == 5 and self.slot2[0] == 5 and self.slot3[0] == 5:
            print("hi fives")
            self.three_fives = True
            self.no_matches = False


        if self.slot1[0] == 6 and self.slot2[0] == 6 and self.slot3[0] == 6:
            print("hi sixes")
            self.three_sixes = True
            self.no_matches = False


        if self.slot1[0] == 7 and self.slot2[0] == 7 and self.slot3[0] == 7:
            print("hi sevens")
            self.three_sevens = True
            self.no_matches = False


        if self.slot1[0] == 8 and self.slot2[0] == 8 and self.slot3[0] == 8:
            print("hi eights")
            self.three_eights = True
            self.no_matches = False


        if self.slot1[0] == 9 and self.slot2[0] == 9 and self.slot3[0] == 9:
            print("hi nines")
            self.three_nines = True
            self.no_matches = False


        # print(f"Mapped slot3 values: {self.slot3}")

    # Ensure to call this method within your logic where needed

    def handle_spinning(self, state: "GameState", current_time: int) -> None:
        if self.spinning:
            if current_time - self.last_update_time > self.spin_delay:
                self.last_update_time = current_time  # this and the line above control the speed of spinning slots (spin_delay mainly)
                for i in range(3):  # the positions of the slots (top middle bottom)
                    if not self.stopping_first:
                        self.slot_positions1[i] += 10
                        if self.slot_positions1[i] >= 100:  # this block handles the position of spinning slots as they stop
                            self.slot_positions1[i] = -50  # sets it in the middle
                    if not self.stopping_second:
                        self.slot_positions2[i] += 10
                        if self.slot_positions2[i] >= 100:
                            self.slot_positions2[i] = -50
                    self.slot_positions3[i] += 10
                    if self.slot_positions3[i] >= 100:
                        self.slot_positions3[i] = -50

            if self.stopping:
                if not self.stopping_first:
                    if current_time - self.stop_start_time >= 2000:  # the time is in milliseconds, so 2 seconds
                        self.stopping_first = True
                        self.slot_positions1 = [0, 50, 100]
                elif not self.stopping_second:
                    if current_time - self.stop_start_time >= 3500:  # this stops 1.5 seconds after slot 1 stops
                        self.stopping_second = True
                        self.slot_positions2 = [0, 50, 100]
                elif current_time - self.stop_start_time >= 5000:  # this stops 3 seconds after slot 1 stops / 1.5 after slot 2
                    self.spinning = False
                    self.stopping = False  # this ensures the slots remain stopped
                    print("Spinning stopped.")
                    self.slot_positions3 = [0, 50, 100]
                    self.print_current_slots()
                    self.go_to_results = True
                    # self.test() this is to test spin % out of 10000

        if state.controller.isQPressed:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return



        if state.controller.isAPressed and self.game_state == "spin_screen":
            self.a_key_pressed = True
            if not self.spinning:
                self.spinning = True
                self.stopping = False
                self.stopping_first = False
                self.stopping_second = False
                self.spin_delay = 70
                print("Spinning started.")
                self.generate_numbers(state)  # Call the method to generate new numbers
            else:
                self.stopping = True
                self.stop_start_time = current_time
                print("Stopping initiated.")

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
        if state.musicOn == True:
            if self.music_on == True:
                print("djslfjldsjfj;as")
                self.stop_music()
                self.initialize_music()
                self.music_on = False

        state.player.canMove = False
        if self.secret_item == True:
            self.bet = 50

        if Events.MC_NUGGET_FIRST_QUEST_COMPLETE.value in state.player.level_two_npc_state:
            self.secret_item = True


        current_time: int = pygame.time.get_ticks()  # local variable
        if state.controller.isBPressed:
            self.hide_numbers = not self.hide_numbers

        self.handle_spinning(state, current_time)  # Call the new method here

        controller = state.controller
        controller.update()





        if self.game_state == "welcome_screen":
            self.music_volume = 0.5  # Adjust as needed
            pygame.mixer.music.set_volume(self.music_volume)


            state.player.update(state)

            if state.controller.isEPressed:
                state.player.leveling_up = False



            if state.player.leveling_up == True:
                self.game_state = "level_up_screen"


            # if "Lucky Shoes" in state.player.items:
            #     self.bet = 50
            self.no_matches = True

            self.three_zeros = False
            self.three_ones = False
            self.three_twos = False
            self.three_threes = False
            self.three_fours = False
            self.three_fives = False
            self.three_sixes = False
            self.three_sevens = False
            self.three_eights = False
            self.three_nines = False

            self.go_to_results = False
            self.battle_messages["welcome_message"].update(state)
            
            
            if self.money < 1:
                self.battle_messages["you_win"].update(state)
                if self.battle_messages["you_win"].message_index == 1:
                    Events.add_event_to_player(state.player, Events.SLOTS_RIPPA_SNAPPA_DEFEATED)
                    state.player.canMove = True

                    state.currentScreen = state.area2GamblingScreen
                    state.area2GamblingScreen.start(state)



            if state.player.stamina_points < 1:

                self.lock_down = False
                self.slot_hack = 0
                self.battle_messages["game_over_no_stamina_message"].update(state)
                if self.battle_messages["game_over_no_stamina_message"].message_index == 1:
                    state.player.canMove = True

                    state.currentScreen = state.area2GamblingScreen
                    state.area2GamblingScreen.start(state)

                    self.reset()

            # elif state.player.stamina_points <= 10 and state.player.stamina_points > 0:
            #     self.battle_messages["game_over_low_stamina_message"].update(state)
            #     if self.battle_messages["game_over_low_stamina_message"].message_index == 1:
            #         state.currentScreen = Area2GamblingScreen()
            #         self.reset()



            elif state.player.money < 50 and state.player.money > 0:
                self.battle_messages["game_over_low_money_message"].update(state)
                if self.battle_messages["game_over_low_money_message"].message_index == 1:
                    state.player.canMove = True

                    state.currentScreen = state.area2GamblingScreen
                    state.area2GamblingScreen.start(state)

                    self.reset()


            elif state.player.money <= 0:
                state.player.canMove = True

                self.battle_messages["game_over_no_money_message"].update(state)
                if self.battle_messages["game_over_no_money_message"].message_index == 1:
                    state.currentScreen = GameOver()

            if controller.isUpPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.welcome_screen_index = (self.welcome_screen_index - 1) % len(self.welcome_screen_choices)
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.welcome_screen_index = (self.welcome_screen_index + 1) % len(self.welcome_screen_choices)
                controller.isDownPressed = False

            if self.welcome_screen_index == 0 and controller.isTPressed:
                self.game_state = "spin_screen"

                state.player.stamina_points -= 10
                if self.slot_hack == 0:
                    state.player.money -= self.bet
                    self.money += self.bet

                controller.isTPressed = False
            elif self.welcome_screen_index == 1 and controller.isTPressed and self.slot_hack == 0 and Magic.SLOTS_HACK.value in state.player.magicinventory:
                self.magic_screen_index = 0
                # controller.isTPressed = False

                self.battle_messages["magic_message"].reset()
                self.game_state = "magic_screen"
            elif (self.welcome_screen_index == 2 and controller.isTPressed \
                  and Events.MC_NUGGET_QUEST_1_REWARD not in state.player.level_two_npc_state) and self.secret_item == False:
                self.battle_messages["bet_message"].reset()
                self.game_state = "bet_screen"
                controller.isTPressed = False
            elif self.welcome_screen_index == 3 and controller.isTPressed and self.lock_down == 0:
                state.player.canMove = True

                state.currentScreen = state.area2GamblingScreen
                state.area2GamblingScreen.start(state)
                self.welcome_screen_index = 0
                self.reset()

                controller.isTPressed = False

        elif self.game_state == "level_up_screen":
            self.music_volume = 0  # Adjust as needed
            pygame.mixer.music.set_volume(self.music_volume)
            self.handle_level_up(state, state.controller)


        elif self.game_state == "magic_screen":
            if self.magic_screen_index == 0:
                self.battle_messages["magic_message"].messages = [f"Put a string on a coin"]
            elif self.magic_screen_index == 1:
                self.battle_messages["magic_message"].messages = [f"Go back to main menu."]
            self.battle_messages["results_message"].update(state)
            self.battle_messages["magic_message"].update(state)
            if controller.isUpPressed:
                self.menu_movement_sound.play()  # Play the sound effect once


                self.magic_screen_index = (self.magic_screen_index - 1) % len(self.magic_screen_choices)
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.magic_screen_index = (self.magic_screen_index + 1) % len(self.magic_screen_choices)
                controller.isDownPressed = False
            if self.magic_screen_index == 0 and controller.isTPressed and state.player.focus_points >= self.hack_cast_cost:
                print("hi there line 618")
                self.spell_sound.play()  # Play the sound effect once

                self.slot_hack += 5
                state.player.focus_points -= self.hack_cast_cost
                self.game_state = "welcome_screen"
                controller.isTPressed = False

                print(self.slot_hack)
            elif self.magic_screen_index == 1 and controller.isTPressed:
                self.battle_messages["magic_message"].update(state)
                self.game_state = "welcome_screen"
                controller.isTPressed = False

        if self.game_state == "bet_screen":
            self.battle_messages["bet_message"].update(state)
            if controller.isUpPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.bet += 10
                if self.bet > 60:
                    self.bet = 60
                controller.isUpPressed = False
            elif controller.isDownPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                self.bet -= 10
                if self.bet < 50:
                    self.bet = 50
                controller.isDownPressed = False
            elif controller.isBPressed:
                self.game_state = "welcome_screen"
                controller.isBPressed = False

        if self.game_state == "spin_screen":
            self.battle_messages["spin_message"].update(state)
            if self.go_to_results:
                self.game_state = "results_screen"










        if self.game_state == "results_screen":

            if self.no_matches == True:
                # Assuming you want to display the amount of experience gained
                exp_amount = 7  # This should be the amount of exp gained
                self.battle_messages["results_message"].messages = [
                    f"No Matches! Your spin is {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} and you gain {exp_amount} exp", ""
                ]

                # self.battle_messages["results_message"].update(state)

                if self.resolve_penalty == False:
                    self.exp_gain.gain_exp(state, exp_amount)  # Use the exp_amount variable
                    self.resolve_penalty = True

                self.battle_messages["results_message"].update(state)



            elif self.three_zeros == True:
                if Events.SLOTS_VEST_FOUND.value in state.player.quest_items:
                    self.rib_demon_attack_damage = 25

                self.battle_messages["results_message"].messages = [
                    f"You fail  spin is {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} and take {self.rib_demon_attack_damage} damage and gain 50 exp", ""
                ]

                self.battle_messages["results_message"].update(state)

                if self.resolve_penalty == False:
                    if Events.SLOTS_VEST_FOUND.value not in state.player.quest_items:
                        state.player.stamina_points -= 50
                    elif Events.SLOTS_VEST_FOUND.value in state.player.quest_items:
                        state.player.stamina_points -= 25
                    self.exp_gain.gain_exp(state, 50)  # Adjust the amount of experience points as needed

                    self.resolve_penalty = True

            elif self.three_ones == True:
                self.battle_messages["results_message"].messages = [
                    f"You fail,  spin is {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} and you lose 100 gold and gain 20 exp", ""
                ]

                self.battle_messages["results_message"].update(state)

                if self.resolve_penalty == False:
                    state.player.money -= 100
                    self.exp_gain.gain_exp(state, 25)  # Adjust the amount of experience points as needed

                    self.money += 100
                    self.resolve_penalty = True

            elif self.three_twos == True:
                self.battle_messages["results_message"].messages = [
                    f"You fail, spin is {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} Your locked in, your ribs are now tingling with fear,  and gain 25 exp ", ""
                ]

                self.battle_messages["results_message"].update(state)

                if self.resolve_penalty == False:
                    print("player lock")
                    self.exp_gain.gain_exp(state, 25)  # Adjust the amount of experience points as needed

                    self.resolve_penalty = True
                    self.lock_down = 5
                    self.lucky_strike = 0

            elif self.three_threes == True:
                self.battle_messages["results_message"].messages = [
                    f"You win!  Spin is {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} You win 150 Coins! and 10 exp", ""
                ]

                self.battle_messages["results_message"].update(state)

                if self.resolve_penalty == False:

                    self.resolve_penalty = True
                    # Capture the initial enemy money before adjustment
                    initial_enemy_money = self.money
                    self.exp_gain.gain_exp(state, 10)  # Adjust the amount of experience points as needed

                    print(f"Initial Player Money: {state.player.money}")
                    print(f"Initial Enemy Money: {initial_enemy_money}")

                    # The amount to add or subtract
                    jackpot_amount = 150

                    # Adjust player and enemy money
                    if self.money > 99:
                        state.player.money += jackpot_amount

                    self.money -= jackpot_amount

                    # Print values after jackpot logic
                    print(f"After Jackpot - Player Money: {state.player.money}")
                    print(f"After Jackpot - Enemy Money: {self.money}")

                    print("now its time for a lucky strike")

                    # Use MoneyBalancer to ensure enemy's money does not go below zero
                    self.money_balancer.money = self.money
                    self.money_balancer.balance_money(state, initial_enemy_money)

                    # Update the enemy's money after balancing
                    self.money = self.money_balancer.money



            elif self.three_fours == True:
                self.battle_messages["results_message"].messages = [
                    f"You win, spin of {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} You gain 150 money and 15 exp!", ""
                ]

                self.battle_messages["results_message"].update(state)

                if self.resolve_penalty == False:

                    self.resolve_penalty = True
                    self.exp_gain.gain_exp(state, 15)  # Adjust the amount of experience points as needed

                    # Capture the initial enemy money before adjustment
                    initial_enemy_money = self.money
                    print(f"Initial Player Money: {state.player.money}")
                    print(f"Initial Enemy Money: {initial_enemy_money}")

                    # The amount to add or subtract
                    jackpot_amount = 150

                    # Adjust player and enemy money
                    if self.money > 99:
                        state.player.money += jackpot_amount

                    self.money -= jackpot_amount

                    # Print values after jackpot logic
                    print(f"After Jackpot - Player Money: {state.player.money}")
                    print(f"After Jackpot - Enemy Money: {self.money}")

                    print("now its time for a lucky strike")

                    # Use MoneyBalancer to ensure enemy's money does not go below zero
                    self.money_balancer.money = self.money
                    self.money_balancer.balance_money(state, initial_enemy_money)

                    # Update the enemy's money after balancing
                    self.money = self.money_balancer.money
                    if state.player.stamina_points < state.player.max_stamina_points:
                        state.player.stamina_points += 10
                        if state.player.stamina_points > state.player.max_stamina_points:
                            state.player.stamina_points = state.player.max_stamina_points
                    if state.player.focus_points < state.player.max_focus_points:
                        state.player.focus_points += 5
                        if state.player.focus_points > state.player.max_focus_points:
                            state.player.focus_points = state.player.max_focus_points


            elif self.three_fives == True:
                self.battle_messages["results_message"].messages = [
                    f"You got {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} You gain 150 gold and +15 exp", ""
                ]

                self.battle_messages["results_message"].update(state)

                if self.resolve_penalty == False:

                    self.resolve_penalty = True
                    self.exp_gain.gain_exp(state, 15)  # Adjust the amount of experience points as needed

                    # Capture the initial enemy money before adjustment
                    initial_enemy_money = self.money
                    print(f"Initial Player Money: {state.player.money}")
                    print(f"Initial Enemy Money: {initial_enemy_money}")

                    # The amount to add or subtract
                    jackpot_amount = 150

                    # Adjust player and enemy money
                    if self.money > 99:
                        state.player.money += jackpot_amount

                    self.money -= jackpot_amount

                    # Print values after jackpot logic
                    print(f"After Jackpot - Player Money: {state.player.money}")
                    print(f"After Jackpot - Enemy Money: {self.money}")

                    print("now its time for a lucky strike")

                    # Use MoneyBalancer to ensure enemy's money does not go below zero
                    self.money_balancer.money = self.money
                    self.money_balancer.balance_money(state, initial_enemy_money)

                    # Update the enemy's money after balancing
                    self.money = self.money_balancer.money
                    state.player.exp += 50


            elif self.three_sixes == True:
                self.battle_messages["results_message"].messages = [
                    f"You got {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} You gain 300 gold and 30 exp", ""
                ]

                self.battle_messages["results_message"].update(state)

                if self.resolve_penalty == False:
                    self.resolve_penalty = True
                    self.exp_gain.gain_exp(state, 30)  # Adjust the amount of experience points as needed

                    # Capture the initial enemy money before adjustment
                    initial_enemy_money = self.money
                    print(f"Initial Player Money: {state.player.money}")
                    print(f"Initial Enemy Money: {initial_enemy_money}")

                    # The amount to add or subtract
                    jackpot_amount = 300

                    # Adjust player and enemy money
                    if self.money > 249:
                        state.player.money += jackpot_amount

                    self.money -= jackpot_amount

                    # Print values after jackpot logic
                    print(f"After Jackpot - Player Money: {state.player.money}")
                    print(f"After Jackpot - Enemy Money: {self.money}")

                    print("now its time for a lucky strike")

                    # Use MoneyBalancer to ensure enemy's money does not go below zero
                    self.money_balancer.money = self.money
                    self.money_balancer.balance_money(state, initial_enemy_money)

                    # Update the enemy's money after balancing
                    self.money = self.money_balancer.money


            elif self.three_sevens == True:
                self.battle_messages["results_message"].messages = [
                    f"You got {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} Lucky 7s increased chance of jack pot and 50 exp gained + 100 coins!", ""
                ]

                self.battle_messages["results_message"].update(state)

                if self.resolve_penalty == False:
                    self.resolve_penalty = True
                    self.exp_gain.gain_exp(state, 50)  # Adjust the amount of experience points as needed

                    # Capture the initial enemy money before adjustment
                    initial_enemy_money = self.money
                    print(f"Initial Player Money: {state.player.money}")
                    print(f"Initial Enemy Money: {initial_enemy_money}")

                    # The amount to add or subtract
                    jackpot_amount = 100

                    # Adjust player and enemy money
                    if self.money > 49:
                        state.player.money += jackpot_amount

                    self.money -= jackpot_amount

                    # Print values after jackpot logic
                    print(f"After Jackpot - Player Money: {state.player.money}")
                    print(f"After Jackpot - Enemy Money: {self.money}")

                    print("now its time for a lucky strike")

                    # Use MoneyBalancer to ensure enemy's money does not go below zero
                    self.money_balancer.money = self.money
                    self.money_balancer.balance_money(state, initial_enemy_money)

                    # Update the enemy's money after balancing
                    self.money = self.money_balancer.money




                    self.lucky_strike += 6
                    print("now its time for a lucky strike")


            elif self.three_eights == True:

                if Events.MC_NUGGET_QUEST_1_REWARD.value not in state.player.level_two_npc_state:
                    Events.add_event_to_player(state.player, Events.MC_NUGGET_FIRST_QUEST_COMPLETE)

                    self.battle_messages["results_message"].messages = [
                        f"You got {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} grats you got the super secret item!! + 25 exp", ""
                    ]

                    self.battle_messages["results_message"].update(state)

                elif Events.MC_NUGGET_QUEST_1_REWARD.value in state.player.level_two_npc_state and self.secret_item == True:
                    self.battle_messages["results_message"].messages = [
                        f"You got {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} too bad for you there is only 1 item.!", ""
                    ]

                    self.battle_messages["results_message"].update(state)

                if self.resolve_penalty == False:
                    self.secret_item = True
                    self.exp_gain.gain_exp(state, 25)  # Adjust the amount of experience points as needed

                    state.player.money += 100
                    self.money -= 100

                    # Capture the initial enemy money before adjustment
                    initial_enemy_money = self.money
                    print(f"Initial Player Money: {state.player.money}")
                    print(f"Initial Enemy Money: {initial_enemy_money}")

                    # The amount to add or subtract
                    jackpot_amount = 100

                    # Adjust player and enemy money
                    if self.money > 49:
                        state.player.money += jackpot_amount

                    self.money -= jackpot_amount

                    # Print values after jackpot logic
                    print(f"After Jackpot - Player Money: {state.player.money}")
                    print(f"After Jackpot - Enemy Money: {self.money}")

                    print("now its time for a lucky strike")

                    # Use MoneyBalancer to ensure enemy's money does not go below zero
                    self.money_balancer.money = self.money
                    self.money_balancer.balance_money(state, initial_enemy_money)

                    # Update the enemy's money after balancing
                    self.money = self.money_balancer.money

                    self.resolve_penalty = True

            elif self.three_nines:
                self.battle_messages["results_message"].messages = [
                    f"You got {self.slot1[0]} {self.slot2[0]} {self.slot3[0]} You got the JACK POT!!!! gain 100 exp, 500 coins and some hp /mp back!", ""
                ]

                self.battle_messages["results_message"].update(state)

                if self.resolve_penalty == False:
                    self.resolve_penalty = True
                    self.exp_gain.gain_exp(state, 100)  # Adjust the amount of experience points as needed


                    # Capture the initial enemy money before adjustment
                    initial_enemy_money = self.money
                    print(f"Initial Player Money: {state.player.money}")
                    print(f"Initial Enemy Money: {initial_enemy_money}")

                    # The amount to add or subtract
                    jackpot_amount = 500

                    # Adjust player and enemy money
                    if self.money > 499:
                        state.player.money += jackpot_amount


                    self.money -= jackpot_amount



                    # Use MoneyBalancer to ensure enemy's money does not go below zero
                    self.money_balancer.money = self.money
                    self.money_balancer.balance_money(state, initial_enemy_money)

                    # Update the enemy's money after balancing
                    self.money = self.money_balancer.money

                    if state.player.stamina_points < state.player.max_stamina_points:
                        state.player.stamina_points += 30
                        if state.player.stamina_points > state.player.max_stamina_points:
                            state.player.stamina_points = state.player.max_stamina_points
                    if state.player.focus_points < state.player.max_focus_points:
                        state.player.focus_points += 30
                        if state.player.focus_points > state.player.max_focus_points:
                            state.player.focus_points = state.player.max_focus_points


            if self.battle_messages["results_message"].message_index == 1:
                self.battle_messages["welcome_message"].reset()
                self.battle_messages["results_message"].reset()
                self.resolve_penalty = False
                if self.lucky_strike > 0:
                    self.lucky_strike -= 1
                if self.lock_down > 0:
                    self.lock_down -= 1

                if self.slot_hack > 0:
                    self.slot_hack -= 1

                self.game_state = "welcome_screen"
                if self.secret_item == True and Events.MC_NUGGET_QUEST_1_REWARD.value not in state.player.level_two_npc_state:
                    state.player.level_two_npc_state.append(Events.MC_NUGGET_QUEST_1_REWARD.value)
                print(str(state.player.items))

    def draw(self, state: "GameState") -> None:
        state.DISPLAY.fill((0, 0, 51))
        if not self.hide_numbers:
            self.draw_mask_box(state)

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

        state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True, (255, 255, 255)), (37, 250))
        state.DISPLAY.blit(self.font.render(f"HP: {state.player.stamina_points}", True, (255, 255, 255)), (37, 290))
        state.DISPLAY.blit(self.font.render(f"MP: {state.player.focus_points}", True, (255, 255, 255)), (37, 330))
        if self.lucky_strike > 0:
            state.DISPLAY.blit(self.font.render(f"Lucky {self.lucky_strike}", True, (255, 255, 255)), (37, 205))

        elif self.lock_down < 1:
            state.DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)), (37, 205))
        elif self.lock_down > 0:
            state.DISPLAY.blit(self.font.render(f"Locked Down:{self.lock_down}", True, (255, 0, 0)), (37, 205))


        #
        # self.draw_hero_info_boxes(state)

        self.draw_grid_box(state)
        if self.slot_hack == 0:
            self.draw_enemy_info_box(state)
        elif self.slot_hack > 0:
            self.draw_enemy_info_box_debuff(state)


        if self.hide_numbers:
            self.draw_mask_box(state)

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
            if Magic.SLOTS_HACK.value not in state.player.magicinventory:
                self.magic_lock = True
                self.welcome_screen_choices[1] = "Locked"

            # if self.slot_hack > 0:
            #     self.magic_lock = True
            #     self.welcome_screen_choices[1] = "Locked"

            if self.lock_down == 0 and Magic.SLOTS_HACK.value in state.player.magicinventory:
                self.welcome_screen_choices[1] = "Magic"

            if self.slot_hack > 0:
                self.magic_lock = True

                self.welcome_screen_choices[1] = "Locked"

            if Magic.SLOTS_HACK.value not in state.player.magicinventory:
                self.welcome_screen_choices[1] = "Locked"

            if self.secret_item == True:
                self.welcome_screen_choices[2] = "Locked"


            if self.lock_down > 0:

                self.welcome_screen_choices[3] = "Locked"

            if self.lock_down == 0:
                self.welcome_screen_choices[3] = "Quit"

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

        elif self.game_state == "level_up_screen":
            self.draw_level_up(state)




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
            if Magic.SLOTS_HACK.value in state.player.magicinventory and Magic.SLOTS_HACK.value not in self.magic_screen_choices:
                # Insert Magic.SLOTS_HACK as the new 0th element and shift other elements up
                self.magic_screen_choices.insert(0, Magic.SLOTS_HACK.value)

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

        elif self.game_state == "spin_screen":
            self.battle_messages["spin_message"].draw(state)

        elif self.game_state == "results_screen":
            self.battle_messages["results_message"].draw(state)

        pygame.display.flip()

    def draw_grid_box(self, state: "GameState") -> None:
        screen_width, screen_height = state.DISPLAY.get_size()
        box_size = 50
        line_thickness = 2
        start_x1 = (screen_width - box_size * 3 - line_thickness * 2) // 2  # Adjust for three columns
        start_y = (screen_height - box_size) // 2
        black_color = (0, 0, 0)
        white_color = (255, 255, 255)

        font = pygame.font.Font(None, 36)

        # Draw first column
        for i, pos in enumerate(self.slot_positions1):
            box_x = start_x1
            box_y = start_y + pos
            pygame.draw.rect(state.DISPLAY, black_color, (box_x, box_y, box_size, box_size))
            number_text = font.render(str(self.slot1[i]), True, white_color)
            text_rect = number_text.get_rect(center=(box_x + box_size // 2, box_y + box_size // 2))
            state.DISPLAY.blit(number_text, text_rect)

        # Draw second column
        for i, pos in enumerate(self.slot_positions2):
            box_x = start_x1 + box_size + line_thickness
            box_y = start_y + pos
            pygame.draw.rect(state.DISPLAY, black_color, (box_x, box_y, box_size, box_size))
            number_text = font.render(str(self.slot2[i]), True, white_color)
            text_rect = number_text.get_rect(center=(box_x + box_size // 2, box_y + box_size // 2))
            state.DISPLAY.blit(number_text, text_rect)

        # Draw third column
        for i, pos in enumerate(self.slot_positions3):
            box_x = start_x1 + (box_size + line_thickness) * 2
            box_y = start_y + pos
            pygame.draw.rect(state.DISPLAY, black_color, (box_x, box_y, box_size, box_size))
            number_text = font.render(str(self.slot3[i]), True, white_color)
            text_rect = number_text.get_rect(center=(box_x + box_size // 2, box_y + box_size // 2))
            state.DISPLAY.blit(number_text, text_rect)

        # Draw the white lines
        for start_x in [start_x1, start_x1 + box_size + line_thickness, start_x1 + (box_size + line_thickness) * 2]:
            y = start_y - line_thickness // 2
            pygame.draw.line(state.DISPLAY, white_color, (start_x, y), (start_x + box_size, y), line_thickness)
            y = start_y + box_size + line_thickness // 2
            pygame.draw.line(state.DISPLAY, white_color, (start_x, y), (start_x + box_size, y), line_thickness)
            x = start_x - line_thickness // 2
            pygame.draw.line(state.DISPLAY, white_color, (x, start_y), (x, start_y + box_size), line_thickness)
            x = start_x + box_size + line_thickness // 2
            pygame.draw.line(state.DISPLAY, white_color, (x, start_y), (x, start_y + box_size), line_thickness)

    def draw_mask_box(self, state: "GameState") -> None:
        screen_width, screen_height = state.DISPLAY.get_size()
        box_size = 50
        line_thickness = 2
        total_grid_width = box_size * 3 + line_thickness * 2
        start_x = (screen_width - total_grid_width) // 2
        start_y = (screen_height - box_size) // 2

        mask_box_top = pygame.Surface((total_grid_width, start_y))
        mask_box_bottom = pygame.Surface((total_grid_width, screen_height - (start_y + box_size)))
        mask_box_top.fill((0, 0, 51))
        mask_box_bottom.fill((0, 0, 51))

        state.DISPLAY.blit(mask_box_top, (start_x, 0))
        state.DISPLAY.blit(mask_box_bottom, (start_x, start_y + box_size + line_thickness))

    def draw_bottom_black_box(self, state: "GameState") -> None:
        black_box_height = 130
        black_box_width = 700
        border_width = 5

        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill((0, 0, 0))

        white_border = pygame.Surface((black_box_width + 2 * border_width, black_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))

        screen_width, screen_height = state.DISPLAY.get_size()
        black_box_x = (screen_width - black_box_width) // 2 - border_width
        black_box_y = screen_height - black_box_height - 20 - border_width

        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

    def reset(self):
        self.lock_down = 0
        self.lucky_strike = 0
        self.magic_lock = False
        self.slot_hack = 0
        self.game_state: str = "welcome_screen"
        self.bet: int = 50
        self.welcome_screen_index = 0

    # def test(self) -> None:
    #     match_counts = {i: 0 for i in range(10)}
    #     no_match_count = 0
    #
    #     for _ in range(10000):
    #         self.generate_numbers()
    #         if self.slot1[0] == self.slot2[0] == self.slot3[0]:
    #             match_counts[self.slot1[0]] += 1
    #         else:
    #             no_match_count += 1
    #
    #     for number in range(10):
    #         print(f"Matches for number {number}: {match_counts[number]} times")
    #     print(f"No matches: {no_match_count} times")
    #
    # def map_to_slot_number(self, value: int) -> int:
    #     slot_mapping = {
    #         range(1, 7): 0,  # lose a rib
    #         range(7, 15): 1,  # lost 50 extra coins from your state.player.money
    #         range(15, 21): 2,  # unlucky spin cannot exit out of game + 10% to lose a rib -rib lock status
    #         range(21, 45): 3,  # add 100 coins
    #         range(45, 57): 4,  # gain 10 hp 10 mp 100 coins
    #         range(57, 72): 5,  # gain 20 hp 20 mp 125 coins
    #         range(72, 80): 6,  # add 200 coins
    #         range(80, 87): 7,  # lucky spin better % for jackpot
    #         range(87, 95): 8,  # get special item or 50 coins
    #         range(95, 101): 9,  # jackpot
    #     }
    #     for key in slot_mapping:
    #         if value in key:
    #             return slot_mapping[key]
    #     return 0  # Default value in case something goes wrong
