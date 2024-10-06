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
        self.music_file_level_up: pygame.mixer.Sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/levelup.mp3")
        self.music_level_up_volume: float = 0.3  # Adjust as needed
        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")
        self.menu_movement_sound.set_volume(0.2)




    WELCOME_SCREEN = "welcome_screen"
    MAGIC_MENU_SCREEN= "magic_menu_screen"
    BET_MENU_SCREEN = "bet_menu_screen"
    LEVEL_UP_SCREEN = "level_up_screen"
    GAME_OVER_SCREEN = "game_over_screen"

    WELCOME_MESSAGE = "welcome_message"
    BET_MESSAGE = "bet_message"


    def start(self, state: 'GameState') -> None:
        state.player.canMove = False
        pygame.display.set_caption(self.screenName)

    def update(self, state: 'GameState') -> None:

        controller = state.controller
        controller.update()
        if self.game_state == self.WELCOME_SCREEN:
            if state.player.stamina_points <= self.player_stamina_depleted:
                state.player.canMove = True
                self.game_state = self.GAME_OVER_SCREEN

            if state.player.money <= self.player_bankrupt:
                self.game_state = self.GAME_OVER_SCREEN

            if self.money <= self.enemy_bankrupt:
                state.player.canMove = True
                self.game_state = self.GAME_OVER_SCREEN

            if state.player.leveling_up == True:
                self.game_state = self.LEVEL_UP_SCREEN

            if controller.isUpPressed:
                controller.isUpPressed = False
                self.menu_movement_sound.play()
                # the % modulus  operator keeps our number in the index range
                self.welcome_screen_index = (self.welcome_screen_index - self.move_index_by_1) % len(self.welcome_screen_choices)
            elif controller.isDownPressed:
                controller.isDownPressed = False
                self.menu_movement_sound.play()
                self.welcome_screen_index = (self.welcome_screen_index - self.move_index_by_1) % len(self.welcome_screen_choices)



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
            self.battle_messages["level_up"].messages = [
                f"Grats you leveled up to level {state.player.level}!",
                f"Max Stamina increased by {state.player.stamina_increase_from_level} points!",
                f"Max focus increased by {state.player.focus_increase_from_level} points!",
                ""
            ]
            self.battle_messages["level_up"].update(state)
            if self.battle_messages["level_up"].is_finished():
                state.player.leveling_up = False
                self.battle_messages["level_up"].reset()
                if state.opossumInACanCandyScreen.level_anchor == True:
                    self.game_state = "play_again_or_leave_screen"
                    self.level_up_checker_sound = True

                else:
                    self.game_state = "welcome_screen"
                    self.level_up_checker_sound = True


        elif state.player.stat_point_increase == True:


            self.battle_messages["level_up"].messages = [
                f"Grats you leveled up to level {state.player.level}!",
                f"Max Stamina increased by {state.player.stamina_increase_from_level} points!",
                f"Max focus increased by {state.player.focus_increase_from_level} points!",
                f"You gained a stat point, please allocate, stat points at this level max at 2."
            ]
            self.battle_messages["level_up"].update(state)

            if self.battle_messages["level_up"].message_index == 3 and self.battle_messages["level_up"].current_message_finished():
                if controller.isUpPressed:
                    self.level_up_stat_increase_index = (self.level_up_stat_increase_index - 1) % len(self.level_screen_stats)
                    controller.isUpPressed = False
                elif controller.isDownPressed:
                    self.level_up_stat_increase_index = (self.level_up_stat_increase_index + 1) % len(self.level_screen_stats)
                    controller.isDownPressed = False

                selected_stat = self.level_screen_stats[self.level_up_stat_increase_index]

                if selected_stat == "Body" and state.controller.isTPressed and state.player.body < 2:
                    state.player.body += 1
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.player.leveling_up = False

                    state.player.max_stamina_points += state.player.level_2_body_stamina_increase
                    state.player.stamina_points += state.player.level_2_body_stamina_increase
                    self.battle_messages["level_up"].reset()
                    if state.opossumInACanCandyScreen.level_anchor == True:
                        self.level_up_checker_sound = True

                        self.game_state = "play_again_or_leave_screen"
                    else:
                        self.level_up_checker_sound = True

                        self.game_state = "welcome_screen"


                elif selected_stat == "Mind" and state.controller.isTPressed and state.player.mind < 2:
                    state.player.mind += 1
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.player.leveling_up = False
                    Magic.CRAPS_LUCKY_7.add_magic_to_player(state.player, Magic.CRAPS_LUCKY_7)
                    self.battle_messages["level_up"].reset()
                    state.player.max_focus_points += state.player.level_2_mind_focus_increase
                    state.player.focus_points += state.player.level_2_mind_focus_increase
                    if state.opossumInACanCandyScreen.level_anchor == True:
                        self.level_up_checker_sound = True

                        self.game_state = "play_again_or_leave_screen"
                    else:
                        self.level_up_checker_sound = True

                        self.game_state = "welcome_screen"


                elif selected_stat == "Spirit" and state.controller.isTPressed and state.player.spirit < 2:
                    state.player.spirit += 1
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.player.leveling_up = False
                    self.battle_messages["level_up"].reset()
                    if state.opossumInACanCandyScreen.level_anchor == True:
                        self.level_up_checker_sound = True

                        self.game_state = "play_again_or_leave_screen"
                    else:
                        self.level_up_checker_sound = True

                        self.game_state = "welcome_screen"


                elif selected_stat == "Perception" and state.controller.isTPressed and state.player.perception < 2:
                    state.player.perception += 1
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.player.leveling_up = False
                    self.battle_messages["level_up"].reset()
                    if state.opossumInACanCandyScreen.level_anchor == True:
                        self.level_up_checker_sound = True

                        self.game_state = "play_again_or_leave_screen"
                    else:
                        self.level_up_checker_sound = True

                        self.game_state = "welcome_screen"
                    # state.player.base_perception += 1


                elif selected_stat == "Perception" and state.controller.isTPressed and state.player.perception < 3 and \
                        Equipment.SOCKS_OF_PERCEPTION.value in state.player.equipped_items:
                    state.player.perception += 1
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.player.leveling_up = False
                    self.battle_messages["level_up"].reset()
                    if state.opossumInACanCandyScreen.level_anchor == True:
                        self.level_up_checker_sound = True

                        self.game_state = "play_again_or_leave_screen"
                    else:
                        self.level_up_checker_sound = True

                        self.game_state = "welcome_screen"

                elif selected_stat == "Luck" and state.controller.isTPressed and state.player.luck < 2:
                    state.player.luck += 1
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.player.leveling_up = False
                    self.battle_messages["level_up"].reset()
                    if state.opossumInACanCandyScreen.level_anchor == True:
                        self.level_up_checker_sound = True

                        self.game_state = "play_again_or_leave_screen"
                    else:
                        self.level_up_checker_sound = True

                        self.game_state = "welcome_screen"

                elif selected_stat == "Luck" and state.controller.isTPressed and state.player.luck < 3 and \
                        state.player.enhanced_luck == True:
                    state.player.luck += 1
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.player.leveling_up = False
                    self.battle_messages["level_up"].reset()
                    if state.opossumInACanCandyScreen.level_anchor == True:
                        self.level_up_checker_sound = True

                        self.game_state = "play_again_or_leave_screen"
                    else:
                        self.level_up_checker_sound = True

                        self.game_state = "welcome_screen"


    def draw(self, state: 'GameState') -> None:
        state.DISPLAY.fill(BLUEBLACK)

    def draw_level_up(self, state: 'GameState') -> None:
        if state.player.stat_point_increase and self.game_state == "level_up_screen":
            if self.battle_messages["level_up"].message_index == 3:
                black_box_height = 261 - 50  # Adjust height
                black_box_width = 240 - 10  # Adjust width to match the left box
                border_width = 5
                start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
                start_y_right_box = 200  # Adjust vertical alignment

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
                for idx, choice in enumerate(self.level_screen_stats):
                    y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
                    state.DISPLAY.blit(
                        self.font.render(choice, True, (255, 255, 255)),
                        (start_x_right_box + 60, y_position + 15)
                    )

                # Draw the selection arrow
                arrow_y_positions = [12, 52, 92, 132, 172]  # Y positions for each arrow
                arrow_y = start_y_right_box + arrow_y_positions[self.level_up_stat_increase_index]
                state.DISPLAY.blit(
                    self.font.render("->", True, (255, 255, 255)),
                    (start_x_right_box + 12, arrow_y)
                )

                # Draw the player's current stats (just the numbers) to the right of the menu (30 pixels to the right)
                stats_x_position = start_x_right_box + black_box_width - 30

                # Calculate the actual stats, taking into account equipment and enhancements
                perception = state.player.perception
                luck = state.player.luck

                # Handle enhanced luck (do not show +1 when displaying luck stat)
                if state.player.enhanced_luck:
                    luck -= 1  # Do not show the temporary +1 from enhanced luck

                # Handle perception enhancement (do not show +1 when "Socks of Perception" are equipped)
                if Equipment.SOCKS_OF_PERCEPTION.value in state.player.equipped_items:
                    perception -= 1  # Do not show the temporary +1 from the item

                # Display just the numbers next to the level-up screen
                current_stats = [
                    state.player.body,
                    state.player.mind,
                    state.player.spirit,
                    perception,  # Adjusted perception
                    luck  # Adjusted luck
                ]

                # Display the stats numbers only
                for idx, stat_value in enumerate(current_stats):
                    y_position = start_y_right_box + idx * 40  # Same vertical spacing as the level-up menu
                    state.DISPLAY.blit(
                        self.font.render(f"{stat_value}", True, (255, 255, 255)),
                        (stats_x_position, y_position + 15)
                    )

        # Continue with other drawing logic, like drawing battle messages
        self.battle_messages["level_up"].draw(state)

    def draw_menu_selection_box(self, state: "GameState"):
        # Define local variables for dimensions and positions
        box_height_offset = 50
        box_width_offset = 10
        border_width = 5
        horizontal_padding = 25
        vertical_position = 240
        box_initial_height = 221
        border_padding = 2
        box_initial_width = 200

        # Calculate the adjusted box dimensions
        black_box_height = box_initial_height - box_height_offset
        black_box_width = box_initial_width - box_width_offset

        # Determine the position of the right box
        start_x_right_box = state.DISPLAY.get_width() - black_box_width - horizontal_padding
        start_y_right_box = vertical_position

        # Create the black box
        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill(BLACK)

        # Create a white border
        white_border = pygame.Surface(
            (black_box_width + border_padding * border_width, black_box_height + border_padding * border_width)
        )
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))

        # Determine the position of the white-bordered box
        black_box_x = start_x_right_box - border_width
        black_box_y = start_y_right_box - border_width

        # Blit the white-bordered box onto the display
        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

    def draw_enemy_info_box(self, state: "GameState") -> None:
        # Define local variables for dimensions
        black_box_width = 190
        black_box_height_1 = 100
        black_box_height_2 = 120
        border_width = 5
        padding_x = 25
        padding_y_1 = 20
        padding_y_2 = 60
        border_padding = 2


        # Draw first black box with border
        black_box = pygame.Surface((black_box_width, black_box_height_1))
        black_box.fill(BLACK)
        white_border = pygame.Surface((black_box_width + border_padding * border_width, black_box_height_1 + border_padding * border_width))
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (padding_x, padding_y_1))

        # Draw second black box with border
        black_box = pygame.Surface((black_box_width, black_box_height_2))
        black_box.fill(BLACK)
        white_border = pygame.Surface((black_box_width + 2 * border_width, black_box_height_2 + 2 * border_width))
        white_border.fill(WHITE)
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (padding_x, padding_y_2))

    def draw_hero_info_boxes(self, state: "GameState") -> None:
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
