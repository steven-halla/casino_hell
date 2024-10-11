import pygame

from constants import WHITE, RED, DISPLAY
from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.events import Events
from game_constants.magic import Magic


class BlackJackAlbertScreen(GambleScreen):
    def __init__(self, screenName: str = "Black Jack") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.deck: Deck() = Deck()
        self.player_hand = []
        self.enemy_hand = []

        self.bet: int = 100
        self.money: int = 1000
        self.albert_bankrupt: int = 0
        self.reveal_buff_counter: int = 0
        self.reveal_start_duration: int = 7
        self.reveal_end_not_active: int = 0
        self.magic_lock: bool = False
        self.dealer_name = "albert"
        self.lock_down_inactive: int = 0
        self.initial_hand = 2

        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "This is the welcome screen"
            ]),
            self.BET_MESSAGE: MessageBox([
                "Max bet of 75 during Come out Roll. Point Roll Max is 200"
            ]),
            self.MAGIC_MENU_REVEAL_DESCRIPTION: MessageBox([
                "Reveals enemy score."
            ]),
            self.MAGIC_MENU_BACK_DESCRIPTION: MessageBox([
                "go back to previous menu"
            ]),
            self.DRAW_CARD_MESSAGE: MessageBox([
                "drawing your cards now"
            ]),
        }

    DRAW_CARD_MESSAGE: str = "draw card message"
    MAGIC_MENU_REVEAL_DESCRIPTION: str = "magic_menu_reveal_description"
    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    BET_MESSAGE: str = "bet_message"
    Reveal: str = "reveal"
    DRAW_CARD_SCREEN: str = "draw card screen"


    #demon: why do you guys always draw 1 card per player per round why not just give players thier carss , its faster that way
    # you silly humans make no logical sense

    def start(self, state: 'GameState'):
        self.deck.shuffle()

    def round_reset(self):
        pass

    def reset_black_jack_game(self,state: 'GameState'):
        pass

    def update(self, state: 'GameState'):
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)
        if self.money <= self.albert_bankrupt:
            Events.add_event_to_player(state.player, Events.BLACK_JACK_ALBERT_DEFEATED)

        try:
            if self.reveal_buff_counter > self.reveal_end_not_active:
                self.magic_lock = True
            elif self.reveal_buff_counter == self.reveal_end_not_active:
                self.magic_lock = False
        except AttributeError:
            print("AttributeError: lucky_seven_buff_counter does not exist")
            self.magic_lock = False
        except TypeError:
            print("TypeError: lucky_seven_buff_counter is not of the expected type")
            self.magic_lock = False

        if self.game_state == self.WELCOME_SCREEN:
            self.welcome_screen_update_logic(state, controller)
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
        elif self.game_state == self.DRAW_CARD_SCREEN:
            self.update_draw_card_screen_logic(state)
            self.battle_messages[self.DRAW_CARD_MESSAGE].update(state)


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
        elif self.game_state == self.DRAW_CARD_SCREEN:
            self.draw_draw_card_screen(state)
            # self.draw_draw_card_screen_enemy(state)
            self.battle_messages[self.DRAW_CARD_MESSAGE].draw(state)




        pygame.display.flip()

    def update_draw_card_screen_logic(self, state: 'GameState'):
        # Only draw cards if the hands are empty
        if len(self.player_hand) == 0 and len(self.enemy_hand) == 0:
            self.enemy_hand = self.deck.enemy_draw_hand(2)
            self.player_hand = self.deck.player_draw_hand(2)
            print(self.enemy_hand)
            print(self.player_hand)

    def draw_draw_card_screen(self, state: 'GameState'):
        initial_x_position = 250
        initial_y_position = 1
        player_target_y_position = 300
        enemy_target_y_position = 50
        move_card_x = 75
        card_speed = 4  # Adjust this for speed of movement
        flip_y_position = 90  # Define the y-position where the card will flip

        # Ensure that both player_hand and enemy_hand are not empty
        if len(self.player_hand) == 0 or len(self.enemy_hand) == 0:
            print("Error: player_hand or enemy_hand is empty.")
            return  # Exit if either hand is empty to prevent further errors

        # Initialize card_y_positions and card_x_positions for both player and enemy if they don't already exist
        if not hasattr(self, 'player_card_y_positions') or len(self.player_card_y_positions) != len(self.player_hand):
            self.player_card_y_positions = [initial_y_position] * len(self.player_hand)
            self.player_card_x_positions = [initial_x_position + i * move_card_x for i in range(len(self.player_hand))]

        if not hasattr(self, 'enemy_card_y_positions') or len(self.enemy_card_y_positions) != len(self.enemy_hand):
            self.enemy_card_y_positions = [initial_y_position] * len(self.enemy_hand)
            self.enemy_card_x_positions = [initial_x_position + i * move_card_x for i in range(len(self.enemy_hand))]

        # Flag to control which set of cards (player or enemy) is being dealt
        if not hasattr(self, 'dealing_player_cards'):
            self.dealing_player_cards = True  # Start by dealing player cards first
        if not hasattr(self, 'dealt_cards_count'):
            self.dealt_cards_count = 0  # Track how many cards have been dealt so far

        # Move and draw player cards first, one card at a time
        all_player_cards_finished = True
        for i, card in enumerate(self.player_hand):
            if self.player_card_y_positions[i] < player_target_y_position:
                all_player_cards_finished = False  # Not all player cards are finished moving
                self.player_card_y_positions[i] += card_speed
                if self.player_card_y_positions[i] > player_target_y_position:
                    self.player_card_y_positions[i] = player_target_y_position

            if i == 0 or (i == 1 and self.player_card_y_positions[1] < flip_y_position):
                self.deck.draw_card_face_down((self.player_card_x_positions[i], self.player_card_y_positions[i]), DISPLAY)
            else:
                self.deck.draw_card_face_up(card[1], card[0], (self.player_card_x_positions[i], self.player_card_y_positions[i]), DISPLAY)

        # Only start drawing enemy cards once all player cards are done
        if all_player_cards_finished:
            for i, card in enumerate(self.enemy_hand):
                if self.enemy_card_y_positions[i] < enemy_target_y_position:
                    self.enemy_card_y_positions[i] += card_speed
                    if self.enemy_card_y_positions[i] > enemy_target_y_position:
                        self.enemy_card_y_positions[i] = enemy_target_y_position

                if i == 0:
                    # Draw the first enemy card face down until it reaches the target
                    self.deck.draw_card_face_down((self.enemy_card_x_positions[0], self.enemy_card_y_positions[0]), DISPLAY)
                elif i == 1:
                    # Always flip the second enemy card face up once it reaches or passes the flip_y_position
                    self.deck.draw_card_face_up(self.enemy_hand[1][1], self.enemy_hand[1][0], (self.enemy_card_x_positions[1], self.enemy_card_y_positions[1]), DISPLAY)

                # Ensure that all other cards that have reached their positions are drawn again
                for j in range(2, len(self.enemy_hand)):
                    self.deck.draw_card_face_up(self.enemy_hand[j][1], self.enemy_hand[j][0], (self.enemy_card_x_positions[j], self.enemy_card_y_positions[j]), DISPLAY)

        # Redraw all cards that have already reached their positions to ensure they don't vanish
        for i, card in enumerate(self.player_hand):
            if self.player_card_y_positions[i] == player_target_y_position:
                self.deck.draw_card_face_up(card[1], card[0], (self.player_card_x_positions[i], self.player_card_y_positions[i]), DISPLAY)

        for i, card in enumerate(self.enemy_hand):
            if self.enemy_card_y_positions[i] == enemy_target_y_position:
                self.deck.draw_card_face_up(card[1], card[0], (self.enemy_card_x_positions[i], self.enemy_card_y_positions[i]), DISPLAY)

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
        if self.reveal_buff_counter == self.reveal_end_not_active:
            state.DISPLAY.blit(self.font.render(f"{self.STATUS_GREEN}", True, WHITE), (player_enemy_box_info_x_position, enemy_status_y_position))
        elif self.reveal_buff_counter > self.reveal_end_not_active:
            state.DISPLAY.blit(self.font.render(f"{self.Reveal}: {self.reveal_buff_counter} ", True, WHITE), (player_enemy_box_info_x_position, enemy_status_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE), (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE), (player_enemy_box_info_x_position, player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE), (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE), (player_enemy_box_info_x_position, hero_focus_y_position))

        if self.lock_down <= self.lock_down_inactive:
            state.DISPLAY.blit(self.font.render(f"{self.HERO_HEADER}", True, WHITE), (player_enemy_box_info_x_position, hero_name_y_position))
        elif self.lock_down > self.lock_down_inactive:
            state.DISPLAY.blit(self.font.render(f"{self.LOCKED_DOWN_HEADER}:{self.lock_down}", True, RED), (player_enemy_box_info_x_position, hero_name_y_position))



    def welcome_screen_update_logic(self, state: 'GameState', controller):
        if controller.isTPressed:
            controller.isTPressed = False
            if self.welcome_screen_index  == self.welcome_screen_play_index:
                self.game_state = self.DRAW_CARD_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_magic_index:
                self.game_state = self.MAGIC_MENU_SCREEN

            elif self.welcome_screen_index == self.welcome_screen_bet_index:
                self.game_state = self.BET_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_quit_index:
                print("code will go here later")

        if controller.isUpPressed:
            controller.isUpPressed = False



