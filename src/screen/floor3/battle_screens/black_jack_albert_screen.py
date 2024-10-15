import pygame
import random
from constants import WHITE, RED, DISPLAY, BLACK
from deck import Deck
from entity.gui.screen.gamble_screen import GambleScreen
from entity.gui.textbox.message_box import MessageBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic


class BlackJackAlbertScreen(GambleScreen):
    def __init__(self, screenName: str = "Black Jack") -> None:
        super().__init__(screenName)
        self.enemy_card_y_positions: list[int] = []
        self.player_card_y_positions: list[int] = []
        self.game_state: str = self.WELCOME_SCREEN
        self.deck: Deck() = Deck()
        self.player_hand: list[str] = []
        self.enemy_hand: list[str] = []
        self.player_score: int = 0
        self.enemy_score: int = 0
        self.ace_detected_time = None
        self.ace_effect_triggered = False
        self.lucky_strike: pygame.mixer.Sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/luckystrike.wav")  # Adjust the path as needed
        self.lucky_strike.set_volume(0.6)
        self.bet: int = 100
        self.money: int = 1000
        self.albert_bankrupt: int = 0
        self.reveal_buff_counter: int = 0
        self.reveal_start_duration: int = 7
        self.reveal_end_not_active: int = 0
        self.magic_lock: bool = False
        self.dealer_name: str = "albert"
        self.lock_down_inactive: int = 0
        self.initial_hand: int = 2
        self.hedge_hog_time: bool = False
        self.player_action_phase_index = 0
        self.player_action_phase_play_index = 0
        self.player_action_phase_draw_index = 1
        self.player_action_phase_force_redraw_index = 2
        self.redraw_counter = True
        self.player_action_phase_choices: list[str] = ["Play", "Draw"]
        self.magic_screen_choices: list[str] = [Magic.REVEAL.value, "back"]
        self.redraw_debuff_counter: int = 0
        self.redraw_end_counter: int = 0
        self.redraw_start_counter: int = 10
        self.reveal_debuff_counter: int = 0
        self.reveal_end_counter: int = 0
        self.reveal_start_counter: int = 10
        self.magic_menu_index = 0
        self.magic_menu_reveal_index = 0
        self.redraw_magic_menu_index = 1
        self.back_magic_menu_index = 2
        self.index_stepper: int = 1
        self.spell_sound: pygame.mixer.Sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.reveal_cast_cost = 50
        self.redraw_cast_cost = 30



        self.battle_messages: dict[str, MessageBox] = {
            self.WELCOME_MESSAGE: MessageBox([
                "This is the welcome screen"
            ]),
            self.BET_MESSAGE: MessageBox([
                "Max bet of 75 during Come out Roll. Point Roll Max is 200"
            ]),
            self.MAGIC_MENU_REVEAL_DESCRIPTION: MessageBox([
                "You can feel the print of the face down card."
            ]),
            self.MAGIC_MENU_REDRAW_DESCRIPTION: MessageBox([
                "Asks the enemy very nicely to redraw their face up card."
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
                "BOth of you got 21 its a draw"
            ]),
            self.PLAYER_ACTION_MESSAGE: MessageBox([
                "Time for action"
            ]),
        }

    PLAYER_ACTION_MESSAGE: str = "player_action_message"
    PLAYER_ACTION_SCREEN: str = "player_action_screen"
    PLAYER_BLACK_JACK_MESSAGE: str = "player_black_jack_message"
    ENEMY_BLACK_JACK_MESSAGE: str = "enemy_black_jack_message"
    PLAYER_ENEMY_DRAW_BLACK_JACK_MESSAGE: str = "player_enemy_draw_jack_message"

    DRAW_CARD_MESSAGE: str = "draw card message"
    MAGIC_MENU_REVEAL_DESCRIPTION: str = "magic_menu_reveal_description"
    MAGIC_MENU_BACK_DESCRIPTION: str = "magic_menu_back_description"
    MAGIC_MENU_REDRAW_DESCRIPTION: str = "magic_menu_redraw_description"
    BET_MESSAGE: str = "bet_message"
    REVEAL: str = "reveal"
    REDRAW: str = "redraw"

    DRAW_CARD_SCREEN: str = "draw card screen"
    PLAYER_ENEMY_DRAW_BLACK_JACK_SCREEN: str = "player_enemy_draw_jack_screen "
    PLAYER_BLACK_JACK_SCREEN: str = "player_black_jack_screen"
    ENEMY_BLACK_JACK_SCREEN: str = "enemy_black_jack_screen"
    BACK = "back"

    #demon: why do you guys always draw 1 card per player per round why not just give players thier carss , its faster that way
    # you silly humans make no logical sense

    def start(self, state: 'GameState'):
        self.deck.shuffle()
        # passtt

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
            self.welcome_screen_update_logic(state, controller)
            self.battle_messages[self.WELCOME_MESSAGE].update(state)
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.update_magic_menu(state, controller)
            if Magic.BLACK_JACK_REDRAW.value in state.player.magicinventory:
                if self.magic_menu_index == 0:
                    self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].update(state)
                elif self.magic_menu_index == 1:
                    self.battle_messages[self.MAGIC_MENU_REDRAW_DESCRIPTION].update(state)
                elif self.magic_menu_index == 2:
                    self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)
            elif Magic.BLACK_JACK_REDRAW.value not in state.player.magicinventory:
                if self.magic_menu_index == 0:
                    self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].update(state)
                elif self.magic_menu_index == 1:
                    self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].update(state)
        elif self.game_state == self.DRAW_CARD_SCREEN:
            self.update_draw_card_screen_logic(state)
            self.battle_messages[self.DRAW_CARD_MESSAGE].update(state)
        elif self.game_state == self.PLAYER_ENEMY_DRAW_BLACK_JACK_SCREEN:
            self.battle_messages[self.PLAYER_ENEMY_DRAW_BLACK_JACK_MESSAGE].update(state)
        elif self.game_state == self.PLAYER_BLACK_JACK_SCREEN:
            self.battle_messages[self.PLAYER_BLACK_JACK_MESSAGE].update(state)
        elif self.game_state == self.ENEMY_BLACK_JACK_SCREEN:
            self.battle_messages[self.ENEMY_BLACK_JACK_MESSAGE].update(state)
        elif self.game_state == self.PLAYER_ACTION_SCREEN:
            self.update_player_action_logic(state, controller)
            self.battle_messages[self.PLAYER_ACTION_MESSAGE].update(state)




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
        elif self.game_state == self.MAGIC_MENU_SCREEN:
            self.draw_magic_menu_selection_box(state)
            if Magic.BLACK_JACK_REDRAW.value in state.player.magicinventory:
                if self.magic_menu_index == 0:
                    self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].draw(state)
                elif self.magic_menu_index == 1:
                    self.battle_messages[self.MAGIC_MENU_REDRAW_DESCRIPTION].draw(state)
                elif self.magic_menu_index == 2:
                    self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)
            elif Magic.BLACK_JACK_REDRAW.value not in state.player.magicinventory:
                if self.magic_menu_index == 0:
                    self.battle_messages[self.MAGIC_MENU_REVEAL_DESCRIPTION].draw(state)
                elif self.magic_menu_index == 1:
                    self.battle_messages[self.MAGIC_MENU_BACK_DESCRIPTION].draw(state)







        elif self.game_state == self.DRAW_CARD_SCREEN:
            self.draw_draw_card_screen(state)
            self.battle_messages[self.DRAW_CARD_MESSAGE].draw(state)
        elif self.game_state == self.PLAYER_ENEMY_DRAW_BLACK_JACK_SCREEN:
            self.draw_hands(
                player_hand=self.player_hand,  # Player's hand
                enemy_hand=self.enemy_hand,  # Enemy's hand
                initial_x_position=250,  # Starting X position
                player_target_y_position=300,  # Player's Y position
                enemy_target_y_position=50,  # Enemy's Y position
                move_card_x=75,  # Horizontal gap between cards
                flip_y_position=145,  # Y position where cards flip
                deck=self.deck,  # Deck object to draw cards
                display=state.DISPLAY  # This is your correct display reference
            )

            self.battle_messages[self.PLAYER_ENEMY_DRAW_BLACK_JACK_MESSAGE].draw(state)

        elif self.game_state == self.PLAYER_BLACK_JACK_SCREEN:
            self.draw_hands(
                player_hand=self.player_hand,  # Player's hand
                enemy_hand=self.enemy_hand,  # Enemy's hand
                initial_x_position=250,  # Starting X position
                player_target_y_position=300,  # Player's Y position
                enemy_target_y_position=50,  # Enemy's Y position
                move_card_x=75,  # Horizontal gap between cards
                flip_y_position=145,  # Y position where cards flip
                deck=self.deck,  # Deck object to draw cards
                display=state.DISPLAY  # This is your correct display reference
            )
            self.battle_messages[self.PLAYER_BLACK_JACK_MESSAGE].draw(state)


        elif self.game_state == self.ENEMY_BLACK_JACK_SCREEN:
            self.draw_hands(
                player_hand=self.player_hand,  # Player's hand
                enemy_hand=self.enemy_hand,  # Enemy's hand
                initial_x_position=250,  # Starting X position
                player_target_y_position=300,  # Player's Y position
                enemy_target_y_position=50,  # Enemy's Y position
                move_card_x=75,  # Horizontal gap between cards
                flip_y_position=145,  # Y position where cards flip
                deck=self.deck,  # Deck object to draw cards
                display=state.DISPLAY  # This is your correct display reference
            )
            self.battle_messages[self.ENEMY_BLACK_JACK_MESSAGE].draw(state)


        elif self.game_state == self.PLAYER_ACTION_SCREEN:
            self.draw_hands(
                player_hand=self.player_hand,  # Player's hand
                enemy_hand=self.enemy_hand,  # Enemy's hand
                initial_x_position=250,  # Starting X position
                player_target_y_position=300,  # Player's Y position
                enemy_target_y_position=50,  # Enemy's Y position
                move_card_x=75,  # Horizontal gap between cards
                flip_y_position=145,  # Y position where cards flip
                deck=self.deck,  # Deck object to draw cards
                display=state.DISPLAY  # This is your correct display reference
            )
            self.draw_menu_selection_box(state)
            self.draw_player_action_right_menu(state)

            self.battle_messages[self.PLAYER_ACTION_MESSAGE].draw(state)





        pygame.display.flip()

    def update_magic_menu(self, state: "GameState", controller):
        controller = state.controller

        if controller.isUpPressed:
            controller.isUpPressed = False
            self.menu_movement_sound.play()
            self.magic_menu_index = (self.magic_menu_index - self.index_stepper) % len(self.magic_screen_choices)
        elif controller.isDownPressed:
            controller.isDownPressed = False
            self.menu_movement_sound.play()
            self.magic_menu_index = (self.magic_menu_index + self.index_stepper) % len(self.magic_screen_choices)

        if controller.isTPressed:
            controller.isTPressed = False

            # Handle "Redraw" if it's available and selected
            if Magic.BLACK_JACK_REDRAW.value in self.magic_screen_choices and self.magic_menu_index == self.magic_screen_choices.index(Magic.BLACK_JACK_REDRAW.value):
                if state.player.focus_points >= self.redraw_cast_cost:
                    self.redraw_debuff_counter = self.redraw_start_counter
                    self.spell_sound.play()  # Play the sound effect once
                    state.player.focus_points -= self.redraw_cast_cost
                    self.magic_lock = True
                    self.game_state = self.WELCOME_SCREEN

            # Handle "Reveal" if selected
            elif Magic.REVEAL.value in self.magic_screen_choices and self.magic_menu_index == self.magic_screen_choices.index(Magic.REVEAL.value):
                if state.player.focus_points >= self.reveal_cast_cost:
                    self.reveal_buff_counter = self.reveal_start_counter
                    self.spell_sound.play()  # Play the sound effect for Reveal
                    state.player.focus_points -= self.reveal_cast_cost
                    self.magic_lock = True
                    self.game_state = self.WELCOME_SCREEN

            # Always handle "Back" properly
            elif self.magic_screen_choices[self.magic_menu_index] == "back":
                self.game_state = self.WELCOME_SCREEN

    def draw_magic_menu_selection_box(self, state):
        choice_spacing = 40
        text_x_offset = 60
        text_y_offset = 15
        arrow_x_offset = 12
        black_box_height = 221 - 50  # Adjust height
        black_box_width = 200 - 10  # Adjust width to match the left box
        border_width = 5
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
        start_y_right_box = 240  # Adjust vertical alignment

        # Create the black box and white border
        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill(BLACK)

        white_border = pygame.Surface(
            (black_box_width + 2 * border_width, black_box_height + 2 * border_width)
        )
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))

        black_box_x = start_x_right_box - border_width
        black_box_y = start_y_right_box - border_width

        # Blit the border with the black box inside
        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

        # Conditionally insert Magic.BLACK_JACK_REDRAW.value into position 1 if available in player's magic inventory
        if Magic.BLACK_JACK_REDRAW.value in state.player.magicinventory and Magic.BLACK_JACK_REDRAW.value not in self.magic_screen_choices:
            self.magic_screen_choices.insert(1, Magic.BLACK_JACK_REDRAW.value)

        # Render the choices and handle the arrow dynamically
        for idx, choice in enumerate(self.magic_screen_choices):
            y_position = start_y_right_box + idx * choice_spacing  # Use dynamic spacing
            state.DISPLAY.blit(
                self.font.render(choice, True, WHITE),
                (start_x_right_box + text_x_offset, y_position + text_y_offset)  # Use the defined offsets
            )

        # Draw the arrow dynamically based on the selected index
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

        # Ensure "Redraw" is added before rendering if it's available
        if self.redraw_debuff_counter > self.redraw_end_counter and Magic.BLACK_JACK_REDRAW.value not in self.player_action_phase_choices:
            self.player_action_phase_choices.insert(2, Magic.BLACK_JACK_REDRAW.value)

        # Loop through the choices and render each one
        for idx, choice in enumerate(self.player_action_phase_choices):
            y_position = start_y_right_box + idx * spacing_between_choices

            # Check if the current choice is "Redraw" and if redraw_counter is False
            if choice == Magic.BLACK_JACK_REDRAW.value and self.redraw_counter == False:
                rendered_choice = self.font.render(choice, True, RED)
            else:
                rendered_choice = self.font.render(choice, True, WHITE)

            # Blit the rendered text
            state.DISPLAY.blit(rendered_choice, (start_x_right_box + text_x_offset, y_position + text_y_offset))

        # Draw the arrow based on the current index
        arrow_y_coordinate = arrow_center + start_y_right_box + self.player_action_phase_index * spacing_between_choices
        state.DISPLAY.blit(
            self.font.render("->", True, WHITE),
            (start_x_right_box + arrow_x_coordinate_padding, arrow_y_coordinate)
        )


    def update_player_action_logic(self, state: "GameState", controller):

        if controller.isUpPressed:
            controller.isUpPressed = False
            self.menu_movement_sound.play()
            self.player_action_phase_index = (self.player_action_phase_index - self.move_index_by_1) % len(self.player_action_phase_choices)
            print(f"Current index: {self.player_action_phase_index}")  # Debug print to see the index
        elif controller.isDownPressed:
            controller.isDownPressed = False
            self.menu_movement_sound.play()
            self.player_action_phase_index = (self.player_action_phase_index + self.move_index_by_1) % len(self.player_action_phase_choices)
            print(f"Current index: {self.player_action_phase_index}")  # Debug print to see the index

        elif state.controller.isTPressed:
            state.controller.isTPressed = False
            if self.player_action_phase_index == self.player_action_phase_play_index:
                pass
            if self.player_action_phase_index == self.player_action_phase_draw_index:
                pass
            if self.player_action_phase_index == self.player_action_phase_force_redraw_index and self.redraw_counter == True:
                self.enemy_hand.pop(1)
                new_card = self.deck.enemy_draw_hand(1)[0]  # Draw one card
                self.enemy_hand.insert(1, new_card)
                self.redraw_counter = False
    def draw_hands(self, player_hand: list, enemy_hand: list,
                   initial_x_position: int, player_target_y_position: int,
                   enemy_target_y_position: int, move_card_x: int, flip_y_position: int, deck, display):
        """Draws both player and enemy hands on the screen using state.DISPLAY."""

        # Draw player's hand
        for i, card in enumerate(player_hand):
            player_x_position = initial_x_position + i * move_card_x
            player_y_position = player_target_y_position

            if i == 1 and player_y_position >= flip_y_position:
                deck.draw_card_face_up(card[1], card[0], (player_x_position, player_y_position), display)
            else:
                deck.draw_card_face_up(card[1], card[0], (player_x_position, player_y_position), display)

        # Draw enemy's hand
        for i, card in enumerate(enemy_hand):
            enemy_x_position = initial_x_position + i * move_card_x
            enemy_y_position = enemy_target_y_position

            if i == 0:
                deck.draw_card_face_down((enemy_x_position, enemy_y_position), display)
            else:
                deck.draw_card_face_up(card[1], card[0], (enemy_x_position, enemy_y_position), display)

    def update_draw_card_screen_logic(self, state: 'GameState'):
        luck_muliplier = 5
        lucky_roll = random.randint(1, 100)
        player_bad_score_min_range = 12
        player_bad_score_max_range = 17
        level_1_luck_score = 0
        lucky_strike_threshhold = 75
        initial_hand = 2
        adjusted_lucky_roll = lucky_roll + state.player.luck * luck_muliplier
        # Only draw cards if the hands are empty
        if len(self.player_hand) == 0 and len(self.enemy_hand) == 0:

            self.player_hand = self.deck.player_draw_hand(2)
            self.enemy_hand = self.deck.enemy_draw_hand(2)


            # Compute enemy hand value
            self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)



            # self.player_hand = self.deck.player_draw_hand(2)
            self.player_score = self.deck.compute_hand_value(self.player_hand)

            print("player hand  before effect  : " + str(self.player_hand))
            print("player sc0ret  : " + str(self.player_score))
            print("enemy hand is : " + str(self.enemy_hand))
            print("enemy sc0ret  : " + str(self.enemy_score))


            if state.player.luck > level_1_luck_score:
                if self.player_score > player_bad_score_min_range and self.player_score < player_bad_score_max_range:

                    if adjusted_lucky_roll >= lucky_strike_threshhold:
                        # print(adjusted_lucky_roll)
                        self.lucky_strike.play()
                        while self.player_score > player_bad_score_min_range and self.player_score < player_bad_score_max_range:
                            # this could, at a low % chance, empty out the deck and crash. maybe have 3 re rolls max
                            self.player_hand = self.deck.player_draw_hand(initial_hand)
                            self.player_score = self.deck.compute_hand_value(self.player_hand)
                            self.critical_hit = True
                            print("player hand after affect : " + str(self.player_hand))




    def draw_draw_card_screen(self, state: 'GameState'):


        card_one = 0
        card_two = 1
        initial_x_position = 250
        initial_y_position = 1
        player_target_y_position = 300
        enemy_target_y_position = 50
        move_card_x = 75
        card_speed = 3  # Adjust this for speed of movement
        flip_y_position = 145  # Define the y-position where the card will flip

        # Ensure that both player_hand and enemy_hand are not empty
        if len(self.player_hand) == card_one or len(self.enemy_hand) == card_one:
            print("Error: player_hand or enemy_hand is empty.")
            return  # Exit if either hand is empty to prevent further errors

        # Initialize card_y_positions and card_x_positions for both player and enemy if they don't already exist
        if not hasattr(self, 'player_card_y_positions') or len(self.player_card_y_positions) != len(self.player_hand):
            self.player_card_y_positions = [initial_y_position] * len(self.player_hand)
            self.player_card_x_positions = [initial_x_position + i * move_card_x for i in range(len(self.player_hand))]

        if not hasattr(self, 'enemy_card_y_positions') or len(self.enemy_card_y_positions) != len(self.enemy_hand):
            self.enemy_card_y_positions = [initial_y_position] * len(self.enemy_hand)
            self.enemy_card_x_positions = [initial_x_position + i * move_card_x for i in range(len(self.enemy_hand))]

        # Deal player cards one at a time
        # Deal player cards one at a time
        all_player_cards_dealt = True
        for i, card in enumerate(self.player_hand):
            if self.player_card_y_positions[i] < player_target_y_position:
                self.player_card_y_positions[i] += card_speed
                if self.player_card_y_positions[i] > player_target_y_position:
                    self.player_card_y_positions[i] = player_target_y_position

                # Flip the second player's card at flip_y_position
                if i == 1 and self.player_card_y_positions[i] >= flip_y_position:
                    # Draw the player's second card face up once it reaches flip position
                    self.deck.draw_card_face_up(card[1], card[0],
                                                (self.player_card_x_positions[i], self.player_card_y_positions[i]), DISPLAY)
                else:
                    # Draw player card face down while moving (for all other cards or until it reaches target)
                    self.deck.draw_card_face_down((self.player_card_x_positions[i], self.player_card_y_positions[i]), DISPLAY)

                all_player_cards_dealt = False  # Still dealing player cards
                return  # Ensure we deal one card at a time

            # Draw player card face up once it reaches target position
            self.deck.draw_card_face_up(card[card_two], card[card_one], (self.player_card_x_positions[i], self.player_card_y_positions[i]), DISPLAY)

        # If all player cards are dealt, start dealing enemy cards
        # If all player cards are dealt, start dealing enemy cards one at a time
        if all_player_cards_dealt:
            for i, card in enumerate(self.enemy_hand):
                if self.enemy_card_y_positions[i] < enemy_target_y_position:
                    self.enemy_card_y_positions[i] += card_speed
                    if self.enemy_card_y_positions[i] > enemy_target_y_position:
                        self.enemy_card_y_positions[i] = enemy_target_y_position

                    # Always draw enemy card face down while moving
                    self.deck.draw_card_face_down((self.enemy_card_x_positions[i], self.enemy_card_y_positions[i]), DISPLAY)
                    return  # Ensure we deal one card at a time

                # Always draw the first enemy card (index 0) face down, even at the target position
                if i == card_one:
                    self.deck.draw_card_face_down((self.enemy_card_x_positions[i], self.enemy_card_y_positions[i]), DISPLAY)
                else:
                    # Draw the remaining enemy cards face up once they reach the target position
                    self.deck.draw_card_face_up(card[card_two], card[card_one], (self.enemy_card_x_positions[i], self.enemy_card_y_positions[i]), DISPLAY)

        # Redraw all player cards that have been dealt and are at their final positions
        for i, card in enumerate(self.player_hand):
            self.deck.draw_card_face_up(card[card_two], card[card_one], (self.player_card_x_positions[i], self.player_card_y_positions[i]), DISPLAY)

        # Redraw all enemy cards that have been dealt and are at their final positions
        # Redraw all enemy cards that have been dealt and are at their final positions
        for i, card in enumerate(self.enemy_hand):
            if i == 0:
                # Always draw the first enemy card face down
                self.deck.draw_card_face_down((self.enemy_card_x_positions[i], self.enemy_card_y_positions[i]), DISPLAY)
            else:
                # Draw all remaining enemy cards face up
                self.deck.draw_card_face_up(card[card_two], card[card_one], (self.enemy_card_x_positions[i], self.enemy_card_y_positions[i]), DISPLAY)
        # Global variables to manage Ace detection


        # In your main game logic method:
        # Ace detection logic
        if Equipment.SIR_LEOPOLD_AMULET.value in state.player.equipped_items:
            if len(self.enemy_hand) > 1 and self.enemy_hand[1][0] == "Ace" and not self.ace_effect_triggered:
                if self.ace_detected_time is None:
                    self.ace_detected_time = pygame.time.get_ticks()  # Store the time when Ace is detected
                    print("Timer started: Ace detected")

            if self.ace_detected_time is not None:
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - self.ace_detected_time
                print(f"Elapsed time: {elapsed_time} ms")

                # Handle the Ace effect once the timer has elapsed
                if elapsed_time >= 1200:  # 1200 ms = 1.2 seconds
                    print("Ace time")
                    self.enemy_hand.pop(1)
                    new_card = self.deck.enemy_draw_hand(1)[0]
                    self.enemy_hand.insert(1, new_card)
                    self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)

                    # Reset the timer and flag
                    self.ace_effect_triggered = True
                    self.ace_detected_time = None
                    print("Ace replaced and timer reset")
                else:
                    # Return early to stop further execution if the timer hasn't expired yet
                    return

        print(self.player_score)

        # Additional game state logic
        if self.player_score == 21 and self.enemy_score == 21:
            print("I hope we maek it here")
            self.game_state = self.PLAYER_ENEMY_DRAW_BLACK_JACK_SCREEN
            return

        self.hedge_hog_time = True  # Temporarily force it to True

        if self.player_score == 21 and self.hedge_hog_time:
            print("Triggering Hedge Hog Time")

            self.game_state = self.PLAYER_BLACK_JACK_SCREEN
            return

        if self.enemy_score == 21 and self.hedge_hog_time:
            print("Triggering Hedge Hog Time")

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
        print(self.redraw_debuff_counter)
        print(self.redraw_end_counter)

        state.DISPLAY.blit(self.font.render(self.dealer_name, True, WHITE), (player_enemy_box_info_x_position, enemy_name_y_position))

        state.DISPLAY.blit(self.font.render(f"{self.MONEY_HEADER} {self.money}", True, WHITE), (player_enemy_box_info_x_position, enemy_money_y_position))
        if self.reveal_buff_counter == self.reveal_end_not_active and self.redraw_debuff_counter == self.reveal_end_counter:
            state.DISPLAY.blit(self.font.render(f"{self.STATUS_GREEN}", True, WHITE), (player_enemy_box_info_x_position, enemy_status_y_position))
        elif self.reveal_buff_counter > self.reveal_end_not_active:
            state.DISPLAY.blit(self.font.render(f"{self.REVEAL}: {self.reveal_buff_counter} ", True, WHITE), (player_enemy_box_info_x_position, enemy_status_y_position))
            state.DISPLAY.blit(self.font.render(f" {score_header}: {self.enemy_score} ", True, WHITE), (player_enemy_box_info_x_position_score, score_y_position))

        elif self.redraw_debuff_counter > self.redraw_end_counter:
            print("yess")
            state.DISPLAY.blit(self.font.render(f"{self.REDRAW}: {self.redraw_debuff_counter} ", True, WHITE), (player_enemy_box_info_x_position, enemy_status_y_position))
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
            elif self.welcome_screen_index == self.welcome_screen_magic_index and self.magic_lock == False:
                self.game_state = self.MAGIC_MENU_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_bet_index:
                self.game_state = self.BET_SCREEN
            elif self.welcome_screen_index == self.welcome_screen_quit_index:
                print("code will go here later")





