import pygame
import random
from constants import WHITE, RED, DISPLAY, BLACK
from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic


class HighLowDienaScreen(GambleScreen):
    def __init__(self, screenName: str = "high low") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.enemy_cad_y_position :int = 0
        self.player_card_y_position: int = 0
        self.deck: Deck() = Deck()
        self.player_hand: str = ""
        self.index_stepper: int = 1

        self.enemy_hand: str = ""
        self.player_score: int = 0
        self.enemy_score: int = 0
        self.bet: int = 100
        self.money: int = 1000

        self.diena_bankrupt: int = 0
        self.magic_lock: bool = False
        self.dealer_name: str = "diena"
        self.magic_menu_screen_index: int = 0
        self.low_exp: int = 10
        self.medium_exp: int = 25
        self.high_exp: int = 50
        self.diena_bankrupt: int = 0
        self.magic_menu_selector: list[str] = [Magic.SHIELD.value, self.BACK]
        self.magic_screen_index: int = 0




        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "This is the welcome screen"
            ]),

            self.BET_MESSAGE: MessageBox([
                "Min bet of 50, max of 200. Press up and down keys to increase/decrease bet. Press B to Exit."
            ]),


            self.MAGIC_MENU_BACK_DESCRIPTION: MessageBox([
                "go back to previous menu"
            ]),

            self.LEVEL_UP_SCREEN: MessageBox([
                f"You leveld up!"
            ]),
            self.LEVEL_UP_MESSAGE: MessageBox([
                f"You leveld up!"
            ]),

        }

    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    BET_MESSAGE: str = "bet_message"
    LEVEL_UP: str = "level_up_message"
    BACK = "back"

    LEVEL_UP_SCREEN = "level_up_screen"
    DRAW_CARD_SCREEN = "draw_card_screen"
    PLAYER_DRAWS_ACE_SCREEN = "player_draws_ace_screen"
    ENEMY_DRAWS_ACE_SCREEN = "enemy_draws_ace_screen"
    PLAYER_WINS_SCREEN = "player_wins_screen"
    ENEMY_WINS_SCREEN = "enemy_wins_screen"
    PLAYER_SPREAD_SCREEN = "player_spread_screen"


    def start(self, state: 'GameState'):
        self.deck.shuffle()
        self.build_custom_26_card_deck()

    def build_custom_26_card_deck(self):
        # Start fresh
        self.deck.cards.clear()

        # Define allowed suits and ranks
        allowed_suits = ["Hearts", "Clubs"]
        allowed_ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]

        # Rebuild the deck with only the allowed suits and ranks
        self.deck.cards = [
            (self.deck.rank_strings[rank], suit, self.deck.rank_values[rank])
            for suit in allowed_suits
            for rank in allowed_ranks
        ]

        random.shuffle(self.deck.cards)


    def round_reset_high_low(self):
        self.deck.shuffle()
        self.build_custom_26_card_deck()
        self.player_score = 0
        self.enemy_score = 0
        self.player_hand: str = ""
        self.enemy_hand: str = ""

    def reset_high_low_game(self):
        self.deck.shuffle()
        self.build_custom_26_card_deck()
        self.player_score = 0
        self.enemy_score = 0
        self.player_hand: str = ""
        self.enemy_hand: str = ""

    def update(self, state: 'GameState'):

        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

        if self.money <= self.diena_bankrupt:
            state.currentScreen = state.area3RestScreen
            state.area3RestScreen.start(state)
            Events.add_level_three_event_to_player(state.player, Events.HIGH_LOW_DIENA_DEFEATED)



        if self.game_state == self.WELCOME_SCREEN:
            self.welcome_screen_helper(state, controller)

            self.battle_messages[self.WELCOME_MESSAGE].update(state)


        elif self.game_state == self.BET_SCREEN:
            self.bet_screen_helper(state, controller)
            self.battle_messages[self.BET_MESSAGE].update(state)


        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu_selection_box(controller, state)


        elif self.game_state == self.DRAW_CARD_SCREEN:
            pass

        elif self.game_state == self.PLAYER_DRAWS_ACE_SCREEN:
            pass

        elif self.game_state == self.ENEMY_DRAWS_ACE_SCREEN:
            pass

        elif self.game_state == self.PLAYER_SPREAD_SCREEN:
            pass


        elif self.game_state == self.PLAYER_WINS_SCREEN:
            pass

        elif self.game_state == self.ENEMY_WINS_SCREEN:
            pass


        elif self.game_state == self.GAME_OVER_SCREEN:

            self.game_over_helper()

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
            self.draw_magic_menu_selection_box(state)


        elif self.game_state == self.DRAW_CARD_SCREEN:
            pass

        elif self.game_state == self.PLAYER_DRAWS_ACE_SCREEN:
            pass

        elif self.game_state == self.ENEMY_DRAWS_ACE_SCREEN:
            pass

        elif self.game_state == self.PLAYER_SPREAD_SCREEN:
            pass

        elif self.game_state == self.PLAYER_WINS_SCREEN:
            pass

        elif self.game_state == self.ENEMY_WINS_SCREEN:
            pass


        elif self.game_state == self.GAME_OVER_SCREEN:
            pass

        pygame.display.flip()

    def welcome_screen_helper(self, state: 'GameState', controller):
        draw_screen = 0
        magic_screen = 1
        bet_screen = 2
        leave_game = 3
        # print(self.welcome_screen_index)
        if state.player.money <= 0:
            self.game_state = self.GAME_OVER_SCREEN
            return
        elif state.player.stamina_points <= 0:
            self.game_state = self.GAME_OVER_SCREEN
            return
        elif self.money <= 0:
            print("enemy defeated")

        if controller.confirm_button:
            print("hfdfjdsfad")


            if self.welcome_screen_index == draw_screen:
                print("draw card")
                self.game_state = self.DRAW_CARD_SCREEN

            elif self.welcome_screen_index == magic_screen:
                print("magic")
                self.game_state = self.MAGIC_MENU_SCREEN

            elif self.welcome_screen_index == bet_screen:
                print("bet")
                self.game_state = self.BET_SCREEN

            elif self.welcome_screen_index == leave_game:
                print("mew")

                state.currentScreen = state.area3RestScreen
                state.area3RestScreen.start(state)

    def draw_box_info(self, state: 'GameState'):
        player_enemy_box_info_x_position = 37
        enemy_name_y_position = 33
        enemy_money_y_position = 70
        bet_y_position = 370
        player_money_y_position = 250
        hero_stamina_y_position = 290
        hero_focus_y_position = 330

        state.DISPLAY.blit(self.font.render(self.dealer_name, True, WHITE), (player_enemy_box_info_x_position, enemy_name_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}", True, WHITE), (player_enemy_box_info_x_position, enemy_money_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.BET_HEADER}: {self.bet}", True, WHITE), (player_enemy_box_info_x_position, bet_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER}: {state.player.money}", True, WHITE), (player_enemy_box_info_x_position, player_money_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.HP_HEADER}: {state.player.stamina_points}", True, WHITE), (player_enemy_box_info_x_position, hero_stamina_y_position))
        state.DISPLAY.blit(self.font.render(f"{self.MP_HEADER}: {state.player.focus_points}", True, WHITE), (player_enemy_box_info_x_position, hero_focus_y_position))
        #

    def draw_menu_selection_box(self, state: "GameState"):
        # Define local variables for dimensions and positions
        box_height_offset = 50
        box_width_offset = 10
        border_width = 5
        horizontal_padding = 25
        vertical_position = 240
        box_initial_height = 221
        white_border_top_left = 2
        box_initial_width = 200

        black_box_height = box_initial_height - box_height_offset
        black_box_width = box_initial_width - box_width_offset

        start_x_right_box = state.DISPLAY.get_width() - black_box_width - horizontal_padding
        start_y_right_box = vertical_position

        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill(BLACK)

        white_border = pygame.Surface(
            (black_box_width + white_border_top_left * border_width, black_box_height + white_border_top_left * border_width)
        )
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))

        black_box_x = start_x_right_box - border_width
        black_box_y = start_y_right_box - border_width

        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))




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

    def bet_screen_helper(self, state, controller):

        if controller.isBPressed or controller.isBPressedSwitch:
            controller.isBPressed = False
            controller.isBPressedSwitch = False
            self.game_state = self.WELCOME_SCREEN
        min_bet = 50
        if Equipment.COIN_FLIP_GLOVES.value in state.player.equipped_items:
            max_bet = 400
        else:
            max_bet = 200

        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet += min_bet
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False

            self.menu_movement_sound.play()  # Play the sound effect once
            self.bet -= min_bet

        if self.bet <= min_bet:
            self.bet = min_bet
        elif self.bet >= max_bet:
            self.bet = max_bet
        print(max_bet)

    def game_over_helper(self, controller, state: "GameState"):
        no_money_game_over = 0

        no_stamina_game_over = 0

        if state.player.money <= no_money_game_over:

            if controller.isTPressed or state.controller.isAPressedSwitch:
                controller.isTPressed = False

                controller.isAPressedSwitch = False

                state.currentScreen = state.gameOverScreen

                state.gameOverScreen.start(state)

        elif state.player.stamina_points <= no_stamina_game_over:

            if controller.isTPressed or state.controller.isAPressedSwitch:
                controller.isTPressed = False

                controller.isAPressedSwitch = False

                state.player.money -= 100

                self.reset_high_low_game()

                state.currentScreen = state.area3RestScreen

                state.area3RestScreen.start(state)

    def draw_magic_menu_selection_box(self, state):
        if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value:
            pass


        elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value:
            pass


        elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)


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

        for idx, choice in enumerate(self.magic_menu_selector):
            y_position = start_y_right_box + idx * choice_spacing  # Use the defined spacing variable
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        # Draw the arrow at the current magic screen index position
        arrow_y_position = start_y_right_box + (self.magic_screen_index * choice_spacing) + text_y_offset
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_offset, arrow_y_position)  # Use the arrow offsets
        )

    def update_magic_menu_selection_box(self, controller, state):
        if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value:
            pass
        elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value:

            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].reset()
        elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
            self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)



        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index - self.index_stepper) % len(self.magic_menu_selector)
            # print(f"Current Magic Menu Selector: {self.magic_menu_selector[self.magic_screen_index]}")
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False
            self.menu_movement_sound.play()
            self.magic_screen_index = (self.magic_screen_index + self.index_stepper) % len(self.magic_menu_selector)
            # print(f"Current Magic Menu Selector: {self.magic_menu_selector[self.magic_screen_index]}")

        if controller.isTPressed or controller.isAPressedSwitch:
            controller.isTPressed = False
            controller.isAPressedSwitch = False
            if self.magic_menu_selector[self.magic_screen_index] == Magic.SHIELD.value:

                self.game_state = self.WELCOME_SCREEN
            elif self.magic_menu_selector[self.magic_screen_index] == Magic.HEADS_FORCE.value:

                self.game_state = self.WELCOME_SCREEN
            elif self.magic_menu_selector[self.magic_screen_index] == self.BACK:
                self.game_state = self.WELCOME_SCREEN
