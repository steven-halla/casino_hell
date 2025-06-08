import pygame
import random
from constants import WHITE, RED, DISPLAY, BLACK
from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic

#There is  a bug on the redraw
class BlackJackMackScreen(GambleScreen):
    def __init__(self, screenName: str = "Black Jack") -> None:
        super().__init__(screenName)
        self.enemy_card_y_positions: list[int] = []
        self.player_card_y_positions: list[int] = []
        self.game_state: str = self.WELCOME_SCREEN
        self.deck: Deck() = Deck()
        self.level_up_message_initialized = False


        self.player_hand: list[str] = []
        self.enemy_hand: list[str] = []
        self.player_score: int = 0
        self.enemy_score: int = 0
        self.ace_detected_time = None
        self.ace_effect_triggered = False
        self.lucky_strike: pygame.mixer.Sound = pygame.mixer.Sound("./assets/music/luckystrike.wav")  # Adjust the path as needed
        self.lucky_strike.set_volume(0.6)
        self.bet: int = 100
        self.money: int = 200
        self.fengus_bankrupt: int = 0
        self.reveal_buff_counter: int = 0
        self.reveal_start_duration: int = 7
        self.reveal_end_not_active: int = 0
        self.magic_lock: bool = False
        self.dealer_name: str = "Mack"
        self.lock_down_inactive: int = 0
        self.initial_hand: int = 2
        self.hedge_hog_time: bool = False
        self.player_action_phase_index: int = 0
        self.player_action_phase_play_index: int = 0
        self.player_action_phase_draw_index: int = 1
        self.player_action_phase_force_redraw_index: int = 2
        self.redraw_counter = True
        self.player_action_phase_choices: list[str] = ["Stand", "Draw"]
        self.magic_screen_choices: list[str] = []
        self.redraw_debuff_counter: int = 0
        self.redraw_end_counter: int = 0
        self.redraw_start_counter: int = 10
        self.reveal_debuff_counter: int = 0
        self.reveal_end_counter: int = 0
        self.reveal_start_counter: int = 5
        self.magic_menu_index: int = 0
        self.magic_menu_reveal_index: int = 0
        self.redraw_magic_menu_index: int = 1
        self.back_magic_menu_index: int = 2
        self.index_stepper: int = 1
        self.spell_sound: pygame.mixer.Sound = pygame.mixer.Sound("./assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.reveal_cast_cost: int = 40
        self.redraw_cast_cost: int = 30
        self.low_exp: int = 10
        self.med_exp: int = 20
        self.high_exp: int = 30
        self.critical_multiplier: int = 2
        self.low_stamina_drain: int = 10
        self.med_stamina_drain: int = 20
        self.high_stamina_drain: int = 30
        self.mack_magic_points: int = 1
        self.debuff_ddraw: int = 0
        self.luck_swapping_switch: int = 0
        self.spirit_bonus: int = 0
        self.magic_bonus: int = 0
        self.luck_bonus: int = 0
        self.player_stamina_drain_low: int = 3
        self.player_stamina_drain_high: int = 5
        self.player_debuff_double_draw: int = 0
        self.double_draw_duration_expired: int = 0
        self.double_draw_turns_inflicted: int = 7
        self.draw_one_card: int = 1


        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "Mack: This is the welcome screen"
            ]),
            self.BET_MESSAGE: MessageBox([
                "Min bet of 50, max of 200. Press up and down keys to increase/decrease bet. Press B to Exit."
            ]),
            self.MAGIC_MENU_REVEAL_DESCRIPTION: MessageBox([
                "You can feel the print of the face down card."
            ]),
            self.MAGIC_MENU_REDRAW_DESCRIPTION: MessageBox([
                "Sir Leopold replaces face up card with a new card, once per turn.."
            ]),
            self.MAGIC_MENU_BACK_DESCRIPTION: MessageBox([
                "go back to previous menu"
            ]),
            self.DRAW_CARD_MESSAGE: MessageBox([
                "drawing your cards now"
            ]),
            self.PLAYER_BLACK_JACK_MESSAGE: MessageBox([
                "You got a black jack you win"
            ]),
            self.ENEMY_BLACK_JACK_MESSAGE: MessageBox([
                "Enemy got a black jack you lose"
            ]),
            self.PLAYER_ENEMY_DRAW_BLACK_JACK_MESSAGE: MessageBox([
                f"It's a DRAW! You win 0 gold and win {self.low_exp} experience points"
            ]),
            self.PLAYER_ACTION_MESSAGE: MessageBox([
                "Time for action"
            ]),
            self.PLAYER_WIN_ACTION_MESSAGE: MessageBox([
                "you win"
            ]),
            self.ENEMY_WIN_ACTION_MESSAGE: MessageBox([
                "you lose"
            ]),
            self.PLAYER_ENEMY_DRAW_ACTION_MESSAGE: MessageBox([
                f"It's a DRAW! You win 0 gold and win {self.low_exp} experience points"
            ]),
            self.LEVEL_UP_SCREEN: MessageBox([
                f"You leveld up!"
            ]),
            self.LEVEL_UP_MESSAGE: MessageBox([
                f"You leveld up!"
            ]),
            self.MACK_CASTING_SPELL: MessageBox([
                f"Walking into a fog of confusion, forget and let your brain soak in the mist. Let your reality shift and increase times 2...double draw "
            ]),
            self.GAME_OVER_SCREEN_ZERO_STAMINA_MESSAGE: MessageBox([
                f"You ran out of Stamina, go rest your Hero."
            ]),
        }

    PLAYER_ACTION_MESSAGE: str = "player_action_message"
    PLAYER_BLACK_JACK_MESSAGE: str = "player_black_jack_message"
    ENEMY_BLACK_JACK_MESSAGE: str = "enemy_black_jack_message"
    PLAYER_ENEMY_DRAW_BLACK_JACK_MESSAGE: str = "player_enemy_draw_jack_message"
    DRAW_CARD_MESSAGE: str = "draw card message"
    MAGIC_MENU_REVEAL_DESCRIPTION: str = "magic_menu_reveal_description"
    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    MAGIC_MENU_REDRAW_DESCRIPTION: str = "magic_menu_redraw_description"
    BET_MESSAGE: str = "bet_message"
    PLAYER_WIN_ACTION_MESSAGE: str = "player_win_action_message"
    ENEMY_WIN_ACTION_MESSAGE: str = "enemy_win_action_message"
    PLAYER_ENEMY_DRAW_ACTION_MESSAGE: str = "player_enemy_draw_action_message"
    LEVEL_UP: str = "level_up_message"
    MACK_CASTING_SPELL: str = "MACK_CASTING_SPELL"
    REVEAL: str = "reveal"
    REDRAW: str = "redraw"
    BACK = "back"
    PLAYER_ACTION_SCREEN: str = "player_action_screen"
    LEVEL_UP_SCREEN = "level_up_screen"
    DRAW_CARD_SCREEN: str = "draw card screen"
    PLAYER_ENEMY_DRAW_BLACK_JACK_SCREEN: str = "player_enemy_draw_jack_screen "
    PLAYER_BLACK_JACK_SCREEN: str = "player_black_jack_screen"
    ENEMY_BLACK_JACK_SCREEN: str = "enemy_black_jack_screen"
    PLAYER_WIN_ACTION_SCREEN: str = "player_win_action_phase"
    ENEMY_WIN_ACTION_SCREEN: str = "enemy_win_action_phase"
    PLAYER_ENEMY_DRAW_ACTION_SCREEN: str = "player_enemy_draw_action_phase"
    MACK_CASTING_SPELL_SCREEN: str = "MACK_CASTING_SPELL_screen"

    def start(self, state: 'GameState'):
        self.reset_black_jack_game()
        self.deck.shuffle()
        self.initialize_music()
        self.spirit_bonus: int = state.player.spirit * 10
        self.magic_bonus: int = state.player.mind * 10
        self.luck_bonus: int = state.player.luck * 5
        self.welcome_screen_index = 0

        if Magic.BLACK_JACK_REDRAW.value in state.player.magicinventory and Magic.BLACK_JACK_REDRAW.value not in self.magic_screen_choices:
            self.magic_screen_choices.append(Magic.BLACK_JACK_REDRAW.value)

        if Magic.REVEAL.value in state.player.magicinventory and Magic.REVEAL.value not in self.magic_screen_choices:
            self.magic_screen_choices.append(Magic.REVEAL.value)

        if self.BACK not in self.magic_screen_choices:
            self.magic_screen_choices.append(self.BACK)

    def round_reset(self):
        print("Round Reset")
        self.deck.shuffle()
        self.player_hand.clear()
        self.enemy_hand.clear()
        if self.reveal_buff_counter > 0:
            self.reveal_buff_counter -= 1
        if self.redraw_debuff_counter > 0:
            self.redraw_debuff_counter -= 1
        if self.reveal_buff_counter == 0 and self.redraw_debuff_counter == 0:
            self.magic_lock = False

        if self.player_debuff_double_draw > 0:
            self.player_debuff_double_draw -= 1



        self.ace_effect_triggered = False
        self.hedge_hog_time: bool = False
        self.redraw_counter = True
        self.player_card_y_positions = []
        self.enemy_card_y_positions = []
        self.player_card_x_positions = []
        self.enemy_card_x_positions = []
        self.luck_swapping_switch += 3


        luck_swap_randomizer = 0

        match self.mack_magic_points:
            case 3:
                luck_swap_randomizer = random.randint(1, 90) + self.luck_swapping_switch
            case 2:
                luck_swap_randomizer = random.randint(1, 70) + self.luck_swapping_switch
            case 1:
                luck_swap_randomizer = random.randint(1, 80) + self.luck_swapping_switch

        print(luck_swap_randomizer)

        if luck_swap_randomizer > 100 and self.mack_magic_points > 0 and self.player_debuff_double_draw == 0:
            self.game_state = self.MACK_CASTING_SPELL_SCREEN
            print("yeah boy ")

            self.luck_swapping_switch = 0



    def reset_black_jack_game(self):
        self.player_card_y_positions = []
        self.enemy_card_y_positions = []
        self.player_card_x_positions = []
        self.enemy_card_x_positions = []
        self.deck.shuffle()
        self.player_hand.clear()
        self.enemy_hand.clear()
        self.reveal_buff_counter = 0
        self.redraw_debuff_counter = 0
        self.player_debuff_double_draw = 0
        self.ace_effect_triggered = False
        self.hedge_hog_time: bool = False
        self.redraw_counter = True

    def update(self, state: 'GameState'):
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)
        # print("YOur redraw counter is set at: " + str(self.redraw_debuff_counter))


        if self.money <= self.fengus_bankrupt:
            state.currentScreen = state.area2GamblingScreen
            state.area2GamblingScreen.start(state)
            Events.add_level_two_event_to_player(state.player, Events.BLACK_JACK_MACK_DEFEATED)

        try:
            if self.reveal_buff_counter > self.reveal_end_not_active or self.redraw_debuff_counter > self.redraw_end_counter:
                self.magic_lock = True

            elif self.reveal_buff_counter == self.reveal_end_not_active or self.redraw_debuff_counter == self.redraw_end_counter:
                self.magic_lock = False

        except AttributeError:
            print("AttributeError: lucky_seven_buff_counter does not exist")
            self.magic_lock = False
        except TypeError:
            print("TypeError: lucky_seven_buff_counter is not of the expected type")
            self.magic_lock = False

        if self.game_state == self.WELCOME_SCREEN:
            if state.player.stamina_points <= 0:

                self.game_state = self.GAME_OVER_ZERO_STAMINA_SCREEN
            self.update_welcome_screen_update_logic(state, controller)
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
        elif self.game_state == self.MACK_CASTING_SPELL_SCREEN:
            print("Line 279")
            self.battle_messages[self.MACK_CASTING_SPELL].update(state)
            if state.controller.confirm_button:
                self.mack_magic_points -= 1
                self.player_debuff_double_draw = self.double_draw_turns_inflicted
                self.game_state = self.WELCOME_SCREEN
        elif self.game_state == self.LEVEL_UP_SCREEN:
            self.music_volume = 0
            pygame.mixer.music.set_volume(self.music_volume)
            self.handle_level_up(state, state.controller)
        elif self.game_state == self.BET_SCREEN:
            self.update_bet_screen_helper(controller,state)
            self.battle_messages[self.BET_MESSAGE].update(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu(state)

        elif self.game_state == self.DRAW_CARD_SCREEN:
            self.update_draw_card_screen_logic(state)
            self.battle_messages[self.DRAW_CARD_MESSAGE].update(state)
        elif self.game_state == self.PLAYER_ENEMY_DRAW_BLACK_JACK_SCREEN:
            if state.controller.confirm_button:

                state.player.stamina_points -= self.player_stamina_drain_low
                state.player.exp += self.low_exp
                self.game_state = self.WELCOME_SCREEN
                self.round_reset()

            self.battle_messages[self.PLAYER_ENEMY_DRAW_BLACK_JACK_MESSAGE].update(state)
        elif self.game_state == self.PLAYER_BLACK_JACK_SCREEN:
            self.battle_messages[self.PLAYER_BLACK_JACK_MESSAGE].messages = [f"You got a blackjack! You gain {self.bet * self.critical_multiplier} "
                                                                             f"money and gain {self.med_exp} experience points!"]
            if state.controller.confirm_button:
                state.player.stamina_points -= self.player_stamina_drain_low
                state.player.exp += self.med_exp
                state.player.money += self.bet * self.critical_multiplier
                self.money -= self.bet * self.critical_multiplier
                self.game_state = self.WELCOME_SCREEN
                self.round_reset()

            self.battle_messages[self.PLAYER_BLACK_JACK_MESSAGE].update(state)
        elif self.game_state == self.ENEMY_BLACK_JACK_SCREEN:
            self.battle_messages[self.ENEMY_BLACK_JACK_MESSAGE].messages = [f"Enemy got a blackjack! You Lose {self.bet * self.critical_multiplier} money and gain {self.high_exp} experience points!"]
            if state.controller.confirm_button:
                state.player.stamina_points -= self.player_stamina_drain_high
                state.player.money -= self.bet * self.critical_multiplier
                self.money += self.bet * self.critical_multiplier
                state.player.exp += self.high_exp
                self.game_state = self.WELCOME_SCREEN
                self.round_reset()

            self.battle_messages[self.ENEMY_BLACK_JACK_MESSAGE].update(state)
        elif self.game_state == self.PLAYER_ACTION_SCREEN:
            self.update_player_action_logic(state, controller)
            self.battle_messages[self.PLAYER_ACTION_MESSAGE].update(state)
        elif self.game_state == self.PLAYER_WIN_ACTION_SCREEN:
            self.battle_messages[self.PLAYER_WIN_ACTION_MESSAGE].messages = [f"You WIN! You WIN {self.bet} money and gain {self.low_exp}   experience points!"]
            self.update_player_phase_win(state, controller)
            self.battle_messages[self.PLAYER_WIN_ACTION_MESSAGE].update(state)
        elif self.game_state == self.ENEMY_WIN_ACTION_SCREEN:
            self.battle_messages[self.ENEMY_WIN_ACTION_MESSAGE].messages = [f"You LOSE! You LOSE {self.bet} money and gain {self.low_exp}  experience points!"]
            self.update_player_phase_lose(state, controller)
            self.battle_messages[self.ENEMY_WIN_ACTION_MESSAGE].update(state)
        elif self.game_state == self.PLAYER_ENEMY_DRAW_ACTION_SCREEN:
            self.update_player_phase_draw(state, controller)
            self.battle_messages[self.PLAYER_ENEMY_DRAW_ACTION_MESSAGE].update(state)
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.game_over_screen_level_5(state, controller)
        elif self.game_state == self.GAME_OVER_ZERO_STAMINA_SCREEN:

            self.battle_messages[self.GAME_OVER_SCREEN_ZERO_STAMINA_MESSAGE].update(state)
            if self.battle_messages[
                self.GAME_OVER_SCREEN_ZERO_STAMINA_MESSAGE].is_finished() and state.controller.confirm_button:
                state.player.money -= 100
                state.currentScreen = state.area5RestScreen
                state.area5RestScreen.start(state)
                state.player.canMove = True

    def draw(self, state: 'GameState'):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)
        self.draw_box_info(state)

        if self.game_state == self.MACK_CASTING_SPELL_SCREEN:
            self.battle_messages[self.MACK_CASTING_SPELL].draw(state)
        elif self.game_state == self.WELCOME_SCREEN:
            self.draw_menu_selection_box(state)
            self.draw_welcome_screen_box_info(state)
            self.battle_messages[self.WELCOME_MESSAGE].draw(state)
        elif self.game_state == self.LEVEL_UP_SCREEN:
            self.draw_level_up(state)
        elif self.game_state == self.BET_SCREEN:
            self.battle_messages[self.BET_MESSAGE].draw(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box(state)

        elif self.game_state == self.DRAW_CARD_SCREEN:
            self.draw_draw_card_screen(state)
            self.battle_messages[self.DRAW_CARD_MESSAGE].draw(state)
        elif self.game_state == self.PLAYER_ENEMY_DRAW_BLACK_JACK_SCREEN:
            self.draw_reveal_draw_hands(
                player_hand=self.player_hand,
                enemy_hand=self.enemy_hand,
            )
            self.battle_messages[self.PLAYER_ENEMY_DRAW_BLACK_JACK_MESSAGE].draw(state)
        elif self.game_state == self.PLAYER_BLACK_JACK_SCREEN:
            self.draw_reveal_draw_hands(
                player_hand=self.player_hand,
                enemy_hand=self.enemy_hand,
            )
            self.battle_messages[self.PLAYER_BLACK_JACK_MESSAGE].draw(state)
        elif self.game_state == self.ENEMY_BLACK_JACK_SCREEN:
            self.draw_reveal_draw_hands(
                player_hand=self.player_hand,
                enemy_hand=self.enemy_hand,
            )
            self.battle_messages[self.ENEMY_BLACK_JACK_MESSAGE].draw(state)
        elif self.game_state == self.PLAYER_ACTION_SCREEN:
            self.draw_hands(
                player_hand=self.player_hand,
                enemy_hand=self.enemy_hand,
            )
            self.draw_menu_selection_box(state)
            self.draw_player_action_right_menu(state)
            self.battle_messages[self.PLAYER_ACTION_MESSAGE].draw(state)
        elif self.game_state == self.PLAYER_WIN_ACTION_SCREEN:
            self.draw_reveal_draw_hands(
                player_hand=self.player_hand,
                enemy_hand=self.enemy_hand,
            )
            self.battle_messages[self.PLAYER_WIN_ACTION_MESSAGE].draw(state)
        elif self.game_state == self.ENEMY_WIN_ACTION_SCREEN:
            self.draw_reveal_draw_hands(
                player_hand=self.player_hand,
                enemy_hand=self.enemy_hand,
            )
            self.battle_messages[self.ENEMY_WIN_ACTION_MESSAGE].draw(state)
        elif self.game_state == self.PLAYER_ENEMY_DRAW_ACTION_SCREEN:
            self.draw_reveal_draw_hands(
                player_hand=self.player_hand,
                enemy_hand=self.enemy_hand,
            )
            self.battle_messages[self.PLAYER_ENEMY_DRAW_ACTION_MESSAGE].draw(state)
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.draw_game_over_screen_helper(state)

        elif self.game_state == self.GAME_OVER_ZERO_STAMINA_SCREEN:
            self.battle_messages[self.GAME_OVER_SCREEN_ZERO_STAMINA_MESSAGE].draw(state)

        pygame.display.flip()

    def update_bet_screen_helper(self, controller,state):
        min_bet = 50
        max_bet = 150
        if controller.up_button:
            self.menu_movement_sound.play()
            self.bet += min_bet
        elif controller.down_button:
            self.menu_movement_sound.play()
            self.bet -= min_bet

        if self.bet <= min_bet:
            self.bet = min_bet
        elif self.bet >= max_bet:
            self.bet = max_bet

        if self.bet > self.money:
            self.bet = self.money

        if self.bet > state.player.money:
            self.bet = state.player.money

        if controller.action_and_cancel_button:
            self.game_state = self.WELCOME_SCREEN

    def update_player_phase_win(self, state, controller) -> None:

        if controller.confirm_button:
            state.player.money += self.bet
            self.money -= self.bet
            state.player.stamina_points -= self.player_stamina_drain_low
            state.player.exp += self.low_exp
            self.game_state = self.WELCOME_SCREEN
            self.round_reset()

    def update_player_phase_lose(self, state, controller) -> None:
        if controller.confirm_button:
            state.player.stamina_points -= self.player_stamina_drain_high
            state.player.money -= self.bet
            self.money += self.bet
            state.player.exp += self.low_exp
            self.game_state = self.WELCOME_SCREEN
            self.round_reset()

    def update_draw_card_screen_logic(self, state: 'GameState'):
        luck_muliplier = 5
        lucky_roll = random.randint(1, 100)
        player_bad_score_min_range = 12
        player_bad_score_max_range = 17
        level_1_luck_score = 0
        lucky_strike_threshhold = 75
        initial_hand = 2
        # if self.debuff_buff_luck_switch == 0:
        #     adjusted_lucky_roll = lucky_roll + self.luck_bonus
        # elif self.debuff_buff_luck_switch > 0:
        #     adjusted_lucky_roll = 0
        if len(self.player_hand) == 0 and len(self.enemy_hand) == 0:
            self.player_hand = self.deck.player_draw_hand(2)
            # if self.debuff_buff_luck_switch == 0:
            self.enemy_hand = self.deck.enemy_draw_hand(2)
            # elif self.debuff_buff_luck_switch > 0:
            #     lucky_enemy_roll = random.randint(1, 100)
            #     lucky_enemy_strike = lucky_enemy_roll + self.luck_bonus
            #     ace_card = None
            #     ten_card = None
            #     print("Lucky roll strike is" + str(lucky_enemy_strike))
            #     if lucky_enemy_strike >= 100:
            #         for card in self.deck.cards:
            #             if card[0] == "Ace" and ace_card is None:
            #                 ace_card = card
            #             elif card[2] == 10 and ten_card is None:
            #                 ten_card = card
            #             if ace_card and ten_card:
            #                 break
            #         self.enemy_hand = [ace_card, ten_card]
            #     else:
            #         self.enemy_hand = self.deck.enemy_draw_hand(2)

            self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)
            self.player_score = self.deck.compute_hand_value(self.player_hand)
            attempts = 0
            max_attempts = 3
            while (
                    player_bad_score_min_range < self.player_score < player_bad_score_max_range and attempts < max_attempts):
                self.player_hand = self.deck.player_draw_hand(initial_hand)
                self.player_score = self.deck.compute_hand_value(self.player_hand)
                attempts += 1

            # if state.player.luck > level_1_luck_score:
            #     if self.player_score > player_bad_score_min_range and self.player_score < player_bad_score_max_range:
            #         if adjusted_lucky_roll >= lucky_strike_threshhold:
            #             self.lucky_strike.play()
            #             while self.player_score > player_bad_score_min_range and self.player_score < player_bad_score_max_range:
            #                 self.player_hand = self.deck.player_draw_hand(initial_hand)
            #                 self.player_score = self.deck.compute_hand_value(self.player_hand)
            #                 self.critical_hit = True
            #                 print("LINE 715 MAYBE THE ERROR IS HERE")

    def update_player_phase_draw(self, state, controller) -> None:
        if controller.confirm_button:

            state.player.exp += self.low_exp
            state.player.stamina_points -= self.player_stamina_drain_low
            self.game_state = self.WELCOME_SCREEN
            self.round_reset()

    def update_magic_menu(self, state: "GameState"):
        selected_choice = self.magic_screen_choices[self.magic_menu_index]

        if selected_choice == Magic.REVEAL.value:
            self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].update(state)
            self.battle_messages[self.MAGIC_MENU_REDRAW_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()
        elif selected_choice == Magic.BLACK_JACK_REDRAW.value:
            self.battle_messages[self.MAGIC_MENU_REDRAW_DESCRIPTION].update(state)
            self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()
        elif selected_choice == self.BACK:
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)
            self.battle_messages[self.MAGIC_MENU_REDRAW_DESCRIPTION].reset()
            self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].reset()

        controller = state.controller

        if controller.action_and_cancel_button:
            self.game_state = self.WELCOME_SCREEN
            self.magic_menu_index = 0

        if controller.up_button:
            self.menu_movement_sound.play()
            self.magic_menu_index = (self.magic_menu_index - self.index_stepper) % len(self.magic_screen_choices)
        elif controller.down_button:
            self.menu_movement_sound.play()
            self.magic_menu_index = (self.magic_menu_index + self.index_stepper) % len(self.magic_screen_choices)

        if controller.confirm_button:
            if (Magic.BLACK_JACK_REDRAW.value in self.magic_screen_choices
                    and self.magic_menu_index
                    == self.magic_screen_choices.index(Magic.BLACK_JACK_REDRAW.value)):
                if state.player.focus_points >= self.redraw_cast_cost:
                    self.redraw_debuff_counter = self.redraw_start_counter
                    self.spell_sound.play()
                    state.player.focus_points -= self.redraw_cast_cost
                    self.magic_lock = True
                    self.magic_menu_index = 0
                    self.game_state = self.WELCOME_SCREEN
            elif (Magic.REVEAL.value in self.magic_screen_choices
                  and self.magic_menu_index == self.magic_screen_choices.index(Magic.REVEAL.value)):
                if state.player.focus_points >= self.reveal_cast_cost:
                    self.reveal_buff_counter = self.reveal_start_counter + state.player.mind
                    self.spell_sound.play()
                    state.player.focus_points -= self.reveal_cast_cost
                    self.magic_lock = True
                    self.magic_menu_index = 0
                    self.game_state = self.WELCOME_SCREEN

            elif self.magic_screen_choices[self.magic_menu_index] == "back":
                self.magic_menu_index = 0
                self.game_state = self.WELCOME_SCREEN



    def update_player_action_logic(self, state: "GameState", controller):
        card_max = 3
        max_before_bust = 21

        if controller.up_button:
            self.menu_movement_sound.play()
            self.player_action_phase_index = (self.player_action_phase_index
                                              - self.move_index_by_1) % len(self.player_action_phase_choices)
        elif controller.down_button:
            self.menu_movement_sound.play()
            self.player_action_phase_index = (self.player_action_phase_index
                                              + self.move_index_by_1) % len(self.player_action_phase_choices)
        elif state.controller.confirm_button:
            if self.player_action_phase_index == self.player_action_phase_play_index:
                state.player.stamina_points -= 0
                while self.enemy_score < 16 and len(self.enemy_hand) <= card_max:
                    if self.enemy_score < self.player_score:
                        self.animate_face_down_card(state, len(self.enemy_hand))
                    else:
                        break
                if self.player_score == self.enemy_score:
                    self.game_state = self.PLAYER_ENEMY_DRAW_ACTION_SCREEN
                elif self.enemy_score > max_before_bust:
                    self.game_state = self.PLAYER_WIN_ACTION_SCREEN
                elif self.enemy_score > self.player_score:
                    self.game_state = self.ENEMY_WIN_ACTION_SCREEN
                elif self.enemy_score < self.player_score:
                    self.game_state = self.PLAYER_WIN_ACTION_SCREEN

            if (self.player_action_phase_index == self.player_action_phase_draw_index
                    and len(self.player_hand) <= card_max):
                self.animate_face_down_card_player(state, len(self.player_hand))
                if self.player_score > max_before_bust:
                    if Equipment.BLACK_JACK_HAT.value not in state.player.equipped_items:
                        if self.player_score > max_before_bust:
                            self.game_state = self.ENEMY_WIN_ACTION_SCREEN
                    elif Equipment.BLACK_JACK_HAT.value in state.player.equipped_items:

                        lucky_roll = random.randint(1, 100) + self.spirit_bonus

                        if lucky_roll >= self.LEVEL_4_PERCENTAGE_CHANCE:
                            self.player_hand.pop()
                            self.player_score = self.deck.compute_hand_value(self.player_hand)
                            self.lucky_strike.play()

                        else:
                            self.game_state = self.ENEMY_WIN_ACTION_SCREEN





    def animate_face_down_card_player(self, state, card_index):
        initial_y_position = 0
        target_y_position = 300
        x_position = 250 + card_index * 75
        card_speed = 5

        while initial_y_position < target_y_position:
            self.draw(state)
            initial_y_position += card_speed
            if initial_y_position >= target_y_position:
                initial_y_position = target_y_position
                break

            self.deck.draw_card_face_down((x_position, initial_y_position), state.DISPLAY)
            pygame.display.flip()
            pygame.time.delay(30)

        new_card = self.deck.player_draw_hand(1)[0]

        self.deck.draw_card_face_up(new_card[1], new_card[0],
                                    (x_position, target_y_position), state.DISPLAY)
        self.player_hand.append(new_card)
        self.player_score = self.deck.compute_hand_value(self.player_hand)

        # If double draw is active, draw a second card
        if self.player_debuff_double_draw > self.double_draw_duration_expired:
            # Animate the second card
            x_position = 250 + (card_index + 1) * 75
            initial_y_position = 0

            while initial_y_position < target_y_position:
                self.draw(state)
                initial_y_position += card_speed
                if initial_y_position >= target_y_position:
                    initial_y_position = target_y_position
                    break

                self.deck.draw_card_face_down((x_position, initial_y_position), state.DISPLAY)
                pygame.display.flip()
                pygame.time.delay(30)

            # Draw the second card
            second_card = self.deck.player_draw_hand(1)[0]
            self.deck.draw_card_face_up(second_card[1], second_card[0],
                                      (x_position, target_y_position), state.DISPLAY)
            self.player_hand.append(second_card)
            self.player_score = self.deck.compute_hand_value(self.player_hand)

    def update_welcome_screen_update_logic(self, state: 'GameState', controller):



        if state.player.money <= 0:
            self.game_state = self.GAME_OVER_SCREEN
            return


        if controller.confirm_button:
            if self.welcome_screen_index == self.welcome_screen_play_index:
                self.game_state = self.DRAW_CARD_SCREEN
            elif (self.welcome_screen_index == self.welcome_screen_magic_index
                  and self.magic_lock == False):
                self.game_state = self.MAGIC_MENU_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_bet_index:
                self.game_state = self.BET_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_quit_index:

                state.currentScreen = state.area5RestScreen
                state.area5RestScreen.start(state)
                state.player.canMove = True

    def initialize_music(self):
        pass



    def animate_face_down_card(self, state, card_index):
        initial_y_position = 0
        target_y_position = 50
        x_position = 250 + card_index * 75
        card_speed = 3

        while initial_y_position < target_y_position:
            self.draw(state)
            initial_y_position += card_speed

            if initial_y_position >= target_y_position:
                initial_y_position = target_y_position
                break  # Exit the loop when the card reaches its target

            self.deck.draw_card_face_down((x_position, initial_y_position), state.DISPLAY)
            pygame.display.flip()
            pygame.time.delay(30)

        new_card = self.deck.enemy_draw_hand(1)[0]  # Get the single card drawn
        self.deck.draw_card_face_up(new_card[1], new_card[0], (x_position,
                                                               target_y_position), state.DISPLAY)
        pygame.display.flip()
        self.enemy_hand.append(new_card)
        self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)

    def draw_reveal_draw_hands(self, player_hand: list, enemy_hand: list):
        initial_x_position = 250
        player_target_y_position = 300
        enemy_target_y_position = 50
        move_card_x = 75
        deck = self.deck
        display = DISPLAY

        for i, card in enumerate(player_hand):
            player_x_position = initial_x_position + i * move_card_x
            player_y_position = player_target_y_position
            deck.draw_card_face_up(card[1], card[0], (player_x_position, player_y_position), display)

        for i, card in enumerate(enemy_hand):
            enemy_x_position = initial_x_position + i * move_card_x
            enemy_y_position = enemy_target_y_position
            deck.draw_card_face_up(card[1], card[0], (enemy_x_position, enemy_y_position), display)

    def draw_hands(self, player_hand: list, enemy_hand: list):
        initial_x_position = 250
        player_target_y_position = 300
        enemy_target_y_position = 50
        move_card_x = 75
        flip_y_position = 145
        deck = self.deck
        display = DISPLAY

        for i, card in enumerate(player_hand):
            player_x_position = initial_x_position + i * move_card_x
            player_y_position = player_target_y_position

            if i == 1 and player_y_position >= flip_y_position:
                deck.draw_card_face_up(card[1], card[0], (player_x_position,
                                                          player_y_position), display)
            else:
                deck.draw_card_face_up(card[1], card[0], (player_x_position,
                                                          player_y_position), display)

        for i, card in enumerate(enemy_hand):
            enemy_x_position = initial_x_position + i * move_card_x
            enemy_y_position = enemy_target_y_position

            if i == 0:
                deck.draw_card_face_down((enemy_x_position, enemy_y_position), display)
            else:
                deck.draw_card_face_up(card[1], card[0], (enemy_x_position, enemy_y_position), display)



    def draw_draw_card_screen(self, state: 'GameState'):
        card_one = 0
        card_two = 1
        initial_x_position = 250
        initial_y_position = 1
        player_target_y_position = 300
        enemy_target_y_position = 50
        move_card_x = 75
        card_speed = 3
        flip_y_position = 145

        if len(self.player_hand) == card_one or len(self.enemy_hand) == card_one:
            print("Error: player_hand or enemy_hand is empty.")
            return

        if (not hasattr(self, 'player_card_y_positions') or len(self.player_card_y_positions)
                != len(self.player_hand)):
            self.player_card_y_positions = [initial_y_position] * len(self.player_hand)
            self.player_card_x_positions = [initial_x_position + i * move_card_x
                                            for i in range(len(self.player_hand))]

        if (not hasattr(self, 'enemy_card_y_positions') or len(self.enemy_card_y_positions)
                != len(self.enemy_hand)):
            self.enemy_card_y_positions = [initial_y_position] * len(self.enemy_hand)
            self.enemy_card_x_positions = [initial_x_position + i * move_card_x
                                           for i in range(len(self.enemy_hand))]

        all_player_cards_dealt = True
        for i, card in enumerate(self.player_hand):
            if self.player_card_y_positions[i] < player_target_y_position:
                self.player_card_y_positions[i] += card_speed
                if self.player_card_y_positions[i] > player_target_y_position:
                    self.player_card_y_positions[i] = player_target_y_position

                if i == 1 and self.player_card_y_positions[i] >= flip_y_position:
                    self.deck.draw_card_face_up(card[1], card[0],
                                                (self.player_card_x_positions[i],
                                                 self.player_card_y_positions[i]), DISPLAY)
                else:
                    self.deck.draw_card_face_down((self.player_card_x_positions[i],
                                                   self.player_card_y_positions[i]), DISPLAY)

                all_player_cards_dealt = False
                return

            self.deck.draw_card_face_up(card[card_two], card[card_one], (self.player_card_x_positions[i], self.player_card_y_positions[i]), DISPLAY)

        if all_player_cards_dealt:
            for i, card in enumerate(self.enemy_hand):
                if self.enemy_card_y_positions[i] < enemy_target_y_position:
                    self.enemy_card_y_positions[i] += card_speed
                    if self.enemy_card_y_positions[i] > enemy_target_y_position:
                        self.enemy_card_y_positions[i] = enemy_target_y_position

                    self.deck.draw_card_face_down((self.enemy_card_x_positions[i], self.enemy_card_y_positions[i]), DISPLAY)
                    return

                if i == card_one:
                    self.deck.draw_card_face_down((self.enemy_card_x_positions[i],
                                                   self.enemy_card_y_positions[i]), DISPLAY)
                else:
                    self.deck.draw_card_face_up(card[card_two], card[card_one],
                                                (self.enemy_card_x_positions[i],
                                                 self.enemy_card_y_positions[i]), DISPLAY)

        for i, card in enumerate(self.player_hand):
            self.deck.draw_card_face_up(card[card_two], card[card_one],
                                        (self.player_card_x_positions[i],
                                         self.player_card_y_positions[i]), DISPLAY)

        for i, card in enumerate(self.enemy_hand):
            if i == 0:
                self.deck.draw_card_face_down((self.enemy_card_x_positions[i],
                                               self.enemy_card_y_positions[i]), DISPLAY)
            else:
                self.deck.draw_card_face_up(card[card_two], card[card_one],
                                            (self.enemy_card_x_positions[i],
                                             self.enemy_card_y_positions[i]), DISPLAY)

        # level 5 remove this and put in update no idea why its in draw
        sir_leopold_steal_roll = random.randint(1, 100) + self.spirit_bonus
        if Equipment.SIR_LEOPOLD_AMULET.value in state.player.equipped_items and sir_leopold_steal_roll > self.LEVEL_4_PERCENTAGE_CHANCE:
            if (len(self.enemy_hand) > 1 and self.enemy_hand[1][0]
                    == "Ace" and not self.ace_effect_triggered):
                if self.ace_detected_time is None:
                    self.ace_detected_time = pygame.time.get_ticks()

            if self.ace_detected_time is not None:
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - self.ace_detected_time
                if elapsed_time >= 1200:
                    self.enemy_hand.pop(1)
                    new_card = self.deck.enemy_draw_hand(1)[0]
                    self.enemy_hand.insert(1, new_card)
                    self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)

                    self.ace_effect_triggered = True
                    self.ace_detected_time = None
                else:
                    return

        if self.player_score == 21 and self.enemy_score == 21:
            self.game_state = self.PLAYER_ENEMY_DRAW_BLACK_JACK_SCREEN
            return

        self.hedge_hog_time = True

        if self.player_score == 21 and self.hedge_hog_time:
            self.game_state = self.PLAYER_BLACK_JACK_SCREEN
            return

        if self.enemy_score == 21 and self.hedge_hog_time:

            self.game_state = self.ENEMY_BLACK_JACK_SCREEN
            return

        else:
            self.game_state = self.PLAYER_ACTION_SCREEN

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
            y_position = start_y_right_box + idx * spacing_between_choices
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)
            )

        if Magic.REVEAL.value not in state.player.magicinventory:
            self.magic_lock = True
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif Magic.REVEAL.value in state.player.magicinventory:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if self.magic_lock == True:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.LOCKED
        elif self.magic_lock == False:
            self.welcome_screen_choices[self.welcome_screen_magic_index] = self.MAGIC

        if self.welcome_screen_index == self.welcome_screen_play_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box
                 + arrow_y_coordinate_padding_play)
            )
        elif self.welcome_screen_index == self.welcome_screen_magic_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box
                 + arrow_y_coordinate_padding_magic)
            )
        elif self.welcome_screen_index == self.welcome_screen_bet_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box
                 + arrow_y_coordinate_padding_bet)
            )
        elif self.welcome_screen_index == self.welcome_screen_quit_index:
            state.DISPLAY.blit(
                self.font.render("->", True, WHITE),
                (start_x_right_box + arrow_x_coordinate_padding, start_y_right_box
                 + arrow_y_coordinate_padding_quit)
            )

    def draw_box_info(self, state: 'GameState'):
        player_enemy_box_info_x_position = 37
        player_enemy_box_info_x_position_score = 28
        score_y_position = 150
        enemy_name_y_position = 33
        enemy_money_y_position = 70
        enemy_status_y_position = 110
        bet_y_position = 370
        player_money_y_position = 250
        hero_name_y_position = 205
        hero_stamina_y_position = 290
        hero_focus_y_position = 330
        score_header = "Score"

        state.DISPLAY.blit(self.font.render(self.dealer_name, True, WHITE),
                           (player_enemy_box_info_x_position, enemy_name_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}",
                                            True, WHITE),
                           (player_enemy_box_info_x_position, enemy_money_y_position))
        if (self.reveal_buff_counter == self.reveal_end_not_active and self.redraw_debuff_counter
                == self.reveal_end_counter and self.player_debuff_double_draw == self.double_draw_duration_expired):
            state.DISPLAY.blit(self.font.render(f"{self.STATUS_GREEN}", True, WHITE),
                               (player_enemy_box_info_x_position, enemy_status_y_position))
        elif self.reveal_buff_counter > self.reveal_end_not_active:
            state.DISPLAY.blit(self.font.render(f"{self.REVEAL}: {self.reveal_buff_counter} ",
                                                True, WHITE), (player_enemy_box_info_x_position,
                                                               enemy_status_y_position))
            state.DISPLAY.blit(self.font.render(f" {score_header}: {self.enemy_score} ",
                                                True, WHITE),
                               (player_enemy_box_info_x_position_score, score_y_position))

        elif self.redraw_debuff_counter > self.redraw_end_counter:
            state.DISPLAY.blit(self.font.render(f"{self.REDRAW}:"
                                                f" {self.redraw_debuff_counter} ",
                                                True, WHITE), (player_enemy_box_info_x_position,
                                                               enemy_status_y_position))

        elif self.player_debuff_double_draw > self.double_draw_duration_expired:
            state.DISPLAY.blit(self.font.render(f"D. Draw: {self.player_debuff_double_draw}",
                                                True, RED), (player_enemy_box_info_x_position,
                                                             enemy_status_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}",
                                            True, WHITE),
                           (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}",
                                            True, WHITE), (player_enemy_box_info_x_position,
                                                           player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}",
                                            True, WHITE), (player_enemy_box_info_x_position,
                                                           hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: "
                                            f"{state.player.focus_points}",
                                            True, WHITE), (player_enemy_box_info_x_position,
                                                           hero_focus_y_position))

        if self.lock_down <= self.lock_down_inactive:
            state.DISPLAY.blit(self.font.render(f"{self.HERO_HEADER}",
                                                True, WHITE), (player_enemy_box_info_x_position,
                                                               hero_name_y_position))
        elif self.lock_down > self.lock_down_inactive:
            state.DISPLAY.blit(self.font.render(f"{self.LOCKED_DOWN_HEADER}:{self.lock_down}",
                                                True, RED), (player_enemy_box_info_x_position,
                                                             hero_name_y_position))

    def draw_magic_menu_selection_box(self, state):
        selected_choice = self.magic_screen_choices[self.magic_menu_index]

        if selected_choice == Magic.REVEAL.value:
            self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].draw(state)
        elif selected_choice == Magic.BLACK_JACK_REDRAW.value:
            self.battle_messages[self.MAGIC_MENU_REDRAW_DESCRIPTION].draw(state)
        elif selected_choice == self.BACK:
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

        # if (Magic.BLACK_JACK_REDRAW.value in state.player.magicinventory
        #         and Magic.BLACK_JACK_REDRAW.value not in self.magic_screen_choices):
        #     self.magic_screen_choices.insert(1, Magic.BLACK_JACK_REDRAW.value)

        for idx, choice in enumerate(self.magic_screen_choices):
            y_position = start_y_right_box + idx * choice_spacing  # Use dynamic spacing
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        arrow_y_coordinate = start_y_right_box + self.magic_menu_index * choice_spacing
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_coordinate + text_y_offset)  # Align arrow with the text
        )

    def draw_player_action_right_menu(self, state: 'GameState'):
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
        arrow_center = 10
        player_hand_max = 4
        draw_option = 1


        if (self.redraw_debuff_counter > self.redraw_end_counter
                and Magic.BLACK_JACK_REDRAW.value not in self.player_action_phase_choices):
            self.player_action_phase_choices.insert(2, Magic.BLACK_JACK_REDRAW.value)

        if (self.redraw_debuff_counter <= self.redraw_end_counter
                and Magic.BLACK_JACK_REDRAW.value in self.player_action_phase_choices):
            self.player_action_phase_choices.remove(Magic.BLACK_JACK_REDRAW.value)

        for idx, choice in enumerate(self.player_action_phase_choices):
            y_position = start_y_right_box + idx * spacing_between_choices

            # Check if this is the Draw option and if player has double draw debuff
            display_text = choice
            if idx == draw_option and self.player_debuff_double_draw > 0:
                display_text = "DDraw"

            if choice == Magic.BLACK_JACK_REDRAW.value and self.redraw_counter == False:
                rendered_choice = self.font.render(display_text, True, RED)
            else:
                rendered_choice = self.font.render(display_text, True, WHITE)

            if (choice == self.player_action_phase_choices[draw_option]
                    and len(self.player_hand) == player_hand_max):
                rendered_draw = self.font.render(display_text, True, RED)
            else:
                rendered_draw = self.font.render(display_text, True, WHITE)

            state.DISPLAY.blit(rendered_choice, (start_x_right_box + text_x_offset, y_position + text_y_offset))
            state.DISPLAY.blit(rendered_draw, (start_x_right_box + text_x_offset, y_position + text_y_offset))

        arrow_y_coordinate = arrow_center + start_y_right_box + self.player_action_phase_index * spacing_between_choices
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_coordinate_padding, arrow_y_coordinate)
        )

    def draw_game_over_screen_helper(self, state: 'Gamestate'):
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        no_money_game_over = 0
        no_stamina_game_over = 0
        if state.player.money <= no_money_game_over:
            state.DISPLAY.blit(self.font.render(f"You ran out of money and are now a prisoner of hell", True, WHITE), (self.blit_message_x, self.blit_message_y))
        elif state.player.stamina_points <= no_stamina_game_over:
            state.DISPLAY.blit(self.font.render(f"You ran out of stamina , you lose -100 gold", True, WHITE), (self.blit_message_x, self.blit_message_y))
