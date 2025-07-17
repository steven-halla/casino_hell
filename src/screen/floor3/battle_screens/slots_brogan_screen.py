import random
from typing import Dict, Tuple, List, Optional

import pygame

from constants import WHITE, BLACK, RED
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic

# spell: rib lock on : roll 6 times, take 25 damage per successful hit
# i still need to make a new speical item

class SlotsBroganScreen(GambleScreen):
    def __init__(self, screenName: str = "Slots") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.slots: List[str] = []  # Initialize slots as an empty list
        self.dealer_name: str = "Brogan"
        self.slot_images_sprite_sheet: pygame.Surface = pygame.image.load("./assets/images/slots_images_trans.png")
        self.spell_sound: pygame.mixer.Sound = pygame.mixer.Sound("./assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.magic_screen_choices: list[str] = []
        self.hack_cost:int = 75
        self.money: int = 1000
        self.slot_hack_active: int = 5
        self.slot_hack_inactive: int = 0
        self.slot_hack_debuff: int = 0
        self.exp_gain_low:int = 10
        self.exp_gain_no_match: int = 5
        self.bet = 100
        self.exp_gain_high: int = 50
        self.increased_double_pluck_chance: int = 0


        self.bet_screen_choices: list[str] = ["Back"]
        self.spin_screen_index: int = 0
        self.magic_screen_index: int = 1
        self.bet_screen_index: int = 2
        self.quit_index: int = 3
        self.magic_index = 0
        pygame.mixer.music.stop()
        self.magic_lock: bool = False
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        self.juragan_bankrupt: int = 0
        self.player_stamina_low_cost: int = 12
        self.player_stamina_high_cost: int = 50  # useing higher bet option
        self.player_stamina_med_cost: int = 25
        self.lock_down_inactive: int = 0
        self.index_stepper:int = 1
        self.spin_results_generated:bool = False  # Initialize the flag
        self.slot_3_magnet:bool = False
        self.slot_2_magnet:bool = False
        self.no_match: bool = False
        self.player_coin_high_drain:int = 300
        self.player_coin_low_drain:int = 150
        self.player_coin_med_drain:int = 75
        self.rib_stalker: int = 0
        self.jack_pot:int = 0
        self.lucky_strike:int = 0
        self.secret_item_found:bool = False
        self.debuff_increased_pay_to_play: int = 0
        self.brogan_mp: int = 3
        self.debuff_double_pluck: int = 0
        self.brogan_mp: int = 3
        self.spirit_bonus: int = 0
        self.magic_bonus: int = 0

        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "Brogan: Kee kee kee, you have some tasty looking ribs."
            ]),

            self.BET_MESSAGE: MessageBox([
                "Increase your bet by +50, increase chance for item! Dont' forget to rest to 100 if you get a lucky strike."
            ]),
            self.MAGIC_MENU_HACK_DESCRIPTION: MessageBox([
                "Attach a string to a coin."
            ]),

            self.MAGIC_MENU_BACK_DESCRIPTION: MessageBox([
                "go back to previous menu"
            ]),

            self.PLAYER_WIN_MESSAGE: MessageBox([
                "You won the toss!!!"
            ]),
            self.PLAYER_LOSE_MESSAGE: MessageBox([
                "You lost the toss."
            ]),
            self.PLAYER_DRAW_MESSAGE: MessageBox([
                f"You didn't match 3 in a row."
            ]),
            self.BROGAN_CASTING_SPELL_MESSAGE: MessageBox([
                "single strand of life, sever and cut yourself short...double pluck”"
            ]),
        }

        self.slot_images: Dict[str, pygame.Surface] = {
            "bomb": self.slot_images_sprite_sheet.subsurface(pygame.Rect(450, 100, 50, 52)),
            "lucky_seven": self.slot_images_sprite_sheet.subsurface(pygame.Rect(300, 30, 60, 52)),
            "dice": self.slot_images_sprite_sheet.subsurface(pygame.Rect(350, 100, 50, 52)),
            "coin": self.slot_images_sprite_sheet.subsurface(pygame.Rect(95, 160, 58, 50)),
            "diamond": self.slot_images_sprite_sheet.subsurface(pygame.Rect(30, 170, 75, 52)),
            "crown": self.slot_images_sprite_sheet.subsurface(pygame.Rect(25, 280, 80, 52)),
            "chest": self.slot_images_sprite_sheet.subsurface(pygame.Rect(300, 280, 75, 52)),
            "cherry": self.slot_images_sprite_sheet.subsurface(pygame.Rect(120, 215, 75, 52)),
            "dice_six": self.slot_images_sprite_sheet.subsurface(pygame.Rect(400, 215, 50, 52)),
            "spin": self.slot_images_sprite_sheet.subsurface(pygame.Rect(40, 110, 52, 52)),
        }

        self.slot_image_keys: List[str] = list(self.slot_images.keys())
        self.slot_positions1: List[int] = [-50, 0, 50]
        self.slot_positions2: List[int] = [-50, 0, 50]
        self.slot_positions3: List[int] = [-50, 0, 50]
        self.slot1: List[int] = [0, 0, 0]
        self.slot2: List[int] = [0, 0, 0]
        self.slot3: List[int] = [0, 0, 0]
        self.grid_positions: List[Tuple[int, int]] = []
        self.reel_surfaces: List[pygame.Surface] = []
        self.reel_symbol_names: List[List[str]] = []

        for _ in range(3):
            reel_surface, symbol_names = self.create_reel_surface()
            self.reel_surfaces.append(reel_surface)
            self.reel_symbol_names.append(symbol_names)

        self.reel_positions: List[float] = [0.0, 0.0, 0.0]
        self.spinning: bool = False
        self.initial_spin_speed: float = 400.0
        self.spin_start_time: Optional[int] = None
        self.last_update_time: int = pygame.time.get_ticks()
        self.reel_spinning: List[bool] = [False, False, False]
        self.reel_stop_times: List[Optional[int]] = [None, None, None]
        self.spin_speed: float = 400.0


    SPIN_SCREEN: str = "spin_screen"
    BROGAN_CASTING_SPELL_SCREEN: str = "brogan casting spell screen"
    RESULT_SCREEN: str = "result_screen"
    BACK: str = "Back"
    PLAYER_WIN_MESSAGE: str = "player_win_message"
    CHOOSE_SIDE_MESSAGE: str = "choose_side_message"
    PLAYER_LOSE_MESSAGE: str = "player_lose_message"
    PLAYER_DRAW_MESSAGE: str = "player_draw_message"
    COIN_FLIP_MESSAGE: str = "coin_flip_message"
    MAGIC_MENU_HACK_DESCRIPTION: str = "magic_menu_hack_description"
    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    BET_MESSAGE: str = "bet_message"
    PLAYER_WIN_ACTION_MESSAGE: str = "player_win_action_message"
    ENEMY_WIN_ACTION_MESSAGE: str = "enemy_win_action_message"
    PLAYER_ENEMY_DRAW_ACTION_MESSAGE: str = "player_enemy_draw_action_message"
    BROGAN_CASTING_SPELL_MESSAGE: str = "brogan casting spell message"


    def start(self, state: 'GameState'):
        if Events.SLOTS_LEVEL_3_SECRET_ITEM_ACQUIRED.value in state.player.level_three_npc_state:
            self.secret_item_found = True

        self.spirit_bonus = state.player.spirit * 10
        self.magic_bonus = state.player.mind * 10


    def reset_juragan_slots_game(self):
        self.slot_hack_debuff = 0
        self.rib_stalker = 0
        self.lucky_strike = 0
        self.debuff_increased_pay_to_play = 0
        self.debuff_double_pluck = 0

    def reset_slots_juragan_round(self):
        if self.rib_stalker > 0:
            self.rib_stalker -= 1
        if self.lucky_strike > 0:
            self.lucky_strike -= 1
        if self.debuff_increased_pay_to_play > 0:
            self.debuff_increased_pay_to_play -= 1
        if self.debuff_double_pluck > 0:
            self.debuff_double_pluck -= 1
        if self.debuff_double_pluck > 0:
            self.debuff_double_pluck -= 1
        self.increased_double_pluck_chance += 3
        increased_coin_randomizer = random.randint(1, 100) + self.increased_double_pluck_chance

        if increased_coin_randomizer > 90 and self.brogan_mp > 0:
            self.current_screen = self.BROGAN_CASTING_SPELL_SCREEN
            self.increased_double_pluck_chance = 0

    def update(self, state):
        super().update(state)
        controller = state.controller
        controller.update()
        state.player.update(state)

        if self.money <= self.juragan_bankrupt:
            state.currentScreen = state.area4RestScreen
            state.area4RestScreen.start(state)
            Events.add_level_four_event_to_player(state.player, Events.SLOTS_BROGAN_DEFEATED)

        if self.game_state == self.WELCOME_SCREEN:
            self.spin_results_generated = False
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
            self.battle_messages[self.BET_MESSAGE].reset()
            self.update_welcome_screen_helper(state)
        elif self.game_state == self.BROGAN_CASTING_SPELL_SCREEN:
            self.update_casting_spell_helper(state)
        elif self.game_state == self.BROGAN_CASTING_SPELL_SCREEN:
            self.update_brogan_casting_spell_helper(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu_helper(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].update(state)
            self.update_bet_screen_helper(controller)
        elif self.game_state == self.SPIN_SCREEN:
            self.update_spin_reels_helper(controller, state)
        elif self.game_state == self.RESULT_SCREEN:
            self.update_result_helper(controller, state)
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.game_over_screen_level_4(controller, state)

    def draw(self, state):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)
        self.draw_box_info(state)
        self.draw_grid_box(state)

        if self.game_state == self.WELCOME_SCREEN:
            self.battle_messages[self.WELCOME_MESSAGE].draw(state)
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)
        elif self.game_state == self.BROGAN_CASTING_SPELL_SCREEN:
            self.battle_messages[self.BURBADAN_CASTING_SPELL_MESSAGE].draw(state)
        elif self.game_state == self.BROGAN_CASTING_SPELL_SCREEN:
            self.battle_messages[self.BROGAN_CASTING_SPELL_MESSAGE].draw(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box_slots(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].draw(state)
        elif self.game_state == self.SPIN_SCREEN:
            pass
        elif self.game_state == self.RESULT_SCREEN:
            self.battle_messages[self.PLAYER_WIN_MESSAGE].draw(state)
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.draw_game_over(state)
        pygame.display.flip()


    def update_casting_spell_helper(self, state):
        self.battle_messages[self.BURBADAN_CASTING_SPELL_MESSAGE].update(state)
        if state.controller.confirm_button:
            self.debuff_increased_pay_to_play = 5
            self.brogan_mp -= 1
            self.game_state = self.WELCOME_SCREEN

    def update_brogan_casting_spell_helper(self, state):
        self.battle_messages[self.BROGAN_CASTING_SPELL_MESSAGE].update(state)
        if state.controller.confirm_button:
            self.debuff_double_pluck = 5
            self.brogan_mp -= 1
            self.spell_sound.play()
            self.game_state = self.WELCOME_SCREEN



    def update_magic_menu_helper(self, state):
        if self.magic_screen_choices[self.magic_index] == Magic.SLOTS_HACK.value:
            self.battle_messages[self.MAGIC_MENU_HACK_DESCRIPTION].update(state)
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()
        elif self.magic_screen_choices[self.magic_index] == self.BACK:
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)
            self.battle_messages[self.MAGIC_MENU_HACK_DESCRIPTION].reset()

        controller = state.controller

        if controller.up_button:
            self.menu_movement_sound.play()
            self.magic_index = (self.magic_index - self.index_stepper) % len(self.magic_screen_choices)
        elif controller.down_button:
            self.menu_movement_sound.play()
            self.magic_index = (self.magic_index + self.index_stepper) % len(self.magic_screen_choices)

        if controller.confirm_button:
            if self.magic_screen_choices[self.magic_index] == Magic.SLOTS_HACK.value and state.player.focus_points >= self.hack_cost:
                state.player.focus_points -= self.hack_cost
                self.slot_hack_debuff = 5
                self.spell_sound.play()
                self.magic_lock = True
                self.magic_index = 0
                self.game_state = self.WELCOME_SCREEN
            if self.magic_screen_choices[self.magic_index] == Magic.SLOTS_HACK.value and state.player.focus_points < self.hack_cost:
                print("Nope")
            elif self.magic_screen_choices[self.magic_screen_index] == self.BACK:
                self.magic_index = 0
                self.game_state = self.WELCOME_SCREEN
    def update_result_helper(self, controller, state):
        self.jack_pot = 0

        if self.slots == ["bomb", "bomb", "bomb"]:
            self.battle_messages[self.PLAYER_WIN_MESSAGE].update(state)

            if Events.SLOTS_VEST_FOUND.value not in state.player.quest_items:
                if controller.isTPressed or controller.isAPressedSwitch:
                    controller.isTPressed = False
                    controller.isAPressedSwitch = False
                    if self.debuff_increased_pay_to_play > 0 or self.debuff_double_pluck > 0:
                        state.player.stamina_points -= self.player_stamina_high_cost
                        state.player.stamina_points -= self.player_stamina_high_cost
                        state.player.money -= self.player_coin_high_drain
                        state.player.money -= self.player_coin_high_drain
                        state.player.exp += self.exp_gain_high
                        self.game_state = self.WELCOME_SCREEN
                        self.reset_slots_juragan_round()

                    else:
                        state.player.stamina_points -= self.player_stamina_high_cost
                        state.player.money -= self.player_coin_high_drain
                        state.player.exp += self.exp_gain_high
                        self.game_state = self.WELCOME_SCREEN
                        self.reset_slots_juragan_round()

                self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"double rib plucked! You lose {self.player_stamina_high_cost} HP and {self.player_coin_high_drain} money.Gain {self.exp_gain_high} exp"]
            elif Events.SLOTS_VEST_FOUND.value in state.player.quest_items:
                if controller.confirm_button:
                    if self.debuff_increased_pay_to_play > 0 or self.debuff_double_pluck > 0:
                        state.player.stamina_points -= self.player_stamina_low_cost
                        state.player.stamina_points -= self.player_stamina_low_cost
                        state.player.money -= self.player_coin_high_drain
                        state.player.money -= self.player_coin_high_drain
                        state.player.exp += self.exp_gain_high
                        self.game_state = self.WELCOME_SCREEN
                        self.reset_slots_juragan_round()

                    else:
                        state.player.stamina_points -= self.player_stamina_low_cost
                        state.player.money -= self.player_coin_high_drain
                        state.player.exp += self.exp_gain_high
                        self.game_state = self.WELCOME_SCREEN
                        self.reset_slots_juragan_round()

                self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"rib plucked! You lose {self.player_stamina_med_cost} HP and {self.player_coin_high_drain} money. Gain {self.exp_gain_high} exp"]

        elif self.slots == ["dice", "dice", "dice"]:
            if controller.confirm_button:
                state.player.stamina_points -= self.player_stamina_low_cost
                state.player.money -= self.player_coin_low_drain
                state.player.exp += self.exp_gain_low
                self.game_state = self.WELCOME_SCREEN
                self.reset_slots_juragan_round()

            self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"rib plucked! You lose {self.player_stamina_low_cost} HP and {self.player_coin_low_drain} money. gain {self.exp_gain_low} exp"]

        elif self.slots == ["coin", "coin", "coin"]:
            if controller.confirm_button:
                state.player.stamina_points -= self.player_stamina_low_cost
                state.player.money -= self.player_coin_med_drain
                self.rib_stalker = 5
                state.player.exp += self.exp_gain_low
                self.reset_slots_juragan_round()
                if self.brogan_mp > 0 and self.debuff_increased_pay_to_play == 0:
                    self.game_state = self.BROGAN_CASTING_SPELL_SCREEN
                elif self.brogan_mp > 0 and self.debuff_double_pluck == 0:
                    self.game_state = self.BROGAN_CASTING_SPELL_SCREEN
                else:
                    self.game_state = self.WELCOME_SCREEN

            self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"rib plucked! You lose {self.player_stamina_low_cost} HP and {self.player_coin_med_drain} money. You are cursed and Locked down. Gain {self.exp_gain_low} exp"]
            if self.battle_messages[self.PLAYER_WIN_MESSAGE].current_message_finished() and controller.confirm_button:
                self.game_state = self.WELCOME_SCREEN

        elif self.slots == ["cherry", "cherry", "cherry"]:
            self.jack_pot = 50
            if controller.confirm_button:
                state.player.money += self.jack_pot
                state.player.exp += self.exp_gain_low
                self.reset_slots_juragan_round()
                self.game_state = self.WELCOME_SCREEN
            self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"You win {self.jack_pot} coins. Gain {self.exp_gain_low} exp"]

        elif self.slots == ["spin", "spin", "spin"]:
            self.jack_pot = 100

            if controller.confirm_button:
                state.player.money += self.jack_pot
                state.player.exp += self.exp_gain_low
                self.reset_slots_juragan_round()
                self.game_state = self.WELCOME_SCREEN
            self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"You win {self.jack_pot} coins. Gain {self.exp_gain_low} exp"]

        elif self.slots == ["crown", "crown", "crown"]:
            self.jack_pot = 150
            if controller.confirm_button:
                state.player.money += self.jack_pot
                state.player.exp += self.exp_gain_low
                self.reset_slots_juragan_round()
                self.game_state = self.WELCOME_SCREEN
            self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"You win {self.jack_pot} coins. Gain {self.exp_gain_low} exp"]
        elif self.slots == ["dice_six", "dice_six", "dice_six"]:
            if controller.isTPressed or controller.isAPressedSwitch:
                controller.isTPressed = False
                controller.isAPressedSwitch = False
                self.lucky_strike += 6
                state.player.exp += self.exp_gain_low
                self.reset_slots_juragan_round()
                self.game_state = self.WELCOME_SCREEN

            self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"Lucky Strike activated, time to get that money! Gain {self.exp_gain_low} exp"]

        elif self.slots == ["diamond", "diamond", "diamond"]:
            self.jack_pot = 250
            if controller.confirm_button:
                state.player.money += self.jack_pot
                state.player.exp += self.exp_gain_low
                self.reset_slots_juragan_round()
                self.game_state = self.WELCOME_SCREEN
            self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"You win {self.jack_pot} coins. Gain {self.exp_gain_low} exp"]

        elif self.slots == ["chest", "chest", "chest"]:
            self.jack_pot = 200
            if self.secret_item_found == True:
                if controller.confirm_button:
                    state.player.money += self.jack_pot
                    state.player.exp += self.exp_gain_low
                    self.reset_slots_juragan_round()
                    self.game_state = self.WELCOME_SCREEN
                self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"You win {self.jack_pot} coins. You already got the item. Gain {self.exp_gain_low} exp"]

            elif self.secret_item_found == False:
                if controller.confirm_button:
                    state.player.exp += self.exp_gain_high
                    Events.add_level_four_event_to_player(state.player, Events.SLOTS_LEVEL_3_SECRET_ITEM_ACQUIRED)
                    self.secret_item_found = True
                    self.reset_slots_juragan_round()
                    self.game_state = self.WELCOME_SCREEN
                self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"You acquired the super secret item. Gain {self.exp_gain_high} exp"]

        elif self.slots == ["lucky_seven", "lucky_seven", "lucky_seven"]:
            self.jack_pot = 500

            if controller.confirm_button:
                if Equipment.SLOTS_SHOES.value in state.player.equipped_items and self.debuff_increased_pay_to_play == 0:
                    state.player.stamina_points += 100
                    state.player.focus_points += 50

                state.player.money += self.jack_pot
                state.player.exp += self.exp_gain_high
                self.reset_slots_juragan_round()
                self.game_state = self.WELCOME_SCREEN
            self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"You got the jack pot, you win {self.jack_pot} coins. Gain {self.exp_gain_high} exp"]

        elif self.slots[0] != self.slots[1] or self.slots[0] != self.slots[2]:
            if controller.confirm_button:
                state.player.exp += self.exp_gain_no_match
                self.reset_slots_juragan_round()
                self.game_state = self.WELCOME_SCREEN
            self.battle_messages[self.PLAYER_WIN_MESSAGE].messages = [f"No matches.  Gain {self.exp_gain_no_match} exp"]
        self.battle_messages[self.PLAYER_WIN_MESSAGE].update(state)

    def update_welcome_screen_helper(self, state: "GameState") -> None:
        controller = state.controller
        controller.update()
        if state.controller.confirm_button:
            if self.welcome_screen_index == self.welcome_screen_play_index:
                self.game_state = self.SPIN_SCREEN
                if self.slot_hack_debuff == self.slot_hack_inactive:
                    state.player.stamina_points -= self.player_stamina_med_cost
                    state.player.money -= self.bet
                elif self.slot_hack_debuff > self.slot_hack_inactive:
                    state.player.stamina_points -= self.player_stamina_med_cost
                    if self.bet > 100:
                        state.player.money -= 50

            elif self.welcome_screen_index == self.welcome_screen_magic_index and self.magic_lock == False:
                self.game_state = self.MAGIC_MENU_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_bet_index:
                self.game_state = self.BET_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_quit_index and self.rib_stalker == 0:
                state.currentScreen = state.area4RestScreen
                state.area4RestScreen.start(state)

    def update_spin_reels_helper(self, controller, state):
        # Get current time once at the beginning
        current_time = pygame.time.get_ticks()

        # Only start spinning if reels aren't spinning and results haven't been generated
        if not any(self.reel_spinning) and not self.spin_results_generated:
            # Generate the spin results before starting the spin
            self.slots = self.generate_numbers(state)  # Generate symbols

            # Calculate target positions for each reel based on the generated symbols
            self.calculate_target_positions(self.slots)

            # Start spinning all reels
            self.reel_spinning = [True, True, True]
            self.spin_start_time = current_time  # Record the time when spinning started
            self.last_update_time = current_time  # Reset last update time

            # Set stop times for each reel
            self.reel_stop_times = [
                current_time + 3000,  # Reel 0 stops after 3 seconds
                current_time + 4000,  # Reel 1 stops after 4 seconds
                current_time + 5000  # Reel 2 stops after 5 seconds
            ]

        # Calculate delta_time before updating self.last_update_time
        delta_time = (current_time - self.last_update_time) / 1000.0  # Convert milliseconds to seconds
        self.last_update_time = current_time  # Update after calculating delta_time

        # Update reel positions and check for stopping
        for i in range(3):  # For each reel
            if self.reel_spinning[i]:
                # Update the reel's position
                self.reel_positions[i] = (self.reel_positions[i] - self.spin_speed * delta_time) % self.reel_surfaces[i].get_height()

                # Check if it's time to stop this reel
                if current_time >= self.reel_stop_times[i]:
                    # Stop the reel at the target position
                    self.reel_spinning[i] = False
                    self.reel_positions[i] = self.target_positions[i]

        # Update overall spinning state
        self.spinning = any(self.reel_spinning)

        # Check if all reels have stopped
        if not any(self.reel_spinning) and not self.spin_results_generated:
            # All reels have stopped, proceed with any outcome logic
            self.spin_results_generated = True  # Set the flag to prevent re-running this block

        # Prevent another spin from being triggered automatically
        if not any(self.reel_spinning):
            self.spinning = False  # Reels have stopped, no new spin will start
            self.game_state = self.RESULT_SCREEN

    def update_bet_screen_helper(self, controller):
        print(self.bet)
        if controller.isBPressed or controller.isBPressedSwitch:
            controller.isBPressed = False
            controller.isBPressedSwitch = False
            self.game_state = self.WELCOME_SCREEN

        if self.debuff_increased_pay_to_play == 0:
            min_bet = 100
            bet_step = 50
            max_bet = 150
        elif self.debuff_increased_pay_to_play > 0:
            min_bet = 200
            bet_step = 100
            max_bet = 300


        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet += bet_step
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False

            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet -= bet_step

        if self.bet <= min_bet:
            self.bet = min_bet
        elif self.bet >= max_bet:
            self.bet = max_bet

    def update_welcome_screen_logic(self, controller):
        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            if self.welcome_screen_index == self.spin_screen_index:
                self.game_state = self.SPIN_SCREEN
            elif self.welcome_screen_index == self.magic_screen_index and self.magic_lock == False:
                self.game_state = self.MAGIC_MENU_SCREEN
            elif self.welcome_screen_index == self.bet_screen_index:
                self.game_state = self.BET_SCREEN
            elif self.welcome_screen_index == self.quit_index:
                print("this will come later")

    def game_over_screen_level_4(self, controller, state):
        no_money_game_over = 0
        no_stamina_game_over = 0
        if state.player.money <= no_money_game_over:
            if controller.confirm_button:
                state.currentScreen = state.gameOverScreen
                state.gameOverScreen.start(state)
        elif state.player.stamina_points <= no_stamina_game_over:
            if controller.confirm_button:
                state.player.money -= 100
                self.reset_juragan_slots_game()
                state.currentScreen = state.area4RestScreen
                state.area4RestScreen.start(state)


    def draw_grid_box(self, state: "GameState") -> None:
        screen_width, screen_height = state.DISPLAY.get_size()
        box_width, box_height = 80, 80
        line_thickness = 2
        grid_columns = 3
        total_grid_width = box_width * grid_columns + line_thickness * (grid_columns - 1)

        start_x = (screen_width - total_grid_width) // 2
        start_y = (screen_height - box_height) // 2

        for i in range(3):  # For each reel
            reel_surface = self.reel_surfaces[i]
            reel_height = reel_surface.get_height()

            reel_y_pos = self.reel_positions[i] % reel_height
            rect = pygame.Rect(0, reel_y_pos, box_width, box_height)

            if reel_y_pos + box_height > reel_height:
                upper_part_height = reel_height - reel_y_pos
                lower_part_height = box_height - upper_part_height

                upper_part = reel_surface.subsurface(pygame.Rect(0, reel_y_pos, box_width, upper_part_height))
                lower_part = reel_surface.subsurface(pygame.Rect(0, 0, box_width, lower_part_height))

                combined_surface = pygame.Surface((box_width, box_height)).convert_alpha()
                combined_surface.blit(upper_part, (0, 0))
                combined_surface.blit(lower_part, (0, upper_part_height))
            else:
                combined_surface = reel_surface.subsurface(rect)

            box_x = start_x + i * (box_width + line_thickness)
            box_y = start_y

            state.DISPLAY.blit(combined_surface, (box_x, box_y))

            pygame.draw.rect(state.DISPLAY, WHITE, (box_x, box_y , box_width, box_height), line_thickness)

    def draw_magic_menu_selection_box(self, state):
        if self.magic_screen_choices[self.magic_screen_index] == Magic.SLOTS_HACK.value:
            # self.battle_messages[self.MAGIC_MENU_SHIELD_DESCRIPTION].draw(state)
            pass

        elif self.magic_screen_choices[self.magic_screen_index] == self.BACK:
            pass
            # self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)

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

        for idx, choice in enumerate(self.magic_screen_choices):
            y_position = start_y_right_box + idx * choice_spacing  # Use the defined spacing variable
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        # Draw the arrow at the current magic screen index position
        arrow_y_position = start_y_right_box + (self.magic_index * choice_spacing) + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_position)  # Use the arrow offsets
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

        if Magic.SLOTS_HACK.value not in state.player.magicinventory:
            self.magic_lock = True
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif Magic.SLOTS_HACK.value in state.player.magicinventory:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if Magic.SLOTS_HACK.value in state.player.magicinventory and Magic.SLOTS_HACK.value not in self.magic_screen_choices:
            self.magic_screen_choices.append(Magic.SLOTS_HACK.value)


        if self.BACK not in self.magic_screen_choices:
            self.magic_screen_choices.append(self.BACK)

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

    def draw_slot_images(self, state):
        sprite_data = {
            "bomb": ((10, 20), (450, 100, 50, 52)),
            "lucky_seven": ((100, 20), (300, 30, 60, 60)),
            "dice": ((181, 20), (350, 100, 50, 52)),
            "coin": ((240, 20), (20, 30, 75, 52)),
            "diamond": ((320, 20), (20, 170, 75, 52)),
            "crown": ((400, 20), (15, 275, 80, 52)),
            "chest": ((500, 20), (300, 275, 75, 58)),
            "cherry": ((20, 80), (120, 210, 75, 58)),
            "dice_6": ((120, 80), (400, 210, 50, 58)),
            "spin": ((200, 80), (40, 110, 52, 58)),
        }

        # Loop through the dictionary and blit each sprite
        for name, (blit_coords, sprite_rect) in sprite_data.items():
            sprite = self.slot_images_sprite_sheet.subsurface(pygame.Rect(*sprite_rect))
            state.DISPLAY.blit(sprite, blit_coords)

    def update_reels(self):
        for i in range(3):
            self.reel_positions[i] = (self.reel_positions[i] + 1) % len(self.slot_image_keys)

    def adjust_reels_to_results(self, slots: List[str]):
        symbol_height = 70  # Height of each symbol image
        for i in range(3):  # For each reel
            symbol_name = slots[i]
            # Find the index of the symbol on the reel
            if symbol_name in self.reel_symbol_names[i]:
                symbol_index = self.reel_symbol_names[i].index(symbol_name)
                # Calculate the reel position to align the symbol in the display
                self.reel_positions[i] = (symbol_index * symbol_height) % self.reel_surfaces[i].get_height()
                # Adjust so the symbol is centered in the display
                self.reel_positions[i] -= (symbol_height / 2 + 90)
                self.reel_positions[i] %= self.reel_surfaces[i].get_height()
            else:
                print(f"Symbol {symbol_name} not found on reel {i + 1}")

    def calculate_target_positions(self, slots: List[str]):
        symbol_height = 80  # Height of each symbol image
        self.target_positions = [0.0, 0.0, 0.0]  # Initialize target positions for each reel
        for i in range(3):  # For each reel
            symbol_name = slots[i]
            # Find the index of the symbol on the reel
            if symbol_name in self.reel_symbol_names[i]:
                symbol_index = self.reel_symbol_names[i].index(symbol_name)
                # Calculate the target position to align the symbol in the display
                target_position = (symbol_index * symbol_height) % self.reel_surfaces[i].get_height()
                # Adjust so the symbol is centered in the display
                target_position -= (symbol_height / 2 - 40)
                target_position %= self.reel_surfaces[i].get_height()
                self.target_positions[i] = target_position
            else:
                print(f"Symbol {symbol_name} not found on reel {i + 1}")
                self.target_positions[i] = 0  # Default to position 0 if symbol not found

    def generate_numbers(self, state) -> List[str]:
        # Generate random values for each slot
        generated_values = [random.randint(1, 100) for _ in range(3)]
        # generated_values = [15, 15, 15]
        # print(f"[TEST] Forced generated values: {generated_values}")





        #default
        slot_mapping = {
            range(1, 7): "bomb",
            range(7, 15): "dice",
            range(15, 27): "coin",
            range(27, 42): "cherry",
            range(42, 54): "spin",
            range(54, 66): "crown",
            range(66, 76): "dice_six",
            range(76, 85): "diamond",
            range(85, 95): "chest",
            range(95, 101): "lucky_seven",
        }

        # double pluck spell effect
        if self.debuff_double_pluck > 0:
            slot_mapping = {
                range(1, 25): "bomb",
                range(25, 40): "dice",
                range(40, 55): "coin",
                range(55, 60): "cherry",
                range(60, 70): "spin",
                range(70, 101): "crown",
            }

        # rib demon stalker
        if self.rib_stalker > 0:
            slot_mapping = {
                range(1, 15): "bomb",
                range(15, 25): "dice",
                range(25, 35): "coin",
                range(27, 42): "cherry",
                range(42, 54): "spin",
                range(54, 101): "crown",
            }
        elif self.lucky_strike > 0:
            slot_mapping = {
                range(1, 30): "cherry",
                range(30, 40): "spin",
                range(40, 50): "crown",
                range(50, 60): "dice_six",
                range(60, 70): "diamond",
                range(70, 80): "chest",
                range(80, 101): "lucky_seven",
            }

        elif self.bet > 199 and self.rib_stalker == 0 and self.lucky_strike == 0 and self.debuff_increased_pay_to_play == 0:
            slot_mapping = {
                range(1, 7): "bomb",
                range(7, 15): "dice",
                range(15, 27): "coin",
                range(27, 37): "cherry",
                range(37, 45): "spin",
                range(45, 55): "crown",
                range(55, 66): "dice_six",
                range(66, 75): "diamond",
                range(75, 95): "chest",
                range(95, 101): "lucky_seven",
            }

        elif self.bet > 299 and self.rib_stalker == 0 and self.lucky_strike == 0 and self.debuff_increased_pay_to_play > 0:
            slot_mapping = {
                range(1, 7): "bomb",
                range(7, 15): "dice",
                range(15, 27): "coin",
                range(27, 37): "cherry",
                range(37, 45): "spin",
                range(45, 55): "crown",
                range(55, 66): "dice_six",
                range(66, 75): "diamond",
                range(75, 95): "chest",
                range(95, 101): "lucky_seven",
            }

        # Define a priority mapping for slot symbols
        symbol_priority = {
            "bomb": 1,
            "dice": 2,
            "coin": 3,
            "cherry": 4,
            "spin": 5,
            "crown": 6,
            "dice_six": 7,
            "diamond": 8,
            "chest": 9,
            "lucky_seven": 10
        }

        print(slot_mapping)
        slots = []
        for value in generated_values:
            for key in slot_mapping:
                if value in key:
                    slots.append(slot_mapping[key])
                    break
            else:
                # Default symbol in case no range matches
                slots.append("bomb")  # Or any default symbol you prefer

        if symbol_priority[slots[0]] == 0 and self.rib_stalker > 0:
            if self.debuff_increased_pay_to_play > 0 or self.debuff_double_pluck > 0:
                spell_modifier = 5
            else:
                spell_modifier = 0

            if random.randint(1, 100) <= (50 + spell_modifier):   # Adjusted chance
                print("Im ribbing active")
                self.slot_2_magnet = True
                slots[1] = slots[0]  # Match slot 2 to slot 1
            else:
                self.slot_2_magnet = False

            if random.randint(1, 100) <= (75 + spell_modifier):
                print("Im ribbing active")
                self.slot_3_magnet = True
                slots[2] = slots[0]  # Match slot 3 to slot 1
            else:
                self.slot_3_magnet = False


        slot_2_luck_bonus = 0

        print(f"Slot results: {slots}")
        if symbol_priority[slots[0]] > 3:  # Use symbol's priority for comparison
            for luck in range(state.player.luck):
                slot_2_luck_bonus += 2

        if random.randint(1, 100) <= 50 + slot_2_luck_bonus:  # Adjusted chance
            print("Im active")
            self.slot_2_magnet = True
            slots[1] = slots[0]  # Match slot 2 to slot 1
        else:
            self.slot_2_magnet = False

        print(f"Slot results: {slots}")

        slot_3_luck_bonus = 0

        if symbol_priority[slots[0]] > 2:  # Same logic for slot 3
            for luck in range(state.player.luck):
                slot_3_luck_bonus += 2

        if random.randint(1, 100) <= 40 + slot_3_luck_bonus:
            print("Im active")
            self.slot_3_magnet = True
            slots[2] = slots[0]  # Match slot 3 to slot 1
        else:
            self.slot_3_magnet = False

        print(f"Slot results: {slots}")

        return slots  # Return the list of symbols

    def create_reel_surface(self) -> Tuple[pygame.Surface, List[str]]:
        # Use the same order of images for all reels
        image_keys = self.slot_image_keys.copy()
        # Optionally shuffle if desired
        # random.shuffle(image_keys)

        # Calculate the total height of the reel surface
        box_width, box_height = 80, 80  # Same as in draw_grid_box
        reel_height = box_height * len(image_keys)

        # Create the reel surface
        reel_surface = pygame.Surface((box_width, reel_height)).convert_alpha()
        reel_surface.fill((0, 0, 0, 0))  # Transparent background

        # Blit each image onto the reel surface
        for idx, key in enumerate(image_keys):
            image = self.slot_images[key]
            resized_image = pygame.transform.scale(image, (box_width, box_height))
            reel_surface.blit(resized_image, (0, idx * box_height))

        return reel_surface, image_keys  # Return the surface and the list of symbols



    def draw_box_info(self, state: 'GameState'):
        player_enemy_box_info_x_position = 37
        enemy_name_y_position = 33
        enemy_money_y_position = 70
        bet_y_position = 370
        player_money_y_position = 250
        hero_name_y_position = 205
        hero_stamina_y_position = 290
        hero_focus_y_position = 330

        if self.lucky_strike > 0:
            state.DISPLAY.blit(self.font.render(f"LuckyStrike: {self.lucky_strike}", True, RED), (player_enemy_box_info_x_position, enemy_name_y_position))
        else:
            state.DISPLAY.blit(self.font.render(self.dealer_name, True, WHITE), (player_enemy_box_info_x_position, enemy_name_y_position))

        if self.slot_hack_debuff > 0:
            state.DISPLAY.blit(self.font.render(f"Hacked: {self.slot_hack_debuff}", True, RED), (player_enemy_box_info_x_position, enemy_name_y_position + 122))
        else:
            state.DISPLAY.blit(self.font.render(f"", True, RED), (player_enemy_box_info_x_position, enemy_name_y_position + 122))

        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}", True, WHITE), (player_enemy_box_info_x_position, enemy_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE), (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE), (player_enemy_box_info_x_position, player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE), (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE), (player_enemy_box_info_x_position, hero_focus_y_position))
        if self.rib_stalker == 0:
            state.DISPLAY.blit(self.font.render(f"{self.HERO_HEADER}", True, WHITE), (player_enemy_box_info_x_position, hero_name_y_position))
        elif self.rib_stalker > 0:
            state.DISPLAY.blit(self.font.render(f"Stalker: {self.rib_stalker}", True, RED), (player_enemy_box_info_x_position, hero_name_y_position))

    def draw_game_over(self, state):
        no_money_game_over = 0
        no_stamina_game_over = 0
        if state.player.money <= no_money_game_over:
            state.DISPLAY.blit(self.font.render(f"You ran out of money and are now a prisoner of hell", True, WHITE), (self.blit_message_x, self.blit_message_y))
        elif state.player.stamina_points <= no_stamina_game_over:
            state.DISPLAY.blit(self.font.render(f"You ran out of stamina , you lose -100 gold", True, WHITE), (self.blit_message_x, self.blit_message_y))

    def draw_magic_menu_selection_box_slots(self, state):
        if self.magic_screen_choices[self.magic_index] == Magic.SLOTS_HACK.value:
            self.battle_messages[self.MAGIC_MENU_HACK_DESCRIPTION].draw(state)
        elif self.magic_screen_choices[self.magic_index] == self.BACK:
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

        for idx, choice in enumerate(self.magic_screen_choices):
            y_position = start_y_right_box + idx * choice_spacing  # Use the defined spacing variable
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        arrow_y_position = start_y_right_box + (self.magic_index * choice_spacing) + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_position)  # Use the arrow offsets
        )
