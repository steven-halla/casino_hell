from typing import Optional

import pygame
import pytmx

from constants import BLUEBLACK, WHITE, BLACK
from game_constants.equipment import Equipment
from game_constants.magic import Magic


class GambleScreen:
    def __init__(self, screenName: str, map_path: str = None):
        self.screenName: str = screenName
        self.startedAt: int = pygame.time.get_ticks()
        self.font: pygame.font.Font = pygame.font.Font(None, 36)  # Initialize the font attribute
        self.money: int = 1000  # Add this line
        self.bet: int = 50  # Add this line
        self.lock_down: int = 0
        self.level_up_stat_increase_index: int = 0  # Add this to track the selected stat
        self.level_screen_stats: list[str] = ["Body", "Mind", "Spirit", "Perception", "Luck"]
        self.stat_increase: bool = False
        self.welcome_screen_choices: list[str] = ["Play", "Magic", "Bet", "Quit"]
        self.welcome_screen_index = 0
        self.move_index_by_1 = 1
        self.welcome_screen_play_index = 0
        self.welcome_screen_magic_index = 1
        self.welcome_screen_bet_index = 2
        self.welcome_screen_quit_index = 3
        self.enemy_bankrupt = 0
        self.player_bankrupt = 0
        self.player_stamina_depleted = 0
        self.level_up_checker_sound:bool = True
        self.music_file_level_up: pygame.mixer.Sound \
            = pygame.mixer.Sound("./assets/music/levelup.mp3")
        self.music_level_up_volume: float = 0.3  # Adjust as needed
        self.menu_movement_sound \
            = pygame.mixer.Sound("./assets/music/1BItemMenuItng.wav")
        self.menu_movement_sound.set_volume(0.2)
        self.stat_modifier = 1
        self.game_level_2_stat_max = 2
        self.battle_message_level_up_last_index = 3


    WELCOME_SCREEN = "welcome_screen"
    PLAY_SCREEN = "play_screen"
    MAGIC_MENU_SCREEN= "magic_menu_screen"
    LEVEL_UP_SCREEN = "level_up_screen"
    GAME_OVER_SCREEN = "game_over_screen"
    BET_SCREEN = "bet_screen"

    WELCOME_MESSAGE = "welcome_message"
    LEVEL_UP_MESSAGE = "level_up_message"

    MAGIC = "Magic"
    LOCKED = "Locked"
    MONEY_HEADER = "Money"
    STATUS_GREEN = "Normal Status"
    BET_HEADER = "Bet"
    HP_HEADER = "HP"
    MP_HEADER = "MP"
    HERO_HEADER = "Hero"
    LOCKED_DOWN_HEADER = "Locked Down"

    PLAYER_STAT_BODY = "Body"
    PLAYER_STAT_MIND = "Mind"
    PLAYER_STAT_SPIRIT = "Spirit"
    PLAYER_STAT_PERCEPTION = "Perception"
    PLAYER_STAT_LUCK = "Luck"

    # teh below applies to all equpoment and magic
    # implemtn this at level 5
    LEVEL_1_PERCENTAGE_CHANCE = 45
    LEVEL_2_PERCENTAGE_CHANCE = 55
    LEVEL_3_PERCENTAGE_CHANCE = 65
    LEVEL_4_PERCENTAGE_CHANCE = 75
    LEVEL_5_PERCENTAGE_CHANCE = 85

    def start(self, state: 'GameState') -> None:
        # in future compaion items will affect the below by + 1

        state.player.canMove = False
        pygame.display.set_caption(self.screenName)

    def welcome_screen_logic(self, state: 'GameState') -> None:

        controller = state.controller
        controller.update()
        # if state.player.stamina_points <= self.player_stamina_depleted:
        #     state.player.canMove = True
        #     self.game_state = self.GAME_OVER_SCREEN

        if state.player.money <= self.player_bankrupt:
            self.game_state = self.GAME_OVER_SCREEN

        # if self.money <= self.enemy_bankrupt:
        #     state.player.canMove = True
        #     self.game_state = self.GAME_OVER_SCREEN

        if state.player.leveling_up == True:
            self.game_state = self.LEVEL_UP_SCREEN

        if controller.isUpPressed or controller.isUpPressedSwitch:
            controller.isUpPressed = False
            controller.isUpPressedSwitch = False
            self.menu_movement_sound.play()
            # the % modulus  operator keeps our number in the index range
            self.welcome_screen_index = (self.welcome_screen_index
                                         - self.move_index_by_1) % len(self.welcome_screen_choices)
        elif controller.isDownPressed or controller.isDownPressedSwitch:
            controller.isDownPressed = False
            controller.isDownPressedSwitch = False
            self.menu_movement_sound.play()
            self.welcome_screen_index = (self.welcome_screen_index
                                         + self.move_index_by_1) % len(self.welcome_screen_choices)





    def update(self, state: 'GameState') -> None:
        #


        if self.game_state == self.WELCOME_SCREEN:
            self.welcome_screen_logic(state)


        # if state.musicOn == True:
        #     if self.mucic_on == True:
        #         self.stop_music()
        #         self.initalize_music()
        #         self.music_on = False

        if self.bet > self.money:
            print("Resetting Money")
            self.bet = self.money

    def handle_level_up(self, state: 'GameState', controller) -> None:

        if self.level_up_checker_sound == True:
            self.music_file_level_up.play()  # Play the sound effect once
            self.level_up_checker_sound = False

        if state.player.stat_point_increase == False:
            self.battle_messages[self.LEVEL_UP_SCREEN].messages = [
                f"Grats you leveled up to level {state.player.level}!",
                f"Max Stamina increased by {state.player.stamina_increase_from_level} points!",
                f"Max focus increased by {state.player.focus_increase_from_level} points!",
                ""
            ]
            self.battle_messages[self.LEVEL_UP_MESSAGE].update(state)
            if self.battle_messages[self.LEVEL_UP_MESSAGE].is_finished():
                state.player.leveling_up = False
                self.battle_messages[self.LEVEL_UP_MESSAGE].reset()
                self.game_state = self.WELCOME_SCREEN
                self.level_up_checker_sound = True

        elif state.player.stat_point_increase == True:
            selected_stat = self.level_screen_stats[self.level_up_stat_increase_index]
            print(selected_stat)

            self.battle_messages[self.LEVEL_UP_MESSAGE].messages = [
                f"Grats you leveled up to level {state.player.level}!",
                f"Max Stamina increased by {state.player.stamina_increase_from_level} points!",
                f"Max focus increased by {state.player.focus_increase_from_level} points!",
                f"You gained a stat point, please allocate, stat points at this level max at 2."
            ]

            self.battle_messages[self.LEVEL_UP_MESSAGE].update(state)

            if (self.battle_messages[self.LEVEL_UP_MESSAGE].message_index == self.battle_message_level_up_last_index
                    and self.battle_messages[self.LEVEL_UP_MESSAGE].current_message_finished()):
                if controller.isUpPressed or controller.isUpPressedSwitch:
                    self.level_up_stat_increase_index = (self.level_up_stat_increase_index
                                                         - self.move_index_by_1) % len(self.level_screen_stats)
                    controller.isUpPressed = False
                    controller.isUpPressedSwitch = False
                elif controller.isDownPressed or controller.isDownPressedSwitch:
                    self.level_up_stat_increase_index = (self.level_up_stat_increase_index
                                                         + self.move_index_by_1) % len(self.level_screen_stats)
                    controller.isDownPressed = False
                    controller.isDownPressedSwitch = False

                selected_stat = self.level_screen_stats[self.level_up_stat_increase_index]

                if (selected_stat == self.PLAYER_STAT_BODY and state.controller.isTPressed
                        or state.controller.isAPressedSwitch and state.player.body <  self.game_level_2_stat_max):
                    state.player.body += self.stat_modifier
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.controller.isAPressedSwitch = False
                    state.player.leveling_up = False

                    state.player.max_stamina_points += state.player.level_2_body_stamina_increase
                    state.player.stamina_points += state.player.level_2_body_stamina_increase
                    self.battle_messages[self.LEVEL_UP_MESSAGE].reset()

                    self.level_up_checker_sound = True

                    self.game_state = self.WELCOME_SCREEN


                elif (selected_stat == self.PLAYER_STAT_MIND and state.controller.isTPressed
                      or state.controller.isAPressedSwitch and state.player.mind < self.game_level_2_stat_max):
                    state.player.mind += self.stat_modifier
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.controller.isAPressedSwitch = False
                    state.player.leveling_up = False
                    Magic.CRAPS_LUCKY_7.add_magic_to_player(state.player, Magic.CRAPS_LUCKY_7)
                    self.battle_messages[self.LEVEL_UP_MESSAGE].reset()
                    state.player.max_focus_points += state.player.level_2_mind_focus_increase
                    state.player.focus_points += state.player.level_2_mind_focus_increase
                    self.level_up_checker_sound = True
                    self.game_state = self.WELCOME_SCREEN


                elif (selected_stat == self.PLAYER_STAT_SPIRIT and state.controller.isTPressed
                      or state.controller.isAPressedSwitch and state.player.spirit < self.game_level_2_stat_max):
                    state.player.spirit += self.stat_modifier
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.controller.isAPressedSwitch = False
                    state.player.leveling_up = False
                    self.battle_messages[self.LEVEL_UP_MESSAGE].reset()

                    self.level_up_checker_sound = True

                    self.game_state = self.WELCOME_SCREEN


                elif (selected_stat == self.PLAYER_STAT_PERCEPTION and state.controller.isTPressed
                      or state.controller.isAPressedSwitch and state.player.perception < self.game_level_2_stat_max):
                    state.player.perception += self.stat_modifier
                    print(f"Player {selected_stat} is cow: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.controller.isAPressedSwitch = False
                    state.player.leveling_up = False
                    self.battle_messages[self.LEVEL_UP_MESSAGE].reset()
                    self.level_up_checker_sound = True
                    self.game_state = self.WELCOME_SCREEN
                    # state.player.base_perception += 1


                elif (selected_stat == self.PLAYER_STAT_PERCEPTION and state.controller.isTPressed
                      or state.controller.isAPressedSwitch and state.player.perception < 3 and \
                        Equipment.SOCKS_OF_PERCEPTION.value in state.player.equipped_items):
                    state.player.perception += self.stat_modifier
                    print(f"Player {selected_stat} is cow: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.controller.isAPressedSwitch = False
                    state.player.leveling_up = False
                    self.battle_messages[self.LEVEL_UP_MESSAGE].reset()
                    self.level_up_checker_sound = True
                    self.game_state = self.WELCOME_SCREEN

                elif (selected_stat == self.PLAYER_STAT_LUCK and state.controller.isTPressed
                      or state.controller.isAPressedSwitch and state.player.luck < self.game_level_2_stat_max):
                    state.player.luck += self.stat_modifier
                    print(f"Player {selected_stat} is noww: {getattr(state.player, selected_stat.lower())}")

                    state.controller.isTPressed = False
                    state.controller.isAPressedSwitch = False
                    state.player.leveling_up = False
                    self.battle_messages[self.LEVEL_UP_MESSAGE].reset()
                    self.level_up_checker_sound = True
                    self.game_state = self.WELCOME_SCREEN

                elif (selected_stat == self.PLAYER_STAT_LUCK and state.controller.isTPressed
                      or state.controller.isAPressedSwitch and state.player.luck < 3
                      and state.player.enhanced_luck == True):
                    state.player.luck += self.stat_modifier
                    print(f"Player {selected_stat} is nowww: {getattr(state.player, selected_stat.lower())}")
                    print("moooooooofsoadfdjsa;f;dlsjfjsa;fks")

                    state.controller.isTPressed = False
                    state.controller.isAPressedSwitch = False
                    state.player.leveling_up = False
                    self.battle_messages[self.LEVEL_UP_MESSAGE].reset()
                    self.level_up_checker_sound = True
                    self.game_state = self.WELCOME_SCREEN

    def draw(self, state: 'GameState') -> None:
        state.DISPLAY.fill(BLUEBLACK)

    def draw_level_up(self, state: 'GameState') -> None:
        do_not_show_ehanced_luck = 1
        do_not_show_ehanced_perception = 1

        if state.player.stat_point_increase and self.game_state == "level_up_screen":
            if self.battle_messages[self.LEVEL_UP_MESSAGE].message_index == self.battle_message_level_up_last_index:
                black_box_height = 261 - 50  # Adjust height
                black_box_width = 240 - 10  # Adjust width to match the left box
                border_width = 5
                start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
                start_y_right_box = 200  # Adjust vertical alignment

                black_box = pygame.Surface((black_box_width, black_box_height))
                black_box.fill(BLACK)

                white_thickness = 2

                white_border = pygame.Surface(
                    (black_box_width + white_thickness * border_width, black_box_height + white_thickness * border_width)
                )
                white_border.fill(WHITE)
                white_border.blit(black_box, (border_width, border_width))

                black_box_x = start_x_right_box - border_width
                black_box_y = start_y_right_box - border_width

                state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

                x_offset = 60
                y_offset = 15
                stat_y_padding = 40
                for idx, choice in enumerate(self.level_screen_stats):
                    y_position = start_y_right_box + idx * stat_y_padding  # Adjust spacing between choices
                    state.DISPLAY.blit(
                        self.font.render(choice, True, WHITE),
                        (start_x_right_box + x_offset, y_position + y_offset)
                    )

                arrow_x_offset = 12
                arrow_y_positions = [12, 52, 92, 132, 172]
                arrow_y = start_y_right_box + arrow_y_positions[self.level_up_stat_increase_index]
                state.DISPLAY.blit(
                    self.font.render("->", True, WHITE),
                    (start_x_right_box + arrow_x_offset, arrow_y)
                )

                current_stat_x_offset = 30
                stats_x_position = start_x_right_box + black_box_width - current_stat_x_offset

                perception = state.player.perception
                luck = state.player.luck

                if state.player.enhanced_luck:
                    luck -= do_not_show_ehanced_luck

                if Equipment.SOCKS_OF_PERCEPTION.value in state.player.equipped_items:
                    perception -= do_not_show_ehanced_perception

                current_stats = [
                    state.player.body,
                    state.player.mind,
                    state.player.spirit,
                    perception,  # Adjusted perception
                    luck  # Adjusted luck
                ]

                stat_spacing = 40
                stat_y_offset = 15

                # Display the stats numbers only
                for idx, stat_value in enumerate(current_stats):
                    y_position = start_y_right_box + idx * stat_spacing
                    state.DISPLAY.blit(
                        self.font.render(f"{stat_value}", True, WHITE),
                        (stats_x_position, y_position + stat_y_offset)
                    )

        self.battle_messages[self.LEVEL_UP_MESSAGE].draw(state)

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

    def draw_enemy_info_box(self, state: "GameState") -> None:
        black_box_width = 190
        black_box_height_1 = 100
        black_box_height_2 = 120
        border_width = 5
        padding_x = 25
        padding_y_1 = 20
        padding_y_2 = 60
        white_border_bottom_right = 2
        white_border_top_left = 2

        black_box = pygame.Surface((black_box_width, black_box_height_1))
        black_box.fill(BLACK)
        white_border = pygame.Surface((black_box_width + white_border_bottom_right * border_width, black_box_height_1 + white_border_bottom_right * border_width))
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (padding_x, padding_y_1))

        black_box = pygame.Surface((black_box_width, black_box_height_2))
        black_box.fill(BLACK)
        white_border = pygame.Surface((black_box_width + white_border_top_left * border_width, black_box_height_2 + white_border_top_left * border_width))
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (padding_x, padding_y_2))

    def draw_hero_info_boxes(self, state: "GameState") -> None:
        box_width_offset = 10
        box_height_offset_1 = 180 - box_width_offset
        box_height_offset_2 = 45 - box_width_offset
        border_thickness = 5
        display_x_position_1 = 25
        display_y_position_1 = 235
        display_y_position_2 = 195
        white_border_bottom_right = 2
        white_border_top_left = 2
        box_width = 200

        black_box = pygame.Surface((box_width - box_width_offset, box_height_offset_1))
        black_box.fill(BLACK)
        white_border = pygame.Surface((box_width - box_width_offset + white_border_top_left * border_thickness, box_height_offset_1 + white_border_top_left * border_thickness))
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_thickness, border_thickness))
        state.DISPLAY.blit(white_border, (display_x_position_1, display_y_position_1))

        black_box = pygame.Surface((box_width - box_width_offset, box_height_offset_2))
        black_box.fill(BLACK)
        white_border = pygame.Surface((box_width - box_width_offset + white_border_bottom_right * border_thickness, box_height_offset_2 + white_border_bottom_right * border_thickness))
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_thickness, border_thickness))
        state.DISPLAY.blit(white_border, (display_x_position_1, display_y_position_2))


    def draw_bottom_black_box(self, state: "GameState") -> None:
        black_box_height = 130
        black_box_width = 700
        border_width = 5
        vertical_padding = 20
        border_padding = 2
        center_divisor = 2
        black_box = pygame.Surface((black_box_width, black_box_height))

        black_box.fill(BLACK)
        white_border = pygame.Surface((black_box_width + border_padding * border_width, black_box_height + border_padding * border_width))
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))

        screen_width, screen_height = state.DISPLAY.get_size()
        black_box_x = (screen_width - black_box_width) // center_divisor - border_width
        black_box_y = screen_height - black_box_height - vertical_padding - border_width

        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))


