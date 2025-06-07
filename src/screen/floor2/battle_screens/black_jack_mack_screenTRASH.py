import random
import pygame
from constants import DISPLAY, BLUEBLACK, RED, WHITE, BLACK
from entity.gui.textbox.text_box import TextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic
from screen.examples.screen import Screen
from deck import Deck
from entity.gui.textbox.bordered_box import BorderedBox


class BlackJackMackScreen(Screen):
    def __init__(self):
        Screen.__init__(self, " Black Jack Game")
        self.money = 800
        self.deck = Deck()
        self.last_t_press_time = 0  # Initialize the last T press time
        self.font = pygame.font.Font(None, 36)
        self.ace_up_sleeve_jack = False
        self.ace_up_sleeve_jack_cheat_mode = False
        self.black_jack_rumble_bill_defeated = False
        self.critical_hit = False
        self.first_message_display = ""
        self.second_message_display = ""
        self.third_message_display = ""
        self.game_state = "welcome_screen"
        self.bet = 50
        self.bet_minimum = 50
        self.player_score = 0
        self.enemy_score = 0
        self.player_hand = []
        self.enemy_hand = []
        self.choices = ["Ready", "Draw", "Redraw"]
        self.current_index = 0
        self.welcome_screen_choices = ["Play", "Magic", "Bet", "Quit"]
        self.welcome_screen_index = 0
        self.magic_menu_selector = ["Reveal", "Back"]
        self.magic_menu_index = 0
        self.ace_value = 1
        self.bust_protection = False
        self.player_lock = False
        self.player_black_jack_win = False
        self.enemy_black_jack_win = False
        self.black_jack_draw = False
        self.reveal_magic_cost = 30
        self.mute_music_sound = 0
        self.current_speaker = ""
        self.npc_speaking = False
        self.hero_speaking = False
        self.music_loop = True
        self.despair = False
        self.music_file_level_up = pygame.mixer.Sound("./assets/music/levelup.mp3")  # Adjust the path as needed
        self.music_level_up_volume = 0.3  # Adjust as needed
        self.hero_losing_text_state = False
        self.hero_winning_text_state = False
        self.player_status = ""
        self.enemy_status = ""
        self.sir_leopold_ace_attack = pygame.mixer.Sound("./assets/music/startloadaccept.wav")  # Adjust the path as needed
        self.sir_leopold_ace_attack.set_volume(0.6)
        self.lucky_strike = pygame.mixer.Sound("./assets/music/luckystrike.wav")  # Adjust the path as needed
        self.lucky_strike.set_volume(0.6)
        self.double_draw_casting = False
        self.player_debuff_double_draw = 0
        self.magic_points = 1
        self.reveal_hand = 11
        self.magic_lock = False
        self.redraw_lock = False
        self.music_file = "./assets/music/black_jack_screen.mp3"
        self.music_volume = 0.5  # Adjust as needed
        self.music_on = True
        self.spell_sound = pygame.mixer.Sound("./assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.menu_movement_sound = pygame.mixer.Sound("./assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.5)
        self.locked_text = self.font.render("Locked", True, (255, 255, 255))
        self.low_exp_gain = 7
        self.med_exp_gain = 14
        self.high_exp_gain = 21
        self.max_mp = 1

        self.stamina_drain_high = 8
        self.stamina_drain_med = 5
        self.stamina_drain_low = 3
        self.reveal_not_active = 11
        self.reveal_spell_duration_expired = 0
        self.decrease_counter_by_one = 1
        self.double_draw_duration_expired = 0
        self.mp_depleted = 0
        self.double_draw_turns_inflicted = 7
        self.double_draw_cost = 1
        self.index_zero = 0
        self.play_index = 0
        self.magic_index = 1
        self.bet_index = 2
        self.quit_index = 3
        self.draw_one_card = 1

        self.messages = {
            "welcome_screen": ["Mack: Time to take out the trash.",
                               "You look pretty fresh to me. Time to grind you into hamburger boy.", "Presss T for commands"],
            "hero_intro_text": [
                "I can press up and down to select. Play to start, quit to leave, or magic for an advantage"],

            "bet_intro_text": [
                "Mack: Min Bet is 10 and Max Bet is 100. The more you bet the more your  stamina is drained. "],

            "hero_losing_text": [
                "Hero: This isn't good, I'll need to get serious if I want to make a comeback.",
                "Maybe I should lower my bet until I get the hang of my enemy.",
                ""],
            "enemy_winning_text": [
                "Cheater Bob: HA HA HA! You really stepped in it now!",
                "Do you know what happens when people lose all of their coins?",
                "I bet you have no idea what this place really is.", ""],
            "hero_losing_confused_text": [
                "Hero: Doesn't matter to me much what kind of place this is. I always go where there is gambling.",
                "This guy really means business....I need to focus, and regain my composure.",
                "Why doesn't he hit on 16??? It's like he's afraid to bust for some reason.",
                ""],

            "enemy_losing_text": [
                "Cheater Bob: How is this possible? I'm....Cheater Bob...I'm not supposed to lose.",
                "Your Cheating! There is no way I'd lose to an amateur like you!",
                ""],
            "hero_winning_text": [
                "Hero: I never cheat Cheater Bob. I'm just that good. Why are you sweating so much for?",
                "Care to tell me why your so worried? It's not like their going to kill you or anything.",
                "I can now use my bluff attack.",
                "If I use it I won't be able to use any other magic till this match is over.",
                "Should I use it now or wait a little bit till I'm closer to dealing a final blow?",
                ""],
            "enemy_losing_confused_text": [
                "Cheater Bob: There are some fates worse than death, 'hero'.",
                ".......",
                "If you take all my coins, and if the boss doesn't give me replacement coins..........",
                "NO!!! I won't end up like the others....I won't have you make a fool out of me.....",
                ""],

            "final_strike_text": [
                "Hero: You don't have a lot of coins left. I'll bet you the rest that my next hand will be a black jack.",
                "Of course, if you happen to win you'll be back in the game, sounds pretty nice of me right?",
                "",
            ],
            "enemy_bluffed_text": [
                "Cheater Bob: Do you Realize the odds of that happening?",
                " Why would you take such a bet for?",
                "It doesn't make any sense.",
                ""],

            "hero_bluffing_text": [
                "Hero: Well it's simple really, based on the card positions, and the way you shuffled. ",
                "I can pretty easily tell where each card landed in the deck.",
                "Simply put, I'm not doing a random bet, or a bluff, when you deal out the cards, I will get a black jack. It's all about my intellect and high perception.",
                ""],
            "enemy_falling_for_bluff_text": [
                "Cheater Bob: That's bull crap, there's no way you have that much perception.  ",
                "I'll take your bet, and then I'll tell everyone how much of a fool you are.",
                "I'll teach you to underestimate me!", ""],

            "enemy_crying_text": ["Cheater Bob: Impossible...how did you????",
                                  ""],
            "hero_reveal_text": [
                "Hero: To be honest, it was all a bluff, you were right all along.",
                "However, I never bet against myself, and because of that lady luck is always on my side.",
                "You lost,not because I cheated, but  because you didnt' believe in yourself and gave in to despair.",
                ""],

            "bluff_magic_explain": [
                "Casts Bluff on the enemy. When the enemy seems desperate this will be unlocked. Enemy less likely to hit due to fear of a bust. Magic Lock Permanent .25MP"],
            "reveal_magic_explain": [
                "Based on muscle twitches of enemy plus the way they shuffle cards, you can tell what score they have.Protects you from busts. Magic lock 10 turns.25MP"],
            "avatar_magic_explain": [
                "Your faith is so strong that lady luck herself blesses you. Allows up to 3 redraws per turn.Deck is not reshuffled and cards are burned.Magic lock 5 turns 25MP"],
            "back_magic_explain": ["Back to previous gui"],
            "player_no_money_explain": [
                "Booooooh boy your in for it now, some hero you turned out tobe.",
                "You can feel darkness start to surround you....."],
            "player_no_stamina_explain": [
                "Everything is getting dizzy and dark, you feel yourself passing out from a lack of stamina..(-100 golds)",
            ],

            "score_critical_hit_message": ["luck is on your side,  hand re shuffled.", ""
                                           ],
            "magic_enemy_attack_double_draw": ["Walking into a fog of confusion, forget and let your brain soak in the mist. Let your reality shift and increase times 2...double draw", ""
                                               ],
            "level_up": [f"Grats you levels up. ", "", "", "", ""
                         ],

        }

        self.welcome_screen_text_box = TextBox(self.messages["welcome_screen"],
                                               (50, 450, 50, 45), 30, 500)
        self.welcome_screen_text_box_hero = TextBox(
            self.messages["hero_intro_text"], (50, 450, 50, 45), 30, 500)

        self.bet_screen_text = TextBox(self.messages["bet_intro_text"],
                                       (50, 450, 50, 45), 30, 500)
        self.hero_losing_money_text = TextBox(self.messages["hero_losing_text"],
                                              (50, 450, 50, 45), 30, 500)
        self.enemy_losing_money_text = TextBox(
            self.messages["enemy_losing_text"], (50, 450, 50, 45), 30, 500)

        self.enemy_winning_money_text = TextBox(
            self.messages["enemy_winning_text"], (50, 450, 50, 45), 30, 500)
        self.hero_winning_money_text = TextBox(
            self.messages["hero_winning_text"], (50, 450, 50, 45), 30, 500)

        self.hero_losing_confused_money_text = TextBox(
            self.messages["hero_losing_confused_text"], (50, 450, 50, 45), 30,
            500)
        self.enemy_losing_confused_money_text = TextBox(
            self.messages["enemy_losing_confused_text"], (50, 450, 50, 45), 30,
            500)

        self.final_strike_text_component = TextBox(
            self.messages["final_strike_text"], (50, 450, 50, 45), 30, 500)
        self.enemy_bluffed_text_component = TextBox(
            self.messages["enemy_bluffed_text"], (50, 450, 50, 45), 30, 500)

        self.hero_bluffing_text_component = TextBox(
            self.messages["hero_bluffing_text"], (50, 450, 50, 45), 30, 500)
        self.enemy_falling_for_bluff_text_component = TextBox(
            self.messages["enemy_falling_for_bluff_text"], (50, 450, 50, 45),
            30, 500)

        self.enemy_crying_text_component = TextBox(
            self.messages["enemy_crying_text"], (50, 450, 50, 45), 30, 500)
        self.hero_reveal_text_component = TextBox(
            self.messages["hero_reveal_text"], (50, 450, 50, 45), 30, 500)

        self.bluff_magic_explain_component = TextBox(
            self.messages["bluff_magic_explain"], (50, 450, 50, 45), 30, 500)
        self.reveal_magic_explain_component = TextBox(
            self.messages["reveal_magic_explain"], (50, 450, 50, 45), 30, 500)
        self.avatar_magic_explain_component = TextBox(
            self.messages["avatar_magic_explain"], (50, 450, 50, 45), 30, 500)
        self.back_magic_explain_component = TextBox(
            self.messages["back_magic_explain"], (50, 450, 50, 45), 30, 500)
        self.player_no_money = TextBox(
            self.messages["player_no_money_explain"], (50, 450, 50, 45), 30, 500)
        self.player_no_stamina = TextBox(
            self.messages["player_no_stamina_explain"], (50, 450, 50, 45), 30, 500)
        self.score_critical_hit_message_component = TextBox(
            self.messages["score_critical_hit_message"], (50, 450, 50, 45), 30, 500)
        self.magic_enemy_attack_double_draw_message_component = TextBox(
            self.messages["magic_enemy_attack_double_draw"], (50, 450, 50, 45), 30, 500)

        self.main_bordered_box = BorderedBox((25, 425, 745, 150))

        self.defeated_textbox = TextBox(
            [
                "Mack: I still got the last laugh in the end, Mc Nugg is a chicken because I took his last coins.",

                "You must be something else to beat my double draw attack.I thought I was invincible.",
                ""],
            (50, 450, 50, 45), 30, 500)

        self.exp_gain = 0
        self.food_luck = False
        self.stat_point_allocated = False
        self.level_up_checker_sound = True
        self.level_up_stat_increase_index = 0  # Add this to track the selected stat
        self.level_screen_stats = ["Body", "Mind", "Spirit", "Perception", "Luck"]
        self.level_up_messages = TextBox(
            [
                f"Grats you leveled up to level 1!",
                f"Max Stamina increased by 0 points!",
                f"Max focus increased by 0 points!",
                f"You gained a stat point, please allocate. Stat points at this level max at 2."
            ],
            (50, 450, 50, 45), 30, 500
        )

    pygame.init()

    def start(self, state: 'GameState') -> None:
        self.initialize_music()

    def draw_level_up(self, state: 'GameState') -> None:
        if state.player.stat_point_increase and self.game_state == "level_up_screen":
            if self.level_up_messages.message_index == 3:  # Access level_up_messages
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

                # Position the white-bordered box
                black_box_x = start_x_right_box - border_width
                black_box_y = start_y_right_box - border_width

                # Blit the white-bordered box
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

        # Continue drawing the level-up messages
        self.level_up_messages.draw(state)

    def handle_level_up(self, state: 'GameState', controller) -> None:
        stat_increase = 1

        if self.level_up_checker_sound == True:
            self.music_file_level_up.play()  # Play the sound effect once
            self.level_up_checker_sound = False
        if not state.player.stat_point_increase:
            # Update the level_up_messages with actual player stats
            self.level_up_messages.messages = [
                f"Grats you leveled up to level {state.player.level}!",
                f"Max Stamina increased by {state.player.stamina_increase_from_level} points!",
                f"Max focus increased by {state.player.focus_increase_from_level} points!",
                ""
            ]
            self.level_up_messages.update(state)
            if self.level_up_messages.is_finished():
                state.player.leveling_up = False
                self.level_up_checker_sound = True

                self.level_up_messages.reset()
                self.game_state = "welcome_screen"
        else:
            self.level_up_messages.messages = [
                f"Grats you leveled up to level {state.player.level}!",
                f"Max Stamina increased by {state.player.stamina_increase_from_level} points!",
                f"Max focus increased by {state.player.focus_increase_from_level} points!",
                f"You gained a stat point, please allocate. Stat points at this level max at 2."
            ]
            self.level_up_messages.update(state)

            if self.level_up_messages.message_index == 3 and self.level_up_messages.current_message_finished():
                if controller.isUpPressed:
                    self.level_up_stat_increase_index = (self.level_up_stat_increase_index - 1) % len(self.level_screen_stats)
                    controller.isUpPressed = False
                elif controller.isDownPressed:
                    self.level_up_stat_increase_index = (self.level_up_stat_increase_index + 1) % len(self.level_screen_stats)
                    controller.isDownPressed = False

                selected_stat = self.level_screen_stats[self.level_up_stat_increase_index]

                if selected_stat == "Body" and state.controller.isTPressed and state.player.body < 2:
                    state.player.body += stat_increase
                    state.player.stamina_points += state.player.level_2_body_stamina_increase
                    state.player.max_stamina_points += state.player.level_2_body_stamina_increase
                    self.stat_point_allocated = True
                    self.level_up_checker_sound = True

                elif selected_stat == "Mind" and state.controller.isTPressed and state.player.mind < 2:
                    state.player.mind += stat_increase
                    self.stat_point_allocated = True
                    self.level_up_checker_sound = True

                    state.player.focus_points += state.player.level_2_mind_focus_increase
                    state.player.max_focus_points += state.player.level_2_mind_focus_increase
                    Magic.CRAPS_LUCKY_7.add_magic_to_player(state.player, Magic.CRAPS_LUCKY_7)
                elif selected_stat == "Spirit" and state.controller.isTPressed and state.player.spirit < 2:
                    state.player.spirit += stat_increase
                    self.stat_point_allocated = True
                    self.level_up_checker_sound = True


                elif selected_stat == "Perception" and state.controller.isTPressed and state.player.perception < 2:
                    state.player.perception += stat_increase
                    self.stat_point_allocated = True
                    self.level_up_checker_sound = True


                elif selected_stat == "Perception" and state.controller.isTPressed and state.player.perception < 3 and \
                        Equipment.SOCKS_OF_PERCEPTION.value in state.player.equipped_items:
                    state.player.perception += stat_increase
                    self.level_up_checker_sound = True

                    self.stat_point_allocated = True

                    # state.player.base_perception += 1
                elif selected_stat == "Luck" and state.controller.isTPressed and state.player.luck < 2:
                    state.player.luck += stat_increase
                    self.stat_point_allocated = True
                    self.level_up_checker_sound = True



                elif selected_stat == "Luck" and state.controller.isTPressed and state.player.luck < 3 and \
                        state.player.enhanced_luck == True:
                    state.player.luck += stat_increase
                    self.stat_point_allocated = True
                    self.level_up_checker_sound = True

                if state.controller.isTPressed and self.stat_point_allocated == True:
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.player.leveling_up = False
                    self.level_up_messages.reset()
                    self.stat_point_allocated = False
                    self.level_up_checker_sound = True
                    self.game_state = "welcome_screen"

    def stop_music(self):
        pygame.mixer.music.stop()

    def initialize_music(self):
        loop_music = -1
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loop_music)

    def place_bet(self, state: "GameState"):
        bet_increment = 50
        bet_max = 100
        bet_minimum = 50
        one_hundred_milliseconds = 100

        if state.controller.isUpPressed:

            self.bet += bet_increment
            self.menu_movement_sound.play()  # Play the sound effect once

            pygame.time.delay(one_hundred_milliseconds)
            state.controller.isUpPressed = False

        elif state.controller.isDownPressed:
            self.bet -= bet_increment
            self.menu_movement_sound.play()  # Play the sound effect once

            pygame.time.delay(one_hundred_milliseconds)
            state.controller.isDownPressed = False

        if self.bet < bet_minimum:
            self.bet = bet_minimum

        if self.bet > bet_max:
            self.bet = bet_max

        if self.bet > self.money:
            self.bet = self.money

        if self.bet > state.player.money:
            self.bet = state.player.money

    def update(self, state: "GameState"):
        enemy_zero_money = 0

        if self.money < self.bet:
            self.bet = self.money
        if self.money <= enemy_zero_money:
            Events.add_event_to_player(state.player, Events.BLACK_JACK_BLACK_MACK_DEFEATED)
            Events.add_event_to_player(state.player, Events.MC_NUGGET_THIRD_QUEST_COMPLETE)

        if state.musicOn == True:
            if self.music_on == True:
                self.stop_music()
                self.initialize_music()
                self.music_on = False

        state.player.canMove = False

        if self.money <= enemy_zero_money:
            self.black_jack_rumble_bill_defeated = True
            self.game_state = "defeated"

        controller = state.controller
        controller.update()
        state.player.update(state)

        if self.game_state == "defeated":
            print("enemy defeated")
            self.defeated_textbox.update(state)

        if self.game_state == "welcome_screen":
            music_volume_setting = 0.5
            player_no_stamina = 0

            self.music_volume = music_volume_setting  # Adjust as needed
            pygame.mixer.music.set_volume(self.music_volume)

            if state.player.leveling_up == True:
                self.game_state = "level_up_screen"

            if state.player.stamina_points <= player_no_stamina:
                print("time to leave")

            self.welcome_screen_text_box.update(state)

            self.npc_speaking = True
            self.hero_speaking = False
            self.critical_hit = False
            self.magic_enemy_attack_double_draw_message_component.reset()

            self.redraw_lock = False
            self.ace_up_sleeve_jack_cheat_mode = False
            self.bust_protection = False
            self.current_index = 0
            self.enemy_score = 0
            move_index_by_one = 1

            loop_start = 0
            bet_increment = 50
            double_draw_low_chance_to_cast = 700
            double_draw_high_chance_to_cast = 300

            if self.welcome_screen_text_box.is_finished() and self.welcome_screen_text_box.current_message_finished():
                self.npc_speaking = False
                self.hero_speaking = True

                if controller.isUpPressed:
                    self.menu_movement_sound.play()
                    if not hasattr(self, "welcome_screen_index"):
                        self.welcome_screen_index = len(
                            self.welcome_screen_choices) - move_index_by_one
                    else:
                        self.welcome_screen_index -= move_index_by_one
                    self.welcome_screen_index %= len(
                        self.welcome_screen_choices)
                    controller.isUpPressed = False

                elif controller.isDownPressed:
                    self.menu_movement_sound.play()

                    if not hasattr(self, "welcome_screen_index"):
                        self.welcome_screen_index = len(
                            self.welcome_screen_choices) + move_index_by_one
                    else:
                        self.welcome_screen_index += move_index_by_one
                    self.welcome_screen_index %= len(
                        self.welcome_screen_choices)
                    controller.isDownPressed = False

                if self.welcome_screen_index == self.play_index and controller.isTPressed:
                    controller.isTPressed = False
                    for i in range(loop_start, self.bet, bet_increment):
                        state.player.stamina_points -= self.stamina_drain_low
                    self.deck.shuffle()

                    if self.player_debuff_double_draw <= self.double_draw_duration_expired and self.money < double_draw_high_chance_to_cast and self.magic_points > self.mp_depleted:
                        enemy_magic_cast = random.randint(1, 100)
                        magic_cast_multiplier = 20
                        magic_cast_threshold = 35

                        enemy_magic_cast_modifier = self.magic_points * magic_cast_multiplier

                        if enemy_magic_cast + enemy_magic_cast_modifier >= magic_cast_threshold:

                            print("WURGLE ALERT WURGLE ALERT WURGLE ALERT")
                            self.player_debuff_double_draw += self.double_draw_turns_inflicted
                            self.magic_points -= self.double_draw_cost
                            self.game_state = "double_draw_casting_phase"
                        else:
                            self.game_state = "draw_phase"

                    elif self.player_debuff_double_draw <= self.double_draw_duration_expired and self.money < double_draw_low_chance_to_cast and self.magic_points > self.mp_depleted:
                        enemy_magic_cast = random.randint(1, 100)
                        spell_cast_multiplier = 20
                        magic_cast_threshold = 70
                        player_dubuff_double_draw_length = 7
                        double_draw_cost = 1
                        enemy_magic_cast_modifier = self.magic_points * spell_cast_multiplier

                        if enemy_magic_cast + enemy_magic_cast_modifier >= magic_cast_threshold:
                            self.player_debuff_double_draw += player_dubuff_double_draw_length
                            self.magic_points -= double_draw_cost
                            self.game_state = "double_draw_casting_phase"
                        else:
                            self.game_state = "draw_phase"
                    else:
                        self.game_state = "draw_phase"
                    controller.isTPressed = False
                elif self.welcome_screen_index == self.magic_index and controller.isTPressed and self.magic_lock == False:
                    magic_menu_index = self.index_zero
                    self.magic_screen_index = magic_menu_index
                    self.game_state = "magic_menu"
                    controller.isTPressed = False
                elif self.welcome_screen_index == self.bet_index and controller.isTPressed:
                    self.game_state = "bet_phase"
                    controller.isTPressed = False

                elif self.welcome_screen_index == self.quit_index and controller.isTPressed and self.player_debuff_double_draw <= self.double_draw_duration_expired:
                    controller.isTPressed = False
                    self.welcome_screen_index = self.play_index
                    self.reveal_hand = self.reveal_spell_duration_expired
                    self.magic_lock = False
                    self.bet = self.bet_minimum
                    self.magic_points = self.max_mp
                    state.currentScreen = state.area2GamblingScreen
                    state.area2GamblingScreen.start(state)

                    state.player.canMove = True


        elif self.game_state == "double_draw_casting_phase":
            end_message = 1
            self.magic_enemy_attack_double_draw_message_component.update(state)
            if self.magic_enemy_attack_double_draw_message_component.message_index == end_message:
                self.spell_sound.play()
                self.game_state = "draw_phase"

        elif self.game_state == "bet_phase":
            spell_cast_timer = 300
            if self.money < self.bet:
                self.bet = self.money

            self.bet_screen_text.update(state)
            self.npc_speaking = True
            self.hero_speaking = False
            self.third_message_display = " "
            self.place_bet(state)
            if controller.isTPressed:
                pygame.time.wait(spell_cast_timer)
                self.game_state = "welcome_screen"
                controller.isTPressed = False

        elif self.game_state == "draw_phase":
            luck_muliplier = 5
            lucky_roll = random.randint(1, 100)
            adjusted_lucky_roll = lucky_roll + state.player.luck * luck_muliplier
            black_jack_score = 21
            level_1_luck_score = 0
            player_bad_score_min_range = 12
            player_bad_score_max_range = 17
            lucky_strike_threshhold = 50
            initial_hand = 2
            sir_leopold_steal_threshhold = 40

            self.first_message_display = ""
            self.second_message_display = ""
            self.thrid_message_display = ""
            self.player_black_jack_win = False
            self.enemy_black_jack_win = False
            self.black_jack_draw = False
            self.player_hand = self.deck.player_draw_hand(initial_hand)
            self.player_score = self.deck.compute_hand_value(self.player_hand)

            if self.player_score >= black_jack_score:
                self.player_black_jack_win = True

            aces_to_remove = [
                ('Ace', 'Hearts', 11),
                ('Ace', 'Spades', 11),
                ('Ace', 'Diamonds', 11),
                ('Ace', 'Clubs', 11),
                ('Ace', 'Hearts', 1),
                ('Ace', 'Spades', 1),
                ('Ace', 'Diamonds', 1),
                ('Ace', 'Clubs', 1),
            ]
            self.enemy_hand = self.deck.enemy_draw_hand(initial_hand)
            if self.enemy_score >= black_jack_score:
                self.enemy_black_jack_win = True

            if state.player.luck > level_1_luck_score:
                if self.player_score > player_bad_score_min_range and self.player_score < player_bad_score_max_range:

                    if adjusted_lucky_roll >= lucky_strike_threshhold:
                        self.lucky_strike.play()
                        self.player_hand = self.deck.player_draw_hand(initial_hand)
                        self.player_score = self.deck.compute_hand_value(self.player_hand)
                        self.critical_hit = True

            if "sir leopold's paw" in state.player.equipped_items:
                roll = random.randint(1, 100)
                if roll >= sir_leopold_steal_threshhold:
                    self.enemy_black_jack_win = False

                    for card in self.enemy_hand:
                        if card in aces_to_remove:
                            self.enemy_hand.remove(card)
                            self.sir_leopold_ace_attack.play()
                            self.enemy_hand += self.deck.enemy_draw_hand(self.draw_one_card)
                            break

            self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)

            if self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                self.black_jack_draw = True
                self.thrid_message_display = "Its a draw"
                self.game_state = "results_screen"
            elif self.player_black_jack_win == True and self.enemy_black_jack_win == False:
                self.game_state = "results_screen"
            elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                self.game_state = "results_screen"
            else:
                self.game_state = "menu_screen"

        elif self.game_state == "level_up_screen":

            self.music_volume = self.mute_music_sound
            pygame.mixer.music.set_volume(self.music_volume)
            self.handle_level_up(state, state.controller)

        elif self.game_state == "player_draw_one_card":
            player_bust = 21
            ace_minimum_to_be_one = 10

            self.player_hand += self.deck.player_draw_hand(self.draw_one_card)
            self.deck.compute_hand_value(self.player_hand)
            self.player_score = self.deck.compute_hand_value(self.player_hand)

            if self.player_debuff_double_draw > self.double_draw_duration_expired:
                self.player_hand += self.deck.player_draw_hand(self.draw_one_card)
                self.deck.compute_hand_value(self.player_hand)
                self.player_score = self.deck.compute_hand_value(self.player_hand)

            if self.player_score > ace_minimum_to_be_one:
                self.deck.rank_values["Ace"] = 1

            if self.player_score > player_bust:
                if Equipment.BLACK_JACK_HAT.value not in state.player.equipped_items:
                    state.player.money -= self.bet
                    self.money += self.bet
                    state.player.stamina_points -= self.stamina_drain_low
                    state.player.exp += self.low_exp_gain
                    self.first_message_display = f"You lose {self.stamina_drain_low} HP."
                    self.second_message_display = f"You busted and went over 21! You gain {self.low_exp_gain} and lose {self.bet} "

                elif Equipment.BLACK_JACK_HAT.value in state.player.equipped_items:
                    lucky_roll = random.randint(1, 4)
                    lucky_roll_success = 4
                    if lucky_roll == lucky_roll_success:
                        self.player_hand.pop()
                        self.player_score = self.deck.compute_hand_value(self.player_hand)
                        self.first_message_display = f"You almost went over 21."
                    else:
                        state.player.money -= self.bet
                        self.money += self.bet
                        state.player.stamina_points -= self.stamina_drain_low
                        state.player.exp += self.low_exp_gain
                        self.first_message_display = f"You lose -6 HP."
                        self.second_message_display = f"You busted and went over 21! You gain 10 exp and lose {self.bet} "

            if self.bust_protection == True:
                self.game_state = "results_screen"
            else:
                self.game_state = "menu_screen"

        elif self.game_state == "enemy_draw_one_card":
            dealer_stand = 16
            dealer_bust = 21
            while self.enemy_score < dealer_stand:
                self.enemy_hand += self.deck.enemy_draw_hand(self.draw_one_card)
                self.deck.compute_hand_value(self.enemy_hand)
                self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)
                self.game_state = "results_screen"
                if self.enemy_score > dealer_bust:
                    state.player.money += self.bet
                    self.money -= self.bet
                    state.player.exp += self.low_exp_gain
                    self.second_message_display = "enemy bust player wins"
                    self.game_state = "results_screen"

            if self.enemy_score >= dealer_stand and self.enemy_score <= dealer_bust:
                self.game_state = "results_screen"

        elif self.game_state == "menu_screen":
            player_bust = 21
            move_menu_index_by_one = 1

            if self.player_score >= player_bust:
                self.message_display = "You bust and lose."
                self.game_state = "results_screen"

            if controller.isUpPressed:
                self.menu_movement_sound.play()  # Play the sound effect once
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) - move_menu_index_by_one
                else:
                    self.current_index -= move_menu_index_by_one
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isUpPressed = False

            if controller.isDownPressed:
                self.menu_movement_sound.play()  # Play the sound effect once
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) + move_menu_index_by_one
                else:
                    self.current_index += move_menu_index_by_one
                self.current_index %= len(self.choices)
                controller.isDownPressed = False
                self.game_state = "menu_screen"
                state.controller.isTPressed = False

        elif self.game_state == "magic_menu":
            move_magic_index_by_one = 1
            reveal_spell_index = 0
            set_reveal_duration = 10
            magic_index_back_to_welcome_screen = 1

            self.message_display = "Pick a magic spell and wreck havic. Press K to cast"
            if controller.isUpPressed:
                self.menu_movement_sound.play()
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) - move_magic_index_by_one
                else:
                    self.magic_menu_index -= move_magic_index_by_one
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                self.menu_movement_sound.play()
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) + move_magic_index_by_one
                else:
                    self.magic_menu_index += move_magic_index_by_one
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isDownPressed = False

            if self.magic_menu_index == reveal_spell_index:
                self.reveal_magic_explain_component.update(state)
                if controller.isTPressed:
                    if state.player.focus_points >= self.reveal_magic_cost:
                        state.player.focus_points -= self.reveal_magic_cost
                        self.spell_sound.play()
                        self.reveal_hand = set_reveal_duration
                        self.magic_lock = True
                        self.player_status = "Focus"
                        self.enemy_status = "Reveal"
                        self.game_state = "welcome_screen"
                        self.isTPressed = False

                    elif state.player.focus_points < self.reveal_magic_cost:
                        self.third_message_display = "Sorry but you dont have enough focus points to cast"

            elif self.magic_menu_index == magic_index_back_to_welcome_screen:
                self.back_magic_explain_component.update(state)
                if controller.isTPressed:
                    self.magic_menu_index = reveal_spell_index
                    controller.isTPressed = False
                    self.game_state = "welcome_screen"
                    self.isTPressed = False

        elif self.game_state == "results_screen":
            black_jack_bet_multiplier = 2
            bust_number = 22
            if self.player_black_jack_win == True and self.enemy_black_jack_win == False:
                self.second_message_display = "You win with a black jack press T when ready"
                self.first_message_display = f"You gain 100 exp and {self.bet * black_jack_bet_multiplier} gold "

            elif self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                self.second_message_display = "It's a draw press T when ready"
                self.first_message_display = f"You gain 25 exp and 0 gold "

            elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                self.second_message_display = "Enemy gets blackjack you lose "
                self.first_message_display = f"You gain 30 exp and 0 gold "

            elif self.player_score > self.enemy_score and self.player_score < bust_number:
                self.second_message_display = "You win player press T when ready"
                self.first_message_display = f"You gain 25 exp and {self.bet} gold "

            elif self.player_score < self.enemy_score and self.enemy_score < bust_number:
                self.second_message_display = "You lose player press T when ready"
                self.first_message_display = f"You gain 5 experience and lose {self.bet} gold "

            elif self.player_score == self.enemy_score:
                self.second_message_display = "It's a draw nobody wins press T when Ready"
                self.first_message_display = f"You gain 25 exp and 0 gold "

            if controller.isTPressed:
                critical_multiplier = 2
                spell_timer = 300
                if self.player_black_jack_win == True and self.enemy_black_jack_win == False:
                    self.first_message_display = f"Gain {self.high_exp_gain} and win {self.bet * critical_multiplier} gold "
                    state.player.exp += self.high_exp_gain
                    self.second_message_display = "Player deals a CRITICAL HIT!!! "
                    if self.bet * critical_multiplier < self.money:
                        state.player.money += self.bet * critical_multiplier
                        self.money -= self.bet * critical_multiplier
                    else:
                        state.player.money += self.money
                        self.money = enemy_zero_money

                elif self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                    self.first_message_display = f"You gain 20 exp, 0 gold, you lose 10 HP. "
                    state.player.exp += self.med_exp_gain
                    state.player.stamina_points -= self.stamina_drain_low
                    self.second_message_display = "You tie player press T when ready"

                elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                    state.player.exp += self.high_exp_gain
                    state.player.stamina_points -= self.stamina_drain_high
                    self.first_message_display = f"You gain 15 exp and lose {self.bet * critical_multiplier} gold."
                    self.thrid_message_display = f"You Lose 25 HP "
                    self.second_message_display = "Enemy deals a CRITICAL HIT!!! "
                    state.player.money -= self.bet * critical_multiplier
                    self.money += self.bet * critical_multiplier

                elif self.player_score > self.enemy_score and self.player_score < bust_number:
                    state.player.exp += self.med_exp_gain
                    self.first_message_display = f"You gain 10 exp and {self.bet} gold "
                    self.second_message_display = "You win player press T when ready"
                    state.player.money += self.bet
                    self.money -= self.bet

                elif self.player_score < self.enemy_score and self.enemy_score < bust_number:
                    state.player.exp += self.med_exp_gain
                    state.player.stamina_points -= self.stamina_drain_high
                    self.first_message_display = f"You gain 5 exp and lose {self.bet} gold and -8 HP"
                    self.second_message_display = "You lose player press T when ready"
                    state.player.money -= self.bet
                    self.money += self.bet

                elif self.player_score == self.enemy_score:
                    state.player.exp += self.med_exp_gain
                    state.player.stamina_points -= self.stamina_drain_low
                    self.first_message_display = f"You gain 8 exp and 0 gold, and lose -4 HP "
                    self.second_message_display = "It's a draw nobody wins press T when Ready"

                if self.reveal_hand < self.reveal_not_active:
                    self.reveal_hand -= self.decrease_counter_by_one

                if self.reveal_hand == self.reveal_spell_duration_expired:
                    self.reveal_hand = self.reveal_not_active
                    self.magic_lock = False

                pygame.time.wait(spell_timer)
                if self.player_debuff_double_draw > self.reveal_spell_duration_expired:
                    self.player_debuff_double_draw -= self.decrease_counter_by_one

                self.game_state = "welcome_screen"
                controller.isTPressed = False

    def draw(self, state: "GameState"):
        self.draw_player_box(state)
        self.draw_enemy_box(state)
        self.main_bordered_box.draw(state)

        player_money_critical_low = 300
        player_stamina_critical_low = 20
        player_box_left_menu_x_position = 37
        player_money_y_position = 250
        player_stamina_y_position = 290
        player_focus_y_position = 330
        player_bet_y_position = 370
        hero_name_y_position = 205
        enemy_money_y_position = 70
        enemey_status_y_position = 110
        y_position_spacing = 40
        reveal_spell_score_y_position = 110
        white_line_thickness = 2
        player_stamina_at_0 = 0
        player_money_at_0 = 0
        player_score_y_position = 150
        enemy_name_y_position = 30
        right_box_items_x_modifier = 60
        right_box_items_y_modifier = 15
        arrow_modifier_x = 12
        arrow_modifier_y_0_index = 12
        arrow_modifier_y_1_index = 50
        arrow_modifier_y_2_index = 92
        arrow_modifier_y_3_index = 132
        up_arrow_x_coordinate = 257
        up_arrow_y_coordinate = 510
        down_arrow_x_coordinate = 260
        down_arrow_y_coordinate = 550

        if state.player.money < player_money_critical_low:
            text_color = RED
        else:
            text_color = WHITE

        state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True, text_color), (player_box_left_menu_x_position, player_money_y_position))

        if state.player.stamina_points < player_stamina_critical_low:
            text_color = RED
        else:
            text_color = WHITE

        state.DISPLAY.blit(
            self.font.render(f"HP: {state.player.stamina_points}", True,
                             text_color), (player_box_left_menu_x_position, player_stamina_y_position))

        state.DISPLAY.blit(self.font.render(f"MP: {state.player.focus_points}", True,
                                            WHITE), (player_box_left_menu_x_position, player_focus_y_position))
        state.DISPLAY.blit(
            self.font.render(f"Bet: {self.bet}", True, WHITE),
            (player_box_left_menu_x_position, player_bet_y_position))

        if self.player_debuff_double_draw == self.double_draw_duration_expired:

            state.DISPLAY.blit(self.font.render(f"Hero", True, WHITE),
                               (player_box_left_menu_x_position, hero_name_y_position))

        elif self.player_debuff_double_draw > self.double_draw_duration_expired:
            state.DISPLAY.blit(
                self.font.render(f"D. Draw: {self.player_debuff_double_draw}", True, RED),
                (player_box_left_menu_x_position, hero_name_y_position))

        state.DISPLAY.blit(self.font.render(f"Money: {self.money}", True,
                                            WHITE), (player_box_left_menu_x_position, enemy_money_y_position))

        if self.reveal_hand == self.reveal_not_active:
            state.DISPLAY.blit(self.font.render(f"Normal", True,
                                                WHITE), (player_box_left_menu_x_position, enemey_status_y_position))

        elif self.reveal_hand < self.reveal_not_active:
            state.DISPLAY.blit(self.font.render(f"Reveal: {self.reveal_hand}", True,
                                                WHITE), (player_box_left_menu_x_position, reveal_spell_score_y_position))
            state.DISPLAY.blit(self.font.render(f"Score: {self.enemy_score}", True,
                                                WHITE),
                               (player_box_left_menu_x_position, player_score_y_position))

        elif self.reveal_hand >= self.reveal_not_active:
            state.DISPLAY.blit(self.font.render(f"Score:", True, WHITE),
                               (player_box_left_menu_x_position, player_score_y_position))

        state.DISPLAY.blit(self.font.render(f"Mack", True, WHITE),
                           (player_box_left_menu_x_position, enemy_name_y_position))




        # self.face_down_card((0,0))

        if self.game_state == "welcome_screen":
            if state.player.money <= player_money_at_0:
                self.game_state = "game_over_no_money"
            elif state.player.stamina_points <= player_stamina_at_0:
                self.reveal_hand = 0
                self.magic_lock = False
                self.magic_points = 1
                self.player_debuff_double_draw = 0
                self.game_state = "game_over_no_stamina"

            # will need to update this in future as all screens should have same welcome screen
            black_box_height = 221 - 50  # Adjust height
            black_box_width = 200 - 10  # Adjust width to match the left box
            border_width = 5
            start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
            start_y_right_box = 240  # Adjust vertical alignment

            black_box = pygame.Surface((black_box_width, black_box_height))
            black_box.fill(BLACK)

            white_border = pygame.Surface(
                (black_box_width + white_line_thickness * border_width, black_box_height + white_line_thickness * border_width)
            )
            white_border.fill(WHITE)
            white_border.blit(black_box, (border_width, border_width))

            black_box_x = start_x_right_box - border_width
            black_box_y = start_y_right_box - border_width

            state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

            for idx, choice in enumerate(self.welcome_screen_choices):
                y_position = start_y_right_box + idx * y_position_spacing
                state.DISPLAY.blit(
                    self.font.render(str(choice), True, WHITE),
                    (start_x_right_box + right_box_items_x_modifier, y_position + right_box_items_y_modifier)
                )

            if self.player_debuff_double_draw > self.double_draw_duration_expired:
                self.welcome_screen_choices[self.quit_index] = "Locked"
            elif self.player_debuff_double_draw <= self.double_draw_duration_expired:
                self.welcome_screen_choices[self.quit_index] = "Quit"

            if self.reveal_hand < 11 and self.reveal_hand > 0:
                self.magic_lock = True
                self.welcome_screen_choices[1] = "Locked"
            else:
                self.magic_lock = False
                self.welcome_screen_choices[1] = "Magic"

            if self.welcome_screen_index == self.play_index:
                state.DISPLAY.blit(
                    self.font.render("->", True, WHITE),
                    (start_x_right_box + arrow_modifier_x, start_y_right_box + arrow_modifier_y_0_index)
                )
            elif self.welcome_screen_index == self.magic_index:
                state.DISPLAY.blit(
                    self.font.render("->", True, WHITE),
                    (start_x_right_box + arrow_modifier_x, start_y_right_box + arrow_modifier_y_1_index)
                )
            elif self.welcome_screen_index == self.bet_index:
                state.DISPLAY.blit(
                    self.font.render("->", True, WHITE),
                    (start_x_right_box + arrow_modifier_x, start_y_right_box + arrow_modifier_y_2_index)
                )
            elif self.welcome_screen_index == self.quit_index:
                state.DISPLAY.blit(
                    self.font.render("->", True, WHITE),
                    (start_x_right_box + arrow_modifier_x, start_y_right_box + arrow_modifier_y_3_index)
                )

            self.welcome_screen_text_box.draw(state)

        elif self.game_state == "draw_phase":
            if self.critical_hit == True:
                self.score_critical_hit_message_component.update(state)
                self.score_critical_hit_message_component.draw(state)

        elif self.game_state == "double_draw_casting_phase":
            self.magic_enemy_attack_double_draw_message_component.draw(state)

        elif self.game_state == "defeated":
            self.defeated_textbox.draw(state)
            if self.defeated_textbox.message_index == 2:
                state.player.canMove = True
                state.currentScreen = state.area2GamblingScreen
                state.area2GamblingScreen.start(state)

        elif self.game_state == "hero_is_desperate_state":
            self.hero_losing_money_text.draw(state)
            self.enemy_winning_money_text.draw(state)
            self.hero_losing_confused_money_text.draw(state)

        elif self.game_state == "enemy_is_desperate_state":
            self.enemy_losing_money_text.draw(state)
            self.hero_winning_money_text.draw(state)
            self.enemy_losing_confused_money_text.draw(state)

        elif self.game_state == "bet_phase":
            bet_label_x = 50
            bet_label_y = 530
            self.bet_screen_text.draw(state)
            state.DISPLAY.blit(self.font.render(f"Your Current bet:{self.bet}", True,
                                                WHITE), (bet_label_x, bet_label_y))
            state.DISPLAY.blit(self.font.render(f"v", True, WHITE),
                               (down_arrow_x_coordinate, down_arrow_y_coordinate))
            state.DISPLAY.blit(self.font.render(f"^", True, WHITE),
                               (up_arrow_x_coordinate, up_arrow_y_coordinate))


        elif self.game_state == "menu_screen":
            print("Menuuuuuuuuuu")
            player_card_x = 235
            player_card_y = 195
            enemy_card_x = 235
            enemy_card_y = 15
            move_player_card_x = 75

            for i, card in enumerate(self.player_hand):
                if i == 4:  # Adjust for the 5th card, moving to the second row
                    player_card_y = 305
                    player_card_x = 235  # Start position for the second row
                elif i > 4:
                    # For the 6th card and beyond, increment player_card_x normally
                    player_card_y = 305
                    player_card_x = 300  # Start position for the second row
                self.deck.draw_card_face_up(card[1], card[0], (player_card_x, player_card_y), DISPLAY)

                player_card_x += move_player_card_x

            for index, card in enumerate(self.enemy_hand):
                if index == 0:
                    self.deck.draw_card_face_down((enemy_card_x, enemy_card_y), state.DISPLAY)
                else:
                    self.deck.draw_card_face_up(card[1], card[0], (enemy_card_x, enemy_card_y), state.DISPLAY)
                enemy_card_x += move_player_card_x

            black_box = pygame.Surface((160 - 10, 180 - 10))
            black_box.fill(BLACK)
            border_width = 5
            white_border = pygame.Surface(
                (160 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
            white_border.fill(WHITE)
            white_border.blit(black_box, (border_width, border_width))
            state.DISPLAY.blit(white_border, (620, 235))

            state.DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, WHITE),
                (674, 260))

            if self.player_debuff_double_draw <= self.double_draw_duration_expired:
                state.DISPLAY.blit(
                    self.font.render(f"{self.choices[1]}", True, WHITE),
                    (674, 310))
            elif self.player_debuff_double_draw > self.double_draw_duration_expired:
                state.DISPLAY.blit(
                    self.font.render(f"D Draw", True, WHITE),
                    (674, 310))

            if self.current_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, WHITE),
                    (637, 255))
                if state.controller.isTPressed:
                    pygame.time.wait(300)
                    if self.despair == False:
                        self.game_state = "enemy_draw_one_card"
                    elif self.despair == True:
                        self.game_state = "enemy_despair_draw_one_card"
                    state.controller.isTPressed = False


            elif self.current_index == 1:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, WHITE),
                    (637, 305))
                if state.controller.isTPressed:
                    pygame.time.wait(300)
                    self.game_state = "player_draw_one_card"
                    self.isTPressed = False

            elif self.current_index == 2:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, WHITE),
                    (637, 355))

        elif self.game_state == "magic_menu":
            black_box = pygame.Surface((255, 215))
            black_box_width = 160
            black_box_height = 110
            border_width = 5

            # Calculate the size of the white border based on the black box size and border width
            white_border_width = black_box_width + 2 * border_width
            white_border_height = black_box_height + 2 * border_width

            # Create the black box
            black_box = pygame.Surface((black_box_width, black_box_height))
            black_box.fill((0, 0, 0))

            # Create the white border
            white_border = pygame.Surface((white_border_width, white_border_height))
            white_border.fill((255, 255, 255))

            # Blit the black box onto the white border, positioned by the border width
            white_border.blit(black_box, (border_width, border_width))

            # Determine the position on the screen
            position_x = 620 - 20  # Adjust the position as needed
            position_y = 300  # Adjust the position as needed

            # Blit the white-bordered black box onto the display
            state.DISPLAY.blit(white_border, (position_x, position_y))

            # Use the provided position variables
            # Determine the position on the screen
            position_x = 620 - 20  # Adjust the position as needed
            position_y = 300

            # Now, position the menu items relative to these coordinates
            if self.magic_menu_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, WHITE),
                    (position_x + 20, position_y + 10))  # Adjust offsets as needed

                self.reveal_magic_explain_component.draw(state)

            elif self.magic_menu_index == 1:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, WHITE),
                    (position_x + 20, position_y + 60))  # Adjust offsets as needed

                self.back_magic_explain_component.draw(state)

            # Position the magic menu selectors relative to the black box
            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[0]}", True, WHITE),
                (position_x + 60, position_y + 15))  # Adjust offsets as needed

            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[1]}", True, WHITE),
                (position_x + 60, position_y + 65))  # Adjust offsets as needed

        elif self.game_state == "level_up_screen":
            self.draw_level_up(state)


        elif self.game_state == "game_over_no_money":

            self.player_no_money.update(state)
            self.player_no_money.draw(state)
            if self.player_no_money.is_finished():
                if state.controller.isTPressed:
                    state.currentScreen = state.gameOverScreen
                    state.gameOverScreen.start(state)


        elif self.game_state == "game_over_no_stamina":
            stamina_penalty = 100
            self.reveal_hand = 0
            self.bet = 50
            self.magic_points = 1

            self.magic_lock = False

            self.player_no_stamina.update(state)
            self.player_no_stamina.draw(state)
            if self.player_no_stamina.is_finished():
                if state.controller.isTPressed:
                    state.player.money -= stamina_penalty
                    if state.player.money <= player_money_at_0:
                        state.currentScreen = state.gameOverScreen
                        state.gameOverScreen.start(state)
                    else:
                        self.game_state = "welcome_screen"
                        state.player.canMove = True
                        state.start_area_to_rest_area_entry_point = True

                        state.currentScreen = state.area2RestScreen
                        state.area2RestScreen.start(state)
                        state.player.stamina_points = 1

            if state.player.money <= player_money_at_0:
                self.game_state = "game_over_no_money"
            elif state.player.stamina_points <= player_stamina_at_0:
                self.game_state = "game_over_no_stamina"

        elif self.game_state == "results_screen":
            player_card_x = 235
            player_card_y = 195
            enemy_card_x = 235
            enemy_card_y = 15

            for i, card in enumerate(self.player_hand):
                if i > 3:
                    player_card_y = 305
                    player_card_x = 235
                self.deck.draw_card_face_up(card[1], card[0], (player_card_x, player_card_y), DISPLAY)
                player_card_x += 75

            for index, card in enumerate(self.enemy_hand):
                self.deck.draw_card_face_up(card[1], card[0], (enemy_card_x, enemy_card_y), DISPLAY)

                enemy_card_x += 75

            # self.current_speaker = "cheater bob"

            # state.DISPLAY.blit(character_image, (23, 245))
            state.DISPLAY.blit(self.font.render(f"{self.current_speaker}", True,
                                                WHITE), (155, 350))
            # state.DISPLAY.blit(self.font.render(f"{self.first_message_display}", True, (255, 255, 255)), (45, 390))

            state.DISPLAY.blit(
                self.font.render(f"{self.second_message_display}", True,
                                 WHITE), (45, 450))
            state.DISPLAY.blit(self.font.render(f"{self.first_message_display}", True,
                                                WHITE), (45, 500))
        pygame.display.flip()
