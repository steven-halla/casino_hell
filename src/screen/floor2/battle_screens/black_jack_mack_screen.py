import random  # Make sure to import the random module at the beginning of your script

import pygame

from constants import DISPLAY
from entity.gui.screen.battle_screen import BattleScreen
from entity.gui.textbox.npc_text_box import NpcTextBox
from entity.gui.textbox.text_box import TextBox
from game_constants.coin_flip_constants import CoinFlipConstants
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic
from screen.examples.screen import Screen
from deck import Deck
from entity.gui.textbox.bordered_box import BorderedBox






# DO NOT ALLOW PLAYER TO LEAVE WHEN ENEMY USES ABILITY

class BlackJackMackScreen(Screen):
    def __init__(self):
        Screen.__init__(self, " Black Jack Game")

        self.money = 800
        self.deck = Deck()


        self.last_t_press_time = 0  # Initialize the last T press time
        self.font = pygame.font.Font(None, 36)
        self.black_ace = False  # this is our boss level when talk to NPC set to true set false if game is set to quit
        self.ace_up_sleeve_jack = False
        self.ace_up_sleeve_jack_cheat_mode = False


        self.black_jack_rumble_bill_defeated = False
        self.critical_hit = False

        self.first_message_display = ""
        self.second_message_display = ""
        self.third_message_display = ""
        self.game_state = "welcome_screen"
        self.bet = 50
        self.player_score = 0
        self.enemy_score = 0
        # self.player_cards_list = []
        # self.enemy_cards_list = []
        self.player_hand = []
        self.enemy_hand = []
        self.choices = ["Ready", "Draw", "Redraw"]
        self.current_index = 0
        self.welcome_screen_choices = ["Play", "Magic", "Bet", "Quit"]
        self.welcome_screen_index = 0
        self.magic_menu_selector = ["Reveal",  "Back"]
        self.magic_menu_index = 0
        self.ace_value = 1
        self.bust_protection = False
        self.avatar_of_luck_card_redraw_counter = 3

        self.player_lock = False

        self.player_black_jack_win = False
        self.enemy_black_jack_win = False
        self.black_jack_draw = False

        self.current_speaker = ""
        self.npc_speaking = False
        self.hero_speaking = False
        self.music_loop = True

        self.despair = False
        # self.despair = True

        self.hero_losing_text_state = False
        self.hero_winning_text_state = False
        self.player_status = ""
        self.enemy_status = ""
        self.sir_leopold_ace_attack = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/startloadaccept.wav")  # Adjust the path as needed
        self.sir_leopold_ace_attack.set_volume(0.6)

        self.lucky_strike = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/luckystrike.wav")  # Adjust the path as needed
        self.lucky_strike.set_volume(0.6)



        self.double_draw_casting = False
        self.player_debuff_double_draw = 0
        self.magic_points = 1




        self.reveal_hand = 11
        self.magic_lock = False
        self.luck_of_jack = 7
        self.avatar_of_luck = False
        self.redraw_lock = False
        self.music_file = "/Users/stevenhalla/code/casino_hell/assets/music/black_jack_screen.mp3"
        self.music_volume = 0.5  # Adjust as needed
        # self.initialize_music()
        self.music_on = True
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)

        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.5)

        # maybe include a self.turn_counter = 0 that can be +1 in our welcome screen in conjection with our reveal spell
        # incldue a double bet spell that is CHR based that player gets for free maybe4

        self.locked_text = self.font.render("Locked", True, (255, 255, 255))




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



        # self.bordered_text_box = BorderedTextBox(self.messages["list2"], (230, 200, 250, 45), 30, 500)
        self.main_bordered_box = BorderedBox((25, 425, 745, 150))

        self.defeated_textbox = TextBox(
            [
                "Guy:Looks like you defeated me.....back to eating chili for days and day and days....",

                "pro tip,for some reason the boss is scared of BUST, those demons sure do lick those chops when his cards get high",
            ""],
            (50, 450, 50, 45), 30, 500)

        self.exp_gain = 0
        self.food_luck = False
        self.stat_point_allocated = False

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

    # def draw_level_up(self, state: 'GameState') -> None:
    #     if state.player.stat_point_increase and self.game_state == "level_up_screen":
    #         if self.messages["level_up"].message_index == 3:
    #             black_box_height = 261 - 50  # Adjust height
    #             black_box_width = 200 - 10  # Adjust width to match the left box
    #             border_width = 5
    #             start_x_right_box = state.DISPLAY.get_width() - black_box_width - 25
    #             start_y_right_box = 200  # Adjust vertical alignment
    #
    #             # Create the black box
    #             black_box = pygame.Surface((black_box_width, black_box_height))
    #             black_box.fill((0, 0, 0))
    #
    #             # Create a white border
    #             white_border = pygame.Surface(
    #                 (black_box_width + 2 * border_width, black_box_height + 2 * border_width)
    #             )
    #             white_border.fill((255, 255, 255))
    #             white_border.blit(black_box, (border_width, border_width))
    #
    #             # Determine the position of the white-bordered box
    #             black_box_x = start_x_right_box - border_width
    #             black_box_y = start_y_right_box - border_width
    #
    #             # Blit the white-bordered box onto the display
    #             state.DISPLAY.blit(white_border, (black_box_x, black_box_y))
    #
    #             # Draw the menu options
    #             for idx, choice in enumerate(self.level_screen_stats):
    #                 y_position = start_y_right_box + idx * 40  # Adjust spacing between choices
    #                 state.DISPLAY.blit(
    #                     self.font.render(choice, True, (255, 255, 255)),
    #                     (start_x_right_box + 60, y_position + 15)
    #                 )
    #
    #             # Draw the selection arrow
    #             arrow_y_positions = [12, 52, 92, 132, 172]  # Y positions for each arrow
    #             arrow_y = start_y_right_box + arrow_y_positions[self.level_up_stat_increase_index]
    #             state.DISPLAY.blit(
    #                 self.font.render("->", True, (255, 255, 255)),
    #                 (start_x_right_box + 12, arrow_y)
    #             )
    #
    #     # Continue with other drawing logic, like drawing battle messages
    #     self.messages["level_up"].draw(state)

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
                    state.player.body += 1
                    state.player.stamina_points += state.player.level_2_body_stamina_increase
                    state.player.max_stamina_points += state.player.level_2_body_stamina_increase
                    self.stat_point_allocated = True
                elif selected_stat == "Mind" and state.controller.isTPressed and state.player.mind < 2:
                    state.player.mind += 1
                    self.stat_point_allocated = True

                    state.player.focus_points += state.player.level_2_mind_focus_increase
                    state.player.max_focus_points += state.player.level_2_mind_focus_increase
                    Magic.CRAPS_LUCKY_7.add_magic_to_player(state.player, Magic.CRAPS_LUCKY_7)
                elif selected_stat == "Spirit" and state.controller.isTPressed and state.player.spirit < 2:
                    state.player.spirit += 1
                    self.stat_point_allocated = True

                elif selected_stat == "Perception" and state.controller.isTPressed and state.player.perception < 2:
                    state.player.perception += 1
                    self.stat_point_allocated = True

                elif selected_stat == "Perception" and state.controller.isTPressed and state.player.perception < 3 and \
                        Equipment.SOCKS_OF_PERCEPTION.value in state.player.equipped_items:
                    state.player.perception += 1
                    self.stat_point_allocated = True

                    # state.player.base_perception += 1
                elif selected_stat == "Luck" and state.controller.isTPressed and state.player.luck < 2:
                    state.player.luck += 1
                    self.stat_point_allocated = True


                elif selected_stat == "Luck" and state.controller.isTPressed and state.player.luck < 3 and \
                        state.player.enhanced_luck == True:
                    state.player.luck += 1
                    self.stat_point_allocated = True


                if state.controller.isTPressed and self.stat_point_allocated == True:
                    print(f"Player {selected_stat} is now: {getattr(state.player, selected_stat.lower())}")
                    state.controller.isTPressed = False
                    state.player.leveling_up = False
                    self.level_up_messages.reset()
                    self.stat_point_allocated = False
                    self.game_state = "welcome_screen"

    def stop_music(self):
        pygame.mixer.music.stop()

    def initialize_music(self):
        pass
        # Initialize the mixer
        # pygame.mixer.init()
        #
        # # Load the music file
        # pygame.mixer.music.load(self.music_file)
        #
        # # Set the volume for the music (0.0 to 1.0)
        # pygame.mixer.music.set_volume(self.music_volume)
        #
        # # Play the music, -1 means the music will loop indefinitely
        # pygame.mixer.music.play(-1)

    def place_bet(self, state: "GameState"):
        if state.controller.isUpPressed:

            self.bet += 50
            self.menu_movement_sound.play()  # Play the sound effect once

            pygame.time.delay(100)
            state.controller.isUpPressed = False

        elif state.controller.isDownPressed:
            self.bet -= 50
            self.menu_movement_sound.play()  # Play the sound effect once

            pygame.time.delay(100)
            state.controller.isDownPressed = False

        if self.bet < 50:
            self.bet = 50

        if self.bet > 125:
            self.bet = 125

        if self.bet > self.money:
            self.bet = self.money

        if self.bet > state.player.money:
            self.bet = state.player.money

    def update(self, state: "GameState"):
        if self.money < self.bet:
            self.bet = self.money
        if self.money <= 0:
            Events.add_event_to_player(state.player, Events.BLACK_JACK_BLACK_MACK_DEFEATED)
            Events.add_event_to_player(state.player, Events.MC_NUGGET_THIRD_QUEST_COMPLETE)

        if self.music_on == True:
            self.stop_music()
            self.initialize_music()
            self.music_on = False

        state.player.canMove = False
        if self.money < 10:
            self.black_jack_rumble_bill_defeated = True
            self.game_state = "defeated"

        controller = state.controller
        controller.update()
        state.player.update(state)

        if self.game_state == "defeated":
            print("enemy defeated")
            self.defeated_textbox.update(state)



        if self.game_state == "welcome_screen":

            if state.player.leveling_up == True:
                self.game_state = "level_up_screen"

            if state.player.stamina_points < 1:
                print("time to leave")


            self.welcome_screen_text_box.update(state)

            self.npc_speaking = True
            self.hero_speaking = False
            self.critical_hit = False
            self.magic_enemy_attack_double_draw_message_component.reset()


            self.redraw_lock = False
            self.ace_up_sleeve_jack_cheat_mode = False
            self.bust_protection = False
            self.avatar_of_luck_card_redraw_counter = 3
            self.current_index = 0
            self.enemy_score = 0

            # self.player_cards_list.clear()
            # self.enemy_cards_list.clear()
            # self.player_hand.clear() # todo shouldn't need to do because we override the self.player_hand/enemy_hand when we call: self.xyz_hand = self.deck.draw_hand()
            # self.enemy_hand.clear()

            if self.welcome_screen_text_box.is_finished() and self.welcome_screen_text_box.current_message_finished():
                self.npc_speaking = False
                self.hero_speaking = True
                # self.welcome_screen_text_box_hero.update(state)


                if controller.isUpPressed:
                    print("Nurgle is here for you ")
                    self.menu_movement_sound.play()  # Play the sound effect once

                    # channel3 = pygame.mixer.Channel(3)
                    # sound3 = pygame.mixer.Sound(
                    #     "audio/Fotstep_Carpet_Right_3.mp3")
                    # channel3.play(sound3)
                    if not hasattr(self, "welcome_screen_index"):
                        self.welcome_screen_index = len(
                            self.welcome_screen_choices) - 1
                    else:
                        self.welcome_screen_index -= 1
                    self.welcome_screen_index %= len(
                        self.welcome_screen_choices)
                    controller.isUpPressed = False


                elif controller.isDownPressed:
                    self.menu_movement_sound.play()  # Play the sound effect once

                    print("Nurgle is here for you ")

                    # channel3 = pygame.mixer.Channel(3)
                    # sound3 = pygame.mixer.Sound(
                    #     "audio/Fotstep_Carpet_Right_3.mp3")
                    # channel3.play(sound3)
                    if not hasattr(self, "welcome_screen_index"):
                        self.welcome_screen_index = len(
                            self.welcome_screen_choices) + 1
                    else:
                        self.welcome_screen_index += 1
                    self.welcome_screen_index %= len(
                        self.welcome_screen_choices)
                    controller.isDownPressed = False

                if self.welcome_screen_index == 0 and controller.isTPressed:
                    controller.isTPressed = False
                    for i in range(0, self.bet, 50):
                        state.player.stamina_points -= 3
                    self.deck.shuffle()



                    if self.player_debuff_double_draw <= 0 and self.money < 300 and self.magic_points > 0:
                        enemy_magic_cast = random.randint(1, 100)

                        enemy_magic_cast_modifier = self.magic_points * 20

                        if enemy_magic_cast + enemy_magic_cast_modifier >= 35:
                            print("WURGLE ALERT WURGLE ALERT WURGLE ALERT")
                            self.player_debuff_double_draw += 10
                            self.magic_points -= 1
                            self.game_state = "double_draw_casting_phase"
                        else:
                            self.game_state = "draw_phase"

                    elif self.player_debuff_double_draw <= 0 and self.money < 700 and self.magic_points > 0:
                        enemy_magic_cast = random.randint(1, 100)
                        print("WURGLE ALERT WURGLE ALERT WURGLE ALERT")

                        enemy_magic_cast_modifier = self.magic_points * 20

                        if enemy_magic_cast + enemy_magic_cast_modifier >= 70:
                            print("436")

                            self.player_debuff_double_draw += 10
                            self.magic_points -= 1
                            self.game_state = "double_draw_casting_phase"

                        else:
                            self.game_state = "draw_phase"

                    else:
                        self.game_state = "draw_phase"
                    controller.isTPressed = False
                elif self.welcome_screen_index == 1 and controller.isTPressed and self.magic_lock == False:
                    self.magic_screen_index = 0
                    self.game_state = "magic_menu"
                    controller.isTPressed = False
                elif self.welcome_screen_index == 2 and controller.isTPressed:
                    self.game_state = "bet_phase"

                    controller.isTPressed = False

                elif self.welcome_screen_index == 3 and controller.isTPressed and self.player_debuff_double_draw < 1:
                    controller.isTPressed = False
                    self.welcome_screen_index = 0
                    self.reveal_hand = 0
                    self.magic_lock = False
                    self.bet = 50




                    # self.player_status = "Normal"
                    # self.enemy_status = "Normal"

                    self.magic_points = 1
                    state.currentScreen = state.area2GamblingScreen
                    state.area2GamblingScreen.start(state)

                    state.player.canMove = True


        elif self.game_state == "double_draw_casting_phase":
            self.magic_enemy_attack_double_draw_message_component.update(state)
            if self.magic_enemy_attack_double_draw_message_component.message_index == 1:
                print("Hi there")
                self.game_state = "draw_phase"


        elif self.game_state == "bet_phase":
            if self.money < self.bet:
                self.bet = self.money

            self.bet_screen_text.update(state)

            self.npc_speaking = True
            self.hero_speaking = False

            self.third_message_display = " "
            self.place_bet(state)
            if controller.isTPressed:
                if self.bet > 70:
                    print("-3")
                elif self.bet < 30:


                    print("-1")
                elif self.bet < 70 or self.bet > 20:
                    print("-2")

                pygame.time.wait(300)
                self.game_state = "welcome_screen"
                controller.isTPressed = False

        elif self.game_state == "draw_phase":
            # need to reformat have a reset function
            self.first_message_display = ""
            self.second_message_display = ""
            self.thrid_message_display = ""
            self.black_jack_counter = 0
            self.player_black_jack_win = False
            self.enemy_black_jack_win = False
            self.black_jack_draw = False
            self.player_hand = self.deck.player_draw_hand(2)
            print("Player hand is" + str(self.player_hand))
            self.player_score = self.deck.compute_hand_value(self.player_hand)

            print("Player score is: " + str(self.player_score))

            if self.player_score > 20:
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
            self.enemy_hand = self.deck.enemy_draw_hand(2)
            print("Enemy hand is" + str(self.enemy_hand))
            if self.enemy_score > 20:
                self.enemy_black_jack_win = True




            if state.player.luck > 0:
                # the below has a 15% chance per new hand to trigger
                if self.player_score > 12 and self.player_score < 17:
                    lucky_roll = random.randint(1, 100)  # Get a random number between 1 and 100
                    adjusted_lucky_roll = lucky_roll + state.player.luck * 5
                    if adjusted_lucky_roll >= 45:
                        print("You got a critical hit: dslajfldsjfjsalfjlsjfl;sjfklsjaf;lksjaflksajf;lskajflsjf;saljf;lkasjfl;akjf;lksajfl;sajf;lkasjf;lsjf;lajsfl;")
                        self.lucky_strike.play()  # Play the sound effect once

                        self.player_hand = self.deck.player_draw_hand(2)
                        print("New Player hand is" + str(self.player_hand))
                        self.player_score = self.deck.compute_hand_value(self.player_hand)
                        print(" New Player score is: " + str(self.player_score))
                        self.critical_hit = True

            if "sir leopold's paw" in state.player.items:
                roll = random.randint(1, 100)  # Get a random number between 1 and 100
                if roll >= 40:  # Check if the roll is less than or equal to 30
                    self.enemy_black_jack_win = False

                    for card in self.enemy_hand:
                        if card in aces_to_remove:
                            self.enemy_hand.remove(card)
                            print(f"Hedgehog swiped an Ace! Removed card: {card}")
                            print("Your roll is: " + str(roll))
                            self.sir_leopold_ace_attack.play()  # Play the sound effect once
                            self.enemy_hand += self.deck.enemy_draw_hand(1)
                            break

            print("Enemy hand is" + str(self.enemy_hand))

            self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)
            print("enemy score is: " + str(self.enemy_score))



            print(self.player_black_jack_win)

            if self.black_ace == True:
                if self.enemy_score < 7:
                    self.enemy_hand = self.deck.enemy_draw_hand(2)
                    print("Enemy hand is" + str(self.enemy_hand))
                    print("You get the sense the enemy is somewhat lucky")
                    self.enemy_score = self.deck.compute_hand_value(
                        self.enemy_hand)
                    print("enemy score is: " + str(self.enemy_score))
                    if self.black_jack_counter > 0:
                        print("Enemy black jack win set to true")

                        self.enemy_black_jack_win = True
                    elif self.black_jack_counter == 0:
                        self.enemy_black_jack_win = False

                    print(self.player_black_jack_win)

            if self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                self.black_jack_draw = True
                self.thrid_message_display = "Its a draw"
                print("Its a draw")
                self.game_state = "results_screen"
            elif self.player_black_jack_win == True and self.enemy_black_jack_win == False:

                print("its time for you to have double winnings")
                # state.player.money += self.bet
                # state.player.money += self.bet
                # self.money -= self.bet
                # self.money -= self.bet
                self.game_state = "results_screen"
            elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                print("THE ENEMY HAS A BLAK Jack SORRRYYYYYY")
                # state.player.money -= self.bet
                # state.player.money -= self.bet
                # self.money += self.bet
                # self.money += self.bet

                self.game_state = "results_screen"

            else:
                self.game_state = "menu_screen"



        elif self.game_state == "level_up_screen":
            self.handle_level_up(state, state.controller)


        elif self.game_state == "player_draw_one_card":
            self.player_hand += self.deck.player_draw_hand(1)
            self.deck.compute_hand_value(self.player_hand)
            self.player_score = self.deck.compute_hand_value(self.player_hand)



            if self.player_debuff_double_draw > 0:
                self.player_hand += self.deck.player_draw_hand(1)
                self.deck.compute_hand_value(self.player_hand)
                self.player_score = self.deck.compute_hand_value(self.player_hand)
                # if self.player_score > 21:


            if self.player_score > 10:
                print("hi greater than 10")
                self.deck.rank_values["Ace"] = 1

            print("Player hand is now" + str(self.player_hand))
            print("Player score is now" + str(self.player_score))
            if self.player_score > 21:
                print(self.player_hand)
                print(self.player_hand[-1])
                if Equipment.BLACK_JACK_HAT.value not in state.player.equipped_items:
                    state.player.money -= self.bet
                    self.money += self.bet
                    state.player.stamina_points -= 4
                    print("Going to bust a giant busttttttttter")

                    state.player.exp += 10
                    self.first_message_display = f"You lose -6 HP."
                    self.second_message_display = f"You busted and went over 21! You gain 10 exp and lose {self.bet} "


                elif Equipment.BLACK_JACK_HAT.value in state.player.equipped_items:
                    lucky_roll = random.randint(1,4)
                    print("Lucky roll is: " + str(lucky_roll))
                    if lucky_roll == 4:
                        print("GUARIDAN POP MODE ACTIVATED")
                        print("Player score is ------------------------------------------------: " + str(self.player_score))
                        # self.player_score -= self.deck.compute_hand_value(self.player_hand[-1])
                        print("Player score is----------------------------: " + str(self.player_score))

                        self.player_hand.pop()
                        self.player_score = self.deck.compute_hand_value(self.player_hand)

                        print("Player score is---------------: " + str(self.player_score))

                        self.first_message_display = f"You almost went over 21."
                        lucky_roll = 0
                    else:
                        print("GUARIDAN POP MODE IS NOT ACTIVATED")


                        state.player.money -= self.bet
                        self.money += self.bet
                        state.player.stamina_points -= 4
                        print("sdlfj;sdjf----------------------------------------------------")

                        state.player.exp += 10
                        self.first_message_display = f"You lose -6 HP."
                        self.second_message_display = f"You busted and went over 21! You gain 10 exp and lose {self.bet} "

                    # for card in range(self.player_hand):
                    #     self.player_hand[-1]





            if self.bust_protection == True:
                self.game_state = "results_screen"
            else:
                self.game_state = "menu_screen"

        elif self.game_state == "enemy_draw_one_card":
            print("this is the start of enemy draw one card")
            while self.enemy_score < 16:  # this is 15 in order to make game a little easier
                print("thi sis our while loop")
                # if "sir leopolds paw" in state.player.items:
                print("Meowwwwwwwwwwwwwwwwwwwwww")
                self.enemy_hand += self.deck.enemy_draw_hand(1)
                self.deck.compute_hand_value(self.enemy_hand)


                self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)
                print("enemy hand is now" + str(self.enemy_hand))
                print("enemy score is now" + str(self.enemy_score))
                self.game_state = "results_screen"

                if self.enemy_score > 21:
                    print("if the enemy is going to bust")
                    state.player.money += self.bet
                    self.money -= self.bet
                    print("enemy bust")
                    state.player.exp += 25
                    self.second_message_display = "enemy bust player wins"
                    self.game_state = "results_screen"

            if self.enemy_score > 14 and self.enemy_score < 22:
                print("stay here")
                self.game_state = "results_screen"

        elif self.game_state == "enemy_despair_draw_one_card":
            print("enemy is in despair")
            while self.enemy_score < 14:  # this is 15 in order to make game a little easier
                print("this is our despair loop")

                self.enemy_hand += self.deck.enemy_draw_hand(1)
                self.deck.compute_hand_value(self.enemy_hand)
                self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)
                print("enemy hand is now" + str(self.enemy_hand))
                print("enemy score is now" + str(self.enemy_score))
                self.game_state = "results_screen"

                if self.enemy_score > 21:
                    print("if the enemy is going to bust")
                    state.player.money += self.bet
                    self.money -= self.bet
                    print("enemy bust")
                    self.second_message_display = "enemy bust player wins"
                    self.game_state = "results_screen"

            if self.enemy_score > 14 and self.enemy_score < 22:
                print("stay here")
                self.game_state = "results_screen"




        elif self.game_state == "menu_screen":
            # print("at the menu screen")

            if self.player_score > 21:
                self.message_display = "You bust and lose."
                # state.player.money -= self.bet
                # self.money += self.bet
                self.game_state = "results_screen"

            if controller.isUpPressed:
                print("Nurgle is here for you ")
                self.menu_movement_sound.play()  # Play the sound effect once

                # channel3 = pygame.mixer.Channel(3)
                # sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                # channel3.play(sound3)
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) - 1
                else:
                    self.current_index -= 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isUpPressed = False

            if controller.isDownPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                print("Nurgle is here for you ")

                # channel3 = pygame.mixer.Channel(3)
                # sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                # channel3.play(sound3)
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) + 1
                else:
                    self.current_index += 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isDownPressed = False

            if self.current_index == 2 and state.controller.isTPressed and self.avatar_of_luck == True and self.redraw_lock == False:
                print("Redrawing your hand")
                self.player_hand = self.deck.player_draw_hand(
                    2)  # no need to call self.player_hand.clear() befoe this, as we are already overriding it here
                print("Player hand is" + str(self.player_hand))
                print("Enemy hand is" + str(self.enemy_hand))
                print("player card list is " + str(self.player_hand))
                print("enemy card list is " + str(self.enemy_hand))
                self.player_score = self.deck.compute_hand_value(
                    self.player_hand)
                self.avatar_of_luck_card_redraw_counter -= 1

                if self.avatar_of_luck_card_redraw_counter < 1:
                    self.redraw_lock = True

                self.game_state = "menu_screen"
                state.controller.isTPressed = False

                # 534534543535353525532535353354

        elif self.game_state == "magic_menu":

            self.message_display = "Pick a magic spell and wreck havic. Press K to cast"

            if controller.isUpPressed:
                print("Nurgle is here for you ")
                self.menu_movement_sound.play()  # Play the sound effect once

                # channel3 = pygame.mixer.Channel(3)
                # sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                # channel3.play(sound3)
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) - 1
                else:
                    self.magic_menu_index -= 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                print("Nurgle is here for you ")
                self.menu_movement_sound.play()  # Play the sound effect once

                # channel3 = pygame.mixer.Channel(3)
                # sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                # channel3.play(sound3)
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) + 1
                else:
                    self.magic_menu_index += 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isDownPressed = False

            # we need to make this work right after a black jack
            # set a counter to minus 1 this is the counter is above 0

            if self.magic_menu_index == 0:
                self.reveal_magic_explain_component.update(state)

                if controller.isTPressed:
                    # channel3 = pygame.mixer.Channel(3)
                    # sound3 = pygame.mixer.Sound("audio/SynthChime5.mp3")
                    # channel3.play(sound3)
                    if state.player.focus_points >= 10:
                        state.player.focus_points -= 10
                        self.spell_sound.play()  # Play the sound effect once

                        self.reveal_hand = 10
                        self.magic_lock = True
                        self.player_status = "Focus"
                        self.enemy_status = "Reveal"

                        print("You cast reveal")
                        self.game_state = "welcome_screen"
                        self.isTPressed = False


                    elif state.player.focus_points < 10:
                        self.third_message_display = "Sorry but you dont have enough focus points to cast"
                # elif self.luck_activated > 0:
                #     self.third_message_display = "sorry but you can't stack magic spells"


            ##########################have a message state reserved for buff states

            ##### boss enemies will use magic under more strict conditions


            elif self.magic_menu_index == 1:
                self.back_magic_explain_component.update(state)

                if controller.isTPressed:
                    self.magic_menu_index = 0
                    print(str(controller.isTPressed))
                    controller.isTPressed = False
                    print(str(controller.isTPressed))
                    self.game_state = "welcome_screen"
                    self.isTPressed = False
                    print(str(controller.isTPressed))





        elif self.game_state == "results_screen":

            if self.player_black_jack_win == True and self.enemy_black_jack_win == False:
                self.second_message_display = "You win with a black jack press T when ready"
                self.first_message_display = f"You gain 100 exp and {self.bet * 2} gold "




            elif self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                self.second_message_display = "It's a draw press T when ready"
                self.first_message_display = f"You gain 25 exp and 0 gold "





            elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                self.second_message_display = "Enemy gets blackjack you lose "
                self.first_message_display = f"You gain 30 exp and 0 gold "





            elif self.player_score > self.enemy_score and self.player_score < 22:
                self.second_message_display = "You win player press T when ready"
                self.first_message_display = f"You gain 25 exp and {self.bet} gold "

            elif self.player_score < self.enemy_score and self.enemy_score < 22:
                self.second_message_display = "You lose player press T when ready"
                self.first_message_display = f"You gain 5 experience and lose {self.bet} gold "


            elif self.player_score == self.enemy_score:

                self.second_message_display = "It's a draw nobody wins press T when Ready"
                self.first_message_display = f"You gain 25 exp and 0 gold "

            if controller.isTPressed:

                if self.player_black_jack_win == True and self.enemy_black_jack_win == False:
                    if self.bet <= 50:
                        state.player.exp += 20
                        self.first_message_display = f"Gain 20 exp and win {self.bet * 2} gold "

                    else:
                        self.first_message_display = f"Gain 40 exp and win {self.bet * 2} gold "

                        state.player.exp += 40

                    self.second_message_display = "Player deals a CRITICAL HIT!!! "
                    if self.bet * 2 < self.money:
                        state.player.money += self.bet * 2
                        self.money -= self.bet * 2
                    else:
                        state.player.money += self.money
                        self.money = 0


                elif self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                    if self.bet <= 50:
                        state.player.exp += 10
                        state.player.stamina_points -= 3
                        self.first_message_display = f"You gain 10 exp, 0 gold, you lose 5 HP. "

                    else:
                        self.first_message_display = f"You gain 20 exp, 0 gold, you lose 10 HP. "

                        state.player.exp += 20
                        state.player.stamina_points -= 5

                    self.second_message_display = "You tie player press T when ready"




                elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                    if self.bet <= 49:
                        state.player.exp += 10
                        state.player.stamina_points -= 15
                        self.first_message_display = f"You gain 10 exp and lose {self.bet * 2} gold."
                        self.thrid_message_display = f"You Lose 25 HP "
                    else:
                        state.player.exp += 20
                        state.player.stamina_points -= 25
                        self.first_message_display = f"You gain 15 exp and lose {self.bet * 2} gold."
                        self.thrid_message_display = f"You Lose 25 HP "

                    self.second_message_display = "Enemy deals a CRITICAL HIT!!! "

                    state.player.money -= self.bet * 2
                    self.money += self.bet * 2






                elif self.player_score > self.enemy_score and self.player_score < 22:
                    if self.bet <= 49:
                        state.player.exp += 5
                        self.first_message_display = f"You gain 5 exp and {self.bet} gold "
                    else:
                        state.player.exp += 20
                        self.first_message_display = f"You gain 10 exp and {self.bet} gold "
                    self.second_message_display = "You win player press T when ready"

                    state.player.money += self.bet
                    self.money -= self.bet




                elif self.player_score < self.enemy_score and self.enemy_score < 22:
                    if self.bet <= 50:
                        state.player.exp += 3
                        state.player.stamina_points -= 4
                        self.first_message_display = f"You gain 3 exp and lose {self.bet} gold and -4 HP"

                    else:
                        state.player.exp += 6
                        state.player.stamina_points -= 8
                        self.first_message_display = f"You gain 5 exp and lose {self.bet} gold and -8 HP"

                    self.second_message_display = "You lose player press T when ready"
                    state.player.money -= self.bet
                    self.money += self.bet




                elif self.player_score == self.enemy_score:
                    if self.bet <= 49:
                        state.player.exp += 4
                        state.player.stamina_points -= 2
                        self.first_message_display = f"You gain 8 exp and 0 gold, and lose -2 HP "

                    else:
                        state.player.exp += 15
                        state.player.stamina_points -= 4
                        self.first_message_display = f"You gain 8 exp and 0 gold, and lose -4 HP "

                    self.second_message_display = "It's a draw nobody wins press T when Ready"


                if self.reveal_hand < 11:
                    self.reveal_hand -= 1

                if self.reveal_hand == 0:
                    self.reveal_hand = 11
                    self.magic_lock = False

                if self.luck_of_jack < 7:
                    self.luck_of_jack -= 1

                if self.luck_of_jack == 0:
                    self.luck_of_jack = 6
                    self.avatar_of_luck = False
                    self.magic_lock = False

                pygame.time.wait(300)
                print("Hey there going to the welcome_screen")
                if self.player_debuff_double_draw > 0:
                    self.player_debuff_double_draw -= 1
                    print("Player debuff turns left: " + str (self.player_debuff_double_draw))

                    print("printing 976")
                self.game_state = "welcome_screen"
                controller.isTPressed = False

    def hand_to_str(self, hand) -> str:
        msg = ""
        i = 0
        for card in hand:
            if i > 0:
                msg += ", "
            msg += card[0] + " " + card[1]
            i += 1
        return msg

    def draw(self, state: "GameState"):
        # change to dealer image
        # character_image = pygame.image.load("images/128by128.png")
        # hero_image = pygame.image.load("images/hero.png")

        state.DISPLAY.fill((0, 0, 51))

        black_box = pygame.Surface((200 - 10, 180 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 235))

        black_box = pygame.Surface((200 - 10, 45 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 195))


        if state.player.money < 100:
            text_color = (255, 0, 0)  # Red color
        else:
            text_color = (255, 255, 255)  # White color

        state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True, text_color), (37, 250))

        # state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True,
        #                               (255, 255, 255)), (37, 250))
        if state.player.stamina_points < 20:
            text_color = (255, 0, 0)  # Red color
        else:
            text_color = (255, 255, 255)  # White color

        state.DISPLAY.blit(
            self.font.render(f"HP: {state.player.stamina_points}", True,
                             text_color), (37, 290))

        state.DISPLAY.blit(self.font.render(f"MP: {state.player.focus_points}", True,
                                      (255, 255, 255)), (37, 330))
        state.DISPLAY.blit(
            self.font.render(f"Bet: {self.bet}", True, (255, 255, 255)),
            (37, 370))

        if self.player_debuff_double_draw == 0:

            state.DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)),
                         (37, 205))

        elif self.player_debuff_double_draw > 0:
            state.DISPLAY.blit(
                self.font.render(f"D. Draw: {self.player_debuff_double_draw}", True, (255, 0, 0)),
                (37, 205))

        black_box = pygame.Surface((200 - 10, 110 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 20))

        black_box = pygame.Surface((200 - 10, 130 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 130 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 60))

        state.DISPLAY.blit(self.font.render(f"Money: {self.money}", True,
                                      (255, 255, 255)), (37, 70))

        if self.reveal_hand == 0:
            state.DISPLAY.blit(self.font.render(f"Status: Normal", True,
                                          (255, 255, 255)), (37, 110))
        elif self.reveal_hand > 0:
            state.DISPLAY.blit(self.font.render(f"Reveal: {self.reveal_hand}", True,
                                                (255, 255, 255)), (37, 110))

        if self.reveal_hand < 11:
            state.DISPLAY.blit(self.font.render(f"Score: {self.enemy_score}", True,
                                          (255, 255, 255)),
                         (37, 150))
        elif self.reveal_hand > 10:
            state.DISPLAY.blit(self.font.render(f"Score:", True, (255, 255, 255)),
                         (37, 150))

        # state.DISPLAY.blit(self.font.render(f"Cheater Bob", True, (255, 255, 255)),
        #              (37, 30))
        state.DISPLAY.blit(self.font.render(f"Exo {state.player.exp}", True, (255, 255, 255)),
                           (37, 30))

        self.main_bordered_box.draw(state)
        # state.DISPLAY.blit(character_image, (633, 15))
        state.DISPLAY.blit(self.font.render(f"Cheater Bob", True, (255, 255, 255)),
                     (625, 145))

        # self.face_down_card((0,0))

        if self.game_state == "welcome_screen":
            if state.player.money < 1:
                self.game_state = "game_over_no_money"
            elif state.player.stamina_points < 1:
                self.reveal_hand = 0
                self.magic_lock = False

                # self.player_status = "Normal"
                # self.enemy_status = "Normal"

                self.magic_points = 1
                self.player_debuff_double_draw = 0
                self.game_state = "game_over_no_stamina"
            #
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
                # Example render method ensuring all items are strings
                state.DISPLAY.blit(
                    self.font.render(str(choice), True, (255, 255, 255)),
                    (start_x_right_box + 60, y_position + 15)
                )

            if self.player_debuff_double_draw > 0:
                self.welcome_screen_choices[3] = "Locked"
            elif self.player_debuff_double_draw < 1:
                self.welcome_screen_choices[3] = "Quit"


            if self.reveal_hand < 11 and self.reveal_hand > 0:
                self.magic_lock = True
                self.welcome_screen_choices[1] = "Locked"   # if I use a constant it shows it as the full name not the string part
            else:
                self.magic_lock = False
                self.welcome_screen_choices[1] = "Magic"

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

            self.welcome_screen_text_box.draw(state)
            # self.welcome_screen_text_box_hero.draw(state)
            # self.bordered_text_box.draw(state)

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
            self.bet_screen_text.draw(state)

            # self.current_speaker = "cheater bob"

            # state.DISPLAY.blit(character_image, (23, 245))
            # state.DISPLAY.blit(self.font.render(f"{self.current_speaker}", True, (255, 255, 255)), (155, 350))

            state.DISPLAY.blit(self.font.render(f"Your Current bet:{self.bet}", True,
                                          (255, 255, 255)), (50, 530))
            state.DISPLAY.blit(self.font.render(f"v", True, (255, 255, 255)),
                         (260, 550))
            state.DISPLAY.blit(self.font.render(f"^", True, (255, 255, 255)),
                         (257, 510))


        elif self.game_state == "menu_screen":
            player_card_x = 235
            player_card_y = 195
            enemy_card_x = 235
            enemy_card_y = 15


            for i, card in enumerate(self.player_hand):
                if i == 4:  # Adjust for the 5th card, moving to the second row
                    player_card_y = 305
                    player_card_x = 235  # Start position for the second row
                elif i > 4:
                    # For the 6th card and beyond, increment player_card_x normally
                    player_card_y = 305
                    player_card_x = 300  # Start position for the second row
                self.deck.draw_card_face_up(card[1], card[0], (player_card_x, player_card_y), DISPLAY)

                player_card_x += 75

                # pygame.display.update()

            # pygame.display.update()

            for index, card in enumerate(self.enemy_hand):
                if index == 0:
                    self.deck.draw_card_face_down((enemy_card_x, enemy_card_y), state.DISPLAY)
                else:
                    self.deck.draw_card_face_up(card[1], card[0], (enemy_card_x, enemy_card_y), state.DISPLAY)
                enemy_card_x += 75

            black_box = pygame.Surface((160 - 10, 180 - 10))
            black_box.fill((0, 0, 0))
            border_width = 5
            white_border = pygame.Surface(
                (160 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
            white_border.fill((255, 255, 255))
            white_border.blit(black_box, (border_width, border_width))
            state.DISPLAY.blit(white_border, (620, 235))

            state.DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (674, 260))

            if self.player_debuff_double_draw < 1:
                state.DISPLAY.blit(
                    self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                    (674, 310))
            elif self.player_debuff_double_draw > 0:
                state.DISPLAY.blit(
                    self.font.render(f"D Draw", True, (255, 255, 255)),
                    (674, 310))

            if self.avatar_of_luck == True and self.redraw_lock == False:
                state.DISPLAY.blit(self.font.render("Redraw", True, (255, 255, 255)),
                                   (687, 360))

            elif self.avatar_of_luck == False or self.redraw_lock == True:
                state.DISPLAY.blit(self.font.render("Locked", True, (255, 255, 255)),
                                   (674, 360))
            else:
                state.DISPLAY.blit(self.font.render("Locked", True, (255, 255, 255)),
                                   (674, 360))

            if self.current_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
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
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 305))
                if state.controller.isTPressed:
                    pygame.time.wait(300)
                    self.game_state = "player_draw_one_card"
                    self.isTPressed = False



            elif self.current_index == 2:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 355))

                if state.controller.isTPressed and self.avatar_of_luck == True and self.redraw_lock == False:
                    pygame.display.update()

                    self.game_state = "menu_screen"



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
                    self.font.render(f"->", True, (255, 255, 255)),
                    (position_x + 20, position_y + 10))  # Adjust offsets as needed

                self.reveal_magic_explain_component.draw(state)

            elif self.magic_menu_index == 1:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (position_x + 20, position_y + 60))  # Adjust offsets as needed

                self.back_magic_explain_component.draw(state)

            # Position the magic menu selectors relative to the black box
            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[0]}", True, (255, 255, 255)),
                (position_x + 60, position_y + 15))  # Adjust offsets as needed

            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[1]}", True, (255, 255, 255)),
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
            self.reveal_hand = 0
            self.bet = 50
            self.magic_points = 1

            self.magic_lock = False

            self.player_no_stamina.update(state)
            self.player_no_stamina.draw(state)
            if self.player_no_stamina.is_finished():
                if state.controller.isTPressed:
                    state.player.money -= 100
                    if state.player.money < 1:
                        state.currentScreen = state.gameOverScreen
                        state.gameOverScreen.start(state)
                    else:
                        self.game_state = "welcome_screen"
                        state.player.canMove = True
                        state.start_area_to_rest_area_entry_point = True

                        state.currentScreen = state.area2RestScreen
                        state.area2RestScreen.start(state)
                        state.player.stamina_points = 1


            if state.player.money < 1:

                self.game_state = "game_over_no_money"
            elif state.player.stamina_points < 1:
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

                # pygame.display.update()

            # pygame.display.update()

            for index, card in enumerate(self.enemy_hand):
                self.deck.draw_card_face_up(card[1], card[0], (enemy_card_x, enemy_card_y), DISPLAY)

                enemy_card_x += 75

            # self.current_speaker = "cheater bob"

            # state.DISPLAY.blit(character_image, (23, 245))
            state.DISPLAY.blit(self.font.render(f"{self.current_speaker}", True,
                                          (255, 255, 255)), (155, 350))
            # state.DISPLAY.blit(self.font.render(f"{self.first_message_display}", True, (255, 255, 255)), (45, 390))

            state.DISPLAY.blit(
                self.font.render(f"{self.second_message_display}", True,
                                 (255, 255, 255)), (45, 450))
            state.DISPLAY.blit(self.font.render(f"{self.first_message_display}", True,
                                          (255, 255, 255)), (45, 500))
            # state.DISPLAY.blit(self.font.render(f"{self.third_message_display}", True, (255, 255, 255)), (45, 510))

            # state.DISPLAY.blit(self.font.render(f"Player bet:{self.bet}", True, (255, 255, 255)), (10, 155))

        pygame.display.flip()
